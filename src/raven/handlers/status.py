from aiohttp import web


async def status(request):
    return web.json_response({'status': 'OK'})
