from dotenv import load_dotenv
import os

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

LLM_MODEL = "openai/gpt-oss-120b:free"

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

VECTOR_DB_DIR = "vector_store"

VIDEO_ID = "qN_2fnOPY-M"

WINDOW_SIZE = 10

RETRIEVAL_K = 5
MIN_RETRIEVAL_SCORE = 0.2
MIN_CONTEXT_CHARACTERS = 80
MIN_QUESTION_LENGTH = 3
MAX_QUESTION_LENGTH = 1000
