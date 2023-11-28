from flask import Flask, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import datetime
from mongoengine import *
from config import Config
from job_model import Job

app = Flask(__name__)
scheduler = BackgroundScheduler()
scheduler.start()
db = connect(Config.DB_NAME, host=Config.DB_HOST, port=int(Config.DB_PORT), username=Config.DB_USER,
             password=Config.DB_PASSWD,
             authentication_source='admin')


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
    cron_expression = data.get("cron_expression")
    delay = data.get("delay")
    job_id = data.get("id")

    if delay:
        delay_seconds = int(delay)
        run_at = datetime.datetime.now() + datetime.timedelta(seconds=delay_seconds)
        # 创建 Job 对象并保存到数据库
        job = Job(job_id=job_id, url=url, run_at=run_at)
        job.save()
        scheduler.add_job(http_request, 'date', run_date=run_at, args=[url], id=job_id)

    elif cron_expression:
        # 创建 Job 对象并保存到数据库
        job = Job(job_id=job_id, url=url, cron_expression=cron_expression)
        job.save()
        scheduler.add_job(http_request, 'cron', day_of_week=cron_expression, args=[url], id=job_id)
    else:
        return jsonify({"error": "No valid timer setting provided"}), 400

    return jsonify({"message": "Timer set successfully"}), 200


@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message": "pong"}), 200


# 服务启动后从数据库拉取所有 Job 并添加到调度器
from mongoengine.queryset.visitor import Q


def load_jobs_from_db():
    # 查询所有Cron任务以及未执行的延迟任务
    jobs = Job.objects(Q(run_at__gt=datetime.datetime.now()) | Q(cron_expression__exists=True))
    for job in jobs:
        if job.run_at:
            scheduler.add_job(http_request, 'date', run_date=job.run_at, args=[job.url], id=job.job_id)
        elif job.cron_expression:
            try:
                scheduler.add_job(http_request, 'cron', cron=job.cron_expression, args=[job.url], id=job.job_id)
            except Exception as e:
                print(f"Error adding job {job.job_id} to scheduler: {e}")
