#!/bin/bash
# 重建並重啟 Docker 容器
# Created on 2025-01-12
# Purpose: Rebuild Docker containers with updated uvicorn configuration

echo "停止所有容器..."
docker-compose down

echo "重建容器..."
docker-compose build --no-cache

echo "啟動容器..."
docker-compose up -d

echo "等待服務啟動..."
sleep 5

echo "檢查容器狀態..."
docker-compose ps

echo "檢查後端日誌..."
docker-compose logs backend --tail=50

echo "完成！"
