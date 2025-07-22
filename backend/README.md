1. PPT-related Sub-Agents
Backend Dependencies
pip install -r requirements.txt
Directory Structure
simpleOutline # For front-end testing of outline generation
simplePPT     # For front-end testing of simple PPT generation
slide_outline # For front-end outline generation, generates outlines through retrieval, more professional
slide_agent   # Standard multi-agent system, generates PPTs based on outlines, more professional
save_ppt      # Saves as a PPT file, uses python-pptx to save as a .pptx file from a PPT master
Gemini is currently the most compatible (must try Gemini first, others still have bugs), for support of other LLMs, you can modify create_model.py and then configure the MODEL_PROVIDER and LLM_MODEL environment variables in your .env file.
 * File: slide_agent/slide_agent/create_model.py
 * File: simpleOutline/create_model.py
 * File: simplePPT/create_model.py
 * File: hostAgentAPI/hosts/multiagent/create_model.py
Under Development (To Be Improved)
super_agent   # Text-based multi-agent system, used to connect multiple Agents, pure text input, output, controls outline and PPT generation
Notes for Multi-Agent Development:
The description of each sub-agent must be clear, as the Super Agent determines its input information based on each sub-agent's task.
2. Developing Your Own Multi-Agent Project (Detailed introduction below, unrelated to this PPT project)
hostAgentAPI  # The main Agent for a pure A2A API version, used to connect multiple Agents
multiagent_front # Front-end code for the Super Agent
slide_outline # Sub-agent client implemented with MCP tool calls
simplePPT # Sub-agent client implemented with ADK
A2A, ADK, and MCP: Building a Multi-Agent Hierarchical Calling System
This document, based on the MultiAgentPPT project, delves into how to leverage the latest version of the A2A (Agent-to-Agent) framework, integrating Google ADK and FastMCP, to build an efficient multi-agent hierarchical calling system. Through the multiagent_front front-end interface, users can easily register sub-agents, initiate tasks, and track conversations, while the Host Agent is responsible for coordinating sub-agents to distribute and execute tasks. We will use PPT outline and content generation as an example to demonstrate A2A's hierarchical calling mechanism, ADK's task enhancement capabilities, and FastMCP's streaming output support, with a focus on system architecture design and implementation details.
I. A2A Multi-Agent Hierarchical Calling Architecture
The core of the A2A framework lies in the Host Agent's ability to implement hierarchical calls and management of multiple agents. The Host Agent acts as a central coordinator, responsible for sub-agent registration, task assignment, context management, and result integration. By combining Google ADK and MCP, the system achieves the following key functionalities:
 * Sub-Agent Registration and Management: The Host Agent maintains a list of sub-agents through the /agent/register and /agent/list interfaces. The functional description of each sub-agent (e.g., generating PPT outlines or content) is clearly defined to ensure accurate task assignment.
 * Hierarchical Task Assignment: The Host Agent parses user requests and dynamically assigns tasks to appropriate sub-agents (e.g., slide_outline or slide_agent), supporting serial or parallel execution.
 * Context Management: Through the /conversation/create and /message/send interfaces, the Host Agent maintains conversation states, ensuring task continuity.
 * Streaming Response and Event Tracking: Combined with FastMCP's SSE (Server-Sent Events) support, the system can return real-time task status and results, and track events through /events/get and /events/query.
 * ADK Integration: Google ADK enhances the sub-agents' ability to handle complex tasks, such as generating structured content via the GenAI API.
Hierarchical Calling Process in the Project
Taking PPT generation as an example, the process is as follows:
 * The user inputs a task (e.g., "Research on the development of electric vehicles") via the multiagent_front front-end.
 * The Host Agent creates a conversation and assigns the task to the slide_outline sub-agent to generate an outline.
 * After the user confirms the outline, the Host Agent calls the slide_agent sub-agent to generate the PPT content.
 * The sub-agent processes the task by calling the GenAI API via ADK, and FastMCP provides streaming results via SSE.
II. Environment Setup
1. Backend Environment
Configure according to the HostAgentAPI README:
 * Install Dependencies:
   Ensure Python 3 is installed, then run:
   Execute pip install -r requirements.txt in the terminal.
 * Configure Model:
   Copy env_template.txt to .env and configure the model provider (e.g., Google, OpenAI). Example:
   In the .env file, configure MODEL_PROVIDER=google and GOOGLE_API_KEY=your_api_key_here.
   Refer to hostAgentAPI/hosts/multiagent/create_model.py to set up supported models.
 * Start Host Agent API:
   Run:
   Execute python host_agent_api.py in the terminal.
   The API runs by default on http://localhost:13000.
