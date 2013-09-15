def generate_views(apis):
    for api in apis:
        for operation in api['operations']:
            yield 'def %s(request):' % operation['nickname']
            yield '    """%s"""' % operation['summary']
            yield '    return {}'
            yield ''
            yield ''

