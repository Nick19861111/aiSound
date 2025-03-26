# modules/intent_parser.py
import jieba

class IntentParser:
    def __init__(self, config):
        self.config = config
        self.cities = ["上海", "武汉", "长沙", "南京", "北京", "广州"]
        self.time_frames = ["now", "today", "tomorrow"]

    def parse(self, text, context=None):
        words = jieba.lcut(text)
        print(f"分词结果: {words}")

        cities = [word for word in words if word in self.cities]
        print(f"提取城市: {cities}")

        if context == "awaiting_news_selection":
            number_map = {
                "第一": 0, "第二": 1, "第三": 2, "第四": 3, "第五": 4,
                "第六": 5, "第七": 6, "第八": 7, "第九": 8, "第十": 9,
                "一": 0, "二": 1, "三": 2, "四": 3, "五": 4,
                "六": 5, "七": 6, "八": 7, "九": 8, "十": 9
            }
            for word in words:
                if word in number_map:
                    return f"select_news_{number_map[word]}"
            return "unknown"

        if "现在" in text and "几点" in text:
            return "check_time"

        if "天气" in text:
            time_frame = "now"
            for tf in self.time_frames:
                if tf in text.lower():
                    time_frame = tf
                    break
            if cities:
                return f"check_weather_{'_'.join(cities)}_{time_frame}"
            return "check_weather"

        if "开灯" in text:
            return "turn_on_light"
        if "关灯" in text:
            return "turn_off_light"

        if "新闻" in text:
            return "check_news"

        return "unknown"