2. Frontend Environment
Configure multiagent_front according to the A2A Multi-Agent Chat Frontend README:
 * Install Dependencies:
   Ensure Node.js and npm are installed, then run:
   Execute npm install in the multiagent_front directory.
 * Configure Environment Variables:
   Check the .env file to confirm that REACT_APP_HOSTAGENT_API points to the API address:
   In the multiagent_front/.env file, confirm REACT_APP_HOSTAGENT_API=http://127.0.0.1:13000.
 * Start Frontend:
   Run:
   Execute npm run dev in the multiagent_front directory.
   The frontend runs by default on http://localhost:5173.
3. Run Sub-Agent to Generate Outline
Navigate to the slide_outline directory:
Execute cd slide_outline in the terminal.
 * MCP Configuration:
   Check mcp_config.json:
   Execute cat mcp_config.json in the terminal.
   Add Google GenAI API key to .env:
   Add GOOGLE_GENAI_API_KEY=your_genai_api_key to the slide_outline/.env file.
 * Start MCP Service in SSE Mode:
   Execute fastmcp run --transport sse mcpserver/rag_tool.py in the slide_outline directory.
 * Start Main Service:
   Execute python main_api.py in the slide_outline directory.
   The sub-agent's listening address is http://localhost:10001.
4. Run Second Sub-Agent to Generate Content Based on Outline
Navigate to the simplePPT directory:
Execute cd simplePPT in the terminal.
Copy environment file:
Execute cp env_template .env in the terminal.
 * Start Main Service:
   Execute python main_api.py in the simplePPT directory.
   The sub-agent's listening address is http://localhost:10011.
