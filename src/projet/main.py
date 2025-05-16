import sys
try:
    import pysqlite3
    sys.modules["sqlite3"] = sys.modules["pysqlite3"]
except ImportError:
    pass
#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
import streamlit as st 
from projet.crew import Projet

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    st.title("📘 Article Generator avec CrewAI")

    # Input utilisateur
    topic = st.text_input("Sujet de recherche.....")
    run_button = st.button("Lancer la génération d'article")

    if run_button and topic:
        with st.spinner("Génération en cours..."):
            # Lancer CrewAI
            inputs = {
                'topic': "AI LLMs",
                'current_year': str(datetime.now().year)
            }
        try:
            result=Projet().crew().kickoff(inputs=inputs)
        # Afficher la sortie
        #print(result)
            st.success("Article généré avec succès !")
            st.markdown(result)
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
        Projet().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Projet().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    try:
        Projet().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
