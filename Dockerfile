# 使用官方 Python 运行时作为父镜像
FROM --platform=linux/amd64 registry.ap-southeast-1.aliyuncs.com/pdfgpt/pycron:v0.0.5
#RUN apt-get update && apt-get install -y tzdata
#ENV TZ=Asia/Shanghai
#RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 设置工作目录为 /app
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# 使端口 8000 可供此容器外部的环境使用
ENV PYTHONUNBUFFERED=1
ENV LANG zh_CN.UTF-8

# 定义环境变量
EXPOSE 8000

# 使用 gunicorn 运行应用
CMD ["gunicorn", "-b", "0.0.0.0:8000", "wsgi:app"]
