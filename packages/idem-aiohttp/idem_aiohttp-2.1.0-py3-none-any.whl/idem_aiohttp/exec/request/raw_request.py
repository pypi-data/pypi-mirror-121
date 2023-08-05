from typing import List

__virtualname__ = "raw"


async def delete(hub, ctx, url: str, success_codes: List[int] = None, **kwargs):
    if not success_codes:
        success_codes = [200]
    async with await hub.tool.request.session.delete(
        ctx, url=url, **kwargs
    ) as response:
        return {
            "ret": await response.read(),
            "status": response.status in success_codes,
            "comment": response.reason,
        }


async def get(hub, ctx, url: str, success_codes: List[int] = None, **kwargs):
    if not success_codes:
        success_codes = [200]
    async with await hub.tool.request.session.get(ctx, url=url, **kwargs) as response:
        return {
            "ret": await response.read(),
            "status": response.status in success_codes,
            "comment": response.reason,
        }


async def patch(hub, ctx, url: str, success_codes: List[int] = None, **kwargs):
    if not success_codes:
        success_codes = [200]
    async with await hub.tool.request.session.patch(ctx, url=url, **kwargs) as response:
        return {
            "ret": await response.read(),
            "status": response.status in success_codes,
            "comment": response.reason,
        }


async def post(hub, ctx, url: str, success_codes: List[int] = None, **kwargs):
    if not success_codes:
        success_codes = [200]
    async with await hub.tool.request.session.post(ctx, url=url, **kwargs) as response:
        return {
            "ret": await response.read(),
            "status": response.status in success_codes,
            "comment": response.reason,
        }


async def put(hub, ctx, url: str, success_codes: List[int] = None, **kwargs):
    if not success_codes:
        success_codes = [200]
    async with await hub.tool.request.session.put(ctx, url=url, **kwargs) as response:
        return {
            "ret": await response.read(),
            "status": response.status in success_codes,
            "comment": response.reason,
        }
