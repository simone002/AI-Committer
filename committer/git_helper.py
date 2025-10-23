import subprocess
import sys

class GitHelperError(Exception):
    """Eccezione custom per errori git."""
    pass

def get_staged_diff() -> str | None:
    """
    Recupera il 'diff' dei file in staging.
    Restituisce None se non c'è nulla in staging.
    """
    try:
        # Esegue il comando 'git diff --staged'
        result = subprocess.run(
            ["git", "diff", "--staged"],
            capture_output=True,
            text=True,
            check=True,
            encoding="utf-8"
        )
        
        if not result.stdout:
            return None
        return result.stdout

    except FileNotFoundError:
        raise GitHelperError("Comando 'git' non trovato. Assicurati che Git sia installato e nel PATH.")
    except subprocess.CalledProcessError as e:
        # Errore se non è un repository git o altri problemi
        raise GitHelperError(f"Errore Git: {e.stderr}")

def commit(message: str) -> None:
    """
    Esegue il commit con il messaggio fornito.
    """
    try:
        subprocess.run(
            ["git", "commit", "-m", message],
            check=True,
            capture_output=True, # Nasconde l'output di git
            text=True
        )
    except subprocess.CalledProcessError as e:
        raise GitHelperError(f"Errore durante il commit: {e.stderr}")
    
    # aggiungo un commento per vedere se il commit funziona