# modules/utils.py
import pyaudio
import numpy as np
import json
import time  # 添加 time 模块导入

def listen_while_speaking(voice_recognizer, timeout=1.0):
    print("开始监听语音（播报中）...")
    try:
        voice_recognizer.stream = voice_recognizer.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=8000,
            input_device_index=1
        )
        voice_recognizer.stream.start_stream()
        total_samples = 0
        silence_counter = 0
        start_time = time.time()
        while time.time() - start_time < timeout:
            data = voice_recognizer.stream.read(4000, exception_on_overflow=False)
            total_samples += len(data) // 2
            audio_data = np.frombuffer(data, dtype=np.int16)
            volume = np.abs(audio_data).mean()
            print(f"音量（播报中）: {volume}")
            if volume < 50:
                silence_counter += 1
                if silence_counter > 10:
                    print("检测到长时间沉默（播报中）")
                    break
            else:
                silence_counter = 0
            if voice_recognizer.recognizer.AcceptWaveform(data):
                result = json.loads(voice_recognizer.recognizer.Result())
                text = result.get("text", "")
                if text:
                    print(f"识别到语音（播报中）: {text}")
                    return text
    except Exception as e:
        print(f"语音识别错误（播报中）: {str(e)}")
    finally:
        if voice_recognizer.stream:
            voice_recognizer.stream.stop_stream()
            voice_recognizer.stream.close()
            voice_recognizer.stream = None
    return None


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