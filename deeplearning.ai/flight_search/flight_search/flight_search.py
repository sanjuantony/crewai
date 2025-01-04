import warnings
import os


from crewai import Crew, Agent, Task
# from utils import get_openai_api_key
from crewai_tools import SerperDevTool, \
                         ScrapeWebsiteTool, \
                         WebsiteSearchTool
from dotenv import load_dotenv
# from IPython.display import Markdow


warnings.filterwarnings("ignore")
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"] = "gpt-3.5-turbo"
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

# Initialize the tools
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

#  Agent 1: Search Flights
search_flights_agent = Agent(
    role="Search Flights",
    goal="Search for flights based on user input. "
        "Provide the user with a list of available flights.",
    backstory=(
        "You are an expert in searching for flights. "
        "You need to find flights based on the user's input. "
    ),
    tools=[search_tool, scrape_tool],
    verbose=True
)


from pydantic import BaseModel
class AvailableFlights(BaseModel):
    flights: list

class FlightDetails(BaseModel):
    airline: str
    price: float
    departure_time: str
    arrival_time: str
    duration: str
    layovers: int
    layover_duration: str

# Task 1: Search Flights
search_flights_task = Task(
    description="Find flights originating from {from_airport} "
                "and flying to {to_airport}. "
                "A round trip flights should be available on {from_date} until {to_date}. ",
    expected_output="The first 5 flights sorted by price. Show me flights which has price data on there. ",
    human_input=True,
    output_json=AvailableFlights,
    output_file="AvailableFlights.json",  
      # Outputs the venue details as a JSON file
    agent=search_flights_agent
)

trip_details = {
    'from_airport': "JFK",
    'to_airport': "PHX",
    'from_date': "01 Feb 2025",
    'to_date': "10 Feb 2025"
}

trip_crew = Crew(
    agents=[search_flights_agent],
    tasks=[search_flights_task], 
    verbose=True
)
result = trip_crew.kickoff(inputs=trip_details)

print ("Run Complete")