#复习课程
#demo1 使用sklearn库
print("hello ai")
import sklearn
print(sklearn.__version__)

#python的一些基础使用
#函数
def update_device(device,status):
    devices = {"lamp":"off","aircon":"off"}
    devices[device] = status # 这是一个哈希表的形式
    return devices

print(update_device("lamp","on"))

#一个代码的基础雏形
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier

# 模拟数据
commands = pd.DataFrame({
    "text": ["开灯", "关灯", "查看天气", "开风扇", "关空调",
             "开电视", "关电视", "查时间", "开窗户", "关门"],
    "intent": [1, 0, 2, 1, 0, 1, 0, 2, 1, 0]
})

# 转为数值特征
def encode_command(cmd):
    if not cmd or len(cmd) < 1:
        return [0, 0, 0, 0]
    verb = cmd[0]
    noun = cmd[1:]
    encoded = [ord(verb)]
    for i in range(3):
        if i < len(noun):
            c = noun[i]
            encoded.append(ord(c))
        else:
            encoded.append(0)
    return encoded

x = np.array([encode_command(cmd) for cmd in commands["text"]])
y = commands["intent"]

# 训练模型
model = DecisionTreeClassifier()
model.fit(x, y)
print("训练数据预测:", model.predict(x))

# 预测函数
def predict_intent(text):
    if not isinstance(text, str) or len(text) < 2 or not any(ord(c) > 127 for c in text):
        print("无效输入（需中文指令），返回默认值 0")
        return 0
    X_new = np.array([encode_command(text)])
    prediction = model.predict(X_new)[0]
    print(f"输入: {text}, X_new: {X_new}, 预测: {prediction}")
    return prediction

# 主程序
def voice_control_system():
    print("智能管家启动！")
    while True:
        command = input("说指令（输入‘退出’结束）: ")
        if command == "退出":
            print("管家关闭")
            break
        intent = predict_intent(command)
        if intent == 1:
            print("设备打开")
        elif intent == 0:
            print("设备关闭")
        else:
            print("查询信息")

if __name__ == "__main__":
    voice_control_system()