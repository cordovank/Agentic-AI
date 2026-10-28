# Agentic-AI Codebase Instructions for AI Agents

## Project Overview
**Agentic-AI** is a hands-on workshop repository exploring autonomous AI agent design, orchestration, and deployment. It contains educational notebooks, implementation examples, and multi-agent workflow demos using frameworks like OpenAI Agents SDK, CrewAI, LangGraph, and AutoGen.

## Environment & Setup
- **Python**: ≥3.12 with UV (Universal Virtualenv Manager)
- **Execution**: `uv run` to setup environment with `pyproject.toml` dependencies
- **Configuration**: `.env` file required for API keys/secrets; use `load_dotenv(override=True)` in code
- **Key dependencies**: openai, crewai, langgraph, langchain, autogen, anthropic, mcp

## Multi-Framework Architecture

The repository is organized by **agent framework complexity tiers**:

### **Tier 1 (Fundamentals)** - `1_Fundamentals/`
Lightweight, no-framework implementations with LangChain or OpenAI SDK:
- **Patterns**: Prompt chaining, routing, parallelization, evaluator-optimizer
- **Models**: Ollama (local), OpenAI API  
- **Key pattern**: `OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")` for Ollama

**Examples**:
- `1_simple_commercial_app.ipynb` - Prompt chaining (LLM1 → LLM2 pipeline)
- `2_routing_sentiment_*` - Routing pattern (conditional LLM dispatch)
- `3_professional_twinbot.ipynb` - RAG-based chatbot with external data

### **Tier 2 (OpenAI Agents SDK)** - `2_OpenAI/`
Pre-built agents with lightweight orchestration:
- **Pattern**: `Agent(name, instructions, tools, model) → Runner.run() → response.final_output`
- **Tools**: `@function_tool` decorators, agent-as-tool via `.as_tool()`, `WebSearchTool`, `FileSearchTool`
- **Key concepts**: Handoffs vs tools (control transfer), structured outputs via Pydantic, guardrails
- **Execution**: Asynchronous via `asyncio` (`async def`, `await`, `asyncio.gather()`)
- **Debugging**: Use `trace("context_name")` context manager for OpenAI Platform logging

**Examples**:
- `agents_coordination_tools_handoffs.ipynb` - Multi-agent collaboration with tools & handoffs
- `agents_with_guardrails.ipynb` - Input/output validation with `@input_guardrail` decorator
- `deep_research_agentic.ipynb` - End-to-end research: planning → parallel searches → synthesis → email
- `product_lens.ipynb` - Real product comparison demo (deployed to HuggingFace Spaces)

### **Tier 3 (CrewAI)** - `3_CrewAI_Crews/`
Declarative, hierarchical multi-agent orchestration:
- **Config**: YAML files (`agents.yaml`, `tasks.yaml`) define agents & tasks
- **Code**: `crew.py` with `@CrewBase`, `@agent`, `@task`, `@crew` decorators
- **Process**: `Process.sequential` (predefined order) or `Process.hierarchical` (manager LLM decides)
- **Tools**: `SerperDevTool` (web search), custom tools via `BaseTool` in `tools/` directory
- **Structured outputs**: Pydantic models on task `output_pydantic` parameter
- **Memory**: Optional RAG/SQLite storage for short/long-term/entity memory
- **Code execution**: `allow_code_execution=True`, `code_execution_mode="safe"` (Docker required)
- **CLI**: `crewai create crew <name>`, `crewai run`

**Examples**:
- SimpleCalculator hierarchical crew - concept → code → tests → docs with manager coordination
- Stock Picker - trending company finder → financial researcher → picker with delegation
- DataQualityProfiler - multi-agent data validation workflow

## Critical Developer Workflows

### Starting a New Agent Workflow
1. **Framework choice**: No deps (Ollama+LangChain) → OpenAI Agents → CrewAI → LangGraph
2. **Model setup**: Use `misc/helpers/model_providers.py` for multi-provider abstraction
   - Ollama: `base_url="http://localhost:11434/v1"`, `api_key="ollama"`
   - OpenAI: Direct API key
   - OpenRouter: `https://openrouter.ai/api/v1` + token
3. **Environment**: Create `.env` with `OPENAI_API_KEY=...` or provider-specific keys

### OpenAI Agents SDK Workflow

