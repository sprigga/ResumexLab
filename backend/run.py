import uvicorn

# 已修改於 2025-01-12，原因：增加 limit_max_requests 以支援大檔案上傳
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        limit_max_requests=None,  # 移除請求限制
        timeout_keep_alive=300     # 延長 keep-alive 超時至 5 分鐘
    )
