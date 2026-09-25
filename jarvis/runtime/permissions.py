from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum


class PermissionLevel(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass(frozen=True)
class PermissionDecision:
    allowed: bool
    reason: str
    requires_confirmation: bool = False
    requires_authentication: bool = False


class PermissionBroker:
    """Central policy gate. The model cannot alter this policy."""

    def __init__(self, max_level: PermissionLevel = PermissionLevel.MEDIUM) -> None:
        self.max_level = max_level

    def decide(
        self,
        level: PermissionLevel,
        *,
        confirmed: bool = False,
        authenticated: bool = False,
    ) -> PermissionDecision:
        if level > self.max_level:
            return PermissionDecision(False, "Permission level exceeds configured policy")
        if level == PermissionLevel.CRITICAL and not authenticated:
            return PermissionDecision(False, "Authentication required", requires_authentication=True)
        if level >= PermissionLevel.HIGH and not confirmed:
            return PermissionDecision(False, "Explicit confirmation required", requires_confirmation=True)
        return PermissionDecision(True, "Allowed")
