import subprocess

def installer_bibliotheque(list_bibliotheque):
    for i in list_bibliotheque:
        try:
            subprocess.check_call(['python','-m','pip', 'install', i])
            print(f"La bibliothèque {i} a été installée avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'installation de {i}: {str(e)}")


if __name__ == "__main__":
    bibliotheque_a_installer = [
    "tk",
    "customtkinter",
    "cython",
    "av",
    "tkvideoplayer",
    "pydub",
    "moviepy",
    "pytube",
    "requests",
    "pygame",
    "Pillow",
    "python-nasa-api",
    "tqdm",
    "datetime ",
    "urllib3",
    "python-nasa-api"
    
]
    
    installer_bibliotheque(bibliotheque_a_installer)