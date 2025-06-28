# 后端的依赖
pip install -r requirements.txt

# 目录结构
simpleOutline   # 用于前端测试的大纲生成
simplePPT     # 用于前端测试的简单PPT生成
slide_outline   # 用于前端的大纲生成，经过检索生成大纲，更专业
slide_agent   #标准多智能体系统，根据大纲生成ppt，更专业

# 开发中（待完善)
super_agent   # 文字版本的多智能体系统，用于串联多个Agent，纯文本的输入，输出，控制大纲和PPT生成
hostAgentAPI  # 纯A2A的API的版本的总Agent，用于串联多个Agent
multiagent_front # super Agent的前端代码

# 多Agent开发时注意实现
每个子Agent的描述必须清晰，因为Super Agent根据每个子Agent任务确定它的输入信息。