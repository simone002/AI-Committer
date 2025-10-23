import os
from openai import OpenAI, OpenAIError

# Inizializza il client. 
# La chiave API viene letta automaticamente dalla variabile d'ambiente OPENAI_API_KEY
try:
    client = OpenAI()
except OpenAIError as e:
    print(f"Errore: Manca la chiave OPENAI_API_KEY. Assicurati di aver creato un file .env")
    # Puoi gestire l'errore in modo più elegante, ma per ora usciamo
    exit(1)


def generate_commit_message(diff: str) -> str:
    """
    Data una stringa di 'diff', genera un messaggio di commit.
    """
    
    # Questo è il "prompt engineering"
    system_prompt = """
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
    
    Rispondi SOLO con il messaggio di commit completo e nient'altro. Non aggiungere spiegazioni.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # Puoi cambiarlo con gpt-4o se preferisci
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Analizza questo diff:\n\n{diff}"}
            ],
            temperature=0.5,
            max_tokens=100
        )
        
        message = response.choices[0].message.content.strip()
        # Pulisce la risposta da eventuali virgolette
        return message.strip('"`')

    except OpenAIError as e:
        return f"Errore durante la chiamata a OpenAI: {e}"
    except Exception as e:
        return f"Errore sconosciuto: {e}"