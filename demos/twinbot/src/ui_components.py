import streamlit as st

def render_page_style():
    st.markdown(
        """
        <style>
        :root {
            --bg: #121212;
            --surface: #1E1E1E;
            --text: #A0A0A0;
            --heading: #E0E0E0;
            --accent: #FF9364;
            --border: rgba(255,255,255,0.08);
        }
        html, body, [class*="css"] {
            background-color: var(--bg);
            color: var(--text);
            font-family: Roboto, system-ui, sans-serif;
        }
        h1, h2, h3 { color: var(--heading); font-family: Ubuntu, sans-serif; }
        .accent-line {
            height: 2px; width: 48px;
            background: linear-gradient(90deg, var(--accent), transparent);
            margin: 0.75rem 0 1.5rem 0;
        }
        button[kind="secondary"] {
            background-color: transparent;
            border: 1px solid var(--border);
            color: var(--text);
            font-size: 0.85rem;
            text-align: left;
        }
        button[kind="secondary"]:hover { border-color: var(--accent); color: var(--heading); }
        .stButton > button {
            background-color: var(--surface);
            border: 1px solid var(--border);
            color: var(--heading);
        }
        .stButton > button:hover { border-color: var(--accent); }

        div[data-testid="stChatMessage"][aria-label="User"] > div {
            background-color: var(--surface);
            border: 1px solid var(--border);
            border-left: 3px solid var(--accent);
        }

        .guided-prompts {
        position: fixed;
        left: 50%;
        transform: translateX(-50%);
        bottom: 90px; /* adjust so it sits above chat_input */
        width: min(900px, 92vw);
        z-index: 9999;
        background: rgba(30,30,30,0.95);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 12px 14px;
        backdrop-filter: blur(8px);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def render_header(name: str, subtitle: str):
    st.markdown(
        f"""
        <h2>
          <span style="color: var(--accent); font-weight: 500;">{name}</span>
          · Interactive Resume
        </h2>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(f"<span style='opacity:0.75;'>*{subtitle}*</span>", unsafe_allow_html=True)
    st.markdown('<div class="accent-line"></div>', unsafe_allow_html=True)

def render_thinking_loader():
    st.markdown(
        "<span style='opacity:0.6;font-size:0.85rem;'>Thinking…</span>",
        unsafe_allow_html=True
        )

def render_chat_header(tagline: str):
    with st.container(border=False):
        st.markdown("### Ask a Question", text_alignment="center")
        st.caption(f"*{tagline}*", text_alignment="center")

def render_history(history: list[dict]):
    for turn in history:
        with st.chat_message("user"):
            st.markdown(turn["user"])

        with st.chat_message("assistant"):
            st.markdown(turn["assistant"] or "")
