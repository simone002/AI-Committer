import pytest
from committer.ai_client import generate_commit_message
from openai.types.chat import ChatCompletion, ChatCompletionMessage
from openai.types.chat.chat_completion import Choice

def test_generate_commit_message_success(mocker):
    """Testa la generazione del messaggio simulando la risposta di OpenAI."""
    
    # 1. Crea una finta risposta OpenAI
    fake_message = ChatCompletionMessage(
        role="assistant",
        content="feat: add awesome feature"
    )
    fake_choice = Choice(
        finish_reason="stop",
        index=0,
        message=fake_message
    )
    fake_response = ChatCompletion(
        id="fake-id",
        choices=[fake_choice],
        created=12345,
        model="gpt-3.5-turbo",
        object="chat.completion"
    )

    # 2. Simula il metodo 'client.chat.completions.create'
    mock_create = mocker.patch('committer.ai_client.client.chat.completions.create')
    mock_create.return_value = fake_response
    
    # 3. Esegui la funzione
    diff = "diff --git a/main.py b/main.py\n+ print('hello')"
    result = generate_commit_message(diff)
    
    # 4. Verifica
    assert result == "feat: add awesome feature"
    mock_create.assert_called_once() # Verifica che l'API sia stata chiamata