# Agentic-AI

**Agentic-AI** is a collection of hands-on projects focused on designing, orchestrating, and deploying autonomous AI agents. 

It explores multi-agent workflows, tool-use, and LLM orchestration using modern frameworks such as OpenAI Agents, CrewAI, LangGraph, AutoGen, and MCP.

It is inspired by the Udemy [AI Engineer Agentic Course](https://www.udemy.com/course/the-complete-agentic-ai-engineering-course/?couponCode=AGENTIC_TRACK_11_25). For more information, visit the [course page](https://edwarddonner.com/2025/04/21/the-complete-agentic-ai-engineering-course/).


# Environment Setup

Clone the repository:

```bash
git clone https://github.com/cordovank/Agentic-AI.git
cd Agentic-AI
```

Install [UV](https://uv.run/) - Universal Virtualenv Manager.

```bash
uv run
```

- `.env` file to store environment variables.
- Load environment variables with `load_dotenv(override=True)` from `.env` file in Jupyter notebooks or Python scripts.


# Models 
Using Ollama Open Models:
- llama2 from Meta          (   3B | 2.0GB)
- phi4-mini from Microsoft  ( 3.8B | 2.5GB)

Ollama API configuration variables are located in `.env`:


Other models can be used if desired.


## License
This project is part of the [AI Engineer Agentic](https://www.udemy.com/course/the-complete-agentic-ai-engineering-course/?couponCode=AGENTIC_TRACK_11_25) course from Udemy and follows the same licensing terms.