# Projet Crew

Bienvenue sur le projet Projet Crew, propulsé par [crewAI](https://crewai.com).

> **Projet réalisé par Adama Coulibaly, Sinaly Kanadjigui et Imane, encadré par Asmae Bentalib.**

Ce projet permet de générer automatiquement des articles sur n'importe quel sujet lié aux systèmes multi-agents (SMA) via une interface chat **Chainlit** ou **Streamlit**. Il s'appuie sur des agents CrewAI, la recherche augmentée par récupération (RAG) sur un corpus de documents spécialisés SMA (indexés avec ChromaDB), et l'export automatique en PDF fidèle au markdown (titres, listes, etc.) dans le dossier `articles/`.

## Fonctionnalités principales

- **Génération d'articles** sur n'importe quel sujet via l'interface chat Chainlit **ou Streamlit**.
- **Recherche contextuelle** grâce à ChromaDB et vectorisation de PDF.
- **Export automatique en PDF** : chaque article généré est converti en PDF formaté (titres, listes, etc.) et sauvegardé dans `articles/`.
- **Téléchargement de PDF** : possibilité de télécharger un PDF arbitraire via la commande `pdf <url> <nom_fichier.pdf>` dans le chat.
- **Compatibilité Python 3.10+** (sqlite3 >= 3.35 requis pour ChromaDB).

## Installation

Assurez-vous d'avoir Python >=3.10 et <3.13 installé sur votre système.

Installez les dépendances :

```bash
pip install -r requirements.txt
```

> **Note** : Si vous rencontrez des problèmes avec sqlite3, le projet utilise pysqlite3-binary pour garantir la compatibilité avec ChromaDB.

## Configuration

Ajoutez vos variables d'environnement (API keys, modèle, etc.) dans le fichier `.env` à la racine du projet :

```
GEMINI_API_KEY=...
MODEL=gemini/gemini-1.5-flash
```

## Lancement de l'application

Pour lancer l'interface chat Chainlit :

```bash
chainlit run src/projet/app_chainlit.py
```

Pour lancer l'interface Streamlit :

```bash
streamlit run src/projet/app.py
```

## Utilisation

- **Générer un article** : Tapez simplement le sujet de votre choix dans le chat Chainlit **ou Streamlit**. L'article sera généré, affiché, et sauvegardé en PDF dans `articles/`.
- **Télécharger un PDF** : Tapez `pdf <url> <nom_fichier.pdf>` pour télécharger un PDF depuis une URL.

Exemple :
```
climate change and AI
```

Exemple de commande PDF :
```
pdf https://arxiv.org/pdf/1234.5678.pdf mon_article.pdf
```

## Support

Pour toute question ou suggestion :
- Consultez la [documentation crewAI](https://docs.crewai.com)
- [GitHub crewAI](https://github.com/joaomdmoura/crewai)
- [Discord crewAI](https://discord.com/invite/X4JWnZnxPb)

---

Créez des articles augmentés et exportez-les en PDF en toute simplicité avec Projet Crew et Chainlit !
