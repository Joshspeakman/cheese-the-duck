"""Local-only speech transport. Learning and gameplay never depend on inference.

Electron owns the native server. Workers receive immutable prompt snapshots;
only the game thread consumes their bounded speech results.
"""
import json
import os
import re
import urllib.request


def clean_speech(text):
    text=re.sub(r'<think>.*?</think>', '', str(text), flags=re.S)
    # Gameplay commands are deliberately not a language-model capability.
    text=re.sub(r'\[(?:ACTION|EMOTE|COMMAND)[^\]]*\]', '', text, flags=re.I)
    text=re.sub(r'<[^>]+>', '', text)
    text=' '.join(text.split()).strip('"')[:600]
    return text


def speak(messages, fallback):
    port=os.environ.get('CHEESE_SPEECH_PORT','')
    token=os.environ.get('CHEESE_SPEECH_TOKEN','')
    if not port.isdigit() or not token:return {'text':fallback,'source':'authored','detail':'Local voice is unavailable; memories and learning are active.'}
    payload={'messages':messages,'max_tokens':150,'temperature':.8,'top_p':.85,'top_k':20,
             'repeat_penalty':1.12,'stream':False,'chat_template_kwargs':{'enable_thinking':False}}
    request=urllib.request.Request('http://127.0.0.1:'+port+'/v1/chat/completions',
        data=json.dumps(payload).encode(),headers={'Content-Type':'application/json','Authorization':'Bearer '+token})
    try:
        # Bypass environment proxy settings: a conversation never leaves this Mac.
        opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
        with opener.open(request,timeout=25) as response:data=json.load(response)
        choice=data['choices'][0]
        text=clean_speech(choice['message'].get('content',''))
        if not text:raise ValueError('empty local response')
        # Avoid displaying a visibly cut-off word/sentence at a token limit.
        if choice.get('finish_reason')=='length':
            end=max(text.rfind('.'),text.rfind('!'),text.rfind('?'))
            if end>40:text=text[:end+1]
        return {'text':text,'source':'local','detail':'Qwen3 · running on this Mac'}
    except Exception as exc:
        return {'text':fallback,'source':'authored','detail':'Local voice is warming up or unavailable. Learning continues.','error':type(exc).__name__}
