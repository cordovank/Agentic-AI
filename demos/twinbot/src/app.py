import streamlit as st
from config import AppConfig, validate_config
from context_loader import load_context
from llm_client import get_openai_client, chat_completion, Turn
from prompts import PROMPT_GROUPS
from state import PersonaContext, build_system_prompt, init_session_state
from tools.notifications import push_pushover
from ui_components import (
    render_page_style, 
    render_header, 
    render_thinking_loader,
    render_chat_header,
    render_history, 
    )


cfg = AppConfig()

# -------------------------------------------------
# Helper Functions
# -------------------------------------------------
def start_request(prompt: str):
    """Kick off a request and force a rerun so the UI can render the Thinking bubble at bottom."""
    
    # Ignore new requests while busy
    if st.session_state.get("is_thinking"):
        return  

    # Request info
    st.session_state.pending_prompt = prompt
    st.session_state.is_thinking = True

    st.rerun()


def execute_pending_request():
    """If a prompt is pending, call the model, append to history, clear flags, and rerun."""
    prompt = st.session_state.pending_prompt

    try:
        answer = chat_completion(
            client=get_openai_client(base_url=cfg.URL, api_key=cfg.API_KEY),
            model=cfg.MODEL_NAME,
            system_prompt=system_prompt,
            user_message=prompt,
            history=[Turn(**t) for t in st.session_state.history],
        )
    except Exception as e:
        st.session_state.is_thinking = False
        st.session_state.pending_prompt = None
        st.error("Something went wrong while contacting the model. Please try again.")
        st.exception(e)  
        st.stop()

    # ------------------------------------------------------
    # PUSHOVER NOTIF
    # ------------------------------------------------------
    if not answer:
        push_pushover(
            token=cfg.pushover_token,
            user=cfg.pushover_user,
            message=f"Unknown question: {prompt}",
        )
        answer = "I don’t have enough information to answer that from my background."

    st.session_state.history.append({"user": prompt, "assistant": answer})
    st.session_state.has_chatted = True

    st.session_state.is_thinking = False
    st.session_state.pending_prompt = None
    st.rerun()

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(page_title="TwinBot - Interactive Resume", page_icon="🧠", layout="centered")
render_page_style()

# Config warnings (non-fatal)
for w in validate_config(cfg):
    st.warning(w)

# Session state
init_session_state()

# Context (cached)
summary, linkedin = load_context(cfg.summary_path, cfg.linkedin_pdf_path)
ctx = PersonaContext(name=cfg.name, summary=summary, linkedin=linkedin)
system_prompt = build_system_prompt(ctx)

# -------------------------------------------------
# Page Header
# -------------------------------------------------
render_header(cfg.name, cfg.subtitle)

# -------------------------------------------------
# Guided prompts (OPTIONAL, hidden by default)
# -------------------------------------------------
st.divider()
with st.expander("Example questions", expanded=False):
    st.caption("Grouped by role. Click to ask immediately.")
    for group_name, prompts in PROMPT_GROUPS.items():
        with st.expander(group_name, expanded=False):
            for p in prompts:
                if st.button(p, key=f"{group_name}:{p}", type="secondary"):
                    start_request(p)
# st.caption("Optional guide

st.divider()

# -------------------------------------------------
# Chat 
# -------------------------------------------------
render_chat_header(cfg.tagline)
render_history(st.session_state.history)

# Thinking loader
if st.session_state.get("is_thinking"):
    with st.chat_message("assistant"):
        render_thinking_loader()

# If pending prompt exists and thinking state True, execute now
if st.session_state.get("is_thinking") and st.session_state.get("pending_prompt"):
    execute_pending_request()

# -------------------------------------------------
# Chat input box (always pinned at the bottom)
# -------------------------------------------------
user_input = st.chat_input(placeholder="Ask about my experience and projects…")

if user_input:
    start_request(user_input)
