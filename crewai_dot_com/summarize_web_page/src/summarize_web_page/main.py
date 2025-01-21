#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from summarize_web_page.crew import SummarizeWebPage

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        # 'url': 'https://bessey.dev/blog/2024/05/24/why-im-over-graphql/'
        "url": "https://mobilelive.medium.com/how-to-deploy-a-graphql-api-a-comprehensive-guide-611afe23dfd#:~:text=Cloud%20Platforms%3A%20Deploy%20your%20GraphQL,Lambda%20or%20Google%20Cloud%20Functions."
    }
    
    try:
        SummarizeWebPage().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        SummarizeWebPage().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        SummarizeWebPage().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        SummarizeWebPage().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
