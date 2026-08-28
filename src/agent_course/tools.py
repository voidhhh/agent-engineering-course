from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any


class ToolValidationError(ValueError):
    pass


JsonHandler = Callable[[dict[str, Any]], Any]


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    parameters: dict[str, Any]
    handler: JsonHandler = field(repr=False, compare=False)
    risk: str = "read"

    def model_schema(self) -> dict[str, Any]:
        return {
            "type": "function",
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }


def _type_matches(value: Any, expected: str) -> bool:
    mapping: dict[str, tuple[type, ...]] = {
        "string": (str,),
        "integer": (int,),
        "number": (int, float),
        "boolean": (bool,),
        "object": (dict,),
        "array": (list, tuple),
    }
    if expected not in mapping:
        return True
    if expected in {"integer", "number"} and isinstance(value, bool):
        return False
    return isinstance(value, mapping[expected])


def validate_arguments(schema: dict[str, Any], arguments: dict[str, Any]) -> None:
    """Validate the small JSON-Schema subset used in the offline course labs."""

    if not isinstance(arguments, dict):
        raise ToolValidationError("tool arguments must be an object")
    properties = schema.get("properties", {})
    for name in schema.get("required", []):
        if name not in arguments:
            raise ToolValidationError(f"missing required argument: {name}")
    if schema.get("additionalProperties") is False:
        unknown = set(arguments) - set(properties)
        if unknown:
            raise ToolValidationError(f"unknown arguments: {sorted(unknown)}")
    for name, value in arguments.items():
        expected = properties.get(name, {}).get("type")
        if expected and not _type_matches(value, expected):
            raise ToolValidationError(
                f"argument {name!r} must be {expected}, got {type(value).__name__}"
            )


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolSpec] = {}
        self._completed_calls: dict[str, Any] = {}

    def register(self, tool: ToolSpec) -> None:
        if tool.name in self._tools:
            raise ValueError(f"tool already registered: {tool.name}")
        self._tools[tool.name] = tool

    def get(self, name: str) -> ToolSpec:
        try:
            return self._tools[name]
        except KeyError as exc:
            raise KeyError(f"unknown tool: {name}") from exc

    def schemas(self) -> list[dict[str, Any]]:
        return [self._tools[name].model_schema() for name in sorted(self._tools)]

    def execute(self, call_id: str, name: str, arguments: dict[str, Any]) -> tuple[Any, bool]:
        """Execute once. The boolean reports whether a cached result was reused."""

        if call_id in self._completed_calls:
            return self._completed_calls[call_id], True
        tool = self.get(name)
        validate_arguments(tool.parameters, arguments)
        result = tool.handler(arguments)
        self._completed_calls[call_id] = result
        return result, False

    def clear_call_cache(self) -> None:
        self._completed_calls.clear()


class TaskStore:
    """Small deterministic domain store shared by examples and tests."""

    def __init__(self) -> None:
        self._tasks: dict[int, dict[str, Any]] = {}
        self._next_id = 1

    def add(self, title: str) -> dict[str, Any]:
        task = {"id": self._next_id, "title": title, "done": False}
        self._tasks[self._next_id] = task
        self._next_id += 1
        return dict(task)

    def list(self) -> list[dict[str, Any]]:
        return [dict(self._tasks[key]) for key in sorted(self._tasks)]


def build_course_tools(store: TaskStore | None = None) -> ToolRegistry:
    store = store or TaskStore()
    registry = ToolRegistry()
    registry.register(
        ToolSpec(
            name="add_numbers",
            description="Add two numbers. Use only for arithmetic addition.",
            parameters={
                "type": "object",
                "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
                "required": ["a", "b"],
                "additionalProperties": False,
            },
            handler=lambda args: args["a"] + args["b"],
        )
    )
    registry.register(
        ToolSpec(
            name="add_task",
            description="Create one local task and return its assigned id.",
            parameters={
                "type": "object",
                "properties": {"title": {"type": "string"}},
                "required": ["title"],
                "additionalProperties": False,
            },
            handler=lambda args: store.add(args["title"]),
            risk="write",
        )
    )
    registry.register(
        ToolSpec(
            name="list_tasks",
            description="List tasks stored by this local course session.",
            parameters={
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
            handler=lambda _args: store.list(),
        )
    )
    return registry
