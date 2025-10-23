import click
import sys
from dotenv import load_dotenv

load_dotenv()

from committer.git_helper import get_staged_diff, commit, GitHelperError
from committer.ai_client import generate_commit_message



@click.command()
def main():
    """
    Genera automaticamente un messaggio di commit per i file in staging
    utilizzando l'IA.
    """
    click.echo("Controllo dei file in staging...")
    
    try:
        diff = get_staged_diff()
        
        if diff is None:
            click.secho("Nessun file trovato in staging. Fai 'git add' prima di eseguire.", fg="yellow")
            sys.exit(0)
            
        click.echo("File trovati. Invio il diff all'IA per l'analisi...")
        
        # 2. Genera il messaggio di commit
        suggestion = generate_commit_message(diff)
        
        click.echo("\n" + "="*30)
        click.secho("Suggerimento dell'IA:", bold=True)
        click.secho(f"{suggestion}", fg="cyan")
        click.echo("="*30 + "\n")
        
        # 3. Chiedi conferma (Fase 4 del piano)
        if click.confirm("Vuoi eseguire il commit con questo messaggio?"):
            commit(suggestion)
            click.secho("Commit eseguito con successo!", fg="green")
        else:
            click.secho("Commit annullato.", fg="red")

    except GitHelperError as e:
        click.secho(f"ERRORE: {e}", fg="red")
        sys.exit(1)
    except Exception as e:
        click.secho(f"Errore imprevisto: {e}", fg="red")
        sys.exit(1)

if __name__ == "__main__":
    main()