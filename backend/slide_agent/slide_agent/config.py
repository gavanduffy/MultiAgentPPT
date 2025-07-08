#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2025/6/19 11:16
# @File  : config.py.py
# @Author: johnson
# @Contact : github: johnson7788
# @Desc  :  项目的基本配置

##每个Agent的使用的模型配置
SPLIT_TOPIC_AGENT_CONFIG = {
    # "provider": "google",
    # "model": "gemini-2.0-flash",
    "provider": "ali",
    "model": "qwen-turbo-latest",
}

TOPIC_RESEARCH_AGENT_CONFIG = {
    # "provider": "google",
    # "model": "gemini-2.0-flash",
    # "provider": "deepseek",
    # "model": "gpt-4.1",
    # "model": "gpt-4.1-nano-2025-04-14",
    # "model": "deepseek-chat",
    "provider": "ali",
    "model": "qwen-turbo-latest",
}
SUMMARY_AGENT_CONFIG = {
    # "provider": "google",
    # "model": "gemini-2.0-flash",
    # "provider": "openai",
    # "model": "gpt-4.1",
    # "model": "gemini-2.0-flash",
    # "provider": "local_ali",  # 如果使用local_ali需要使用tools/LLM_cache.py用于中间缓存
    # "model": "qwen-turbo-latest",
    "provider": "ali",
    "model": "qwen-turbo-latest",
}