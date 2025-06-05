import enum


class NotificationType(str, enum.Enum):
    proxy_expiring = "proxy_expiring"
    balance_low = "balance_low"
