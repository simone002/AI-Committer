import pytest
import subprocess
from committer.git_helper import get_staged_diff, commit, GitHelperError

def test_get_staged_diff_success(mocker):
    """Testa se il diff viene letto correttamente."""
    fake_diff = "diff --git a/file.txt b/file.txt\n--- a/file.txt\n+++ b/file.txt\n@@ -1 +1 @@\n-hello\n+world"
    
    # Simula subprocess.run
    mock_run = mocker.patch('subprocess.run')
    mock_run.return_value.stdout = fake_diff
    mock_run.return_value.stderr = ""
    
    assert get_staged_diff() == fake_diff
    mock_run.assert_called_once_with(
        ["git", "diff", "--staged"],
        capture_output=True, text=True, check=True, encoding="utf-8"
    )

def test_get_staged_diff_empty(mocker):
    """Testa se non c'è nessun diff."""
    mock_run = mocker.patch('subprocess.run')
    mock_run.return_value.stdout = "" # Output vuoto
    
    assert get_staged_diff() is None

def test_commit_success(mocker):
    """Testa se il comando di commit viene chiamato correttamente."""
    mock_run = mocker.patch('subprocess.run')
    message = "feat: add new feature"
    
    commit(message)
    
    mock_run.assert_called_once_with(
        ["git", "commit", "-m", message],
        check=True, capture_output=True, text=True
    )