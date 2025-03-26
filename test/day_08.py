#什么是神经网络
#分为三层。 输入层-隐藏层-输出层
#输入的数据传入到隐藏层，隐藏层通过激活函数，把权重和一些参数的结果输出给输出层
#什么是神经原激活函数（这个是吧

#程序代码
inputs = [1,2,3]
weights = [0.2,0.8,-0.5]
bias = 1
output = sum(i * w for i, w in zip(inputs, weights)) + bias
print("加权和:", output)         # 1.3
print("激活输出:", max(0, output))  # 1.3 激活函数

#安装库文件
#pip3 install tensorflow
#pip3 install pandas
#pip3 install numpy
#理解tensorflow和netty本质上来说是一个道理，区别在于一个是网络环境一个是人工智能的库
#降级就不会出现警告了：pip install urllib3==1.26.18

import pandas as pd
import numpy as np
import tensorflow as tf

# 模拟数据
commands = pd.DataFrame({
    "text": ["开灯", "关灯", "查看天气", "开风扇", "关空调",
             "开电视", "关电视", "查时间", "开窗户", "关门"],
    "intent": [1, 0, 2, 1, 0, 1, 0, 2, 1, 0]
})

def encode_command(cmd):
    if not cmd:
        return [0, 0, 0, 0]
    verb = cmd[0]
    noun = cmd[1:]
    encoded = [ord(verb)]
    for i in range(3):
        encoded.append(ord(noun[i]) if i < len(noun) else 0)
    return encoded

x = np.array([encode_command(cmd) for cmd in commands["text"]], dtype=np.float32)
y = tf.keras.utils.to_categorical(commands["intent"], num_classes=3)

# 搭建模型
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(4,)),
    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.Dense(32, activation="relu"),
    tf.keras.layers.Dense(3, activation="softmax")
])

# 编译模型
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# 训练模型
model.fit(x, y, epochs=20, verbose=1)

# 预测函数
def predict_intent(text):
    X_new = np.array([encode_command(text)], dtype=np.float32)
    prediction = model.predict(X_new, verbose=0)
    intent = np.argmax(prediction)
    print(f"输入: {text}, 预测概率: {prediction}, 类别: {intent}")
    return intent

# 测试
try:
    while True:
        command = input("说指令（输入‘退出’结束）: ")
        if command == "退出":
            print("程序退出")
            break
        intent = predict_intent(command)
        if intent == 1:
            print("设备打开")
        elif intent == 0:
            print("设备关闭")
        else:
            print("查询信息")
except KeyboardInterrupt:
    print("\n程序被手动中断，已退出")