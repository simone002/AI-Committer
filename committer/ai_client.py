import os
import google.generativeai as genai

try:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise KeyError
    genai.configure(api_key=api_key)
    
except KeyError:
    print("Errore: Manca la chiave GOOGLE_API_KEY. Assicurati di aver creato un file .env e inserito la chiave.")
    exit(1)
except Exception as e:
    print(f"Errore durante la configurazione di Google AI: {e}")
    exit(1)


def generate_commit_message(diff: str) -> str:
    """
    Data una stringa di 'diff', genera un messaggio di commit usando Google Gemini.
    """
    
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
    Sei un assistente esperto nella scrittura di messaggi di commit git.
    Analizza il diff seguente e genera un messaggio di commit che segua le specifiche "Conventional Commits".

    Il formato deve essere: <tipo>[scope opzionale]: <descrizione>
    
    Tipi comuni:
    - feat: Una nuova funzionalità
    - fix: Una correzione di bug
    - docs: Cambiamenti alla documentazione
    - style: Modifiche che non impattano il codice (spazi, formattazione)
    - refactor: Una modifica al codice che non aggiunge funzionalità né corregge bug
    - test: Aggiunta o modifica di test
    - chore: Modifiche a build, CI/CD o altri compiti di manutenzione
    
    Rispondi SOLO con il messaggio di commit completo e nient'altro. Non aggiungere spiegazioni o markup.

    Ecco il diff da analizzare:
    ---
    {diff}
    ---
    """

    try:
        response = model.generate_content(prompt)
        
        message = response.text.strip()
        return message.strip('"`')

    except Exception as e:
        return f"Errore durante la chiamata a Google Gemini: {e}"