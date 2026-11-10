"""Install pinned, checksum-verified local speech assets. Never runs at game startup.

The model lives outside app updates in Application Support. Native code goes into
ignored build output, then electron-builder includes it in the signed app.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import tarfile
import tempfile
import time
import urllib.request

ENGINE=Path(__file__).resolve().parent
MODEL_DIR=Path.home()/'Library/Application Support/Cheese the Duck ASCII Engine/local-ai'
MODEL='Qwen3-4B-Q4_K_M.gguf'
REVISION='bc640142c66e1fdd12af0bd68f40445458f3869b'
MODEL_SHA='7485fe6f11af29433bc51cab58009521f205840f5b4ae3a32fa7f92e8534fdf5'
RUNTIME='llama-b12255-bin-macos-arm64.tar.gz'
RUNTIME_SHA='56074dd37cd369d4c73658d7ce3b1198ec359fb501ad8f2278b4f8fb36178a48'


def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(4*1024*1024),b''):h.update(block)
    return h.hexdigest()


def download(url,path,digest):
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists() and sha(path)==digest:
        print('Verified existing '+path.name,flush=True);return
    partial=path.with_suffix('.part')
    print('Downloading '+path.name,flush=True)
    with urllib.request.urlopen(url,timeout=90) as source,partial.open('wb') as target:
        shutil.copyfileobj(source,target,4*1024*1024)
    if sha(partial)!=digest:
        partial.unlink();raise RuntimeError('Checksum mismatch: '+path.name)
    partial.replace(path);print('Verified '+path.name,flush=True)


def main():
    build=ENGINE/'build/local-ai'
    download('https://github.com/ggml-org/llama.cpp/releases/download/b12255/'+RUNTIME,build/'runtime.tar.gz',RUNTIME_SHA)
    runtime=build/'runtime'
    marker=runtime/'verified-archive.sha256'
    # Extract to fresh inodes: replacing running signed Mach-O files in place
    # invalidates macOS's executable-page cache even when bytes are identical.
    if not marker.exists() or marker.read_text().strip()!=RUNTIME_SHA:
        folder=Path(tempfile.mkdtemp(prefix='runtime-install-',dir=build))
        with tarfile.open(build/'runtime.tar.gz') as tar:
            for member in tar.getmembers():
                target=(folder/member.name).resolve()
                if folder.resolve() not in target.parents:raise RuntimeError('Invalid archive path')
                if member.issym() or member.islnk():
                    link=(target.parent/member.linkname).resolve()
                    if folder.resolve() not in link.parents:raise RuntimeError('Invalid archive link')
            tar.extractall(folder)
        (folder/'verified-archive.sha256').write_text(RUNTIME_SHA+'\n')
        if runtime.exists():runtime.rename(build/('runtime-previous-'+str(time.time_ns())))
        folder.rename(runtime)
    download('https://huggingface.co/Qwen/Qwen3-4B-GGUF/resolve/'+REVISION+'/'+MODEL+'?download=true',MODEL_DIR/MODEL,MODEL_SHA)
    shutil.copy2(ENGINE/'licenses/Qwen3-LICENSE.txt',MODEL_DIR/'Qwen3-LICENSE.txt')
    manifest={'model':'Qwen/Qwen3-4B-GGUF','revision':REVISION,'quantization':'Q4_K_M','sha256':MODEL_SHA,
              'runtime':'llama.cpp b12255','runtime_archive_sha256':RUNTIME_SHA}
    (MODEL_DIR/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Local speech is ready. No network access is needed to play.')


if __name__=='__main__':main()
