from aiohttp import web, ClientSession
from marshmallow import Schema, fields


class DataSchema(Schema):
    url = fields.Str()
    method = fields.Str()
    message = fields.Dict()


class RegisterSchema(Schema):
    channel = fields.Str()
    data = fields.Nested(DataSchema())


async def make_request(method, url, message):
    resp = None

    async with ClientSession() as session:
        if method.upper() == 'GET':
            resp = await session.get(url=url, params=message)

        elif method.upper() == 'POST':
            resp = await session.post(url=url, json=message)

    return resp


async def register(request):
    steps = []
    status = 200

    body = await request.json()

    schema = RegisterSchema()

    errors = schema.validate(body)
    if not errors:
        if body.get('channel') == 'http':
            data = body.get('data')
            url = data.get('url')
            message = data.get('message')
            method = data.get('method')

            resp = await make_request(method=method, url=url, message=message)
            steps.append({'status': 'sent'})

            if resp and resp.status == 200:
                steps.append({'status': 'notified'})
            else:
                steps.append({'status': 'failed'})

    else:
        steps = {'status': 'bad_request', 'errors': errors}
        status = 400

    return web.json_response({'status': steps}, status=status)
