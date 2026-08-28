from agent_course.context import ContextBuilder


def test_context_builder_inserts_compaction_marker() -> None:
    messages = [{"role": "user", "content": str(i)} for i in range(8)]
    context = ContextBuilder(max_messages=5).build(messages)

    assert len(context) == 5
    assert context[0]["role"] == "system"
    assert "4 earlier messages omitted" in context[0]["content"]
    assert [item["content"] for item in context[1:]] == ["4", "5", "6", "7"]
