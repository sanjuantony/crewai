# Add your utilities or helper functions to this file.

import os
from dotenv import load_dotenv, find_dotenv

# these expect to find a .env file at the directory above the lesson.                                                                                                                     # the format for that file is (without the comment)                                                                                                                                       #API_KEYNAME=AStringThatIsTheLongAPIKeyFromSomeService                                                                                                                                     
def load_env():
    _ = load_dotenv(find_dotenv())

def get_openai_api_key():
    load_env()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    return openai_api_key

def get_serper_api_key():
    load_env()
    serper_api_key = os.getenv("SERPER_API_KEY")
    return serper_api_key

def get_openai_model_name():
    load_env()
    openai_model_name = os.getenv("OPENAI_MODEL_NAME")
    return openai_model_name

def get_judge_llm_model_name():
    load_env()
    judge_llm_model_name = os.getenv("JUDGE_LLM_MODEL_NAME")
    return judge_llm_model_name
