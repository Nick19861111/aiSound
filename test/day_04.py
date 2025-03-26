#学习逻辑回归,基础代码

import sklearn
from sklearn.linear_model import LogisticRegression
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# #
# # #数据：温度vs空调开关（0=关，1是代表开）
# x = np.array([[10],[20],[30],[40]]) #温度的训练数据
# y = np.array([0,1,1,0]) #是否开启空调的数据
# #
# model = LogisticRegression()
# model.fit(x,y)
#
# # 预测模型的好坏区别
# from sklearn.metrics import accuracy_score, confusion_matrix
#
# y_true = [0,0,1,1]
# y_pred = model.predict(x)
#
# print("准确率:", accuracy_score(y_true, y_pred))
# print("混淆矩阵:\n", confusion_matrix(y_true, y_pred))

data = pd.read_csv("train.csv") #读取数据
data["Sex"] = data["Sex"].map({"male": 0, "female": 1})
x = data[["Age", "Sex"]].fillna(0)
y = data['Survived'].values.ravel()
model = LogisticRegression()
model.fit(x,y)

# 预测不同年龄（假设男性）
ages = [10, 20, 30, 40, 50, 60]
X_predict = pd.DataFrame([[age, 0] for age in ages], columns=["Age", "Sex"])
probs = model.predict_proba(X_predict)[:, 1]  # 取生存概率

# 画柱状图
plt.bar(ages, probs)
plt.title("model yu ce")
plt.xlabel("age")
plt.ylabel("Survived")
plt.show()
