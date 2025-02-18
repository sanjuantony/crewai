import warnings
import os


from crewai import Crew, Agent, Task
from crewai_tools import SerperDevTool, \
                         ScrapeWebsiteTool
from dotenv import load_dotenv
from IPython.display import Markdown


warnings.filterwarnings("ignore")
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"] = os.getenv("OPENAI_MODEL_NAME")

# Initialize the tools
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

# Agents needed - Planner, Writer, Editor
# Tasks: Plan, Write, Edit
# Wire up the crew

##### Agents ####
planner = Agent(
    role="Agents Planner",
    goal="Identify CrewaAI agents that can help me write code to satisfy the requested task. ",
    backstory="You are an expert in the field of Agentic AI. "
                "Your knowledge about CrewAI is excellent and you have  "
                "numerous years of experience working with the CrewAI framework. "
                "Your expertise helps you to plan for the number of agents "
                "needed to achieve the task requested. "
                "You can use any appropriate tools to help you plan better. ",
    allow_delegation=False,
    verbose=True,
    tools=[search_tool, scrape_tool]
)

# writer = Agent(
#     role="Content Writer",
#     goal="Write insightful and factually accurate "
#          "opinion piece about the topic: {topic}",
#     backstory="You're working on a writing "
#               "a new opinion piece about the topic: {topic}. "
#               "You base your writing on the work of "
#               "the Content Planner, who provides an outline "
#               "and relevant context about the topic. "
#               "You follow the main objectives and "
#               "direction of the outline, "
#               "as provide by the Content Planner. "
#               "You also provide objective and impartial insights "
#               "and back them up with information "
#               "provide by the Content Planner. "
#               "You acknowledge in your opinion piece "
#               "when your statements are opinions "
#               "as opposed to objective statements.",
#     allow_delegation=False,
#     verbose=True
# )

# editor = Agent(
#     role="Content Editor",
#     goal="Edit a given blog post to align with "
#          "the writing style of the organization. ",
#     backstory="You are an editor who receives a blog post "
#               "from the Content Writer. "
#               "Your goal is to review the blog post "
#               "to ensure that it follows journalistic best practices,"
#               "provides balanced viewpoints "
#               "when providing opinions or assertions, "
#               "and also avoids major controversial topics "
#               "or opinions when possible.",
#     allow_delegation=False,
#     verbose=True
# )

##### Tasks ####
plan = Task(
    description=(
        "1. Your task is to identify the right number of agents to achieve the task request in {topic}. "
        "2. Think and reason on how what kind of CrewAI agents would be needed to achieve the requested task."
        "3. List the agents, their names, their role and backstory that I can use in my CrewAI code."
    ),
    expected_output="A listing of all agents, their names, their roles and backstory "
                    "in a table format with columns headers as below "
                    "CrewAI Agent # | CrewAI Agent Name | CrewAI Agent Role | CrewAI Agent Backstory",
    agent=planner
)

# write = Task(
#     description=(
#         "1. Use the content plan to craft a compelling "
#             "blog post on {topic}.\n"
#         "2. Incorporate SEO keywords naturally.\n"
# 		"3. Sections/Subtitles are properly named "
#             "in an engaging manner.\n"
#         "4. Ensure the post is structured with an "
#             "engaging introduction, insightful body, "
#             "and a summarizing conclusion.\n"
#         "5. Proofread for grammatical errors and "
#             "alignment with the brand's voice.\n"
#     ),
#     expected_output="A well-written blog post "
#         "in markdown format, ready for publication, "
#         "each section should have 2 or 3 paragraphs.",
#     agent=writer,
# )

# edit = Task(
#     description=("Proofread the given blog post for "
#                  "grammatical errors and "
#                  "alignment with the brand's voice."),
#     expected_output="A well-written blog post in markdown format, "
#                     "ready for publication, "
#                     "each section should have 2 or 3 paragraphs.",
#     agent=editor
# )

### Assemble the Crew ###
crew = Crew(
    agents=[planner],
    tasks=[plan],
    verbose=True
)


### Kickoff the Crew ###
result = crew.kickoff(inputs={"topic": "Search for jobs that satisfy a certain criteria. "})

print(result)

# Below line needed only if running in Jupyter notebook, so as to get a formatted output
# Markdown(result)