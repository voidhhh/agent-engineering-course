from __future__ import annotations

import argparse
import json
import os
from typing import Any

from agent_course import DeepSeekChatAdapter, MiniHarness, ToolRegistry, ToolSpec
from agent_course.deepseek import DEFAULT_BASE_URL, DEFAULT_MODEL, DeepSeekConfigurationError


def require_key() -> str:
    key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if not key or key.lower().startswith(("replace-", "<your", "your_")):
        raise DeepSeekConfigurationError(
            "Copy .env.example to .env and set a real DEEPSEEK_API_KEY"
        )
    return key


def sdk_client() -> Any:
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise DeepSeekConfigurationError(
            'Install the live dependency with: pip install -e ".[deepseek]"'
        ) from exc
    return OpenAI(
        api_key=require_key(),
        base_url=os.environ.get("DEEPSEEK_BASE_URL", DEFAULT_BASE_URL),
        timeout=60.0,
    )


def run_chat(prompt: str) -> None:
    adapter = DeepSeekChatAdapter.from_env()
    turn = adapter.complete([{"role": "user", "content": prompt}], [])
    print(turn.content or "")
    print(f"\nusage={turn.usage}")


def run_stream(prompt: str) -> None:
    model = os.environ.get("DEEPSEEK_MODEL", DEFAULT_MODEL)
    effort = os.environ.get("DEEPSEEK_REASONING_EFFORT", "high")
    enabled = os.environ.get("DEEPSEEK_THINKING", "enabled") == "enabled"
    stream = sdk_client().responses.create(
        model=model,
        instructions="Answer directly and do not expose secrets.",
        input=prompt,
        stream=True,
        reasoning={"effort": effort if enabled else "none"},
        max_output_tokens=int(os.environ.get("DEEPSEEK_MAX_TOKENS", "512")),
    )
    completed_response: Any | None = None
    for event in stream:
        if event.type == "response.output_text.delta":
            print(event.delta, end="", flush=True)
        elif event.type == "response.completed":
            completed_response = event.response
        elif event.type == "response.incomplete":
            raise RuntimeError("DeepSeek stream ended before a complete response")
        elif event.type == "response.failed":
            raise RuntimeError(f"DeepSeek stream failed: {event.response.error}")
    if completed_response is None:
        raise RuntimeError("DeepSeek stream ended without a terminal response event")
    usage = completed_response.usage
    print(
        "\nusage="
        f"{{'input_tokens': {usage.input_tokens}, "
        f"'output_tokens': {usage.output_tokens}, 'total_tokens': {usage.total_tokens}}}"
    )


def run_json(prompt: str) -> None:
    response = sdk_client().chat.completions.create(
        model=os.environ.get("DEEPSEEK_MODEL", DEFAULT_MODEL),
        messages=[
            {
                "role": "system",
                "content": (
                    "Return one JSON object with string fields summary and next_action. "
                    'Example: {"summary":"...","next_action":"..."}'
                ),
            },
            {"role": "user", "content": f"Analyze this text and answer in JSON: {prompt}"},
        ],
        response_format={"type": "json_object"},
        max_tokens=256,
        extra_body={"thinking": {"type": "disabled"}},
    )
    content = response.choices[0].message.content or "{}"
    print(json.dumps(json.loads(content), ensure_ascii=False, indent=2))
    usage = response.usage
    print(
        f"usage={{'prompt_tokens': {usage.prompt_tokens}, "
        f"'completion_tokens': {usage.completion_tokens}, "
        f"'total_tokens': {usage.total_tokens}}}"
    )


def arithmetic_tools() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(
        ToolSpec(
            name="add_numbers",
            description="Add exactly two numbers and return the numeric result.",
            parameters={
                "type": "object",
                "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
                "required": ["a", "b"],
                "additionalProperties": False,
            },
            handler=lambda arguments: arguments["a"] + arguments["b"],
        )
    )
    return registry


def run_harness(prompt: str) -> None:
    adapter = DeepSeekChatAdapter.from_env()
    adapter.initial_tool_choice = "required"
    harness = MiniHarness(adapter, arithmetic_tools(), max_steps=4)
    result = harness.run("deepseek-live", prompt)
    print(f"status={result.status}")
    print(f"output={result.output}")
    print("trace:")
    for event in harness.trace("deepseek-live"):
        print(f"  {event.sequence:02d} {event.kind} {event.payload}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Real DeepSeek API course demos")
    parser.add_argument("mode", choices=("chat", "stream", "json", "harness"))
    parser.add_argument(
        "prompt",
        nargs="?",
        default="Use the add_numbers tool to calculate 17 + 25, then answer briefly.",
    )
    args = parser.parse_args()
    runners = {
        "chat": run_chat,
        "stream": run_stream,
        "json": run_json,
        "harness": run_harness,
    }
    runners[args.mode](args.prompt)


if __name__ == "__main__":
    main()
