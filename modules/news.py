# modules/news_service.py
import requests
import time

class NewsService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://gnews.io/api/v4/top-headlines"
        self.articles = []

    def get_hot_news(self):
        params = {
            "token": self.api_key,
            "lang": "en",
            "max": 10
        }
        print(f"发送新闻请求: {self.base_url}, 参数: {params}")
        for attempt in range(3):
            try:
                response = requests.get(self.base_url, params=params, timeout=5)
                response.raise_for_status()
                data = response.json()
                self.articles = data.get("articles", [])
                result = ""
                for i, article in enumerate(self.articles, 1):
                    result += f"新闻 {i}：{article['title']}\n"
                return result.strip()
            except requests.RequestException as e:
                print(f"获取新闻失败 (尝试 {attempt + 1}/3): {str(e)}")
                if attempt < 2:
                    time.sleep(2)
                else:
                    raise Exception("无法获取新闻，请检查网络或 API 密钥")

    def get_article_content(self, index):
        if 0 <= index < len(self.articles):
            article = self.articles[index]
            return f"{article['title']}\n{article['description']}"
        return "无法获取该新闻内容"