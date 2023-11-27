from flask import Flask, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import datetime

app = Flask(__name__)
scheduler = BackgroundScheduler()
scheduler.start()


# 定义一个函数来执行 HTTP 请求
def http_request(url):
    try:
        response = requests.get(url)
        print(f"Requested {url}, response: {response.status_code}")
    except Exception as e:
        print(f"Error requesting {url}: {e}")


# 设置定时任务的路由
@app.route('/set-timer', methods=['POST'])
def set_timer():
    data = request.json
    url = data.get("url")
    cron_expression = data.get("cron")
    delay = data.get("delay")

    if delay:
        # 延时任务
        delay_seconds = int(delay)
        scheduler.add_job(http_request, 'date',
                          run_date=datetime.datetime.now() + datetime.timedelta(seconds=delay_seconds), args=[url])
    elif cron_expression:
        # Cron 表达式任务
        scheduler.add_job(http_request, 'cron', cron=cron_expression, args=[url])
    else:
        return jsonify({"error": "No valid timer setting provided"}), 400

    return jsonify({"message": "Timer set successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True)
