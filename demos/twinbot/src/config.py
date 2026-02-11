from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv(override=True)

@dataclass(frozen=True)
class AppConfig:
    title: str = "Nellie · Interactive Resume"
    subtitle: str = "Explore my experience, projects, and technical background"
    tagline: str = "Responses are grounded strictly in my resume and LinkedIn profile."

    linkedin_pdf_path: str = os.getenv("LINKEDIN_PDF_PATH", "src/me/linkedin.pdf")
    summary_path: str = os.getenv("SUMMARY_PATH", "src/me/summary.txt")
    name: str = os.getenv("TWINBOT_NAME", "Nellie")

    # ------------------------------------------------------
    # LLM CONFIG
    # ------------------------------------------------------
    provider: str = os.getenv("PROVIDER", "")
    API_KEY = None
    URL = None
    MODEL_NAME = None

    if provider == "OLLAMA":
        URL = "http://localhost:11434/v1"
        API_KEY = "OLLAMA"
        MODEL_NAME = os.getenv("OLLAMA_MODEL", "gpt-oss")
    elif provider == "OPENROUTER":
        URL = "https://openrouter.ai/api/v1"
        API_KEY = os.getenv("OPENROUTER_API_KEY")
        MODEL_NAME = os.getenv("OPENROUTER_MODEL")
    else:
        API_KEY = os.getenv("OPENAI_API_KEY")
        MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-5-nano")

    # ------------------------------------------------------
    # TOOLS CONFIG
    # ------------------------------------------------------
    pushover_token: str | None = os.getenv("PUSHOVER_TOKEN")
    pushover_user: str | None = os.getenv("PUSHOVER_USER")

def validate_config(cfg: AppConfig) -> list[str]:
    warnings: list[str] = []

    if not cfg.API_KEY:
        warnings.append("API key not set. Model calls will fail.")
    
    if cfg.provider in ("OLLAMA", "OPENROUTER") and not cfg.URL:
        warnings.append("Base URL not set for provider; requests will fail.")

    if not cfg.MODEL_NAME:
        warnings.append("MODEL not set; using default.")

    # Pushover is optional
    if (cfg.pushover_token and not cfg.pushover_user) or (cfg.pushover_user and not cfg.pushover_token):
        warnings.append("Pushover is partially configured; notifications will be disabled.")
    
    return warnings
