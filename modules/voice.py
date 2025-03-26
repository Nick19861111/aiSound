# modules/voice_recognizer.py
import pyaudio
import numpy as np
import json
from vosk import Model, KaldiRecognizer

class VoiceRecognizer:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.model = Model("models/vosk-model-cn-0.22")
        # 设置解码参数，通过 JSON 字符串传递
        config = json.dumps({"beam": 15, "max-active": 10000})
        self.recognizer = KaldiRecognizer(self.model, 16000, config)
        self.recognizer.SetWords(True)

        print("可用音频设备：")
        for i in range(self.p.get_device_count()):
            dev = self.p.get_device_info_by_index(i)
            print(f"设备 {i}: {dev['name']}, 输入通道: {dev['maxInputChannels']}")
        default_input_device = self.p.get_default_input_device_info()
        print(f"默认输入设备: {default_input_device['name']}, 索引: {default_input_device['index']}")

    def listen(self, timeout=None):
        print("使用设备索引: 1")
        print("Start speaking...")
        try:
            self.stream = self.p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=8000,
                input_device_index=1
            )
            self.stream.start_stream()
            total_samples = 0
            silence_counter = 0
            start_time = None
            if timeout is not None:
                import time
                start_time = time.time()

            while True:
                if timeout is not None and start_time is not None:
                    if time.time() - start_time > timeout:
                        print(f"监听超时（{timeout}秒），停止监听")
                        return None

                data = self.stream.read(4000, exception_on_overflow=False)
                total_samples += len(data) // 2
                audio_data = np.frombuffer(data, dtype=np.int16)
                volume = np.abs(audio_data).mean()
                print(f"读取到音频数据，长度: {len(data)} 字节，样本数: {total_samples}")
                print(f"音量: {volume}")

                if volume < 30:  # 降低阈值到 30
                    silence_counter += 1
                    if silence_counter > 20:
                        print("检测到长时间沉默，停止监听")
                        return None
                else:
                    silence_counter = 0

                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get("text", "")
                    print(f"识别到语音: {text}")
                    return text
                else:
                    partial_result = json.loads(self.recognizer.PartialResult())
                    print(f"部分识别结果: {partial_result.get('partial', '')}")
        except Exception as e:
            print(f"语音识别错误: {str(e)}")
            return "error_recognition"
        finally:
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
                self.stream = None

    def cleanup(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()