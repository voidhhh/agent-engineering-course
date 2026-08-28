from __future__ import annotations

import os

import pytest

from agent_course import DeepSeekChatAdapter

LIVE_ENABLED = os.environ.get("DEEPSEEK_LIVE_TEST") == "1"
KEY = os.environ.get("DEEPSEEK_API_KEY", "").strip().lower()
HAS_REAL_KEY = bool(KEY) and not KEY.startswith(("replace-", "<your", "your_"))


@pytest.mark.live
@pytest.mark.skipif(
    not (LIVE_ENABLED and HAS_REAL_KEY),
    reason="set DEEPSEEK_LIVE_TEST=1 and DEEPSEEK_API_KEY to run the paid live smoke test",
)
def test_deepseek_live_chat_completion() -> None:
    adapter = DeepSeekChatAdapter.from_env()
    adapter.thinking = False
    adapter.max_tokens = 32

    turn = adapter.complete(
        [{"role": "user", "content": "Reply with exactly: DEEPSEEK_LIVE_OK"}], []
    )

    assert turn.content
    assert "DEEPSEEK_LIVE_OK" in turn.content
