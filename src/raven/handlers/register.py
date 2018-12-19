import json

from aiohttp import web
from marshmallow import Schema, fields

from raven.handlers.redis import RedisKeys


class DataSchema(Schema):
    url = fields.Str(required=True)
    method = fields.Str(required=True)
    message = fields.Dict(required=True)


class RegisterSchema(Schema):
    channel = fields.Str(required=True)
    data = fields.Nested(DataSchema(), required=True)


async def register(request):
    response = {}
    status = 200

    body = await request.json()

    schema = RegisterSchema()
    errors = schema.validate(body)

    if not errors:
        if body.get('channel') == 'http':
            data = body.get('data')

            if data:
                print('Inserting data in redis')
                request.app['redis'].lpush(key=RedisKeys.TO_PROCESS, value=json.dumps(data))
                response = {'status': 'registered'}

        else:
            response = {'status': 'bad_request', 'errors': {'channel': 'channel not allowed'}}
            status = 400

    else:
        response = {'status': 'bad_request', 'errors': errors}
        status = 400

    return web.json_response(response, status=status)
