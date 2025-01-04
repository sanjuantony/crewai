import os
from crewai import Crew
# from langchain_openai import ChatOpenAI
from textwrap import dedent
from agents import TravelAgents
from tasks import TravelTasks
from dotenv import load_dotenv
load_dotenv()

# Install duckduckgo-search for this example:
# !pip install -U duckduckgo-search

# from langchain.tools import DuckDuckGoSearchRun

# search_tool = DuckDuckGoSearchRun()

# os.environ["OPENAI_API_KEY"] = config("OPENAI_API_KEY")
# os.environ["OPENAI_ORGANIZATION"] = config("OPENAI_ORGANIZATION_ID")

# This is the main class that you will use to define your custom crew.
# You can define as many agents and tasks as you want in agents.py and tasks.py


class TravelCrew:
    def __init__(self, origin, city, travel_dates, interests):
        self.origin = origin
        self.city = city
        self.travel_dates = travel_dates
        self.interests = interests

    def run(self):
        # Define your custom agents and tasks in agents.py and tasks.py
        agents = TravelAgents()
        tasks = TravelTasks()

        # Define your custom agents and tasks here
        agent_expert_travel = agents.agent_expert_travel()
        agent_city_selection_expert = agents.agent_city_selection_expert()
        agent_local_tour_guide = agents.agent_local_tour_guide()

        # Custom tasks include agent name and variables as input
        task_plan_itinerary = tasks.task_plan_itinerary(
            agent_expert_travel,
            self.city,
            self.interests,
            self.travel_dates
        )

        task_identify_city = tasks.task_identify_city(
            agent_city_selection_expert,
            self.origin,
            self.city,
            self.travel_dates,
            self.interests
        )

        task_gather_city_info = tasks.task_gather_city_info(
            agent_local_tour_guide,
            self.city,
            self.travel_dates,
            self.interests
        )

        # Define your custom crew here
        crew = Crew(
            agents=[agent_city_selection_expert, agent_local_tour_guide, agent_expert_travel],
            tasks=[task_identify_city, task_gather_city_info, task_plan_itinerary],
            verbose=True
        )

        result = crew.kickoff()
        return result


# This is the main function that you will use to run your custom crew.
if __name__ == "__main__":
    print("## Welcome to Travel Planner AI")
    print("-------------------------------")
    origin = input(dedent("""Enter departing location: """))
    city = input(dedent("""Enter city  are you interested in: """))
    travel_dates = input(dedent("""Enter travel date range: """))
    interests = input(dedent("""Enter activites you are interested in: """))

    travel_crew = TravelCrew(origin, city, travel_dates, interests)
    result = travel_crew.run()
    print("\n\n########################")
    print("## Here is you travel crew run result:")
    print("########################\n")
    print(result)
