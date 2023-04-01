# Reference

Not so common commands I often forget.

## CI/CD


`[skip netlify]` in commit message doesn't trigger deployment.  
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

## Workflow

Formatting music pages:
```
find: ([^\s])\n(.)
replace: $1  \n$2
span + br hack -> <p><br></p>
```

