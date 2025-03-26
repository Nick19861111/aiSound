#条件语句的基础使用
#>,<,==,in,in是第一次使用等会使用例子

# temp = 15
# if temp > 30:
#     print("太热了，开空调")
# elif temp < 20:
#     print("有点冷关空调")
# else:
#     print("温度刚刚好")


#demo2
# weather = "下雨"
# weather = "晴天"
# if "雨" in weather:
#     print("带伞出门")
# elif "晴" in weather:
#     print("出门晒太阳")
# else:
#     print("天气不错")

#用户输入的部分
# text = input("提示文字：")
#
# if text == "你好":
#     print("你好！有什么需要帮助的吗")
# else:
#     print("在说一遍")

#基础的命令工作程序
# tasks = ["关灯","开灯","查看天气"]
#
# command = input("指令：")
# for task in tasks:
#     if command == task:
#         print("执行："+task);
#         break;
# else:
#     print("暂时没有这个功能")

# 库的基础使用
# import numpy as np
# import pandas as pd
#
# statuses = np.array(["on","off","on"])
# print(statuses)
# data = pd.DataFrame({"device":["lamp","aircon","fan"],"status":["on","off","on"]})
# print(data)
# data.loc[len(data)] = ["tv","off"]
# print(data)

#可视化的程序基础
# import pandas as pd
# import matplotlib.pyplot as plt
#
# log = pd.DataFrame({"command":["开灯","关空调"],"time":[1,2]})
# log.to_csv("log.csv")#写入到csv文件下
# log = pd.read_csv("log.csv") #读取csv文件
# plt.plot(log["time"],log.index)
# plt.title("time")
# plt.show()

# 线形回归的基础
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

x = np.array([[1],[2],[3],[4]]) #时间
y = np.array([20,26,11,36])

#训练模型
model = LinearRegression()
model.fit(x,y)

#预测
print(model.predict([[5]])) #第五个小时的温度

#可视化
plt.plot(x,y,color='blue')
plt.plot(x,model.predict(x),color='red')
plt.title("wenduji")
plt.show()