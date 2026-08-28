from __future__ import annotations

import json
import os
from collections.abc import Sequence
from typing import Any

from .models import ModelTurn, ToolCall

DEFAULT_BASE_URL = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-v4-flash"


class DeepSeekConfigurationError(ValueError):
    """Raised before a network call when the DeepSeek configuration is unsafe or incomplete."""


class DeepSeekProtocolError(RuntimeError):
    """Raised when a provider response cannot be normalized for the Agent loop."""


def _looks_like_placeholder(value: str) -> bool:
    normalized = value.strip().lower()
    return not normalized or normalized.startswith(("replace-", "<your", "your_"))


def _provider_tools(tools: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    converted: list[dict[str, Any]] = []
    for tool in tools:
        if tool.get("type") != "function":
            raise DeepSeekProtocolError(f"unsupported tool type: {tool.get('type')!r}")
        converted.append(
            {
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": tool["parameters"],
                },
            }
        )
    return converted


def _provider_messages(
    messages: Sequence[dict[str, Any]], *, include_reasoning: bool
) -> list[dict[str, Any]]:
    converted: list[dict[str, Any]] = []
    for message in messages:
        role = message["role"]
        item: dict[str, Any] = {"role": role}
        content = message.get("content", "")
        if role == "tool" and not isinstance(content, str):
            content = json.dumps(content, ensure_ascii=False, sort_keys=True)
        item["content"] = content

        if role == "assistant" and message.get("tool_calls"):
            item["tool_calls"] = [
                {
                    "id": call["id"],
                    "type": "function",
                    "function": {
                        "name": call["name"],
                        "arguments": json.dumps(
                            call["arguments"], ensure_ascii=False, sort_keys=True
                        ),
                    },
                }
                for call in message["tool_calls"]
            ]
            if include_reasoning and message.get("reasoning") is not None:
                item["reasoning_content"] = message["reasoning"]

        if role == "tool":
            item["tool_call_id"] = message["tool_call_id"]
            if message.get("name"):
                item["name"] = message["name"]
        converted.append(item)
    return converted


def _usage_dict(raw: Any) -> dict[str, int]:
    if raw is None:
        return {}
    fields = ("prompt_tokens", "completion_tokens", "total_tokens")
    return {
        field: value
        for field in fields
        if isinstance((value := getattr(raw, field, None)), int)
    }


class DeepSeekChatAdapter:
    """OpenAI-compatible DeepSeek adapter for the course Mini Harness.

    The optional ``client`` argument is a seam for deterministic offline tests. When it is
    omitted, the OpenAI Python SDK is imported lazily and a real DeepSeek client is built.
    """

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        model: str = DEFAULT_MODEL,
        thinking: bool = True,
        reasoning_effort: str = "high",
        initial_tool_choice: str = "auto",
        max_tokens: int = 512,
        timeout: float = 60.0,
        client: Any | None = None,
    ) -> None:
        if reasoning_effort not in {"low", "high", "max"}:
            raise DeepSeekConfigurationError(
                "reasoning_effort must be one of: low, high, max"
            )
        if initial_tool_choice not in {"auto", "required"}:
            raise DeepSeekConfigurationError(
                "initial_tool_choice must be auto or required"
            )
        if model not in {
            "deepseek-v4-flash",
            "deepseek-v4-pro",
            "deepseek-v4-flash-vision-exp",
        }:
            raise DeepSeekConfigurationError(f"unsupported course model baseline: {model}")
        if max_tokens < 1:
            raise DeepSeekConfigurationError("max_tokens must be positive")
        if client is None:
            if api_key is None or _looks_like_placeholder(api_key):
                raise DeepSeekConfigurationError(
                    "Set DEEPSEEK_API_KEY to a real key; placeholders are rejected"
                )
            try:
                from openai import OpenAI
            except ImportError as exc:
                raise DeepSeekConfigurationError(
                    'Install the optional dependency with: pip install -e ".[deepseek]"'
                ) from exc
            client = OpenAI(api_key=api_key, base_url=base_url, timeout=timeout)
        self.client = client
        self.base_url = base_url
        self.model = model
        self.thinking = thinking
        self.reasoning_effort = reasoning_effort
        self.initial_tool_choice = initial_tool_choice
        self.max_tokens = max_tokens

    @classmethod
    def from_env(cls) -> DeepSeekChatAdapter:
        key = os.environ.get("DEEPSEEK_API_KEY", "")
        thinking_value = os.environ.get("DEEPSEEK_THINKING", "enabled").strip().lower()
        if thinking_value not in {"enabled", "disabled"}:
            raise DeepSeekConfigurationError(
                "DEEPSEEK_THINKING must be enabled or disabled"
            )
        return cls(
            api_key=key,
            base_url=os.environ.get("DEEPSEEK_BASE_URL", DEFAULT_BASE_URL),
            model=os.environ.get("DEEPSEEK_MODEL", DEFAULT_MODEL),
            thinking=thinking_value == "enabled",
            reasoning_effort=os.environ.get("DEEPSEEK_REASONING_EFFORT", "high"),
            initial_tool_choice=os.environ.get("DEEPSEEK_INITIAL_TOOL_CHOICE", "auto"),
            max_tokens=int(os.environ.get("DEEPSEEK_MAX_TOKENS", "512")),
        )

    def complete(
        self,
        messages: Sequence[dict[str, Any]],
        tools: Sequence[dict[str, Any]],
    ) -> ModelTurn:
        request: dict[str, Any] = {
            "model": self.model,
            "messages": _provider_messages(messages, include_reasoning=bool(tools)),
            "max_tokens": self.max_tokens,
            "extra_body": {
                "thinking": {"type": "enabled" if self.thinking else "disabled"}
            },
        }
        if self.thinking:
            request["reasoning_effort"] = self.reasoning_effort
        if tools:
            request["tools"] = _provider_tools(tools)
            request["tool_choice"] = (
                "auto"
                if any(message.get("role") == "tool" for message in messages)
                else self.initial_tool_choice
            )

        response = self.client.chat.completions.create(**request)
        if not getattr(response, "choices", None):
            raise DeepSeekProtocolError("DeepSeek returned no choices")
        choice = response.choices[0]
        message = choice.message
        normalized_calls: list[ToolCall] = []
        for raw_call in getattr(message, "tool_calls", None) or []:
            try:
                arguments = json.loads(raw_call.function.arguments)
            except (json.JSONDecodeError, TypeError) as exc:
                raise DeepSeekProtocolError(
                    f"invalid JSON arguments for tool {raw_call.function.name!r}"
                ) from exc
            if not isinstance(arguments, dict):
                raise DeepSeekProtocolError("tool arguments must decode to an object")
            normalized_calls.append(
                ToolCall(
                    id=raw_call.id,
                    name=raw_call.function.name,
                    arguments=arguments,
                )
            )

        return ModelTurn(
            content=getattr(message, "content", None),
            reasoning=getattr(message, "reasoning_content", None),
            tool_calls=tuple(normalized_calls),
            finish_reason=getattr(choice, "finish_reason", None) or "stop",
            usage=_usage_dict(getattr(response, "usage", None)),
        )
