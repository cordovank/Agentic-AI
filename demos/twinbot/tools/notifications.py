import requests

def push_pushover(
    *,
    token: str | None,
    user: str | None,
    message: str,
    timeout_s: int = 5,
) -> bool:
    if not token or not user:
        return False
    try:
        requests.post(
            "https://api.pushover.net/1/messages.json",
            data={"token": token, "user": user, "message": message[:500]},
            timeout=timeout_s,
        )
        return True
    except requests.RequestException:
        return False
