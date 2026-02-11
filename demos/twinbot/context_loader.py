from pathlib import Path
from pypdf import PdfReader
import streamlit as st

@st.cache_data(show_spinner=False)
def load_context(summary_path: str, linkedin_pdf_path: str) -> tuple[str, str]:
    summary = Path(summary_path).read_text(encoding="utf-8")

    reader = PdfReader(linkedin_pdf_path)
    linkedin = "".join((p.extract_text() or "") for p in reader.pages)

    return summary, linkedin
