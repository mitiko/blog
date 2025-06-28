# Reference

Not so common commands I often forget.

## CI/CD

<!-- Haven't configured a way to skip deployments with Cloudflare yet -->
`tf-apply` and `tf-destroy` in commit message run terraform.

## Latex

\mathcal{S} -> fancy symbols (by default capital letters are not fancy-fied)  
\mid -> conditional probability  
\quad -> spacing  
\qquad -> double space

## Markdown

```md
~~striketrough~~
<hr> = ---
[inline link](https://example.com "Title shows when hovered")
[reference link][1]
[1]: https://example.com "Title"
![images](/imgs/a.jpg "Descripton shows when hovered")
```

## Converting vscode theme (monaco) to textmate

I need to convert to textmate to be used by Zola.

```bash
cd themes
cp ~/.vscode/extensions/github.github-vscode-theme-6.3.5/themes/light-default.json github-light-default.json
./convert-to-tmtheme.py github-light-default.json
```
