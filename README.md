# 🚀 MultiAgentPPT

一个基于 A2A + MCP + ADK 的多智能体系统，支持流式并发生成高质量 (可在线编辑）PPT 内容。

## 🧠 项目简介

MultiAgentPPT 利用多智能体架构实现从主题输入到完整演示文稿生成的自动化流程，主要步骤包括：

1. **大纲生成 Agent**：根据用户需求生成初步内容大纲。
2. **Topic 拆分 Agent**：将大纲内容细分为多个主题。
3. **Research Agent 并行工作**：多个智能体分别对每个主题进行深入调研。
4. **Summary Agent 汇总输出**：将调研结果汇总生成 PPT 内容，实时流式返回前端。

## 优点
- **多Agent协作**：通过多智能体并行工作，提高内容生成的效率和准确性。
- **实时流式返回**：支持流式返回生成的 PPT 内容，提升用户体验。
- **高质量内容**：结合外部检索和智能体协作，生成高质量的内容大纲和演示文稿。
- **可扩展性**：系统设计灵活，易于扩展新的智能体和功能模块。

## 近期升级计划
- 多模态的理解图片，图片格式处理（例如方向，大小等检测），用于PPT的不同位置。

## 使用界面截图展示

以下是 MultiAgentPPT 项目的核心功能演示：

### 1. 输入主题界面

用户在界面中输入希望生成的 PPT 主题内容：

![输入主题界面](docs/1测试界面输入主题.png)

### 2. 流式生成大纲过程

系统根据输入内容，实时流式返回生成的大纲结构：

![流式生成大纲](docs/2流式生成大纲.png)

### 3. 生成完整大纲

最终系统将展示完整的大纲，供用户进一步确认：

![完整大纲](docs/3完整大纲.png)

### 4. 流式生成PPT内容

确认大纲后，系统开始流式生成每页幻灯片内容，并返回给前端：

![流式生成PPT](docs/4流式生成PPT.png)


## 📊 并发的多Agent的协作流程
```mermaid
flowchart TD
    A[大纲生成 Agent<br>根据用户需求生成初步内容大纲] --> B[Topic 拆分 Agent<br>将大纲细分为多个主题]
    B --> C1[Research Agent 1<br>对主题 1 调研]
    B --> C2[Research Agent 2<br>对主题 2 调研]
    B --> C3[Research Agent N<br>对主题 N 调研]
    C1 --> D[Summary Agent 汇总输出<br>整合调研结果生成 PPT 内容]
    C2 --> D
    C3 --> D
    D --> E[实时流式返回前端]
```


## 🗂️ 项目结构

```bash
MultiAgentPPT/
├── backend/              # 后端多Agent服务目录
│   ├── simpleOutline/    # 简化版大纲生成服务（无外部依赖）
│   ├── simplePPT/        # 简化版PPT生成服务（不使用检索或并发）
│   ├── slide_outline/    # 带外部检索的大纲生成大纲服务（大纲根据MCP工具检索后更精准）
│   ├── slide_agent/      # 并发式多Agent PPT生成主要xml格式的PPT内容
├── frontend/             # Next.js 前端界面
```

---

## ⚙️ 快速开始

### 🐍 后端环境配置（Python）

1. 创建并激活 Conda 虚拟环境（推荐python3.11以上版本，否则可能有bug）：

   ```bash
   conda create --name multiagent python=3.12
   conda activate multiagent
   ```

2. 安装依赖：

   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. 设置后端环境变量：

   ```bash
   # 为所有模块复制模板配置文件
   cd backend/simpleOutline && cp env_template .env
   cd ../simplePPT && cp env_template .env
   cd ../slide_outline && cp env_template .env
   cd ../slide_agent && cp env_template .env
   ```

---

### 🧪 启动后端服务

| 模块              | 功能              | 默认端口                       | 启动命令                 |
| --------------- | --------------- | -------------------------- | -------------------- |
| `simpleOutline` | 简单大纲生成          | 10001                      | `python main_api.py` |
| `simplePPT`     | 简单PPT生成         | 10011                      | `python main_api.py` |
| `slide_outline` | 高质量大纲生成（带检索）    | 10001（需关闭 `simpleOutline`） | `python main_api.py` |
| `slide_agent`   | 多Agent并发生成完整PPT | 10011（需关闭 `simplePPT`）     | `python main_api.py` |

---

## 🧱 前端数据库设置和安装与运行（Next.js）

数据库存储用户生成的PPT：


1. 使用 Docker 启动 PostgreSQL：

   ```bash
   docker run --name postgresdb -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=welcome -d postgres
   ```

2. 修改`.env` 示例配置：

   ```env
   DATABASE_URL="postgresql://postgres:welcome@localhost:5432/presentation_ai"
   A2A_AGENT_OUTLINE_URL="http://localhost:10001"
   A2A_AGENT_SLIDES_URL="http://localhost:10011"
   ```

3. 安装依赖并推送数据库模型：

   ```bash
   # 安装前端依赖
   pnpm install
   # 推送数据库模型和插入用户数据
   pnpm db:push
   # 启动前端
   npm run dev
   ```

4. 打开浏览器访问：[http://localhost:3000/presentation](http://localhost:3000/presentation)

---


---

## 🧪 示例数据说明

> 当前系统内置调研示例为：**“电动汽车发展概述”**。如需其他主题调研，请配置对应 Agent 并对接真实数据源。

---

## 📎 参考来源

前端项目部分基于开源仓库：[allweonedev/presentation-ai](https://github.com/allweonedev/presentation-ai)

## 作者微信号
johnsongzc
