+++
title = "Python"
date = 2024-02-02
extra.exclude_meta = true
+++

<!-- tricks -->

### Absolute directory path

```py
import os

if __name__ == '__main__':
    __directory = os.path.dirname(__file__)
    relative_path = os.path.join(__directory, '../parent/../../grandparent')
    assert isinstance(relative_path, str)
```

### Reverse string

```py
a = 'abcdef'
b = a[::-1]
assert b == 'fedcba'
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
