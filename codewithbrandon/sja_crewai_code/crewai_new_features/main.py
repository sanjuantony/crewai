## test

from langchain_openai import ChatOpenAI
from agents import AINewsLetterAgents
from file_io import save_markdown
from tasks import AINewsLetterTasks
from crewai import Crew, Process
from dotenv import load_dotenv
load_dotenv()

# Initialize the OpenAI GPT-4 model
OpenAIGPT4 = ChatOpenAI(
    model="gpt-4"
)

# Set up agents
agents = AINewsLetterAgents()
agent_editor = agents.editor_agent()
agent_news_fetcher = agents.news_fetcher_agent()
agent_news_analyzer = agents.news_analyzer_agent()
agent_newsletter_compiler = agents.newsletter_compiler_agent()

# set up tasks
tasks = AINewsLetterTasks()
task_news_fetcher = tasks.fetch_news_task(
    agent_news_fetcher)
task_analyze_news = tasks.analyze_news_task(
    agent_news_analyzer, [task_news_fetcher])
task_compile_newsletter = tasks.compile_newsletter_task(
    agent_newsletter_compiler, [task_analyze_news], callback_function=save_markdown)

# Set up tools
crew = Crew(
    agents=[agent_editor, agent_news_fetcher, agent_news_analyzer, agent_newsletter_compiler],
    tasks=[task_news_fetcher, task_analyze_news, task_compile_newsletter],
    process=Process.hierarchical,
    manager_llm=OpenAIGPT4
)

results = crew.kickoff()

print("********* AI Editor Crew Results **********")
print(results)