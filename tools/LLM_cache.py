#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2025/6/22
# @File  : LLM_cache.py
# @Author: johnson
# @Desc  : 大语言模型代理，缓存到本地文件
"""
curl -X POST http://localhost:6688/chat/completions \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_AUTH_TOKEN" \
     -d '{
         "model": "qwen-turbo-latest",
         "messages": [
             {"role": "user", "content": "你好"}
         ],
         "stream": true
     }'
"""

import os
import httpx
import hashlib
import asyncio
from fastapi import FastAPI, Request
from starlette.responses import StreamingResponse
from fastapi.responses import PlainTextResponse
from google import genai   #pip install google-genai
import dotenv
dotenv.load_dotenv()
async def generate_google_streaming_text(prompt: str, api_key, model="gemini-2.0-flash"):
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

    for chunk in client.models.generate_content_stream(
            model=model, contents=prompt
    ):
        print(chunk.text, end='')
        yield chunk.text


CACHE_DIR = "llm_cache"
os.makedirs(CACHE_DIR, exist_ok=True)

class AppLogger:
    def __init__(self, log_file="llm.log"):
        self.log_file = log_file
        with open(self.log_file, 'w') as f:
            f.write("")

    def log(self, message: str):
        with open(self.log_file, 'a') as f:
            f.write(message + "\n")
        print(message)

app = FastAPI(title="LLM API Logger")
logger = AppLogger("llm.log")
#模型名称对应的访问的base url， 注意chat/completions结尾哦
provider2url = {
    "openrouter": "https://openrouter.ai/api/v1/chat/completions",
    "qwen-turbo-latest": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
    "qwq-plus-latest": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
    "gpt-4.1": "https://api.openai.com/v1/chat/completions",
    "gpt-4.1-nano-2025-04-14": "https://api.openai.com/v1/chat/completions",
    "deepseek-chat": "https://api.deepseek.com/v1/chat/completions"
}

def check_cache_for_errors(delete_error_files=True):
    print(f"检查缓存文件中是否存在错误内容...， 日志记录到llm.log和{CACHE_DIR}中")
    for filename in os.listdir(CACHE_DIR):
        if filename.endswith(".txt"):
            file_path = os.path.join(CACHE_DIR, filename)
            try:
                find_errors = False
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "error" in content.lower():
                        print(f"⚠️  警告：缓存文件 {filename} 中包含 'error'，这会影响LLM")
                        find_errors = True
                if find_errors and delete_error_files:
                    os.remove(file_path)
                    print(f"已删除错误文件：{file_path}")
            except Exception as e:
                print(f"读取缓存文件 {filename} 失败：{e}")

def get_provider_url_by_model(model: str):
    """
    :param model: 
    :return: 
    """
    assert model in provider2url, f"{model} not support，请手动添加模型对应的供应商url,{provider2url}"
    url = provider2url.get(model)
    return url

def compute_hash(data: str) -> str:
    """计算 SHA256 哈希作为缓存键"""
    return hashlib.sha256(data.encode("utf-8")).hexdigest()

def get_cache_path(hash_key: str) -> str:
    """返回缓存文件路径"""
    return os.path.join(CACHE_DIR, f"{hash_key}.txt")

@app.post("/chat/completions")
async def proxy_request(request: Request):
    body_bytes = await request.body()
    body_str = body_bytes.decode("utf-8")
    logger.log(f"模型请求：{body_str}")
    body = await request.json()
    provider_url = get_provider_url_by_model(body["model"])
    cache_key = compute_hash(body_str)
    cache_path = get_cache_path(cache_key)
    request_cache_path = os.path.join(CACHE_DIR, f"{cache_key}.request")
    if not os.path.exists(request_cache_path):
        logger.log(f"记录请求信息到文件中：{request_cache_path}")
        with open(request_cache_path, 'w', encoding='utf-8') as f:
            f.write(body_str)

    # 读取缓存
    if os.path.exists(cache_path):
        logger.log(f"命中本地缓存：{cache_path}")
        async def cached_stream():
            with open(cache_path, 'r', encoding='utf-8') as f:
                for line in f:
                    print(f"缓存{cache_path}对应的内容是:{line[:100]}")
                    await asyncio.sleep(0.2)  # 每行间隔 0.2 秒
                    yield line  # 每行已含 \n
        return StreamingResponse(cached_stream(), media_type="text/event-stream")

    logger.log(f"未命中缓存，开始请求模型{provider_url}的模型{body['model']}, 请求信息是总长度: {len(body_str)}")

    assert provider_url, "请检查模型名称是否正确,提供的模型是否有对应的链接？"
    async def event_stream():
        lines = []
        async with httpx.AsyncClient(timeout=None, verify=False) as client:
            async with client.stream(
                "POST",
                provider_url,
                json=body,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "text/event-stream",
                    "Authorization": request.headers.get("Authorization"),
                },
            ) as response:
                async for line in response.aiter_lines():
                    if line.strip():  # 忽略空行
                        logger.log(line)
                        lines.append(line + "\n")
                        yield line + "\n"

        # 写入本地缓存文件
        if "Incorrect API key" in lines or "RequestTimeOut" in lines or "error_msg" in lines:
            logger.log(f"ERROR: 请求信息是总长度: {len(body_str)}失败，请求信息: {body_str}")
            logger.log(";".join(lines))
            # 跳过一些错误的的返回
            return
        with open(cache_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        logger.log(f"已写入本地缓存：{cache_path}")

    return StreamingResponse(event_stream(), media_type="text/event-stream")

@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def unsupported_path(request: Request, path_name: str):
    logger.log(f"不支持的路径访问: {request.method} {request.url.path}")
    return PlainTextResponse("错误：不支持的路径", status_code=404)

# 启动时检查缓存中是否包含 "error"
check_cache_for_errors()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=6688)
