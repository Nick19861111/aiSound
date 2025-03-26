import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
import speech_recognition as sr

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

# 数据准备
x = np.array([encode_command(cmd)[0] for cmd in commands["text"]], dtype=np.float32)
y = tf.keras.utils.to_categorical(commands["intent"], num_classes=3)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# 模型训练
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(4,)),
    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(32, activation="relu"),
    tf.keras.layers.Dense(3, activation="softmax")
])
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
model.fit(x_train, y_train, epochs=100, batch_size=2, validation_data=(x_test, y_test), verbose=1)

# 预测函数
def predict_intent(text):
    encoded, is_valid = encode_command(text)
    if not is_valid:
        print(f"输入: {text}, 无法识别该指令")
        return -1  # 无效标志
    X_new = np.array([encoded], dtype=np.float32)
    prediction = model.predict(X_new, verbose=0)
    intent = np.argmax(prediction)
    print(f"输入: {text}, 预测概率: {prediction}, 类别: {intent}")
    if max(prediction[0]) < 0.7:
        print("置信度过低，无法识别")
        return -1
    return intent

# 语音输入与整合
recognizer = sr.Recognizer()
try:
    while True:
        with sr.Microphone() as source:
            print("请说指令（3秒内）：")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = recognizer.listen(source, timeout=3)
                command = recognizer.recognize_google(audio, language="zh-CN")
                print(f"识别结果: {command}")
                intent = predict_intent(command)
                if intent == 1:
                    print("设备打开")
                elif intent == 0:
                    print("设备关闭")
                elif intent == 2:
                    print("查询信息")
                else:
                    print("无法识别该指令")
            except sr.WaitTimeoutError:
                print("没听到声音，请再说一次")
            except sr.UnknownValueError:
                print("无法识别语音")
            except sr.RequestError:
                print("网络或API错误")
except KeyboardInterrupt:
    print("\n程序被手动中断")