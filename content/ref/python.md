+++
title = "Python"
date = 2024-02-02
aliases = ["/ref/py"]
+++

### Scripting (shebang + [uv](https://docs.astral.sh/uv/))

Install uv:
- using cargo: `cargo install --git https://github.com/astral-sh/uv uv`
- using brew: `brew install uv`
- using shell: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- windows: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

```bash
#!/usr/bin/env uv run --no-project --with toml
```

You may add as many `--with` as you'd like and specify the version as with requirements.txt.  
Update uv using `uv self update`.

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