#### Basic Agent Structure
```python
from agents import Agent, Runner, trace, function_tool
import asyncio

@function_tool
def my_tool(param: str) -> str:
    return f"Result: {param}"

async def run_agent(query: str):
    agent = Agent(
        name="MyAgent",
        instructions="Be helpful and concise",
        model="gpt-4",
        tools=[my_tool]
    )
    with trace("agent_trace"):
        response = await Runner.run(agent=agent, input=query)
    return response.final_output

# Execute with: asyncio.run(run_agent("question"))
```

#### Structured Outputs with Pydantic
OpenAI Agents SDK supports structured outputs to ensure responses adhere to predefined schemas:
```python
from pydantic import BaseModel, Field
from agents import Agent, Runner

class OutputSchema(BaseModel):
    recommendation: str = Field(description="Final recommendation")
    confidence: float = Field(description="Confidence level 0-1")

agent = Agent(
    name="Advisor",
    instructions="Provide recommendations",
    model="gpt-4",
    output_schema=OutputSchema
)

response = await Runner.run(agent=agent, input="query")
output: OutputSchema = response.parsed_output  # Type-safe, structured
```

#### ModelSettings for Tool Control
Use `ModelSettings` to enforce tool usage or control agent behavior:
```python
from agents.model_settings import ModelSettings

# Force tool invocation (useful for guaranteed data extraction)
agent = Agent(
    name="Extractor",
    model="gpt-4",
    tools=[extraction_tool],
    model_settings=ModelSettings(tool_choice="required")
)
```

#### Parallel Execution with asyncio.gather()
For independent tasks, execute agents concurrently:
```python
async def research_parallel(topic: str):
    agent1 = Agent(name="DataAgent", ..., model="gpt-4")
    agent2 = Agent(name="NewsAgent", ..., model="gpt-4")
    
    results = await asyncio.gather(
        Runner.run(agent=agent1, input=f"Data on {topic}"),
        Runner.run(agent=agent2, input=f"News about {topic}")
    )
    return [r.final_output for r in results]
```

#### Input Guardrails
Validate and filter inputs before agents process them:
```python
from agents import input_guardrail

@input_guardrail
def name_guardrail(input: str) -> GuardrailFunctionOutput:
    if "john" in input.lower():
        return GuardrailFunctionOutput(tripwire=True, message="Personal names not allowed")
    return GuardrailFunctionOutput(tripwire=False)

agent = Agent(
    name="Manager",
    input_guardrails=[name_guardrail],
    ...
)
```

#### Hosted Tools
Use OpenAI's built-in tools for common tasks:
```python
from agents import WebSearchTool

web_search = WebSearchTool(search_context_size="medium")  # low/medium/high (cost/quality trade-off)

# Agent will automatically use WebSearchTool when relevant
agent = Agent(
    name="Researcher",
    tools=[web_search],
    ...
)
```

#### Tracing for Debugging
OpenAI Platform traces show agent execution flow, decisions, and tool calls:
```python
with trace("research_workflow") as trace_ctx:
    response = await Runner.run(agent=manager, input="complex query")
    # View traces at https://platform.openai.com/playground - helps debug multi-step workflows
```

### CrewAI Workflow

#### Basic Project Setup
```bash
crewai create crew my_crew  # Scaffold project
cd my_crew
# Directory structure created:
# my_crew/
#   src/my_crew/
#     config/
#       agents.yaml
#       tasks.yaml
#     crew.py
#     main.py
```

#### YAML Configuration Pattern
**agents.yaml**: Define agent roles and capabilities
```yaml
agents:
  researcher:
    role: Senior Researcher
    goal: Gather comprehensive information on topics
    backstory: You are an expert researcher with 20 years of experience
    tools: [SerperDevTool]
    memory: true
    
  analyst:
    role: Data Analyst
    goal: Analyze and interpret research findings
    tools: [custom_analysis_tool]
```

**tasks.yaml**: Define specific assignments
```yaml
tasks:
  research_task:
    description: "Research {topic} thoroughly"
    expected_output: "Detailed research report with citations"
    agent: researcher
    output_file: research_report.md
    
  analysis_task:
    description: "Analyze the research findings"
    expected_output: "Analysis with recommendations"
    agent: analyst
    context: [research_task]  # Pass output from previous task
    output_pydantic: AnalysisResult  # Structured output
```

