#!/usr/bin/env python3

from .utils import execute


def test_completion_script_is_generated():
    for shell in ["bash", "zsh", "fish", "powershell"]:
        result = execute(["kosmorro", f"--completion={shell}"])

        assert result.successful
        assert result.stdout != ""
        assert result.stderr == ""


def test_completion_script_returns_error_for_unsupported_shell():
    result = execute(["kosmorro", "--completion=deuchshell"])

    assert not result.successful
    assert result.stderr == "No completion script available for this shell.\n"
    assert result.stdout == ""
