# Server-driven notifications

The bot exposes a lightweight HTTP endpoint that allows the backend to push
notifications directly to a Telegram user. The web server is started together
with the bot (`start_webserver` in `main.py`) and listens on port `8081` by
default.

## Authentication

Every request must include an `X-API-Key` header. The value is compared against
`INTERNAL_API_TOKEN` from the environment. Requests without a valid key are
rejected with `401 Unauthorized`.

## Endpoint

```
POST /notify
Content-Type: application/json
X-API-Key: <internal api token>
```

### Payload schema

```json
{
  "telegram_id": 123456789,
  "data": {
    "language": "ru",
    "type": "proxy_expiring",
    "message": "<optional custom text>",
    "host": "<optional proxy host>",
    "...": "<any additional fields are preserved>"
  }
}
```

* `telegram_id` — chat id that will receive the message.
* `language` — two-letter locale code. Defaults to `ru` when omitted.
* `type` — one of the supported notification identifiers from
  `enums/notification_type.py`.
* `message` — optional custom text. If absent, the server falls back to the
  localized template stored in `data/locales.py`.
* `host` — optional proxy label for `proxy_expiring` notifications.

### Response

Successful deliveries return:

```json
{"success": true}
```

Validation errors (missing fields, unsupported type, invalid JSON) are reported
with HTTP 400 and a description inside the `error` field.

Failures to send a Telegram message return HTTP 500 with the exception message.

## Adding new notification types

1. Extend `NotificationType` with a new enum value.
2. Add localized templates into `data/locales.py` using the
   `notification_<type>` naming convention.
3. Update `_build_notification_text` in `webserver.py` if the new payload needs
   additional formatting rules.
4. Cover the behaviour with a unit test in `tests/test_webserver_notifications.py`.

This workflow keeps the webhook contract explicit and prevents regressions for
future notification types.