#### Hierarchical Crew with Manager Agent
```python
from crewai import Agent, Task, Crew, Process
from pydantic import BaseModel

class ResearchOutput(BaseModel):
    findings: str
    confidence: float

@CrewBase
class MyResearchCrew:
    @agent
    def researcher(self) -> Agent:
        return Agent(
            role="Researcher",
            goal="Find relevant information",
            tools=[SerperDevTool()],
            memory=True
        )
    
    @agent
    def manager(self) -> Agent:
        return Agent(
            role="Research Manager",
            goal="Coordinate research and make decisions",
            allow_delegation=True  # Can delegate to other agents
        )
    
    @task
    def research_task(self) -> Task:
        return Task(
            description="Research {topic}",
            agent=self.researcher(),
            output_pydantic=ResearchOutput
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.researcher(), self.manager()],
            tasks=[self.research_task()],
            process=Process.hierarchical,
            manager_agent=self.manager()
        )
```

#### Custom Tools in CrewAI
Create tools in `src/my_crew/tools/custom_tool.py`:
```python
from crewai.tools import BaseTool
from pydantic import BaseModel

class PushNotificationInput(BaseModel):
    message: str
    priority: str = "normal"

class PushNotificationTool(BaseTool):
    name: str = "push_notification"
    description: str = "Send push notifications to users"
    args_schema: type[BaseModel] = PushNotificationInput
    
    def _run(self, message: str, priority: str = "normal") -> str:
        # Tool logic
        return f"Notification sent: {message}"

# In crew.py, add to agent's tools parameter:
# tools=[PushNotificationTool()]
```

#### Structured Outputs with Pydantic
```python
from pydantic import BaseModel, Field

class CompanyAnalysis(BaseModel):
    company_name: str = Field(description="Name of company")
    market_position: str = Field(description="Current market standing")
    investment_potential: str = Field(description="Investment potential assessment")

# Use in task
task = Task(
    description="Analyze company {company}",
    agent=analyst,
    output_pydantic=CompanyAnalysis  # Ensures structured JSON output
)
```

#### Memory Management
```python
from crewai.memory import EntityMemory, ShortTermMemory, LongTermMemory
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage

short_term = ShortTermMemory(
    storage=RAGStorage(
        embedder_config={
            "provider": "openai",
            "config": {"model": "text-embedding-3-small"}
        },
        type="short_term",
        path="./memory/"
    )
)

long_term = LongTermMemory(
    storage=LTMSQLiteStorage(db_path="./memory/ltm.db")
)

crew = Crew(
    agents=agents,
    tasks=tasks,
    memory=True,
    short_term_memory=short_term,
    long_term_memory=long_term
)
```

#### Code Execution with Safety
```python
agent = Agent(
    role="Python Developer",
    allow_code_execution=True,
    code_execution_mode="safe",  # Runs in isolated Docker container
    max_execution_time=30,
    max_retry_limit=5
)
```

#### Running CrewAI Projects
```bash
crewai run  # Execute from project root directory
# Output saves to stdout and files specified in tasks.yaml
```

## Project Conventions & Patterns

### Environment Variable Management
- All API keys/credentials in `.env` (template: `.env-example`)
- Load at module start: `from dotenv import load_dotenv; load_dotenv(override=True)`
- Access: `os.environ["KEY_NAME"]`

### Model Provider Abstraction
Located in `misc/helpers/model_providers.py`:
- `LLM_Provider` class handles Ollama/HuggingFace/OpenRouter client initialization
- Use `get_async_client()` for concurrent operations, `get_sync_client()` for sequential

### Notebook vs. Script Patterns
- **Notebooks** (.ipynb): Educational demos with markdown explanations, incremental execution
  - Use `from IPython.display import Markdown, display` for formatted output
  - Load data: `with open('path/file')` from `me/` or `knowledge/` subdirectories
- **Scripts** (.py): Production deployments (e.g., Gradio UI in HuggingFace Spaces)
  - Requires `requirements.txt` (not pyproject.toml for Spaces)
  - Entry point: `app.py` with `if __name__ == "__main__"`

### Agent Design Principles (from labs notes)
1. **Single responsibility**: Each agent does one focused job
2. **Clear inputs/outputs**: Use Pydantic models for structured data flow
3. **Asynchronous parallelization**: Use `asyncio.gather()` for independent tasks
4. **Explainability**: Structured outputs + tracing over black-box responses

## Cross-Component Communication

### Data Flow Patterns
- **Chaining**: Task output → Task input (via context in CrewAI or function returns)
- **Parallelization**: Manager spawns multiple agents → aggregator collects results
- **Handoffs**: Control passes between agents; tools return control to caller

