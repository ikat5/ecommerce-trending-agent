import os
from pathlib import Path
from langchain_groq import ChatGroq

def _load_local_env():
    """Load key-value pairs from .env without extra dependencies."""
    env_path = Path(__file__).resolve().parent / ".env"
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_local_env()

def get_llm():
    if not os.getenv("GROQ_API_KEY"):
        raise ValueError("GROQ_API_KEY not found. Add it in .env or export it in your environment.")

    # Llama 3 70B runs on Groq's servers instantly, taking 0 RAM on your PC
    return ChatGroq(
        model="llama-3.3-70b-versatile", 
        temperature=0.2
    )