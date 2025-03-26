# main.py
import yaml
import time
import jieba
import datetime  # 添加 datetime 模块
from modules import VoiceRecognizer, WeatherService, Speaker, IntentParser, NewsService

# 加载配置
with open("config/config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# 初始化模块
voice = VoiceRecognizer()
weather = WeatherService(config["api"]["weather_key"])
news = NewsService(config["api"]["gnews_key"])
speaker = Speaker()
nlp = IntentParser(None)

# 全局状态
context = None
stop_program = False

try:
    print("开始监听（说‘武汉 天气’或‘开灯’或‘查新闻’或‘停止’）...")
    while not stop_program:
        text = voice.listen()
        if not text:
            result = config["responses"]["no_sound"]
            speaker.speak(result)
            print(result)
            continue

        if text == "error_recognition":
            result = config["responses"]["recognition_error"]
            speaker.speak(result)
            print(result)
            continue

        print(f"识别结果: {text}")
        stop_keywords = ["停止", "退出", "停职", "停", "停止播放", "暂停", "停下", "别说了", "闭嘴"]
        if any(keyword in text for keyword in stop_keywords) and context != "awaiting_news_selection":
            print("检测到停止指令，程序退出")
            speaker.speak("已停止，程序退出")
            stop_program = True
            continue

        intent = nlp.parse(text, context)
        print(f"意图解析结果: {intent}")

        if intent.startswith("check_weather_"):
            cities_time = intent.split("_")[1:]
            cities = []
            for item in cities_time[:-1]:
                cities.extend([c for c in item.split("_") if c in ["上海", "武汉", "长沙", "南京", "北京", "广州"]])
            time_frame = cities_time[-1] if cities_time and cities_time[-1] in ["now", "today", "tomorrow"] else "now"
            result = ""
            if cities:
                for city in cities:
                    print(f"处理城市: {city}")
                    weather_info = weather.get_weather(city)
                    result += f"{city} {time_frame} 天气：{weather_info.split('天气：')[-1]}\n"
            else:
                result = "请告诉我您想查询哪个城市的天气，例如‘武汉 天气’"
            context = None
            speaker.speak(result.strip())
            print(result.strip())
        elif intent == "turn_on_light":
            result = config["responses"]["turn_on_light"]
            context = None
            speaker.speak(result)
            print(result)
        elif intent == "turn_off_light":
            result = config["responses"]["turn_off_light"]
            context = None
            speaker.speak(result)
            print(result)
        elif intent == "check_news":
            print("开始处理 check_news 意图")
            print("准备播报：正在获取新闻，请稍候")
            speaker.speak("正在获取新闻，请稍候")
            print("播报完成：正在获取新闻，请稍候")
            print("尝试获取新闻...")
            try:
                result = news.get_hot_news()
                print(f"新闻获取结果: {result}")
            except Exception as e:
                print(f"获取新闻失败: {str(e)}")
                result = "无法获取新闻，请稍后再试"
                speaker.speak(result)
                continue
            result += "\n请说‘第一’到‘第十’选择新闻，10 秒后默认读第一条"
            context = "awaiting_news_selection"

            print("准备播报新闻列表")
            interrupt_text = speaker.speak(result, voice_recognizer=voice)
            print("播报完成：新闻列表")

            if interrupt_text:
                stop_keywords = ["停止", "退出", "停职", "停", "停止播放", "暂停", "停下", "别说了", "闭嘴"]
                if any(keyword in interrupt_text for keyword in stop_keywords):
                    print("检测到停止指令，退出新闻列表读取状态")
                    context = None
                    speaker.speak("已退出新闻列表读取状态")
                    continue
                intent = nlp.parse(interrupt_text, context)
                print(f"新闻选择意图: {intent}")
                if intent.startswith("select_news_"):
                    index = int(intent.split("_")[-1])
                    result = news.get_article_content(index)
                    context = None
                    speaker.speak(result)
                    print(result)
                    continue

            start_time = time.time()
            while time.time() - start_time < 10:
                text = voice.listen(timeout=1.0)
                if text:
                    stop_keywords = ["停止", "退出", "停职", "停", "停止播放", "暂停", "停下", "别说了", "闭嘴"]
                    if any(keyword in text for keyword in stop_keywords):
                        print("检测到停止指令，退出新闻列表读取状态")
                        speaker.stop()
                        context = None
                        speaker.speak("已退出新闻列表读取状态")
                        break
                    intent = nlp.parse(text, context)
                    print(f"新闻选择意图: {intent}")
                    if intent.startswith("select_news_"):
                        speaker.stop()
                        index = int(intent.split("_")[-1])
                        result = news.get_article_content(index)
                        context = None
                        speaker.speak(result)
                        print(result)
                        break
                    else:
                        print("无法识别新闻选择指令，提示用户重试")
                        speaker.speak("无法识别您的选择，请说‘第一’到‘第十’，例如‘第三’")
            else:
                if not stop_program:
                    speaker.stop()
                    result = "无法识别选择，默认读取第一条"
                    result += "\n" + news.get_article_content(0)
                    context = None
                    speaker.speak(result)
                    print(result)
        elif intent == "check_time":
            current_time = datetime.datetime.now().strftime("%H点%M分")
            result = f"现在是{current_time}"
            context = None
            speaker.speak(result)
            print(result)
        else:
            result = config["responses"]["unknown_command"]
            result += " 请再说一遍，我没听清楚。您可以试试说‘武汉 天气’或‘查新闻’。"
            context = None
            speaker.speak(result)
            print(result)
except KeyboardInterrupt:
    print("\n程序正在退出...")
    speaker.cleanup()
    voice.cleanup()
    print("程序已退出")