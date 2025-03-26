name = "小明"
age = 25
temp = 23.5
is_on = False

print(name)
print(age+1)
print("你好!"+name)
print(type(age)) #获得相关的类型

#列表的练习
tasks = ["开灯","查天气","关门"]
#添加
tasks.append("播放音乐")
tasks.append("打扫房间")
#获得数组的所有数据
for task in tasks:
    print("管家可以做的事:"+task)

#做一个功能需要添加三个数据的和
nums = [1,2,3,4,5]
total = 0
for num in nums:
    total += num

print(total)

#h函数就是功能操作
def say_hello(name):
    print("Hello, " + name)

say_hello("小明")