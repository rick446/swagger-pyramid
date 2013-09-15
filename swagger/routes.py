def generate_routes(apis):
    yield PREAMBLE_ROUTES
    for api in apis:
        yield '    config.add_route(%r, %r)' % (api['name'], api['path'])

    yield PREAMBLE_VIEWS
    for api in apis:
        for operation in api['operations']:
            args = dict(route_name=api['name'], request_method=operation['method'])
            args = ', '.join('%s=%r' % (k, v) for k, v in args.items())
            yield '    config.add_view(getattr(views, %r), %s)' % (
                operation['nickname'], args)


PREAMBLE_ROUTES = '''
def add_routes(config):'''

PREAMBLE_VIEWS = '''
def add_views(config, views):'''
