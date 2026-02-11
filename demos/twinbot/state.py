from dataclasses import dataclass
from llm_client import Turn

@dataclass(frozen=True)
class PersonaContext:
    name: str
    summary: str
    linkedin: str

def build_system_prompt(ctx: PersonaContext) -> str:   
    return f"""
        You are acting as {ctx.name}, answering questions about your professional background.

        Rules:
        - Only answer using the provided resume + LinkedIn context.
        - If you don't know the answer, say so and do not invent details.
        - Be professional and concise.

        ## Summary
        {ctx.summary}

        ## LinkedIn
        {ctx.linkedin}
        """.strip()

def init_session_state():
    import streamlit as st
    if "history" not in st.session_state:
        st.session_state.history = []  # list[Turn-like dict]
    if "has_chatted" not in st.session_state:
        st.session_state.has_chatted = False
    if "is_thinking" not in st.session_state:
        st.session_state.is_thinking = False
    if "pending_prompt" not in st.session_state:
        st.session_state.pending_prompt = None
