import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
import speech_recognition as sr
import requests

from gtts import gTTS    # Google TTS
import pygame

# 数据
commands = pd.DataFrame({
    "text": ["开灯", "关灯", "查看天气", "开风扇", "关空调",
             "开电视", "关电视", "查时间", "开窗户", "关门",
             "开灯亮", "关风扇", "查温度", "开空调", "关窗户",
             "开音响", "关音响", "查日期", "开电扇", "关电灯",
             "开冰箱", "关冰箱", "查湿度", "开加湿器", "关加湿器",
             "开电脑", "关电脑", "查新闻", "开灯请", "关灯吧"],
    "intent": [1, 0, 2, 1, 0, 1, 0, 2, 1, 0, 1, 0, 2, 1, 0,
               1, 0, 2, 1, 0, 1, 0, 2, 1, 0, 1, 0, 2, 1, 0]
})

# 编码函数
def encode_command(cmd):
    cmd = cmd.strip()
    if not cmd:
        return [0, 0, 0, 0], False
    verb = cmd[0]
    noun = cmd[1:] if len(cmd) > 1 else ""
    verb_map = {"开": 1, "关": 0, "查": 2, "看": 2}
    if verb not in verb_map:
        return [0, 0, 0, 0], False
    encoded = [verb_map[verb]]
    for i in range(3):
        encoded.append(ord(noun[i]) / 65535.0 if i < len(noun) else 0)
    return encoded, True

# 数据准备与模型训练
x = np.array([encode_command(cmd)[0] for cmd in commands["text"]], dtype=np.float32)
y = tf.keras.utils.to_categorical(commands["intent"], num_classes=3)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(4,)),
    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(32, activation="relu"),
    tf.keras.layers.Dense(3, activation="softmax")
])
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
model.fit(x_train, y_train, epochs=100, batch_size=2, validation_data=(x_test, y_test), verbose=1)

# 城市 ID 获取
def get_city_id(city_name, api_key):
    url = f"https://geoapi.qweather.com/v2/city/lookup?location={city_name}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200 and response.json().get("code") == "200":
        data = response.json()
        if data["location"]:
            return data["location"][0]["id"]
    return None

# 天气查询
def get_weather(city_id, api_key):
    url = f"https://devapi.qweather.com/v7/weather/now?location={city_id}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200 and response.json().get("code") == "200":
        data = response.json()
        return f"天气：{data['now']['text']}，温度 {data['now']['temp']}°C"
    return "天气查询失败"

# 语音播报
def speak(text):
    tts = gTTS(text=text, lang="zh-CN")  # 中文
    tts.save("output.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


# 处理语音指令
def process_voice_command(recognizer, source, model, api_key):
    import time
    import pygame
    print("请说指令（3秒内，如‘开灯’或‘查上海天气’）：")
    try:
        pygame.mixer.init()
        pygame.mixer.Sound("button.mp3").play()
        time.sleep(0.5)  # 等待播放
    except Exception as e:
        print(f"(无提示音，错误: {str(e)})")  # 文件缺失时提示
    time.sleep(0.5)
    try:
        audio = recognizer.listen(source, timeout=3)
        command = recognizer.recognize_google(audio, language="zh-CN")
        print(f"识别结果: {command}")
        encoded, is_valid = encode_command(command)
        if not is_valid:
            return "无法识别该指令"
        if "查" in command and "天气" in command:
            city = command.replace("查", "").replace("天气", "").strip()
            city_id = get_city_id(city, api_key)
            if city_id:
                return f"{city} {get_weather(city_id, api_key)}"
            return f"未找到 {city} 的城市 ID"
        X_new = np.array([encoded], dtype=np.float32)
        prediction = model.predict(X_new, verbose=0)
        intent = np.argmax(prediction)
        if max(prediction[0]) < 0.7:
            return "无法识别该指令"
        return {1: "设备打开", 0: "设备关闭", 2: "查询信息"}[intent]
    except sr.WaitTimeoutError:
        return "没听到声音，请再说一次"
    except sr.UnknownValueError:
        return "无法识别语音"
    except sr.RequestError:
        return "网络或API错误"

# 主程序
api_key = "cc8a12efcb214d79b6478d309889b6bb"  # 替换为和风天气 api_key
recognizer = sr.Recognizer()
try:
    with sr.Microphone() as source:
        while True:
            result = process_voice_command(recognizer, source, model, api_key)
            print(result)
            speak(result)
except KeyboardInterrupt:
    print("\n程序被手动中断")