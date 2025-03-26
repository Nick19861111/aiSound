# modules/utils.py
import pyaudio
import numpy as np
import json
import time  # 添加 time 模块导入

# modules/utils.py
def listen_while_speaking(voice_recognizer, timeout=0.5):
    print(f"开始监听语音（播报中），超时时间: {timeout}秒...")
    text = voice_recognizer.listen(timeout=timeout)
    if text:
        print(f"播报中识别到语音: {text}")
        return text
    else:
        print("播报中未识别到语音")
    return None