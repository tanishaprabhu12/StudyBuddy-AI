from dotenv import load_dotenv
import os

load_dotenv()

print("OPENROUTER_API_KEY:", os.getenv("OPENROUTER_API_KEY"))
print("LLM_API_KEY:", os.getenv("LLM_API_KEY"))
print("EMBEDDING_API_KEY:", os.getenv("EMBEDDING_API_KEY"))