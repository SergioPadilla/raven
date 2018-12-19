from aiohttp import ClientSession


class RedisKeys:
    TO_PROCESS = 'to_process'
    FAILED = 'failed'
    PROCESSED = 'processed'


async def process_request(data):
    resp = None

    url = data.get('url')
    message = data.get('message')
    method = data.get('method')

    print('Requesting')
    print(f'url: {url}')
    print(f'message: {message}')
    print(f'method: {method.upper()}')

    async with ClientSession() as session:
        if method.upper() == 'GET':
            resp = await session.get(url=url, params=message)

        elif method.upper() == 'POST':
            resp = await session.post(url=url, json=message)

    print(f'Response: {resp}')
    return bool(resp and resp.status == 200)
