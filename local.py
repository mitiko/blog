#!/usr/bin/env uv run --no-project --with toml

import toml
import os
import shutil

def r(relative_path: str):
    return os.path.join(os.path.dirname(__file__), relative_path)

config = toml.loads(open(r('config.toml')).read())

config['extra']['favicon_url'] = '/local_favicon.png'

if not os.path.exists('/tmp/blog'):
    os.mkdir('/tmp/blog')

open('/tmp/blog/config.toml', 'w').write(toml.dumps(config))
shutil.copytree(r('themes'), "/tmp/blog/themes", dirs_exist_ok=True)

os.system('zola --config /tmp/blog/config.toml serve --drafts -i 127.0.0.1 -p 1111')
