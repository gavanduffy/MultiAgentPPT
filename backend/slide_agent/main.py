#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2025/6/19 08:49
# @File  : t1.py
# @Author: johnson
# @Contact : github: johnson7788
# @Desc  :
import dotenv
from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.parallel_agent import ParallelAgent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from slide_agent.agent import root_agent
dotenv.load_dotenv()


# 5. 初始化 Runner 并执行
runner = Runner(
    app_name="example",
    agent=root_agent,
    session_service=InMemorySessionService()
)

def parse_event(event):
    parsed_output = {}

    if event.content and event.content.parts:
        part = event.content.parts[0]

        # Parse text content
        if part.text:
            parsed_output = {"type": "text", "content": part.text}

        # Parse function call information
        if part.function_call:
            function_call_name = part.function_call.name
            function_call_args = part.function_call.args
            parsed_output = {
                "type": "function call",
                "content": f"function_name: {function_call_name}, function_args: {function_call_args}"
            }

        # Parse function result information
        if part.function_response:
            function_response_name = part.function_response.name # Assuming name is always present for function_response
            function_response_result = None

            if part.function_response.response and 'result' in part.function_response.response:
                result_obj = part.function_response.response['result']
                if hasattr(result_obj, 'content') and result_obj.content:
                    extracted_texts = []
                    for content_part in result_obj.content:
                        if hasattr(content_part, 'text') and content_part.text:
                            extracted_texts.append(content_part.text)
                    function_response_result = "\n".join(extracted_texts)
                else:
                    function_response_result = result_obj # Fallback if 'content' is not found

            if function_response_result is not None:
                parsed_output = {
                    "type": "function result",
                    "content": f"function_name: {function_response_name}, function_result: {function_response_result}"
                }
            else:
                 # Handle cases where function_response has no result or an empty result
                parsed_output = {
                    "type": "function result",
                    "content": f"function_name: {function_response_name}, function_result: No result or empty result found."
                }

    return parsed_output

async def run_workflow(outline: str):
    # 1. 先准备好所有初始状态
    initial_state = {
        'outline': outline,
    }
    print(f"准备初始状态: {initial_state}")
    session = await runner.session_service.create_session(
        app_name=runner.app_name,
        user_id="user1",
        session_id="session1",
        state=initial_state
    )
    print(f"创建新会话: {session.id}")
    # 验证一下返回的session是否已经包含了state
    print(f"创建后，session.state['outline'] 长度: {len(session.state.get('outline', ''))}")
    message_content = types.Content(parts=[types.Part(text=outline)])
    async for event in runner.run_async(
        user_id="user1",
        session_id="session1",
        new_message=message_content
    ):
        event_out = parse_event(event)
        #打印event的信息
        print(event.author)
        print(event_out.get("type"))
        print(event_out.get("content"))

if __name__ == '__main__':
    # 示例调用
    import asyncio
    outline = """Ivonescimab: Clinical Research and Progress in Non-Small Cell Lung Cancer
1. Introduction
Background: Overview of non-small cell lung cancer (NSCLC) and current treatment challenges.
Rationale for Ivonescimab: Dual targeting of PD-1 and VEGF-A as a novel therapeutic strategy.
2. Mechanism of Action and Pharmacological Characteristics
Bispecific Antibody Design: Tetravalent structure targeting PD-1 and VEGF-A.
Cooperative Binding: Enhanced PD-1 blockade in the presence of VEGF-A.
Fc-Silencing Mutations: Reduced effector function for improved safety.
3. Clinical Research Progress
3.1 Phase 1 Studies
First-in-Human Trials: Safety, pharmacokinetics, and preliminary efficacy in advanced solid tumors.
Key findings: Manageable safety profile and promising antitumor activity.
Dose Escalation: Identification of optimal dosing regimens (e.g., 20 mg/kg Q2W).
3.2 Phase 2 Studies
Monotherapy Efficacy: Objective response rates (ORR) in PD-L1-positive NSCLC.
Subgroup analysis: Higher ORR in patients with PD-L1 TPS ≥50%.
Combination Therapy: Ivonescimab with chemotherapy in first-line NSCLC.
Results: Improved ORR and disease control rate (DCR) in squamous and non-squamous subtypes.
3.3 Phase 3 Studies
HARMONi-A Trial: Ivonescimab plus chemotherapy vs. chemotherapy alone in EGFR-mutant NSCLC post-TKI failure.
Primary endpoint: Progression-free survival (PFS) significantly improved (HR 0.46).
Safety: Manageable toxicity with chemotherapy-related adverse events.
HARMONi-2 Trial: Ivonescimab vs. pembrolizumab in PD-L1-positive NSCLC.
Results: Superior PFS with ivonescimab (11.1 vs. 5.8 months).
4. Comparative Analysis with Other Therapies
4.1 Ivonescimab vs. Pembrolizumab
Efficacy: Longer PFS in PD-L1-positive NSCLC.
Safety: Comparable immune-related adverse events but higher VEGF-related toxicity.
4.2 Ivonescimab vs. Bevacizumab-Based Regimens
Mechanistic Advantage: Dual targeting vs. single-pathway inhibition.
Clinical Outcomes: Higher ORR and PFS in combination with chemotherapy.
4.3 Ivonescimab vs. Amivantamab
Target Spectrum: PD-1/VEGF vs. EGFR/MET.
Patient Subgroups: Ivonescimab benefits broader populations, including EGFR-mutant NSCLC.
5. Safety and Tolerability
Common Adverse Events: Proteinuria, hypertension, and hematologic toxicities.
Grade ≥3 Events: Primarily chemotherapy-related; manageable with dose adjustments.
Unique Safety Profile: Lower incidence of severe immune-related adverse events compared to other PD-1 inhibitors.
6. Future Directions and Challenges
6.1 Ongoing Clinical Trials
Expansion to Other Cancers: Breast, liver, and gastric cancers.
Novel Combinations: Ivonescimab with other immunotherapies or targeted agents.
6.2 Biomarker Development
Predictive Biomarkers: PD-L1 expression, VEGF levels, and tumor microenvironment characteristics.
Patient Stratification: Identifying subgroups most likely to benefit.
6.3 Regulatory and Market Integration
Global Approvals: Current status and potential expansion beyond China.
Cost and Accessibility: Challenges in widespread adoption.
7. Conclusion
Summary of Key Findings: Ivonescimab represents a breakthrough in NSCLC treatment with dual-pathway inhibition.
Clinical Implications: Potential to redefine first- and second-line therapy paradigms.
Future Prospects: Continued research to optimize dosing, combinations, and patient selection."""
    asyncio.run(run_workflow(outline))