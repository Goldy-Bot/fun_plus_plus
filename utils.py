from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from GoldyBot import Goldy

async def uwuify_string(string: str, goldy: Goldy) -> str:
    """UwUifies text."""
    r = await goldy.http_client._session.post(
        "https://nameless-frog-4917.zeeraa.net/Englishtouwu/translate",
        data = string
    )
    data = await r.json()
    return data["result"]