### Tool Integration Points
- **OpenAI Agents**: `@function_tool` decorators or pre-built `WebSearchTool`
- **CrewAI**: `tools=[]` agent parameter + custom `BaseTool` in `tools/` subdir
- **Web search**: Ollama has HTTP API (`/search`); OpenAI has `WebSearchTool`

### External Services (from demos)
- **SendGrid**: Email sending via `SendGrid(api_key)` 
- **Pushover**: Notifications (free tier available)
- **Serper**: Google search API (2500 free credits, `SerperDevTool` in CrewAI)
- **HuggingFace Spaces**: Deployment target for Gradio UI demos

## Key Files & References

| File/Dir | Purpose |
|----------|---------|
| `pyproject.toml` | Dependencies, metadata (UV-managed) |
| `.env`, `.env-example` | Environment secrets (API keys) |
| `1_Fundamentals/` | Pattern tutorials: chaining, routing, RAG |
| `2_OpenAI/` | OpenAI Agents SDK examples + deployed ProductLens |
| `3_CrewAI_Crews/` | CrewAI hierarchical crews + SimpleCalculator demo |
| `WORKSHOP/` | Full course material (1_foundations → 6_mcp) |
| `misc/helpers/` | Shared utilities: `model_providers.py`, `helpers.py` |
| `misc/AGENTIC_AI_LABS_NOTES.md` | Comprehensive API reference & lab summaries |

## When to Use Each Framework

| Use Case | Framework | Why |
|----------|-----------|-----|
| Learning agent basics | 1_Fundamentals + Ollama | Transparent, low-dependency |
| Rapid prototyping | OpenAI Agents SDK | Built-in tools, minimal boilerplate |
| Production multi-agent | CrewAI | YAML config, hierarchical control, memory |
| Complex state machines | LangGraph | Full workflow graph control (in WORKSHOP) |
| Distributed agents | AutoGen | Multi-agent collaboration at scale (in WORKSHOP) |

## Advanced Framework Patterns

### **LangGraph** - `WORKSHOP/4_langgraph/`
Explicit state-machine orchestration for complex workflows:

#### Core Concepts
- **StateGraph**: Directed graph where nodes are functions, edges are state transitions
- **State**: Shared context passed between nodes (Pydantic BaseModel or TypedDict)
- **Reducers**: Functions that merge new state with old state (e.g., `add_messages`)
- **Conditional Edges**: Route execution based on node output

#### Basic Pattern
```python
from typing import Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from pydantic import BaseModel

class State(BaseModel):
    messages: Annotated[list, add_messages]  # Reducer merges messages

def node_fn(state: State) -> State:
    # Process state and return new values
    return State(messages=[{"role": "assistant", "content": "response"}])

# Build graph
graph = StateGraph(State)
graph.add_node("node_1", node_fn)
graph.add_edge(START, "node_1")
graph.add_edge("node_1", END)
runnable = graph.compile()

# Execute
result = runnable.invoke(State(messages=[]))
```

#### Conditional Routing
```python
def route_decision(state: State) -> str:
    # Return next node name based on state
    if "urgent" in state.messages[-1].content:
        return "priority_handler"
    return "normal_handler"

graph.add_conditional_edges("triage", route_decision)
```

#### Advantages & When to Use
- **Full control**: Explicit state transitions visible in code
- **Complex workflows**: Non-linear, multi-path execution logic
- **Persistence**: Built-in checkpointing for long-running processes
- **Best for**: Research agents, state machines, workflows needing audit trails

---

### **AutoGen** - `WORKSHOP/5_autogen/`
Framework for multi-agent collaboration at scale:

#### Agent Chat Pattern (AgentChat)
Simple, high-level API similar to CrewAI:
```python
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken

# Create model client
model = OpenAIChatCompletionClient(model="gpt-4o-mini")

# Create agent
agent = AssistantAgent(
    name="helper",
    model_client=model,
    system_message="You are a helpful assistant"
)

# Send message
message = TextMessage(content="What is 2+2?", source="user")
response = await agent.on_messages([message], CancellationToken())
print(response.chat_message.content)
```

