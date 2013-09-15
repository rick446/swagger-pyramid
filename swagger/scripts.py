import sys
import json
import urllib
from contextlib import closing

from docopt import docopt

from .validators import generate_formencode_validators
from .models import generate_ming_models
from .routes import generate_routes
from .views import generate_views


def pgen():
    args = docopt("""Usage:
        swagger-pgen [options] <swagger-spec-url>

    Options:
        -h --help                 show this help message and exit
        -f --formencode           generate formencode validators
        -m --ming                 generate ming models
        -r --routes               generate route & view configs
        -v --views                generate view stubs
    """)
    with closing(urllib.urlopen(args['<swagger-spec-url>'])) as fp:
        spec = json.load(fp)
    if args['--formencode']:
        for line in generate_formencode_validators(spec['models']):
            sys.stdout.write(line + '\n')
    if args['--ming']:
        for line in generate_ming_models(spec['models']):
            sys.stdout.write(line + '\n')
    if args['--routes']:
        for line in generate_routes(spec['apis']):
            sys.stdout.write(line + '\n')
    if args['--views']:
        for line in generate_views(spec['apis']):
            sys.stdout.write(line + '\n')
