# LAB NOTES FOR AGENTIC AI ENGINEERING WORKSHOP
This file contains notes and summaries for the labs in the Agentic AI Workshop. These notes are for personal reference and may not cover all details from the labs. Refer to this as understanding/knowledge gained from the concepts and implementations discussed during the labs.

---

# MODELS
<!-- - llama2 from Meta          (   3B | 2.0GB)
- phi4-mini from Microsoft  ( 3.8B | 2.5GB)
- Gemma3 from Google        (   4B | 3.3GB)
- Mistral from Mistral AI   (   7B | 4.1GB) -->
- phi4 from Microsoft       (  14B | 9.1GB)
- gpt-oss:20b from OpenAI   (  20B |  14GB)
- Qwen2.5 | Qwen3 - Alibaba Cloud

# RESOURCES

**Models**
* [OpenAI API Models](https://platform.openai.com/docs/pricing?latest-pricing=standard)
* [Ollama Models](https://ollama.com/search)
* [Ollama Cloud Models - Tool compatible](https://ollama.com/search?c=cloud)
* [HuggingFace Models](https://huggingface.co/models)
* [OpenRouter Free models](https://openrouter.ai/models?q=free)

**ResponseAPI compatibility**
* [OpenAI Responses API](https://platform.openai.com/docs/guides/migrate-to-responses) ([Medium Tut](https://medium.com/@odhitom09/openai-responses-api-a-comprehensive-guide-ad546132b2ed))
* [OpenRouter Responses API](https://openrouter.ai/docs/api/reference/responses/overview)
* [OpenRouter-OpenAI SDK integration](https://openrouter.ai/docs/guides/community/openai-sdk)
**GPT-OSS**
* [GTP-OSS OPENAI](https://github.com/openai/gpt-oss/blob/main/examples/agents-sdk-python/example.py)
* [GTP-OSS HF](https://huggingface.co/docs/inference-providers/guides/gpt-oss)

**Other**
* [Prompting Guide](https://cookbook.openai.com/examples/gpt-5/gpt-5-2_prompting_guide#9-web-search-and-research)

---

# APIs Basics

## OpenAI API
OpenAI()

## Ollama API
OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

## HuggingFace API

**Install**
langchain-huggingface
huggingface-hub
transformers

```python
    from langchain_huggingface import HuggingFaceEndpoint, HuggingFacePipeline
    from langchain import LLMChain, PromptTemplate
    
    repo_id=""
    llm = HuggingFaceEndpoint(repo_id=repo_id, model_kwargs={"temperature":0.7, "max_length":512, token=HF_TOKEN})
    
    template = "<|USER|>: {text}\n<|ASSISTANT|>: "
    prompt = PromptTemplate(template=template, input_variables=["text"])
    
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    response = llm_chain.invoke("text")

    pipe = pipeline("text-generation", model=repo_id, tokenizer=repo_id, model_kwargs={"max_new_tokens":512})
    llm_pipe = HuggingFacePipeline(pipeline=pipe)
    response = llm_pipe.invoke("text")

    from langchain_core.prompts import PromptTemplate
    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm
    response = chain.invoke("text")
```

---

# TOOLS
- Pushover API for notifications (free trial available)
- SendGrid API for emails (free trial available)
- Resend API for emails (free monthly limits)
- OpenAI Agents SDK built-in tools:
    - WebSearchTool
    - FileSearchTool
    - ComputerTool
- Ollama
    - [web search]([Ollama's web search API](https://docs.ollama.com/capabilities/web-search))
- [Serper](serper.dev) - run google queries with code (2500 free credits)
---

# Template for Labs

## Lab1
- level 1
    - level 2

### Implementations

### Challenge

Title:
    - level 1
        -level 2

### DEMO
**Name**
- level 1

---

# 1_FUNDAMENTALS

## Lab1
- Setup project with UV and installed necessary packages: `uv run`
    - langchain (LLM framework)
    - dotenv (env variable management)
    - ollama (local LLM interface)
    - openai (OpenAI API interface)
- Created `.env` file to store environment variables.
- Set up a virtual environment using UV (load env vars) with `load_dotenv(override=True)`
    
### Implementations
- Built simple agentic workflow using Ollama for text generation.
    - Input: User prompt
    - LLM: Ollama model (e.g., llama2)
    - Output: Generated text response

### Challenge

Simple Commercial Application:
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

### Implementations

- Simple Parallel Pattern workflow:
    - Question Generation Agent
    - Answer Generation Agents -- responding in parallel
    - Judger Agent -- evaluating the answers

### Challenge

Multi-agent system using Agentic Design Patterns:

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

    - **Resources**: augment LLM knowledge by retrieving relevant information from external sources
    - **Tools**: extend LLM autonomy and capabilities by enabling interaction with external systems

### Implementations

**Simple Career Twinbot:**

- Built a simple chat interface to interact with the professional TwinBot
- Used Ollama model (phi4-mini)
- Loaded data about me (summary text file + pdf linked profile)
- Interactive way to present my professional background
<!-- - Tweaked the chatbot to retrieve web information too. -->
- `app.py` is python version of the chatbot, `3_professional_twinbot.ipynb` is the notebook version.


## Lab4
- Deployment to HuggingFace Spaces:
    - Created `requirements.txt` with dependencies
    - Created `app.py` for Gradio app
    - Created HuggingFace account and generated token for this Space
    - Provide token names & values in the Secrets section of the Space settings
    - no git access needed
    - need requirements.txt, app.py, data files in the Space repo
    - remove Readme.md within deployment repo/dir to avoid conflicts

## DEMO

**Career Twinbot with Tools**
- Simple Career Twinbot using LLM with tools
- Tool integration: 
    - User-defined functions as tools
    - External tools: Pushover service for notifications
- Terminal: launched with `uv run app.py`
- Used gradio for the twinbot interface and deployed
- Used HuggingFace Spaces for hosting

---

# 2_OPENAI_AGENTS_SDK

- **asyncio** for asynchronous programming
    - asynchronous python code
    - lightweight version of multi-threading

    ```python
    async def processing_fn() -> str:
         # some code
         return "done"
    result = await processing_fn()
    ```

    - How it works:
        - functions defined with async def are coroutines -they can be paused/resumed
        - calling it returns an object, which is not executed immediately.
        - they are scheduled for execution within an event loop when using await
        - the event loop can run other coroutines while the function is waiting for something 

    - Call multiple coroutines:

    ```python
    result = await asyncio.gather(coroutine1(), coroutine2(),)
    ```

## Lab1&2

- **OpenAI SDK Agents**
    - Pre-built agents for common tasks
    - Lightweight, flexible, limited customization
    - Implementations:

        ```python
        from agents import Agent, Runner, trace
        with trace("Some trace name"):
            agent = Agent(name="MyAgent", instruction= "You are a helpful assistant.", model="gpt-4")
            runner = Runner.run(agent=agent)    # coroutine
            response = await runner.run("User question?")
            output = response.final_output 
        ```
        - `Agent`: defines the agent's behavior
        - `Runner`: manages execution of the agent
        - `trace`: for logging and debugging, we can view them in OpenAI platform
    
    - `@function_tool` decorator to define custom tools for agents:
        ```python
        from agents import function_tool

        @function_tool
        def my_tool(param1: str) -> str:
            # tool logic
            return "result"
        ```
    
    - `.as_tool()` method to convert an agent into a tool:
        ```python
        agent = Agent(name="MyAgent", instructions="Do something", model="gpt-4")
        agent_tool = agent.as_tool(tool_name="agent_tool", tool_description="Agent that does something")
        ```

- Agent collaboration via **tools** and **handoffs**
    - Agents can call other specialized agents as tools for collaboration
    - Handoffs & Agents-as-tools are similar: in both cases, an Agent can collaborate with another Agent.
        - With tools, control passes back
        - With handoffs, control passes across

    - **Agent with tools:**
        ```python
        tools = [agent_tool, function_tool]
        manager_agent = Agent(name="Manager", instructions="Some instructions for the manager", tools=tools, model="gpt-4")
        with trace("Manager Agent with Tools"):
            response = await Runner.run(agent=manager_agent, input="some message")
            output = response.final_output
        ```

    - **Handoff Agent:**
        ```python
        handoffs = [agent_handoff]
        manager_agent = Agent(name="Manager", instructions="Some instructions for the manager", tools=tools, handoffs=handoffs, model="gpt-4")
        with trace("Manager Agent with Handoffs"):
            response = await Runner.run(agent=manager_agent, input="some message")
            output = response.final_output
        ``` 

### Implementations

- **Sales Manager:** with Tools & Handoffs
    - Tools: user-defined functions + specialized agents
        - Specialized agents:
            - Email Writer Agent: generates sales email content
            - Subject Line Generator Agent: creates catchy subject lines
            - HTML Formatter Agent: formats email content into HTML
        - User-defined Function: send emails using SendGrid API
    
    - Created Sales Manager Agent that uses tools & handoffs to delegate tasks to other agents/tools.
        - The Sales Manager agent plans the email generation process and decides when to call each tool/agent.
        - Used OpenAI SDK
    - ***TO DO (OPTIONAL):*** For more practice, add more tools/handoffs as needed to enhance the sales email generation process. (e.g., send to group of recipients, automated follow-ups, SendGrid API webhooks for replies, ...)


- **TODO - Challenge:** Commercial Application - AI Agent with Tools & Handoffs
    - **Research Manager:** with Tools & Handoffs
    - Create specialized agents:
        - Research Agent: gathers information on a given topic
        - Summary Agent: summarizes the gathered information
    - Created Research Manager Agent that uses tools & handoffs to delegate tasks to other agents/tools.
    - The Research Manager agent plans the research process and decides when to call each tool/agent.
    - Potential Alternative Ideas: 
        - Career: Candidate Fit Analysis, Career Coaching Assistant, Learning Path Advisor, Interview Preparation Coach
        - Business: Market Research Analyst, Competitive Analysis Assistant, Product Launch Strategist, Customer Feedback Analyzer
        - Personal: Travel Itinerary Planner

## Lab3

- **Multimodel Agentic Integration**
    - Different models have different strengths/weaknesses
    - Combine multiple models to leverage their strengths
    - Implemented a multimodel agentic workflow for **sales email generation**:
        - Email Writer Agent: email content generation (multiple models)
        - Subject Line Generator Agent: creative subject lines
        - HTML Formatter Agent: HTML formatting
        - Email Sender Agent: handoff to send the final email 
        - Sales Manager Agent: overall coordination, picks best content from multiple models
    - Each agent specializes in a specific task, the Sales Manager orchestrates the workflow until it reaches the final handoff to send the email.
    - High-level workflow: Draft (multiple models) → Select best → Convert to HTML → Send.
    - Used OpenAI SDK and Trace feature to monitor the workflow.

- **Agentic Guardrails**
    - **Structured Outputs**:
        - Ensures outputs adhere to specific formats/schemas
        - Used Pydantic models to define output schemas
        - Provided schema during agent initialization on `output_schema` parameter
    - **Functions as Guardrails**:
        - Implemented input guardrails on tool functions using `@input_guardrail` decorator
        - Ensured that inputs to tool functions adhere to specified schemas
        - Returned structured outputs of type `GuardrailFunctionOutput` contains tripwire status

### Implementations

**Personal names Guardrail**
- Guardrail against using personal names in sales emails:
    - Created `NameCheckOutput` Pydantic model to define output schema for name checking
    - Created `guardrail_against_name` function using `@input_guardrail` decorator  
    - Integrated the guardrail function into the Sales Manager Agent's input guardrails
    - If the guardrail is triggered (personal name detected), the agent aborts the email generation process.
    - Demonstrated both failure and success paths of the guardrail.
- Used OpenAI SDK Trace feature to monitor guardrail activations.
- ***TO DO (OPTIONAL):***
    - Add more input and output guardrails
    - Use structured outputs for the email generation


## Lab4

- **OpenAI Hosted Tools**
    - `WebSearchTool` lets an agent search the web (beware of [costs](https://platform.openai.com/docs/pricing#web-search)). Includes `search_context_size` to tune info/cost (low/medium/high).
    - `FileSearchTool` allows retrieving information from OpenAI Vector Stores.  
    - `ComputerTool` allows automating computer use tasks (e.g., taking screenshots, clicking).

- **Deep Research**
    - Build an end‑to‑end research pipeline that plans web searches, performs them (via a hosted WebSearchTool), synthesizes findings into a long-form report, and emails the result.
    - Multimodal agent orchestration, structured outputs (Pydantic), hosted tools, and traceable execution.
    - **E2E Implementation:**
        - Workflow: Compose planner → searcher (parallel) → writer → emailer workflow.
        - Created Agents and tooling:
            - Search Agent: performs web searches using `WebSearchTool` (`ModelSettings(tool_choice="required")`) in parallel.
            - Planner Agent: plans web searches based on a research topic
            - Writer Agent: synthesizes search results into a long-form report
            - Email Sender Tool: sends the report via email using SendGrid API
            - Email Agent: uses the email sender tool to email the report
        - Used structured outputs (Pydantic models) for agent outputs to ensure consistency:
            - `WebSearchPlan`: defines the structure for search plans
            - `ReportData`: defines the structure for the final report
        - Implemented asynchronous execution for search tasks using `asyncio.gather` to run multiple searches in parallel.
        - Controlled costs by limiting the number of searches performed.
        - Monitored and debugged execution using OpenAI traces.
        - Imports agents SDK utilities: Agent, Runner, trace, WebSearchTool, function_tool, ModelSettings, Pydantic BaseModel/Field.

### DEMO

**ProductLens**

- LLM-powered product comparison tool based on user's priorities.
- implemented lightweight agentic workflow: *user intent → planning → parallel research → comparison → final recommendation* 
- Providers enabled: Ollama/OpenAI/OpenRouter
- Tools: 
    - Ollama web search tool (**web search API** from Ollama via HTTP call)
    - alternatively OpenAI `WebSearchTool`
- used OpenAI Agent SDK
- OpenAI **Traces** for logs
- UI implementation with Gradio
- Configurable variables from .env
    - `NUM_SEARCHES` (default 1) and `NUM_PRODUCTS` (default 2)
    - `MODEL_NAME`
    - `PROVIDER` to auto-setup openai client and model
- Demo deployed to HuggingFace Spaces

- **Flow**
    
    A central manager orchestrates planning, parallel product research, and final comparison, ensuring each agent does one focused job and produces an explainable, decision-ready result.

    - **1. Comparison Manager (Orchestrator)**
        * Entry point for the user query
        * Coordinates all agents
        * Manages async execution and data flow
        * Owns the end-to-end lifecycle

    - **2. Planner Agent**
        * Parses the user query and priorities
        * Identifies relevant products/ecosystems to compare
        * Derives evaluation criteria
        * Outputs a structured plan (products + criteria)

    - **3. Product Research Agents (Parallel)**
        * Spawned by the Comparison Manager
        * Each researches one product
        * Uses web search focused on planner criteria
        * Returns concise product summaries

    - **4. Comparator / Decision Agent**
        * Invoked by the Comparison Manager
        * Normalizes research results
        * Evaluates each product against the criteria
        * Produces recommendation, table, and tradeoffs


# 3_CREW (ongoing)

- **What is CrewAI?**
    - An AI agent framework. 
    - Offerings:
        - *CrewAI Enterprise*: multi-agent platform, deploys, runs, monitors Agentic AI.
        - *CrewAI UI Studio*: user tool, no-code/low-code
        - *CrewAI open-source frammework*: agent orchestration
            - CrewAI Crews: AI teams of agents with different roles -> produces autonomous solutions.
                - best for problem-solving, creative collabs, exploratory tasks
            - CrewAI Flows: Structure automation, trasforms complex tasks -> precise workflows.
                - best for deterministic outcomes, auditability, precise control over execution
                
- **Core concepts**
    - **Agent**: autonomous unit with LLM + role, goal, backstory, memory, tools
    - **Task**: specific assignment to execute + description, expected output, agent
    - **Crew**: team of Agents and Tasks. Sequential (predefined order)/Hierarchical (use manager LLM) execution.
    - **YAML config**: defines Agents and Tasks
    - **`crew.py`**: python decorators:     `@CrewBase`, `@agent`, `@task`, `@crew`
    - **LiteLLM framework**: used under the hood to interface with any LLM (`LLM(model="provider_name/model_name", base_url, api_key)`)

- **Basics of implementations**
    - CrewAI = UV projects
    - install: `uv tool install crewai`
    - create new project: `crewai create crew my_crew`
    - directory structrure:
        ```text
        my_crew
            src
                my_crew
                    config
                        agents.yaml
                        tasks.yaml
                    crew.py
                    main.py
        ```
    - run within directory: `crewai run` 

## Lab1
- **Debate** mini-project
    - run ```crewai create crew debate```, then select provider and model name + api key (or skip)
    - automatically creates project folders&files
        - `knowledge/`
        - `debate/src/debate/` with config files, `crew.py`, and `main.py`

    - `agents.yaml`: 1 debater agent in favor/opposition of a "motion", 1 judge agent that decides based on arguments for a "motion"
    - `tasks.yaml`: "propose" and "oppose" tasks for the debater agent, "decide" task for the judge agent. Outputs saved in specified file with `output_file`
    - `crew.py`: loads agents and tasks from config files & setups agents/tasks/crew with decorators returning instances of each. Process (flow) specified here too.
    - `main.py`: defines crew inputs (motion)

    - execute with ```crewai run```

## Lab2
> Goal: Use tools and additional context/info for AI Agents

- Concepts
    - Tools
        - [Serper](serper.dev) - run google queries with code (2500 free credits)
    - Context
        - Information passed from a task to another task

- **Financial Researcher** mini-project
    - run ```crewai create financial_researcher```

    - `agents.yaml`: 1 senior researcher agent finding relevant info about a "company", 1 analyst agent that makes market analysis and report for a "company"
    - `tasks.yaml`: "research" task for the researcher agent, "analysis" task for the analyst agent. 
        - `output_file` - outputs saved in specified file 
        - `context` - researcher task info given to analyst task 
    
    - `crew.py`: loads agents and tasks from config files & setups agents/tasks/crew with decorators returning instances of each. 
        - Researcher agent uses `SerperDevTool` tools. 
        - Process (flow) specified here too.
    - `main.py`: defines crew inputs (company)

    - execute with ```crewai run```

## Lab3
> Goal: Build a multi-agent system & use custom tools and pydantic outputs (JSON schemas) for AI Agents

- Concepts
    - Structure outputs
        - use `Pydantic` models
    - Custom tool
        - use `src/stock_picker/tools/` to define one
        - `push_tool.py` - a push notification with 
            - `BaseModel` input from `pydantic`
            - `BaseTool` tool from `crewai.tools`
    - Hierarchical process
        - defined under `Crew` instance with a manager.

- **Stock Picker with structture outputs+custom tools** mini-project
    - run ```crewai create crew stock_picker```

    - `agents.yaml`: 
        - 1 trending company finder agent finding trending companies, 
        - 1 financial researcher agent that makes an analysis of a list of trending companies and reports about them, 
        - 1 stock picker agent that selects the best one for investment
        - 1 manager agent that delegate tasks

    - `tasks.yaml`: 
        - "find trending companies" task for the trending company finder agent in a given "sector", 
        - "research trending companies" task for the researcher agent + `context` from previous task
        - "pick best company" task for stock picker agent + `context` from previous task
        - `output_file` - outputs saved in specified file 
  
    - `crew.py`: loads agents and tasks from config files & setups agents/tasks/crew with decorators returning instances of each. 
        - Structured output: use `Pydantic` models for
            - `TrendingCompany` (name+ticker+symbol), 
            - `TrendingCompanyList` (companies), 
            - `TrendingCompanyResearch` (name+market position+future outlook+investment potential), 
            - `TrendingCompanyResearchList` (research list)

        - trending company finder and financial researcher agents use `SerperDevTool` tools + stock picker agent uses custom *push_tool*

        - tasks are specified `output_pydantic` based on models previously created.

        - manager agent created independently within `@crew` with `allow_delegation=True`

        - `Crew` instance specifies         
            - `process=Process.hierarchical` & 
            - `manager_agent=manager`

    - `main.py`: defines crew inputs (sector)
    - execute with ```crewai run```

## Lab4

> Goal: Use vector storage and SQL implementation for AI Agents

- Concepts
    - **Memory**: provides contextual information
        - *STM*: temp recent interactions/outcomes using RAG (vector DB)
        - *LTM*: 
        - *Entity Memory*: peoples, places, and concepts in RAG db.
        - ***Contextual Memory***: umbrella term for STM, LTM, and Entity Memory
        - ***User Memory***: user-specific mem

- **Stock Picker with Memory** mini-project

    - run ```crewai create crew stock_picker```

    - `crew.py` creates memories:
        - load        
            - `LongTermMemory`, `ShortTermMemory`, `EntityMemory`
            - `RAGStorage` from `crewai.memory.storage.rag_storage`
            - `LTMSQLiteStorage` from `crewai.memory.storage.ltm_sqlite_storage`

        - in `@crew`, afetr manager instance:

            - **short_term_memory** instance using RAG storage with specified embedder:
                ```python
                ShortTermMemory(
                    storage = RAGStorage(
                        embedder_config=(
                            "provider": "", 
                            "config":{"model": ''}
                            ),
                        type="short_term",
                        path="./memory/"
                    )
                )
                ```
            - **longt_term_memory** instance using RAG storage with specified embedder:
                ```python
                LongTermMemory(
                    storage = LTMSQLiteStorage(
                        db_path="./memory/ltm_storage.db"
                    )
                )
                ```
            - **entity_memory** instance using RAG storage with specified embedder:
                ```python
                EntityMemory(
                    storage = RAGStorage(
                        embedder_config=(
                            "provider": "", 
                            "config":{"model": ''}
                            ),
                        type="short_term",
                        path="./memory/"
                    )
                )
                ```
            - add to `Crew()` instance and return:
                - `memory=True`
                - `short_term_memory=short_term_memory`
                - `long_term_memory=long_term_memory`
                - `entity_memory=entity_memory`

        - give memory to the agents defined as `@agent` with `memory=True` (trending company finder agent, stock picker agent)

## Lab4
> Goal: give coding skills to AI agents, execute the code in a Docker container and investigate the results.

- Concepts
    - instance an `Agent()` and include:
        - `allow_code_execution=True` 
        - `code_execution_mode="safe"`
    - This allows agents to execute code, and safe mode will run it in a Docker container

- **Coder Agents** mini-project
    - run ```crewai create crew coder```

    - `agents.yaml`: 
        - 1 python developer agent to achieve an "assignment" 

    - `tasks.yaml`: 
        - "coding" task for the python dev agent for a given "assignment", 
        - `output_file` - code and its output saved in specified file 
  
    - `crew.py`: loads agents and tasks from config files & setups agents/tasks/crew with decorators returning instances of each. 
        - Structured output: use `Pydantic` models for
            - `TrendingCompany` (name+ticker+symbol), 
            - `TrendingCompanyList` (companies), 
            - `TrendingCompanyResearch` (name+market position+future outlook+investment potential), 
            - `TrendingCompanyResearchList` (research list)

        - python developer agent with:
            - `allow_code_execution=True` 
            - `code_execution_mode="safe"` 
            - `max_execution_time=30`
            - `max_retry_limit=5`

        - tasks are specified `output_pydantic` based on models previously created.

        - manager agent created independently within `@crew` with `allow_delegation=True`

        - `Crew` instance specifies         
            - `process=Process.hierarchical` & 
            - `manager_agent=manager`

    - `main.py`: define our own `run` function similar to predetermined main function:
        - assign inputs "assignment" (note that initial assignment is more complex to verify this works as expected.)
        - assignemnt='Write a python program to calculate the 1st 10,000 terms of this series, multiplying the total by 4: 1 - 1/3 + 1/5 - 1/7 + ...'
        - kickoff Crew() with the input

    - execute with ```crewai run```

### Implementations

* **Tools / Config**

  * **Ollama**: `base_url="http://localhost:11434/v1"`, `api_key="ollama"`.
  * **FileReadTool**: read existing repo files before writing.
  * **YAML configs**: `agents.yaml`, `tasks.yaml` for modularity.


#### **SimpleCalculator — Sequential Crew (Concept → Code)**

> **Goal**: Basic “SimpleCalculator” build via CrewAI multi-agent workflow with minimal manual coding.

* **Process**: `Process.sequential`

* **Agents**

  * **Product**: generates project specs given project name as input.
  * **Coder**: implements calculator core + app entrypoints; optional `allow_code_execution=True`, 

* **Workflow**

  1. Minimal requirements needed to develop the app.
  2. Code core functions (add/sub/mul/div + validation)

#### **SimpleCalculator — Hierarchical Crew (Concept → Code → Tests → Docs → UI)**

> **Goal**: End-to-end “SimpleCalculator” build via CrewAI multi-agent workflow with minimal manual coding.

* **Process**: `Process.hierarchical` with **Manager Agent** coordinating + gating completion.

* **Agents**

  * **Coder**: implements calculator core + app entrypoints; optional `allow_code_execution=True`, `code_execution_mode="safe"`.
  * **Tester**: writes/runs `pytest` suite (ops + edge cases like div/0, floats, invalid input).
  * **Writer**: generates README + brief implementation report (run/test/UI commands).

* **Workflow**

  1. Code core functions (add/sub/mul/div + validation)
  2. Generate + run tests
  3. Write docs + usage
  4. Optional: **Gradio UI** wired to the same core functions

* **Outputs**

  * `src/...` calculator module, `tests/`, `README.md`, optional `app.py` (Gradio), optional task `output_file` logs.

* **Notes**

  * Docker required for `"safe"` execution; Ollama must be running with the target model available.
  * Manager acceptance criteria: tests pass + docs include exact commands + UI calls shared core logic (no duplication).

* **Next**

  * Add **critic/reviewer agent** (lint/style/edge cases) + lightweight tracing of task outputs.

## DEMO








---
Template:
### Implementations
### Challenge

Title:
    - level 1
        -level 2

### DEMO
**Tower Defense GameAI**
- level 1