#### Agent Core Pattern (Distributed)
Low-level API for complex multi-agent systems with custom routing:
```python
from autogen_core import RoutedAgent, message_handler, MessageContext
from autogen_agentchat.agents import AssistantAgent

class CustomAgent(RoutedAgent):
    def __init__(self, name: str):
        super().__init__(name)
        self._delegate = AssistantAgent(
            name,
            model_client=OpenAIChatCompletionClient(model="gpt-4o-mini")
        )
    
    @message_handler
    async def handle_message(self, message, ctx: MessageContext):
        # Custom logic, can route to other agents
        response = await self._delegate.on_messages([message], ctx.cancellation_token)
        return response
```

#### Key Patterns
- **Tools as functions**: Auto-wrapped for agent use
- **Message-based communication**: Agents pass typed messages
- **Flexible routing**: Custom @message_handler decorators
- **Group chat**: Multiple agents in conversation (AgentChat)
- **Distributed execution**: Agents can run in separate processes

#### When to Use
- **Multi-agent conversations**: Group problem-solving
- **Distributed systems**: Agents across multiple machines
- **Complex collaboration**: Custom routing and message flow
- **Production scale**: Enterprise multi-agent deployments

---

## HuggingFace Spaces Deployment Workflow

### Deployment Requirements
Create three key files in your Spaces repository:

#### `requirements.txt`
```
openai>=1.68.2
gradio>=5.22.0
python-dotenv>=1.0.1
anthropic>=0.49.0
```
**Note**: Spaces uses `requirements.txt`, not `pyproject.toml` from UV.

#### `app.py` (Gradio Application)
```python
import gradio as gr
from dotenv import load_dotenv
import os
import asyncio

load_dotenv(override=True)

async def process_input(user_input: str) -> str:
    # Your agent logic here
    from agents import Agent, Runner
    
    agent = Agent(
        name="MyAgent",
        instructions="Be helpful",
        model="gpt-4"
    )
    response = await Runner.run(agent=agent, input=user_input)
    return response.final_output

# Gradio interface
def gradio_handler(user_input: str) -> str:
    return asyncio.run(process_input(user_input))

interface = gr.Interface(
    fn=gradio_handler,
    inputs="text",
    outputs="text",
    title="My AI App"
)

if __name__ == "__main__":
    interface.launch()  # Spaces will automatically run this
```

#### Data Files
Place any required data in repository root or subdirectories:
```
my_space/
  app.py
  requirements.txt
  data/
    knowledge.txt
    profiles.json
  me/
    summary.txt
```

### Secrets Management in Spaces
1. Go to Space settings → Secrets
2. Add environment variables (e.g., `OPENAI_API_KEY`)
3. Access in code via `os.environ["OPENAI_API_KEY"]`
4. **Never commit `.env` file to repository**

### Deployment Checklist
- ✅ `requirements.txt` with all dependencies (no `pyproject.toml`)
- ✅ `app.py` with `if __name__ == "__main__"` and `interface.launch()`
- ✅ All data files in repository
- ✅ Secrets configured in Space settings
- ✅ Remove or rename conflicting `README.md` if needed
- ✅ Test locally: `python app.py` works standalone

### Common Issues
| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Check all imports in `requirements.txt` |
| `OPENAI_API_KEY not found` | Add to Secrets section, not `.env` |
| App hangs | Add timeout handling; avoid blocking calls |
| Large model loads slow | Use model caching; pre-load in startup |

### Examples in Repo
- **ProductLens**: `2_OpenAI/product_lens.ipynb` (deployed to Spaces)
- **Career TwinBot**: `1_Fundamentals/4_twinbot_with_tools.ipynb` (deployed to Spaces)

## Common Pitfalls & Solutions

### Environment & Dependencies
| Issue | Solution |
|-------|----------|
| `"Model not found"` | Ensure Ollama running (`ollama serve`) with model pulled (`ollama pull gpt-oss`) |
| `API key errors` | Check `.env` exists, `load_dotenv(override=True)` called, key names match environment |
| `ModuleNotFoundError` | Run `uv run` to update dependencies; restart notebook kernel |
| `Notebook kernel stale` | Restart kernel after dependency changes in `pyproject.toml` |

### Async & Execution
| Issue | Solution |
|-------|----------|
| `Async deadlock` | Never `await` sync code; use `.run_in_executor()` for blocking calls |
| `Event loop already running` | Avoid `asyncio.run()` in notebooks; use `await` directly |
| `Timeout in Spaces` | Implement request timeouts; avoid blocking operations in Gradio |

