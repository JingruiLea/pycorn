#!/bin/sh

# 获取当前时间，格式为 yyyyMMdd_HH:mm:ss
version=$(date "+%Y%m%d%H%M%S")
echo "The version is $version"

# 构建镜像
docker build . -t registry.ap-southeast-1.aliyuncs.com/pdfgpt/pycron:$version
docker push registry.ap-southeast-1.aliyuncs.com/pdfgpt/pycron:$version

# 使用 sed 替换 deployment.yaml 中的镜像版本
ssh ali "kubectl set image deployment/pycron pycron=registry.ap-southeast-1.aliyuncs.com/pdfgpt/pycron:$version"