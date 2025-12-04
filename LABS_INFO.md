## Lab1
- Setup project with UV and installed necessary packages: `uv run`
    - langchain (LLM framework)
    - dotenv (env variable management)
    - ollama (local LLM interface)
    - openai (OpenAI API interface)
- Created `.env` file to store environment variables.
- Set up a virtual environment using UV (load env vars) with `load_dotenv(override=True)`
- Additional models:
    - llama2 from Meta          (   3B | 2.0GB)
    - phi4-mini from Microsoft  ( 3.8B | 2.5GB)
    - Gemma3 from Google        (   4B | 3.3GB)
    - Mistral from Mistral AI   (   7B | 4.1GB)
    - phi4 from Microsoft       (  14B | 9.1GB)
    - gpt-oss:20b from OpenAI   (  20B |  14GB)
    - Qwen2.5 | Qwen3 - Alibaba Cloud

**Implementations:**
- Built simple agentic workflow using Ollama for text generation.
    - Input: User prompt
    - LLM: Ollama model (e.g., llama2)
    - Output: Generated text response

**Challenge:** Simple Commercial Application
    - Prompt chaining implementation (input > LLM1 > LLM2 > output)
        - LLM1: Agentic AI opportunity identification for business idea generation and selection
        - LLM2: Agentic AI solution -  marketing plan creation for the selected business idea

- *TODO - OpenAI API setup for comparison.*


## Lab2
- Explored Workflow Design Patterns:
    - Prompt Chaining (I > LLM1 > LLM2 > … > O)
    - Routing (I > LLM Router > [LLM_i] > O)
    - Parallelization (I > Coordinator >> LLMs >> Aggregator > O)
    - Orchestrator-Worker (I > LLM Orchestrator >> LLMs >> LLM Synthesizer > O)
    - Evaluator-Optimizer (I > LLM Generator <=> LLM Evaluator > O)

- Comparison with Agents
    - I > LLM call | <= Action, Feedback => Environment | => Stop
    - Open-ended (can have infinite steps)
    - Feedback loop (allowing for iterative improvement)
    - No fixed path (fluid and dynamic)
    - More powerful but less predictable
    - Concerns about control and safety, accountability

**Implementations:**
- Simple Parallel Pattern workflow:
    - Question Generation Agent
    - Answer Generation Agents -- responding in parallel
    - Judger Agent -- evaluating the answers

**Challenge:** Multi-agent system using Agentic Design Patterns.
    - Implemented Customer Sentiment Analysis with Routing Pattern.
    - Used Ollama models + LangChain.


## Lab3
- Explored Agentic AI Workflows by complexity levels:
    1. Bottom level: 
        - No framework (custom implementation: transparent, direct control, flexible)
        - MCP (opensource; allows models connect to datasources, tools without glue code)
    2. Mid level:
        - OpenAI Agents SDK (pre-built agents: lightweight, flexible, limited customization)
        - CrewAI (agent orchestration platform: low-code,scalable, robust, enterprise features, cost-effective)
    3. Top level:
        - LangGraph (LLM framework: modular, extensible, supports complex workflows, steep learning curve)
        - Autogen (agent framework: multi-agent collaboration, complex tasks, high resource usage)

- Resources vs Tools
    - Resources: augment LLM knowledge by retrieving relevant information from external sources
    - Tools: extend LLM autonomy and capabilities by enabling interaction with external systems

**Implementations:**
-  Professional Twin Chatbot:
    - Built a simple chat interface to interact with the Professional Twin
    - Used Ollama model (phi4-mini)
    - Loaded data about me (summary text file + pdf linked profile)
    - Interactive way to present my professional background
- Tweaked the chatbot to retrieve web information too.
