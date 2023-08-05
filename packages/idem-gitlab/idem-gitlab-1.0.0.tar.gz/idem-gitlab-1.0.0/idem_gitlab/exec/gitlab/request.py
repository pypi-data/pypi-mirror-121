import re
from typing import Any
from typing import Dict
from typing import List


LINK = re.compile(r"<(.*)>")


async def paginate(hub, ctx, url: str) -> List[Dict[str, Any]]:
    """
    Paginate items from the given gitlab url
    :param hub:
    :param ctx:
    :param url:
    :return:
    """
    while url:
        ret = await hub.exec.request.json.get(
            ctx,
            url=url,
            params={"per_page": 100, "pagination": "keyset"},
            success_codes=[200],
        )
        if not ret["status"]:
            return
        for result in ret["ret"]:
            yield result
        url = LINK.match(ret["headers"].get("Link", "")).group(1)
