
from typing import Dict, List, Any, AsyncGenerator, Optional, Union
from google.genai import types
from google.adk.agents.llm_agent import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest, LlmResponse
from ...config import SUMMARY_AGENT_CONFIG
from ...create_model import create_model
from . import prompt


def my_before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    # 1. 检查每个并发的子agent的输入，然后读取state对应的key
    research_output_keys = callback_context.state.get("research_output_keys", [])
    assert len(research_output_keys) >0, "没有获取到research_output_keys，请检查research agent的输出代码"
    # 逐个读取所有研究发现的内容
    llm_request.contents = [] # 清空输入
    research_outputs = []
    for research_output_key in research_output_keys:
        research_output = callback_context.state.get(research_output_key, "")
        assert research_output, f"没有获取到{research_output}的agent的输出，请检查research agent的输出"
        research_outputs.append(research_output_key + '\n' + research_output)
    research_outputs_content = "\n\n".join(research_outputs)
    llm_request.contents.append(
        types.Content(role="user", parts=[types.Part(text=research_outputs_content)])
    )
    # 返回 None，继续调用 LLM
    return None

summary_writer_agent = Agent(
    model=create_model(model=SUMMARY_AGENT_CONFIG["model"], provider=SUMMARY_AGENT_CONFIG["provider"]),
    name="SummaryAgent",
    description="专业的医学文章撰写和内容整合医学专家",
    instruction=prompt.PPT_AGENT_PROMPT,
    before_model_callback=my_before_model_callback
)
