import enum


class NotificationType(str, enum.Enum):
    proxy_expiring = "proxy_expiring"
    proxy_expired = "proxy_expired"
    proxy_auto_prolong_success = "proxy_auto_prolong_success"
    proxy_auto_prolong_failed = "proxy_auto_prolong_failed"
    balance_low = "balance_low"
    admin_alert = "admin_alert"
