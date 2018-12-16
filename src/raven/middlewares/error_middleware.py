from aiohttp.web_middlewares import middleware


@middleware
async def error_middleware(request, handler):

    try:
        resp = await handler(request)

    except Exception as e:
        resp = {'status': 'KO', 'exception': type(e)}

    return resp
