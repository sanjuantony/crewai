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
class FlightDetails(BaseModel):
    airline: str
    price: float
    travel_date: str
    airline_preference: str

class AvailableFlights(BaseModel):
    flights: list[FlightDetails]



# Task 1: Search Flights
search_flights_task = Task(
    description="Find ONE WAY flights originating from {from_airport} to {to_airport}.  "
                "The departing travel date should be between {from_date} and {to_date}. "
                "DO NOT search for flights outside of this date range. "
                "If there is a preference of airline as stated in {airline_preference} "
                "search only that airline, else any airline is fine. "
                "Find flights with the LOWEST price. ",
    expected_output="A list of 10 available flights sorted by price. ",
    human_input=True,
    output_json=AvailableFlights,
    output_file="AvailableFlights.json",
    agent=search_flights_agent
)

trip_details = {
    'from_airport': "JFK",
    'to_airport': "BOM",
    'from_date': "15 June 2025",
    'to_date': "15 July 2025",
    'airline_preference': "Virgin Atlantic"
}

trip_crew = Crew(
    agents=[search_flights_agent],
    tasks=[search_flights_task], 
    verbose=True
)
result = trip_crew.kickoff(inputs=trip_details)

print ("Run Complete")