from enum import Enum
import os
from dotenv import load_dotenv


load_dotenv()


class ENV_VALUES(Enum):
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    GEMINI_MODEL = os.environ.get("GEMINI_LLM_MODEL")
