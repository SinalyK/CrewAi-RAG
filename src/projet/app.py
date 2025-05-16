import sys
try:
    import pysqlite3
    sys.modules["sqlite3"] = sys.modules["pysqlite3"]
except ImportError:
    pass

from datetime import datetime
import streamlit as st 
from projet.crew import Projet


st.title("📘 Article Generator avec CrewAI")

    # Input utilisateur
topic = st.text_input("Sujet de recherche.....")
run_button = st.button("Lancer la génération d'article")

if run_button and topic:
    with st.spinner("Génération en cours..."):
            # Lancer CrewAI
        inputs = {
            'topic': topic,
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