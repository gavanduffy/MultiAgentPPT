#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2025/6/22
# @File  : LLM_cache.py
# @Author: johnson
# @Desc  : Large Language Model proxy, cached to local files
"""
Can also be configured in .env: HTTP_PROXY
HTTP_PROXY=http://127.0.0.1:7890
HTTPS_PROXY=http://127.0.0.1:7890

curl -X POST http://localhost:6688/chat/completions \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_AUTH_TOKEN" \
     -d '{
         "model": "qwen-turbo-latest",
         "messages": [
             {"role": "user", "content": "Hello"}
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
from google import genai  # pip install google-genai
import dotenv
import time

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
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write("")

    def log(self, message: str):
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(message + "\n")
        print(message)


app = FastAPI(title="LLM API Logger")
logger = AppLogger("llm.log")

# Base URLs for different model providers, note the chat/completions endpoint
provider2url = {
    "openrouter": "https://openrouter.ai/api/v1/chat/completions",
    "qwen-turbo-latest": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
    "qwq-plus-latest": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
    "gpt-4.1": "https://api.openai.com/v1/chat/completions",
    "gpt-4.1-nano-2025-04-14": "https://api.openai.com/v1/chat/completions",
    "deepseek-chat": "https://api.deepseek.com/v1/chat/completions",
    "doubao-seed-1-6-flash-250615": "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
    "doubao-seed-1-6-thinking-250715": "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
    "doubao-seed-1-6-250615": "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
    "deepseek-r1-250528": "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
    "deepseek-v3-250324": "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
}


def check_cache_for_errors(delete_error_files=True):
    print(f"Checking cache files for error content... Logs are recorded in llm.log and {CACHE_DIR}")
    for filename in os.listdir(CACHE_DIR):
        if filename.endswith(".txt"):
            file_path = os.path.join(CACHE_DIR, filename)
            try:
                find_errors = False
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "error" in content.lower():
                        print(f"⚠️ Warning: Cache file {filename} contains 'error', which may affect the LLM.")
                        find_errors = True
                if find_errors and delete_error_files:
                    os.remove(file_path)
                    print(f"Deleted error file: {file_path}")
            except Exception as e:
                print(f"Failed to read cache file {filename}: {e}")


def get_provider_url_by_model(model: str):
    """
    :param model:
    :return:
    """
    assert model in provider2url, f"{model} not supported. Please manually add the corresponding provider URL for the model, {provider2url}"
    url = provider2url.get(model)
    return url


def compute_hash(data: str) -> str:
    """Computes SHA256 hash as cache key"""
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def get_cache_path(hash_key: str) -> str:
    """Returns the cache file path"""
    return os.path.join(CACHE_DIR, f"{hash_key}.txt")


@app.post("/chat/completions")
async def proxy_request(request: Request):
    body_bytes = await request.body()
    body_str = body_bytes.decode("utf-8")
    logger.log(f"Model request: {body_str}")
    body = await request.json()
    provider_url = get_provider_url_by_model(body["model"])
    cache_key = compute_hash(body_str)
    cache_path = get_cache_path(cache_key)
    request_cache_path = os.path.join(CACHE_DIR, f"{cache_key}.request")

    if not os.path.exists(request_cache_path):
        logger.log(f"Recording request information to file: {request_cache_path}")
        with open(request_cache_path, 'w', encoding='utf-8') as f:
            f.write(body_str)

    # Read from cache
    if os.path.exists(cache_path):
        logger.log(f"Cache hit: {cache_path}")

        async def cached_stream():
            with open(cache_path, 'r', encoding='utf-8') as f:
                for line in f:
                    print(f"Content corresponding to cache {cache_path} is: {line[:100]}")
                    await asyncio.sleep(0.2)  # 0.2 seconds delay per line
                    yield line  # Each line already contains \n

        return StreamingResponse(cached_stream(), media_type="text/event-stream")

    logger.log(f"Cache miss. Starting request to model {body['model']} from {provider_url}, total request length: {len(body_str)}")

    assert provider_url, "Please check if the model name is correct, and if the provided model has a corresponding link."

    async def event_stream():
        lines = []
        max_retries = 3
        retry_delay = 1

        for attempt in range(max_retries):
            try:
                logger.log(f"Attempting to connect to LLM server (Attempt {attempt + 1})")

                # Increase timeout and add retry mechanism
                timeout = httpx.Timeout(600.0, connect=20.0)

                async with httpx.AsyncClient(
                        timeout=timeout,
                        verify=False,
                        limits=httpx.Limits(max_connections=20, max_keepalive_connections=10)
                ) as client:

                    headers = {
                        "Content-Type": "application/json",
                        "Accept": "text/event-stream",
                        "User-Agent": "LLM-Cache-Proxy/1.0",
                        "Connection": "keep-alive"
                    }

                    # Add authorization header
                    if request.headers.get("Authorization"):
                        headers["Authorization"] = request.headers.get("Authorization")

                    async with client.stream(
                            "POST",
                            provider_url,
                            json=body,
                            headers=headers,
                    ) as response:
                        logger.log(f"Received response status code: {response.status_code}")

                        # Check response status
                        if response.status_code != 200:
                            error_text = await response.aread()
                            logger.log(f"Request failed, status code: {response.status_code}, error: {error_text}")
                            if attempt < max_retries - 1:
                                logger.log(f"Waiting {retry_delay} seconds before retrying...")
                                await asyncio.sleep(retry_delay)
                                retry_delay *= 2
                                continue
                            else:
                                yield f"data: {{'error': 'Request failed, status code: {response.status_code}'}}\n\n"
                                return

                        # Process streaming response
                        async for line in response.aiter_lines():
                            if line.strip():  # Ignore empty lines
                                logger.log(f"Received data: {line}")
                                lines.append(line + "\n")
                                yield line + "\n"

                        # If successful, break out of retry loop
                        break

            except httpx.RemoteProtocolError as e:
                logger.log(f"Server connection error (Attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    logger.log(f"Waiting {retry_delay} seconds before retrying...")
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                else:
                    error_msg = f"data: 'error': 'Server connection failed after {max_retries} retries'\n\n"
                    yield error_msg
                    return

            except httpx.TimeoutException as e:
                logger.log(f"Request timeout (Attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    logger.log(f"Waiting {retry_delay} seconds before retrying...")
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                else:
                    error_msg = f"data: 'error': 'Request timed out after {max_retries} retries'\n\n"
                    yield error_msg
                    return

            except Exception as e:
                logger.log(f"Unknown error (Attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    logger.log(f"Waiting {retry_delay} seconds before retrying...")
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                else:
                    error_msg = f"data: 'error': 'Unknown error: {str(e)}'\n\n"
                    yield error_msg
                    return

        # Write to local cache file
        if lines:
            # Check for error messages
            content_str = "".join(lines)
            if any(error_keyword in content_str.lower() for error_keyword in
                   ["incorrect api key", "requesttimeout", "error_msg", "error"]):
                logger.log(f"ERROR: Request failed, not writing to cache. Request info length: {len(body_str)}")
                logger.log(f"Error response: {content_str[:500]}...")
                return

            # Write to cache
            try:
                with open(cache_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                logger.log(f"Written to local cache: {cache_path}")
            except Exception as e:
                logger.log(f"Failed to write to cache: {e}")

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def unsupported_path(request: Request, path_name: str):
    logger.log(f"Unsupported path access: {request.method} {request.url.path}")
    return PlainTextResponse("Error: Unsupported path", status_code=404)


# Check for "error" in cache on startup
check_cache_for_errors()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=6688)
