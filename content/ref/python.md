+++
title = "Python"
date = 2024-02-02
extra.exclude_meta = true
+++

<!-- tricks -->

### Absolute directory path

```py
import os
__directory = os.path.dirname(__file__)
os.path.join(__directory, '../')
```

### Reverse string

```py
rev = 'abcdef'[::-1]
```

## Jinja

### Minimal Jinja setup

```py
import jinja2

template = jinja2.Template(open('template.jinja').read())
obj = {
    'name': 'My Template',
    'property': [0, 1, 2],
}
payload = tempalte.render(obj)
```
