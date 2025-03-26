# modules/speaker.py
import pyttsx3
import time
from .utils import listen_while_speaking

class Speaker:
    def __init__(self):
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('voice', 'com.apple.voice.compact.zh-CN.Tingting')
            self.engine.setProperty('rate', 180)  # 调整语速为 180
            self.is_speaking = False
            self.should_stop = False
            voices = self.engine.getProperty('voices')
            print("可用语音：")
            for voice in voices:
                print(f"语音 ID: {voice.id}, 名称: {voice.name}, 语言: {voice.languages}")
            self.test_speak()
        except Exception as e:
            print(f"初始化播报引擎失败: {str(e)}")

    def test_speak(self):
        try:
            print("测试播报：你好，这是一个测试")
            self.engine.say("你好，这是一个测试")
            self.engine.runAndWait()
            print("测试播报完成")
        except Exception as e:
            print(f"测试播报失败: {str(e)}")

    def speak(self, text, voice_recognizer=None):
        print(f"开始播报: {text}")
        self.should_stop = False
        self.is_speaking = True
        try:
            sentences = text.split("。") if "。" in text else [text]
            for sentence in sentences:
                if self.should_stop:
                    print("播报被打断")
                    break
                if sentence.strip():
                    self.engine.say(sentence)
                    self.engine.runAndWait()
                    if voice_recognizer:
                        text = listen_while_speaking(voice_recognizer, timeout=0.5)
                        if text:
                            stop_keywords = ["停止", "退出", "停职", "停", "停止播放", "暂停", "停下", "别说了", "闭嘴"]
                            if any(keyword in text for keyword in stop_keywords):
                                print("检测到停止指令，打断播报")
                                self.should_stop = True
                                break
                            return text
                    time.sleep(0.1)
        except Exception as e:
            print(f"播报错误: {str(e)}")
        finally:
            self.is_speaking = False
            self.should_stop = False
            print("播报结束")
        return None

    def stop(self):
        if self.is_speaking:
            self.should_stop = True
            try:
                self.engine.stop()
            except Exception as e:
                print(f"停止播报引擎错误: {str(e)}")

    def cleanup(self):
        self.stop()
        try:
            self.engine.endLoop()
        except Exception as e:
            print(f"清理播报引擎错误: {str(e)}")