import argparse

from aiohttp import web

from raven.handlers.status import status
from raven.middlewares.error_middleware import error_middleware


def parse_args():
    parser = argparse.ArgumentParser(description='Raven Service')

    parser.add_argument('-d', '--debug', action='store_true', help='debug mode')

    return parser.parse_args()


def main():
    args = parse_args()

    app = web.Application(middlewares=[error_middleware])

    app.add_routes([web.post('/status', status)])

    web.run_app(app)
