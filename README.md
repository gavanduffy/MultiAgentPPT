🚀 MultiAgentPPT
A multi-agent system based on A2A + MCP + ADK that supports highly concurrent, streaming generation of high-quality (editable online) PPT content.
🧠 I. Project Introduction
MultiAgentPPT leverages a multi-agent architecture to automate the process from theme input to complete presentation generation. The main steps include:
 * Outline Generation Agent: Generates a preliminary content outline based on user requirements.
 * Topic Splitting Agent: Divides the outline content into multiple topics.
 * Research Agent Parallel Work: Multiple agents conduct in-depth research on each topic in parallel.
 * Summary Agent Aggregation Output: Aggregates research results to generate PPT content, returning it to the frontend in real-time via streaming.
Advantages
 * Multi-Agent Collaboration: Improves content generation efficiency and accuracy through parallel work of multiple agents.
 * Real-time Streaming Return: Supports streaming the generated PPT content in real-time, enhancing user experience.
 * High-Quality Content: Combines external retrieval and agent collaboration to generate high-quality content outlines and presentations.
 * Scalability: Flexible system design, easy to extend with new agents and functional modules.
II. Recent Upgrades
✅ Completed (Done)
 * ✅ Fixed streaming output bugs for all models except Gemini, and issues with ADK and A2A packages: View details
 * ✅ Image Rendering: Dynamically switches styles (object-cover or object-contain) based on whether an image is a background, and displays descriptive text for non-background images. To ensure unique PPT pages, uses page_number from the large model's output as a unique identifier, replacing the previous title-based method, to support content updates and proofreading.
 * ✅ Uses a looping Agent to generate each PPT page instead of generating all content at once, allowing for more pages and avoiding LLM token output limitations.
 * ✅ Introduced a PPTChecker Agent to check the quality of each generated PPT page. Actual testing shows good results; please replace with real image data and content RAG data.
 * ✅ Frontend displays the generation status for each Agent.
 * ✅ PPTX download: Uses python-pptx to download frontend JSON data, rendered by the backend.
📝 To-Do
 * 🔄 Multimodal Image Understanding: Includes handling image orientation, size, and other formatting for adaptation to different PPT positions.
 * 🔄 Metadata Transmission: Supports frontend-to-agent configuration transmission, and agents returning results with metadata.
III. User Interface Screenshots
Below are demonstrations of the core features of the MultiAgentPPT project:
1. Input Topic Interface
Users enter the desired PPT topic content in the interface:
2. Streaming Outline Generation Process
The system generates the outline structure in real-time, streaming it back based on the input content:
3. Generated Complete Outline
Finally, the system displays the complete outline for user confirmation:
4. Streaming PPT Content Generation
After confirming the outline, the system begins streaming the generation of each slide's content, returning it to the frontend:
5. Detailed Progress Display for Multi-Agent PPT Generation in slide_agent
📊 Concurrent Multi-Agent Collaboration Process (slide_agent + slide_outline)
flowchart TD
    A[User Inputs Research Content] --> B[Calls Outline Agent]
    B --> C[MCP Retrieves Information]
    C --> D[Generates Outline]
    D --> E{User Confirms Outline}
    E --> F[Sends Outline to PPT Generation Agent]

    F --> G[Split Outline Agent Splits Outline]
    G --> H[Parallel Agent Processes in Parallel]

    %% Concurrent Research Agents
    H --> I1[Research Agent 1]
    H --> I2[Research Agent 2]
    H --> I3[Research Agent 3]

    I1 --> RAG1[Automated Knowledge Base Retrieval RAG]
    I2 --> RAG2[Automated Knowledge Base Retrieval RAG]
    I3 --> RAG3[Automated Knowledge Base Retrieval RAG]

    RAG1 --> J
    RAG2 --> J
    RAG3 --> J

    J --> L[Loop PPT Agent Generates Slides]

    subgraph Loop PPT Agent
        L1[Write PPT Agent<br>Generates Each Slide]
        L2[Check PPT Agent<br>Checks Each Page's Content Quality, Retries up to 3 times]
        L1 --> L2
        L2 --> L1
    end

    L --> L1

🗂️ Project Structure
MultiAgentPPT/
├── backend/              # Backend multi-agent service directory
│   ├── simpleOutline/    # Simplified outline generation service (no external dependencies)
│   ├── simplePPT/        # Simplified PPT generation service (no retrieval or concurrency)
│   ├── slide_outline/    # High-quality outline generation service with external retrieval (more accurate outline after MCP tool retrieval)
│   ├── slide_agent/      # Concurrent multi-agent PPT generation outputs mainly XML-formatted PPT content
├── frontend/             # Next.js frontend interface

⚙️ IV. Quick Start
🐍 4.1 Backend Environment Configuration (Python)
 * Create and activate a Conda virtual environment (Python 3.11+ recommended to avoid bugs):
   conda create --name multiagent python=3.12
conda activate multiagent

 * Install dependencies:
   cd backend
pip install -r requirements.txt

 * Set backend environment variables:
   # Copy template config files for all modules
cd backend/simpleOutline && cp env_template .env
cd ../simplePPT && cp env_template .env
cd ../slide_outline && cp env_template .env
cd ../slide_agent && cp env_template .env

🧪 4.2 Start Backend Services
| Module | Function | Default Port | Startup Command |
|---|---|---|---|
| simpleOutline | Simple outline generation | 10001 | python main_api.py |
| simplePPT | Simple PPT generation | 10011 | python main_api.py |
| slide_outline | High-quality outline generation (with retrieval) | 10001 (requires simpleOutline to be off) | python main_api.py |
| slide_agent | Multi-Agent concurrent PPT generation | 10011 (requires simplePPT to be off) | python main_api.py |
🧱 V. Frontend Database Setup, Installation, and Running (Next.js)
The database stores user-generated PPTs:
 * Start PostgreSQL using Docker:
   # Use this when using a VPN
docker run --name postgresdb -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=welcome -d postgres
# Use this in China
docker run --name postgresdb -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=welcome -d swr.cn-north-4.myhuaweicloud.com/ddn-k8s/quay.io/sclorg/postgresql-15-c9s:latest

 * Modify the .env example configuration:
   DATABASE_URL="postgresql://postgres:welcome@localhost:5432/presentation_ai"
A2A_AGENT_OUTLINE_URL="http://localhost:10001"
A2A_AGENT_SLIDES_URL="http://localhost:10011"

 * Install dependencies and push the database model:
   # Install frontend dependencies
pnpm install
# Push database schema and insert user data
pnpm db:push
# Start the frontend
npm run dev

 * Open your browser and navigate to: http://localhost:3000/presentation
🧪 Example Data Description
> The current system has a built-in research example: "Overview of Electric Vehicle Development". For other research topics, please configure the corresponding Agent and connect to a real data source.
> To configure real data, simply change the prompt and the corresponding MCP tool.
> 
📎 VI. References
Part of the frontend project is based on the open-source repository: allweonedev/presentation-ai
Add the author's WeChat for questions
johnsongzc
Star History
