import requests

# 替换为你的 API 密钥
GNEWS_API_KEY = "76f2537e330e6fa8aa565f0cc97d60af"
# 使用搜索接口进行关键词查询
BASE_URL = "https://gnews.io/api/v4/search"

params = {
    # 去掉了布尔运算符“OR”，改为简单空格分隔关键词
    "q": "finance market economy",
    "lang": "en",
    "token": GNEWS_API_KEY,
    "max": 3
}

try:
    response = requests.get(BASE_URL, params=params, timeout=5)
    response.raise_for_status()
    data = response.json()
    print(data)
    if "articles" in data and data["articles"]:
        for i, article in enumerate(data["articles"]):
            print(f"金融新闻 {i+1}：{article['title']}")
    else:
        print("无法获取金融新闻")
        print(f"响应: {data}")
except Exception as e:
    print(f"错误: {str(e)}")
