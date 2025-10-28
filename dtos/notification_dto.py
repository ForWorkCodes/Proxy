from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional

from enums.notification_type import NotificationType


@dataclass(slots=True)
class NotificationData:
    """Payload of a notification that should be delivered to the user."""

    language: str
    type: NotificationType
    message: Optional[str] = None
    host: Optional[str] = None
    extras: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> "NotificationData":
        if not isinstance(raw, Mapping):
            raise ValueError("Notification payload must be a mapping")

        try:
            notification_type = NotificationType(raw["type"])
        except KeyError as exc:
            raise ValueError("Notification type is required") from exc
        except ValueError as exc:
            raise ValueError("Unsupported notification type") from exc

        language = str(raw.get("language", "")).strip() or "ru"
        message = raw.get("message") or raw.get("text")
        message = message.strip() if isinstance(message, str) else None

        host = raw.get("host")
        host = host.strip() if isinstance(host, str) else None

        extras = {
            key: value
            for key, value in raw.items()
            if key not in {"type", "language", "message", "text", "host"}
        }

        return cls(language=language, type=notification_type, message=message, host=host, extras=dict(extras))


@dataclass(slots=True)
class IncomingNotification:
    telegram_id: int
    payload: NotificationData

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> "IncomingNotification":
        if not isinstance(raw, Mapping):
            raise ValueError("Incoming data must be a mapping")

        if "telegram_id" not in raw:
            raise ValueError("telegram_id is required")

        telegram_id = raw["telegram_id"]
        try:
            telegram_id = int(telegram_id)
        except (TypeError, ValueError) as exc:
            raise ValueError("telegram_id must be an integer") from exc

        payload_raw = raw.get("data") or raw.get("payload")
        if payload_raw is None:
            raise ValueError("Notification payload is required")

        payload = NotificationData.from_mapping(payload_raw)
        return cls(telegram_id=telegram_id, payload=payload)
