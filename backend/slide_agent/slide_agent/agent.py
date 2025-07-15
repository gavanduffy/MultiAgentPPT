from google.adk.agents.llm_agent import Agent
from google.adk.agents.sequential_agent import SequentialAgent

from .sub_agents.research_topic.agent import parallel_search_agent
from .sub_agents.split_topic.agent import split_topic_agent
from .sub_agents.ppt_writer.agent import ppt_generator_loop_agent
from dotenv import load_dotenv
# 在模块顶部加载环境变量
load_dotenv('.env')

root_agent = SequentialAgent(
    name="WritingSystemAgent",
    description="多Agent写作系统的总协调器",
    sub_agents=[
        split_topic_agent,
        parallel_search_agent,
        ppt_generator_loop_agent
    ],
)
