from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from .models import ToolCall
from .tools import ToolSpec


class ApprovalDecision(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    REQUIRE_APPROVAL = "require_approval"


@dataclass
class StaticApprovalPolicy:
    """A deliberately small policy used to teach policy/approval separation."""

    denied_tools: set[str] = field(default_factory=set)
    approval_risks: set[str] = field(default_factory=lambda: {"write", "execute"})

    def decide(self, call: ToolCall, tool: ToolSpec) -> ApprovalDecision:
        if call.name in self.denied_tools:
            return ApprovalDecision.DENY
        if tool.risk in self.approval_risks:
            return ApprovalDecision.REQUIRE_APPROVAL
        return ApprovalDecision.ALLOW
