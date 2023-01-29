# python version
FROM python:3.9.10

# 작업 디렉토리
WORKDIR /usr/src/app

# requirements 이동 및 설치
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Project 복사
COPY . .
