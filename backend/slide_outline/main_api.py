import logging
import os
from dotenv import load_dotenv
load_dotenv()
logfile = os.path.join("api.log")
# 日志的格式
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(name)s -  %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S',
    level=logging.INFO,
    handlers=[
        logging.FileHandler(logfile, mode='w', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

import click
import uvicorn
from adk_agent_executor import ADKAgentExecutor
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from starlette.routing import Route
from google.adk.agents.run_config import RunConfig,StreamingMode
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from starlette.middleware.cors import CORSMiddleware
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from adk_agent import create_agent
from load_mcp import load_mcp_tools


@click.command()
@click.option("--host", "host", default="localhost", help="服务器绑定的主机名（默认为 localhost,可以指定具体本机ip）")
@click.option("--port", "port", default=10001,help="服务器监听的端口号（默认为 10001）")
@click.option("--prompt", "agent_prompt_file", default="prompt.txt",help="Agent 的 prompt 文件路径（默认为 prompt.txt）")
@click.option("--model", "model_name", default="gemini-2.0-flash",help="使用的模型名称（如 deepseek-chat, claude-3-5-sonnet-20241022, claude-sonnet-4-20250514, gpt-4.1）")
@click.option("--provider", "provider", default="google", type=click.Choice(["google","openai", "deepseek", "ali","claude"]),help="模型提供方名称（如 deepseek、openai 等）")
@click.option("--mcp_config", "mcp_config_path", default="mcp_config.json",help="MCP 配置文件路径（默认为 mcp_config.json）")
@click.option("--agent_url", "agent_url", default="",help="Agent Card中对外展示和访问的地址")
def main(host, port, agent_prompt_file, model_name, provider, mcp_config_path, agent_url=""):
    # 每个小的Agent都流式的输出结果
    streaming = os.environ.get("STREAMING") == "true"
    agent_card_name = "PPT Agent"
    agent_name = "ppt_agent"
    agent_description = "可以根据用户的需求生成PPT大纲"
    with open(agent_prompt_file, "r") as f:
        agent_instruction = f.read()
    skill = AgentSkill(
        id=agent_name,
        name=agent_name,
        description=agent_description,
        tags=["ppt", "outline"],
        examples=["生成特斯拉汽车大纲"],
    )

    agent_card = AgentCard(
        name=agent_card_name,
        description=agent_description,
        url=f"http://{host}:{port}/",
        version="1.0.0",
        defaultInputModes=["text"],
        defaultOutputModes=["text"],
        capabilities=AgentCapabilities(streaming=True),
        skills=[skill],
    )
    mcptools = load_mcp_tools(mcp_config_path=mcp_config_path)
    adk_agent = create_agent(model_name, provider, agent_name,agent_description,agent_instruction, mcptools=mcptools)
    runner = Runner(
        app_name=agent_card.name,
        agent=adk_agent,
        artifact_service=InMemoryArtifactService(),
        session_service=InMemorySessionService(),
        memory_service=InMemoryMemoryService(),
    )
    # 支持流式的SSE模式的输出
    if streaming:
        run_config = RunConfig(
            streaming_mode=StreamingMode.SSE,
            max_llm_calls=500
        )
    else:
        run_config = RunConfig(
            streaming_mode=StreamingMode.NONE,
            max_llm_calls=500
        )
    agent_executor = ADKAgentExecutor(runner, agent_card, run_config)

    request_handler = DefaultRequestHandler(
        agent_executor=agent_executor, task_store=InMemoryTaskStore()
    )

    a2a_app = A2AStarletteApplication(
        agent_card=agent_card, http_handler=request_handler
    )
    app = a2a_app.build()
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    main()
