# 导入必要的库
import pandas as pd              # 作用：处理表格数据（指令和意图）
                                 # 确认：用于创建20条指令的 DataFrame，已正确导入

import numpy as np               # 作用：处理数组和数学运算（如编码、拆分）
                                 # 确认：支持 x 和 y 的生成，已正确导入

import tensorflow as tf          # 作用：主框架，搭建和训练神经网络
                                 # 确认：版本 2.18.0，已正常使用

from sklearn.model_selection import train_test_split  # 作用：拆分训练和测试数据
                                                      # 确认：将20条数据拆为16训练+4测试，已正确导入

# 固定随机种子，确保结果可复现
tf.random.set_seed(42)           # 作用：固定 TensorFlow 的随机数生成（如权重初始化）
                                 # 确认：与 np.random.seed 配合，结果一致

np.random.seed(42)               # 作用：固定 NumPy 的随机数生成（如数据拆分）
                                 # 确认：保证 train_test_split 每次拆分相同

# 定义扩充数据（20条指令）
commands = pd.DataFrame({        # 作用：创建数据表格，存储指令和意图
    "text": [                    # 列1：指令文本
        "开灯", "关灯", "查看天气", "开风扇", "关空调",
        "开电视", "关电视", "查时间", "开窗户", "关门",
        "开灯亮", "关风扇", "查温度", "开空调", "关窗户",
        "开音响", "关音响", "查日期", "开电扇", "关电灯"
    ],
    "intent": [                  # 列2：意图（0:关，1:开，2:查）
        1, 0, 2, 1, 0,
        1, 0, 2, 1, 0,
        1, 0, 2, 1, 0,
        1, 0, 2, 1, 0
    ]
})                               # 确认：20条数据，意图分布均匀（8开，8关，4查）

# 定义编码函数，将指令转为数值
def encode_command(cmd):         # 作用：将文本指令转为4维数值向量
    if not cmd:                  # 检查：如果指令为空
        return [0, 0, 0, 0]      # 返回：4个0，表示无输入
    verb = cmd[0]                # 提取：动词（首字符，如“开”“关”“查”）
    noun = cmd[1:]               # 提取：名词（剩余字符，如“灯”“风扇”）
    encoded = [ord(verb)]        # 转换：动词转为Unicode值（如“开”=24320）
    for i in range(3):           # 循环：处理名词的前3个字符
        if i < len(noun):        # 检查：名词是否有第i个字符
            encoded.append(ord(noun[i]))  # 转换：字符转为Unicode
        else:
            encoded.append(0)    # 补齐：不足3个字符补0
    return [val / 65535.0 for val in encoded]  # 归一化：除以Unicode最大值，缩放到0-1
                                 # 确认：如“开风扇”=[0.3705, 0.5966, 0.3838, 0]，编码正确

# 生成输入数据 x
x = np.array([encode_command(cmd) for cmd in commands["text"]], dtype=np.float32)  
                                 # 作用：将20条指令编码为 20x4 数组
                                 # 确认：x 形状为 (20, 4)，float32 类型，适配TensorFlow

# 生成标签 y
y = tf.keras.utils.to_categorical(commands["intent"], num_classes=3)  
                                 # 作用：将意图转为 one-hot 编码，20x3 数组
                                 # 确认：如 [1, 0, 0] 表示 0（关），[0, 1, 0] 表示 1（开），正确生成

# 拆分训练和测试数据
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)  
                                 # 作用：80%训练（16条），20%测试（4条）
                                 # 确认：random_state=42 固定拆分，包含“开风扇”等关键数据

# 搭建优化后的神经网络模型
model = tf.keras.Sequential([    # 作用：定义顺序模型，堆叠层
    tf.keras.layers.Input(shape=(4,)),  # 输入层：4维输入（编码向量）
    tf.keras.layers.Dense(64, activation="relu"),  # 隐藏层1：64神经元，ReLU激活
    tf.keras.layers.Dropout(0.2),  # Dropout：丢弃20%输出，防过拟合
    tf.keras.layers.Dense(32, activation="relu"),  # 隐藏层2：32神经元，ReLU激活
    tf.keras.layers.Dense(3, activation="softmax")  # 输出层：3类别，Softmax输出概率
])                               # 确认：模型结构合理，Dropout 增强泛化

# 定义优化器
optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)  
                                 # 作用：Adam优化器，学习率0.001（默认）
                                 # 确认：适合小数据集，收敛稳定

# 编译模型
model.compile(                   # 作用：配置训练参数
    optimizer=optimizer,         # 优化器：Adam
    loss="categorical_crossentropy",  # 损失函数：交叉熵，适用于多分类
    metrics=["accuracy"]         # 指标：准确率，评估模型性能
)                                # 确认：编译成功，参数合理

# 训练模型（你改为 epochs=200）
model.fit(                       # 作用：训练模型，调整权重
    x_train, y_train,            # 数据：训练集（16条）
    epochs=200,                  # 轮数：200次，充分学习
    batch_size=2,                # 批次：每次2条，平稳更新
    validation_data=(x_test, y_test),  # 验证：测试集（4条）
    verbose=1                    # 显示：训练进度条
)                                # 确认：epochs=200 时预测正确，训练充分

# 定义预测函数
def predict_intent(text):        # 作用：预测单条指令的意图
    X_new = np.array([encode_command(text)], dtype=np.float32)  # 编码：1x4 数组
    prediction = model.predict(X_new, verbose=0)  # 预测：1x3 概率数组
    intent = np.argmax(prediction)  # 分类：取最大概率索引
    print(f"输入: {text}, 预测概率: {prediction}, 类别: {intent}")  # 输出：结果详情
    return intent                # 返回：意图类别（0, 1, 2）
                                 # 确认：“开风扇”返回 1，预测正常

# 测试循环
try:                             # 作用：捕获异常，优雅退出
    while True:                  # 循环：持续接收输入
        command = input("说指令（输入‘退出’结束）: ")  # 输入：用户指令
        if command == "退出":    # 检查：退出条件
            print("程序退出")    # 提示：退出信息
            break                # 跳出：结束循环
        intent = predict_intent(command)  # 预测：调用函数
        if intent == 1:          # 判断：意图为1
            print("设备打开")    # 输出：开类结果
        elif intent == 0:        # 判断：意图为0
            print("设备关闭")    # 输出：关类结果
        else:                    # 判断：意图为2
            print("查询信息")    # 输出：查类结果
except KeyboardInterrupt:        # 捕获：Ctrl+C 中断
    print("\n程序被手动中断，已退出")  # 提示：中断信息
                                 # 确认：退出正常，无 KeyboardInterrupt 报错