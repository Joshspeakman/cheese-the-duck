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


def fresh_speech(text, messages):
    """Drop long recycled sentences, while allowing deliberate quotations.

    Small local models sometimes answer correctly, then append an entire older
    reply. Keep the new answer; ordinary words, brief catchphrases and explicitly
    requested repeats are untouched. An entirely recycled reply needs a retry.
    """
    question=next((m['content'] for m in reversed(messages) if m['role']=='user'),'')
    if re.search(r'\b(repeat|again|quote|verbatim|exact(?:ly)?|what did you say)\b',question,re.I):
        return text
    normalize=lambda s:' '.join(re.findall(r"\w+",s.casefold()))
    old=[' '+normalize(m['content'])+' ' for m in messages if m['role']=='assistant']
    if not old:return text
    kept=[]
    for sentence in re.split(r'(?<=[.!?])\s+',text):
        words=normalize(sentence)
        if len(words.split())>=8 and any(' '+words+' ' in previous for previous in old):continue
        kept.append(sentence)
    return ' '.join(kept).strip()


def speak(messages, fallback):
    port=os.environ.get('CHEESE_SPEECH_PORT','')
    token=os.environ.get('CHEESE_SPEECH_TOKEN','')
    if not port.isdigit() or not token:return {'text':fallback,'source':'authored','detail':'Local voice is unavailable; memories and learning are active.'}
    payload={'messages':messages,'max_tokens':150,'temperature':.8,'top_p':.85,'top_k':20,
             'repeat_penalty':1.12,'stream':False,'chat_template_kwargs':{'enable_thinking':False}}
    try:
        # Bypass environment proxy settings: a conversation never leaves this Mac.
        opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
        for attempt in range(2):
            request=urllib.request.Request('http://127.0.0.1:'+port+'/v1/chat/completions',
                data=json.dumps(payload).encode(),headers={'Content-Type':'application/json','Authorization':'Bearer '+token})
            with opener.open(request,timeout=25) as response:data=json.load(response)
            choice=data['choices'][0]
            text=clean_speech(choice['message'].get('content',''))
            if not text:raise ValueError('empty local response')
            # Avoid displaying a visibly cut-off word/sentence at a token limit.
            if choice.get('finish_reason')=='length':
                end=max(text.rfind('.'),text.rfind('!'),text.rfind('?'))
                if end>40:text=text[:end+1]
            text=fresh_speech(text,messages)
            if text:return {'text':text,'source':'local','detail':'Qwen3 · running on this Mac'}
            # Immutable retry: the real player's message and saved history stay intact.
            payload['messages']=[dict(m) for m in messages]
            payload['messages'][0]['content']+='\nGive one new, short answer to the last user message. Do not reuse any sentence from your earlier replies.'
        raise ValueError('recycled local response')
    except Exception as exc:
        return {'text':fallback,'source':'authored','detail':'Local voice is warming up or unavailable. Learning continues.','error':type(exc).__name__}
