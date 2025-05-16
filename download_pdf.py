import requests

def download_pdf(url: str, output_path: str):
    """Télécharge un fichier PDF depuis une URL et l'enregistre localement."""
    response = requests.get(url)
    response.raise_for_status()
    with open(output_path, 'wb') as f:
        f.write(response.content)
    print(f"PDF téléchargé et sauvegardé sous : {output_path}")

if __name__ == "__main__":
    url = input("Entrez l'URL du PDF à télécharger : ")
    output = input("Entrez le chemin de sauvegarde (ex: fichier.pdf) : ")
    download_pdf(url, output)
