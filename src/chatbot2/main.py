#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from chatbot2.crew import Chatbot2

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
warnings.filterwarnings("ignore", category=DeprecationWarning)


# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Chat loop with built-in conversational memory
    """ 
    try:
        # Initialize the conversational system once
        
        chatbot = Chatbot2()
        crew = chatbot.crew()
         # Main chat loop
        while True:
            try:
                # Get user input with nice formatting
                user_input = input("Query: ").strip()
                
                inputs = {
                    'query': user_input,
                    'current_year': str(datetime.now().year)
                }
                
                # Execute with built-in memory
                result = crew.kickoff(inputs=inputs)
                print(result)
                
            except KeyboardInterrupt:
                print("\n Chat interrupted. Goodbye!")
                break
                
            except Exception as e:
                print(f"\n encountered an issue: {str(e)}")
                print("💡 Let's try again")
                continue
                
    except Exception as e:
        print(f"\n❌ Failed to initialize the conversational agent:")
        print(f"   Error: {str(e)}")
       



def oldrun():
    """
    Run the crew.
    """
    inputs = {
        "query": "what was the revenue of american express company in 2024?",
        'current_year': str(datetime.now().year)
    }
    
    try:
        Chatbot2().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "query": "what was the revenue of american express company in 2024?",
        'current_year': str(datetime.now().year)
    }
    try:
        Chatbot2().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Chatbot2().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "query": "what was the revenue of american express company in 2024?",
        "current_year": str(datetime.now().year)
    }
    
    try:
        Chatbot2().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
