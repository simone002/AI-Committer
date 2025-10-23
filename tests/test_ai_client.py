import pytest
from committer.ai_client import generate_commit_message

# Simula la classe di risposta di Gemini, che ha un attributo .text
class MockGeminiResponse:
    def __init__(self, text):
        self.text = text

def test_generate_commit_message_success(mocker):
    """Testa la generazione del messaggio simulando la risposta di Gemini."""
    
    # 1. Crea una finta risposta
    fake_response_text = "fix: correct typo in main"
    fake_response = MockGeminiResponse(text=fake_response_text)

    # 2. Simula il *metodo* generate_content
    # Dobbiamo simulare l'istanza del modello
    mock_model_instance = mocker.MagicMock()
    mock_model_instance.generate_content.return_value = fake_response

    # 3. Simula l'*inizializzazione* della classe GenerativeModel
    # per far sì che restituisca la nostra istanza simulata
    mock_model_init = mocker.patch('google.generativeai.GenerativeModel')
    mock_model_init.return_value = mock_model_instance
    
    # 4. Esegui la funzione
    diff = "diff --git a/main.py b/main.py\n- print('helllo')\n+ print('hello')"
    result = generate_commit_message(diff)
    
    # 5. Verifica
    assert result == fake_response_text
    # Controlla che il modello 'gemini-2.5-flash' sia stato chiamato (aggiornato!)
    mock_model_init.assert_called_once_with('gemini-2.5-flash')
    # Controlla che il metodo per generare il contenuto sia stato chiamato
    mock_model_instance.generate_content.assert_called_once()