from formencode import validators as fev
from dateutil import parser


class DateTime(fev.FancyValidator):

    def _to_python(self, value, state=None):
        return parser.parse(value)

    def _from_python(self, value, state=None):
        return value.isoformat()


class Object(fev.FancyValidator):
    '''Basic do-nothing validator'''

    def _to_python(self, value, state=None):
        return value

    def _from_python(self, value, state=None):
        return value


def order_models(models):
    '''Yields the models in order so $refs are always defined before being
    used'''
    yielded = set([
        'string',
        'boolean',
        'integer',
        'array',
        'date-time',
        'object'
    ])

    model_deps = {}
    for key, model in models.items():
        assert model['id'] == key, 'Model name/id mismatch: %s != %s' % (
            model['id'], key)
        model_deps[key] = set(model_depends(model))

    while model_deps:
        len_yielded = len(yielded)
        for key, deps in model_deps.items():
            if not deps - yielded:
                yielded.add(key)
                yield models[key]
                model_deps.pop(key)
        if len(yielded) == len_yielded:
            import ipdb; ipdb.set_trace();
        assert len(yielded) > len_yielded, \
            "Can't make forward progress; deps are %s" % model_deps


def model_depends(model):
    for k, v in model.items():
        if k == '$ref':
            yield v
        elif k == 'type':
            yield v
        elif isinstance(v, dict):
            for dep in model_depends(v):
                yield dep