### Agent & Tool Issues
| Issue | Solution |
|-------|----------|
| `CrewAI tool failures` | Ensure tool return type matches task expectations; use Pydantic for clarity |
| `Agent not using tools` | Use `ModelSettings(tool_choice="required")` in OpenAI Agents |
| `Structured output validation fails` | Ensure Pydantic model matches agent output exactly |
| `LangGraph state errors` | Use `Annotated` with reducers; verify state merging logic |

### Multi-Agent Coordination
| Issue | Solution |
|-------|----------|
| `Agents ignoring context` | Pass structured outputs as Pydantic models; use task `context` in CrewAI |
| `Infinite loops in handoffs` | Set max iterations; use explicit termination conditions |
| `Tool not found by agent` | Register tools with agent before execution; check tool name/description |

### Deployment Issues
| Issue | Solution |
|-------|----------|
| `Secrets not loading in Spaces` | Use HuggingFace Secrets UI, not `.env` files; restart Space after adding |
| `Large models timeout in Spaces` | Use smaller models; implement caching; pre-load in startup |
| `Import errors after deployment` | Verify all imports are in `requirements.txt` with exact versions |

## Project-Specific Patterns & Conventions

### Data Organization
- **Input data**: Store in `{tier}/me/`, `{tier}/knowledge/`, or `data/` subdirectories
- **Outputs**: Save to `output_file` in CrewAI tasks; use `artifact/` dirs in demo projects
- **Database files**: Store in `memory/` (CrewAI) or project root (SQLite for AutoGen)
- **Configuration files**: YAML in `src/{crew_name}/config/` for CrewAI; env vars for others

### Multi-Provider Model Handling
From `misc/helpers/model_providers.py`, use `LLM_Provider` for abstraction:
```python
from misc.helpers.model_providers import LLM_Provider

# Provider can be "ollama", "openrouter", or "huggingface"
provider = LLM_Provider(provider="ollama", api_key="ollama")
client = provider.get_async_client()  # For parallel operations
```

This pattern allows switching between Ollama (local), OpenAI (direct), and OpenRouter without code changes.

### Structured Tracing in OpenAI Agents
Always wrap multi-step workflows with `trace()`:
```python
from agents import trace

with trace("workflow_name") as ctx:
    # Execute agents here
    # Traces viewable at https://platform.openai.com/playground
    pass
```

This helps debug complex agent behavior and is essential for production deployments.

### Async Pattern Consistency
- **Notebooks**: Use `await` directly (IPython has running event loop)
- **Scripts**: Use `asyncio.run()` for top-level execution
- **Parallel tasks**: Always use `asyncio.gather()` for concurrent agent calls
- **Gradio handlers**: Wrap async functions in sync wrappers (see Spaces deployment pattern)

### CrewAI + Pydantic Best Practices
1. **Always use `output_pydantic`** on tasks for structured outputs—avoids free-form text
2. **Field descriptions matter**—LLMs use them to understand what to populate
3. **Compose Pydantic models**—use nested models for complex structures (e.g., `ResearchList` contains `Research[]`)
4. **Task context chaining**—pass structured outputs from one task to another via `context` parameter

### Testing & Validation
- **Unit test agents**: Create minimal `.ipynb` cells that validate agent outputs
- **Pydantic validation**: Let Pydantic catch schema mismatches before deployment
- **Local testing before Spaces**: Test `app.py` locally with `python app.py` before uploading
- **Graceful error handling**: Use try/except in Gradio handlers to prevent Space crashes

## Adding New Content

- **Educational notebook**: Add to `WORKSHOP/` or numbered tier directory with clear markdown sections
- **Framework demo**: Create in appropriate tier folder with `.env-example` and standalone execution
- **Utility function**: Add to `misc/helpers/` with docstrings referencing usage examples
- **Lab notes**: Update `misc/AGENTIC_AI_LABS_NOTES.md` with implementation details and API patterns

## Quick Command Reference

| Task | Command |
|------|---------|
| Setup environment | `uv run` |
| Run notebook | `jupyter notebook` (or open in VS Code) |
| Test CrewAI | `cd 3_CrewAI_Crews/demos/{crew_name} && crewai run` |
| Deploy to Spaces | Push `requirements.txt`, `app.py`, data files; add secrets in UI |
| Start Ollama | `ollama serve` (separate terminal) |
| Pull model | `ollama pull gpt-oss` or `ollama pull phi4` |
| View OpenAI traces | https://platform.openai.com/playground |
