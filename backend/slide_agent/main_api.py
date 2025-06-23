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
from slide_agent.agent import root_agent

@click.command()
@click.option("--host", "host", default="localhost", help="服务器绑定的主机名（默认为 localhost,可以指定具体本机ip）")
@click.option("--port", "port", default=10011,help="服务器监听的端口号（默认为 10011）")
@click.option("--agent_url", "agent_url", default="",help="Agent Card中对外展示和访问的地址")
def main(host, port, agent_url=""):
    # 每个小的Agent都流式的输出结果
    streaming = os.environ.get("STREAMING") == "true"
    last_agent_output = True # 只有最后1个agent的输出，用于测试
    agent_card_name = "Writter PPT Agent"
    agent_name = "writter_agent"
    agent_description = "An agent that can help writer medical ppt"
    skill = AgentSkill(
        id=agent_name,
        name=agent_name,
        description=agent_description,
        tags=["writter", "ppt"],
        examples=["writter ppt agent"],
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
    # mcptools = load_mcp_tools(mcp_config_path=mcp_config_path)
    runner = Runner(
        app_name=agent_card.name,
        agent=root_agent,
        artifact_service=InMemoryArtifactService(),
        session_service=InMemorySessionService(),
        memory_service=InMemoryMemoryService(),
    )
    if streaming:
        # 支持流式的SSE模式的输出
        run_config = RunConfig(
            streaming_mode=StreamingMode.SSE,
            max_llm_calls=500
        )
    else:
        run_config = RunConfig(
            streaming_mode=StreamingMode.NONE,
            max_llm_calls=500
        )
    agent_executor = ADKAgentExecutor(runner, agent_card, run_config, last_agent_output)

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
