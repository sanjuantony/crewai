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

from pydantic import BaseModel
# Define a Pydantic model for venue details 
# (demonstrating Output as Pydantic)
# class AgentDetails(BaseModel):
#     agent_name: str
#     agent_goal: str
#     agent_backstory: str

# Agents needed - Planner, Writer, Editor
# Tasks: Plan, Write, Edit
# Wire up the crew

##### Agents ####
agent_planner = Agent(
    role="Agents Planner",
    goal="Identify CrewaAI agents needed to complete the requested task. ",
    backstory="You are an expert in the field of Agentic AI. "
                "Your knowledge about CrewAI is excellent and you have  "
                "numerous years of experience working with the CrewAI framework. "
                "Your expertise helps you decide the appropriate number of agents "
                "needed to achieve the task requested. "
                "You can use any appropriate tools to help you plan better. ",
    allow_delegation=False,
    verbose=True,
    tools=[search_tool]
)

task_planner = Agent(
    role="Tasks Planner",
    goal="Identify CrewaAI tasks needed for each of the agents identified by the Agent Planner agent. ",
    backstory="You are an expert in the field of Agentic AI. "
                "Your knowledge about CrewAI is excellent and you have  "
                "numerous years of experience working with the CrewAI framework. "
                "Your expertise helps you decide the appropriate task each agent has to perform "
                "to achieve the task requested. "
                "You can use any appropriate tools to help you plan better. ",
    allow_delegation=False,
    verbose=True,
    # tools=[search_tool, scrape_tool]
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
agent_plan = Task(
    description=(
        "Your task is to understand the request made by the user, and identify the right number of "
        "CrewAI agents needed. The topic is: {topic}"
        "Think thoroughly on the kind of CrewAI agents needed to achieve the requested topic. "
        "You also need to find any CrewAI or Langchain tools that the agent needs to perform their task. There "
        "could be multiple tools the agent can use and if so, create them as a list as [tool1, tool2, ...]"
        "List the agents, their names, their role, backstory and tools recommended, that I can use in my CrewAI code."
    ),
    expected_output="A listing of all agents, their names, their roles and backstory "
                    "in a table format with columns headers as below "
                    "CrewAI Agent # | CrewAI Agent Name | CrewAI Agent Role | CrewAI Agent Backstory | List of Tools",
    agent=agent_planner
)

task_plan = Task(
    description=(
        "For each of the agents identified by the task agent, you need to create the appropriate "
        "CrewAI task that can used in the program."
        "Think thoroughly on what task each agent need to do to achieve the results as requested by {topic}"
        "List the Task Name, Task Description, Expected Output and agent name who will perform this task. "
        "I will be using this information in my CrewAI code."
    ),
    expected_output="A listing of all task description, expectde output and agent handling the task  "
                    "in a table format with columns headers as below "
                    "Task Name | Task Description | Expected Output | Agent Perfomring the Task",
    agent=task_planner
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
    agents=[agent_planner, task_planner],
    tasks=[agent_plan, task_plan],
    verbose=True
)


### Kickoff the Crew ###
crew_input={
                "topic": "I need to scrape a website and list down topics and URLs from that website. "
                              "This information need to be passed to another agent which can access each of the URLs "
                              "from the list above, scrape the content from this subsite and then summarize the content."
            }
result = crew.kickoff(inputs=crew_input)

print(result)

# Below line needed only if running in Jupyter notebook, so as to get a formatted output
# Markdown(result)