III. Implementing A2A Hierarchical Calls via Frontend
The multiagent_front frontend provides an intuitive interface, simplifying agent registration, task initiation, and result tracking. The operating procedure is as follows:
1. Register Sub-Agents
 * Open the frontend interface (http://localhost:5173).
 * Go to the Agent Registration page (usually in the top or sidebar).
 * Add sub-agent addresses:
   * http://localhost:10001
   * http://localhost:10011
 * After submission, the Host Agent will record the sub-agents via /agent/register, and the interface will display successful registration.
 * Confirm the sub-agent list on the Agent List page (calling /agent/list).
2. Initiate Task
 * On the Conversation or New Session page, click "Create Session".
 * Enter the task, for example: "Research on the development of electric vehicles".
 * The frontend will call /conversation/create to get the conversation_id, then send the request via /message/send.
3. Host Agent Hierarchical Calling Principle
 * Task Parsing: The Host Agent uses the list_remote_agents tool to query available sub-agents.
 * Task Assignment: Based on the request content, the Host Agent assigns the task to the slide_outline sub-agent to generate an outline.
 * ADK Enhancement: slide_outline calls the Google GenAI API via adk_agent_executor.py to generate a structured outline.
 * FastMCP Streaming Output: FastMCP returns the outline in real-time via SSE, and status updates (e.g., "submitted" → "working" → "completed") will be displayed on the frontend.
4. View Intermediate Results
The frontend will display the outline in real-time. On the Conversation List page, you can view all conversations (/conversation/list). Clicking on a conversation allows you to view message history (/message/list) and event records (/events/query), such as task status updates or artifact generation.
IV. Technical Highlights of A2A Combined with ADK and FastMCP
1. A2A Hierarchical Calling
 * Dynamic Task Assignment: The Host Agent dynamically selects executors based on sub-agent descriptions, supporting complex task decomposition.
 * Tool Support: The Host Agent has built-in list_remote_agents and send_message tools, simplifying task distribution.
 * Event-Driven: By using add_event, user messages, agent status updates, and artifact generation are recorded, ensuring full traceability.
2. Google ADK Integration
 * Enhanced Sub-Agent Capabilities: adk_agent_executor.py integrates the Google GenAI API to handle complex tasks such as structured content generation.
 * Modular Design: ADK logic is separated from A2A, allowing sub-agents to be independently extended.
3. A2A's SSE
 * Streaming Output: A2A pushes task status and results in real-time via SSE, providing a smoother user experience.
4. Schematic Diagram
graph TD
    %% Define Nodes
    A[User] -->|Initiate Task| B(multiagent_front Frontend)
    B -->|Call API| C(Host Agent)
    
    %% Host Agent and Sub-Agent Interaction
    C -->|Assign Task based on Query| F[slide_outline Sub-Agent]
    C -->|Assign Task based on Query| G[simplePPT Sub-Agent]
    
    %% Sub-Agent and External Services
    F -->|Call ADK Multi-Agent| I[ADK Multi-Agent Process]
    G -->|MCP Protocol| H[MCP Tool]
    
    %% Frontend Display
    B -->|Display Data Stream| A
    
    
    %% Style Definition
    classDef host fill:#f9f,stroke:#333,stroke-width:2px;
    classDef agent fill:#bbf,stroke:#333,stroke-width:2px;
    classDef frontend fill:#dfd,stroke:#333,stroke-width:2px;
    classDef external fill:#fbf,stroke:#333,stroke-width:2px;
    
    class C host;
    class F,G agent;
    class B frontend;
    class I,H external;

More complex example for production environment
flowchart TD
    A[User Request] --> C[Host Agent<br/>Control Sub-Agents]
    C --> D[Document Agent<br/>A2A Server]
    C --> P[PPT Agent<br/>A2A Server]
    C --> Q[Excel Agent<br/>A2A Server]
    D --> E[Writer Agent<br/>ADK Structure Sequential]
    E --> F[Translate<br/>Translation Processing]
    F --> G[Outline Generate<br/>Generate Outline]
    G --> H[(RAG Search DB<br/>Knowledge Base Retrieval)]
    H --> G
    G --> I[Split Outline<br/>Outline Splitting]
    I --> J[Parallel Agent<br/>Parallel Processing]
    J --> K1[Research Agent 1]
    J --> K2[Research Agent 2]
    J --> K3[Research Agent n]
    K1 --> L[Summary Agent<br/>Summary Integration]
    K2 --> L
    K3 --> L
    L --> M[Refine Agent<br/>Content Refinement]
    M --> N[(Web Search<br/>Web Search)]
    N --> M
    M --> O[Output<br/>Final Output]

    classDef userInput fill:#e1f5fe
    classDef messageQueue fill:#f3e5f5
    classDef controlAgent fill:#e8f5e8
    classDef documentAgent fill:#fff3e0
    classDef writerAgent fill:#fce4ec
    classDef processNode fill:#f1f8e9
    classDef parallelNode fill:#e3f2fd
    classDef researchNode fill:#fff8e1
    classDef summaryNode fill:#f9fbe7
    classDef refineNode fill:#ffebee
    classDef database fill:#e0f2f1
    classDef output fill:#e8eaf6

    class A userInput
    class B messageQueue
    class C controlAgent
    class D documentAgent
    class E writerAgent
    class F,G,I processNode
    class J parallelNode
    class K1,K2,K3 researchNode
    class L summaryNode
    class M refineNode
    class H,N database
    class O output

V. Testing and Debugging
1. Unit Testing HostAgentAPI
Run test_api.py to verify API interfaces:
Execute python test_api.py in the terminal.
Check status codes, response content, and elapsed time.
2. Overall Testing
Use host_agent_api_client.py to simulate front-end operations:
Execute python host_agent_api_client.py in the terminal.
3. Common Issues
 * PyCharm Exception: If you encounter AttributeError: 'NoneType' object has no attribute 'call_exception_handler', try running python host_agent_api.py from the command line.
VI. Important Notes
 * Clear Sub-Agent Descriptions: During registration, functionality must be clearly defined (e.g., "Generates structured PPT outlines") to ensure the Host Agent correctly assigns tasks.
 * Conversation Management: It is recommended to create independent conversations for each task and use the frontend's conversation list to track task progress.
VII. Summary
Through the A2A framework combined with Google ADK and FastMCP, the MultiAgentPPT project demonstrates an efficient multi-agent hierarchical calling system. The Host Agent coordinates sub-agents (such as slide_outline and simplePPT), automating task processing from input to output. The multiagent_front frontend provides an intuitive interaction interface, supporting agent registration, task initiation, and result tracking, significantly enhancing system flexibility and user experience. This architecture is not only suitable for PPT generation but can also be extended to other multi-agent collaboration scenarios, showcasing the powerful potential of the A2A framework.
