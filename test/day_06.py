#主要内容
#1.理解决策树
#2.学习随机森林
#3.应用到titanic数据集对比逻辑回归效果

#什么是决策树，他的作用
#决策树就像一个流程图，从根节点开始，每次根据某个特征的取值，将数据分到不同的分支，直到到达叶节点。每个叶节点代表一个类别标签（分类）或一个预测值（回归）。
#                             天气状况
#                            /        \
#                          晴朗        阴雨
#                         /   \          \
#                      温度适宜  温度不适宜     湿度
#                     /     \            /   \
#                   适合     不适合       低     高
#                                      /   \
#                                    适合   不适合
#通过分类进行一个数据的回归，给出一个结果

#demo1 实际相关操作
# import pandas as pd
# from sklearn.tree import DecisionTreeClassifier
#
# #读取对应的数据
# data = pd.read_csv("train.csv")
# #数据格式化
# data["Sex"] = data["Sex"].map({"male": 0, "female": 1})
# x = data[["Age","Sex","Pclass"]].fillna(0)
# y = data["Survived"].values.ravel()
#
# #训练模型
# model = DecisionTreeClassifier(max_depth=3)
# model.fit(x,y)
#
# #预测结果
# X_new = pd.DataFrame([[30,1,1]],columns=["Age","Sex","Pclass"])#30岁的男的
# print(model.predict(X_new))

#==========================================================================

#demo2 随机森林的方法
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# #读取对应的数据
data = pd.read_csv("train.csv")
#数据格式化
data["Sex"] = data["Sex"].map({"male": 0, "female": 1})
x = data[["Age","Sex","Pclass"]].fillna(0)
y = data["Survived"].values.ravel()

rf_model = RandomForestClassifier(n_estimators=100,max_depth=3)
rf_model.fit(x,y)

X_new = pd.DataFrame([[30,1,1]],columns=["Age","Sex","Pclass"])#30岁的男的

print(rf_model.predict(X_new))
