+++
title = "Python"
date = 2024-02-02
aliases = ["/ref/py"]
+++

<!-- tricks -->

### Absolute directory path

```py
import os

def r(relative_path: str):
    return os.path.join(os.path.dirname(__file__), relative_path)
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
