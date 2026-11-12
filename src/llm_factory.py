from src.config import Config
from langchain_ollama import OllamaEmbeddings

def get_llm():
    provider = Config.LLM_PROVIDER
    if provider == "ollama":
        from langchain_ollama import ChatOllama
        print(f"🤖 Initializing Local LLM (Ollama: {Config.OLLAMA_MODEL})...")
        return ChatOllama(model=Config.OLLAMA_MODEL, base_url=Config.OLLAMA_BASE_URL, temperature=0.1)
    elif provider == "openai":
        from langchain_openai import ChatOpenAI
        print(f"☁️ Initializing Cloud LLM (OpenAI: {Config.OPENAI_MODEL})...")
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is missing in environment variables.")
        return ChatOpenAI(model=Config.OPENAI_MODEL, api_key=Config.OPENAI_API_KEY, temperature=0.1)
    elif provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        print(f"☁️ Initializing Cloud LLM (Gemini: {Config.GEMINI_MODEL})...")
        if not Config.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is missing in environment variables.")
        return ChatGoogleGenerativeAI(model=Config.GEMINI_MODEL, google_api_key=Config.GOOGLE_API_KEY, temperature=0.1)
    else:
        raise ValueError(f"Unsupported LLM Provider: {provider}.")

def get_embeddings():
    print(f"🧠 Loading Embeddings Model (Ollama: {Config.OLLAMA_EMBED_MODEL})...")
    return OllamaEmbeddings(model=Config.OLLAMA_EMBED_MODEL, base_url=Config.OLLAMA_BASE_URL)
