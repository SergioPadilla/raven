import json
from asyncio import sleep
from pprint import pprint

from aioredis import create_redis, ConnectionForcedCloseError

from raven.handlers.redis import RedisKeys, process_request


async def init_redis(app):
    app['redis'] = await create_redis('redis://localhost/0')


async def close_redis(app):
    app['redis'].close()
    await app['redis'].wait_closed()


async def process_requests(app):
    run = True
    while run:
        try:
            data = await app['redis'].rpop(key=RedisKeys.TO_PROCESS)

            if data:
                try:
                    print(f'Data retrieved from redis queue: {data}')
                    data_json = json.loads(data)

                    print('Processing data')
                    pprint(data_json)
                    processed = await process_request(data_json)
                    if not processed:
                        await app['redis'].lpush(key=RedisKeys.FAILED, value=json.dumps(data))

                except Exception as e:
                    print(f'Data failed: {data}')
                    print(e)
                    await app['redis'].lpush(key=RedisKeys.FAILED, value=json.dumps(data))

            else:
                await sleep(1)

        except ConnectionForcedCloseError:
            run = False

    print('BACKGROUND TASK STOPPED')
