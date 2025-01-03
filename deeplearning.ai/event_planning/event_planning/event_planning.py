import warnings
import os


from crewai import Crew, Agent, Task
# from utils import get_openai_api_key
from crewai_tools import SerperDevTool, \
                         ScrapeWebsiteTool, \
                         WebsiteSearchTool
from dotenv import load_dotenv
# from IPython.display import Markdown


warnings.filterwarnings("ignore")
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"] = "gpt-3.5-turbo"
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

