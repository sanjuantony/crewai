from crewai import Agent
from textwrap import dedent
from langchain_openai import ChatOpenAI
from tools.search_tools import SearchTools
from tools.calculator_tools import CalculatorTools


"""
Creating agents cheat sheet
- Think like a boss. Work backwards from a goal. Think what employee you need
- Captain: Orients other agents towards the goal
- Experts: These are agents that the captain can communicate with and delegate tasks to
-- Build a top down structure of crew

Goal:
    - Create a 7 day itinerary with detailed per-day plan, including budget, packing suggestions and
        safety tips

Captain:
    - Expert Travel Agent

Experts to hire:
    - City Selection Expert
    - Local Tour Guide

Notes:
    - Agents should be result driven and have a clear goal
    - Role = "Job Title"
    - Goals should be "Actionable"
    - Backstory = "Resume"

"""

# This is an example of how to define custom agents.
# You can define as many agents as you want.
# You can also define custom tasks in tasks.py
class TravelAgents:
    def __init__(self):
        self.OpenAIGPT35 = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
        self.OpenAIGPT4 = ChatOpenAI(model="gpt-4", temperature=0.7)
        # self.Ollama = Ollama(model="openhermes")

    def agent_expert_travel(self):
        return Agent(
            role="Expert Travel Agent",
            goal=dedent(f"""
                            Create a 7 day itinerary with detailed per-day plan, 
                            budget, packing suggestions and safety tips
                        """),
            backstory=dedent(f"""
                                Expert in travel planning and logistics. I have decades of experience
                                making travel itineraries
                            """),
            tools=[
                    SearchTools.search_internet, 
                    CalculatorTools.calculate
                ],
            verbose=True,
            llm=self.OpenAIGPT35,
        )

    def agent_city_selection_expert(self):
        return Agent(
            role="City Selection Expert",
            goal=dedent(f"""
                            Select the best cities based on weather, season, price and 
                            travelers interests
                        """),
            backstory=dedent(f"""   
                                Expert at analyzing travel data to pick ideal destinations

                            """),
            tools=[
                    SearchTools.search_internet
                ],
            verbose=True,
            llm=self.OpenAIGPT35,
        )

    def agent_local_tour_guide(self):
        return Agent(
            role="Local Tour Guide",
            goal=dedent(f"""
                            Provide the best insights about the selected city
                        """),
            backstory=dedent(f"""
                                Knowledgeable local guide with extensive information 
                                about the city, its attractions and customs
                            """),
            tools=[
                    SearchTools.search_internet
                ],
            verbose=True,
            llm=self.OpenAIGPT35,
        )