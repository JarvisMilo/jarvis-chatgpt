from jarvis.context import ConversationContext
from jarvis.llm import ChatMessage


def test_context_builds_messages_and_trims():
    context = ConversationContext("system", max_messages=2)
    context.add_user("one")
    context.add_assistant("two")
    context.add_user("three")
    messages = context.messages("memory", "tools")
    assert messages[0] == ChatMessage("system", "system")
    assert messages[1].content == "memory"
    assert messages[2].content == "tools"
    assert [m.content for m in messages[3:]] == ["two", "three"]
