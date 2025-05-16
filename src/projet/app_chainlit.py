import sys
try:
    import pysqlite3
    sys.modules["sqlite3"] = sys.modules["pysqlite3"]
except ImportError:
    pass

from datetime import datetime
import chainlit as cl
from projet.crew import Projet
import requests
import os
from fpdf import FPDF
import re

class MarkdownPDF(FPDF):
    def write_markdown(self, md: str):
        lines = md.splitlines()
        for line in lines:
            line = line.strip()
            if not line:
                self.ln(4)
                continue
            # Titres
            if line.startswith('### '):
                self.set_font('Arial', 'B', 14)
                self.cell(0, 10, line[4:], ln=1)
                self.set_font('Arial', '', 12)
            elif line.startswith('## '):
                self.set_font('Arial', 'B', 16)
                self.cell(0, 12, line[3:], ln=1)
                self.set_font('Arial', '', 12)
            elif line.startswith('# '):
                self.set_font('Arial', 'B', 18)
                self.cell(0, 14, line[2:], ln=1)
                self.set_font('Arial', '', 12)
            # Listes à puces
            elif re.match(r'^[-*+] ', line):
                self.cell(5)
                # Utilise un tiret simple pour éviter les problèmes d'encodage
                self.cell(0, 8, '- ' + line[2:], ln=1)
            # Gras/italique
            else:
                # Remplace **gras** et *italique* par du texte simple (FPDF ne supporte pas le style inline)
                text = re.sub(r'\*\*(.*?)\*\*', r'\1', line)
                text = re.sub(r'\*(.*?)\*', r'\1', text)
                self.multi_cell(0, 8, text)

async def download_pdf(url: str, output_path: str) -> str:
    """Télécharge un fichier PDF depuis une URL et l'enregistre localement."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(output_path, 'wb') as f:
            f.write(response.content)
        return f"PDF téléchargé et sauvegardé sous : {output_path}"
    except Exception as e:
        return f"Erreur lors du téléchargement du PDF : {e}"

async def markdown_to_text(md: str) -> str:
    """Transforme le markdown en texte brut pour le PDF, en gérant les titres et la mise en page."""
    import re
    lines = md.splitlines()
    result = []
    for line in lines:
        # Enlève les balises markdown de titre
        if line.startswith('### '):
            result.append(line[4:].upper())
        elif line.startswith('## '):
            result.append(line[3:].upper())
        elif line.startswith('# '):
            result.append(line[2:].upper())
        else:
            result.append(line)
    # Supprime les lignes vides consécutives
    text = '\n'.join(result)
    text = re.sub(r'\n{2,}', '\n', text)
    return text

def clean_latin1(text: str) -> str:
    """Remplace les caractères non supportés par latin-1 par des équivalents ASCII."""
    replacements = {
        '—': '-',  # tiret long
        '–': '-',  # tiret moyen
        '’': "'", # apostrophe courbe
        '‘': "'",
        '“': '"',
        '”': '"',
        '…': '...',
        '•': '-',
        '→': '->',
        '←': '<-',
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'à': 'a', 'â': 'a', 'ä': 'a',
        'î': 'i', 'ï': 'i',
        'ô': 'o', 'ö': 'o',
        'ù': 'u', 'û': 'u', 'ü': 'u',
        'ç': 'c',
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    # Supprime tout caractère non latin-1 restant
    return text.encode('latin-1', 'replace').decode('latin-1')

async def save_article_as_pdf(title: str, content: str, folder: str = "articles") -> str:
    """Transforme le markdown en texte formaté (titres, listes, etc.) puis enregistre en PDF."""
    os.makedirs(folder, exist_ok=True)
    filename = os.path.join(folder, f"{title}.pdf")
    pdf = MarkdownPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    safe_content = clean_latin1(content)
    pdf.write_markdown(safe_content)
    pdf.output(filename)
    return filename

@cl.on_message
async def main(message: cl.Message):
    content = message.content.strip()
    if content.lower().startswith("pdf "):
        # Usage: pdf <url> <nom_fichier.pdf>
        parts = content.split()
        if len(parts) < 3:
            await cl.Message(content="Utilisation : pdf <url> <nom_fichier.pdf>").send()
            return
        url = parts[1]
        output = parts[2]
        status = await download_pdf(url, output)
        await cl.Message(content=status).send()
        return
    topic = content
    if not topic:
        await cl.Message(content="Veuillez fournir un sujet de recherche.").send()
        return
    await cl.Message(content="Génération en cours...").send()
    inputs = {
        'topic': topic,
        'current_year': str(datetime.now().year)
    }
    try:
        result = Projet().crew().kickoff(inputs=inputs)
        # Correction : CrewOutput n'a pas d'attribut 'split', on extrait le texte de l'article
        article_text = str(result.output) if hasattr(result, 'output') else str(result)
        title = article_text.split('\n')[0].strip()[:100].replace('/', '_').replace('\\', '_')
        pdf_path = await save_article_as_pdf(title, article_text)
        await cl.Message(content=f"Article généré avec succès et sauvegardé en PDF : {pdf_path}\n\n{article_text}").send()
    except Exception as e:
        await cl.Message(content=f"Une erreur est survenue : {e}").send()
