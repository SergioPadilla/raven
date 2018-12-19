import argparse

from aiohttp import web

from raven.handlers.register import register
from raven.handlers.status import status
from raven.middlewares.error_middleware import error_middleware
from raven.tasks.redis_tasks import process_requests, close_redis, init_redis


async def start_background_tasks(app):
    await init_redis(app)
    app['redis_listener'] = app.loop.create_task(process_requests(app))


async def cleanup_background_tasks(app):
    await close_redis(app)
    app['redis_listener'].cancel()
    await app['redis_listener']


def parse_args():
    parser = argparse.ArgumentParser(description='Raven Service')

    parser.add_argument('-d', '--debug', action='store_true', help='debug mode')

    return parser.parse_args()


def main():
    args = parse_args()

    app = web.Application(debug=True)
    routes = [web.route('*', '/status', status), web.post('/register', register)]

    app.add_routes(routes)

    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)

    web.run_app(app)


if __name__ == '__main__':
    main()
