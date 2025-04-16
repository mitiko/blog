+++
title = "CSS"
date = 2024-11-22
+++

### Main layout

```css
main { max-width: 70ch; margin-inline: auto; }
```

### Sticky footer

```css
body { display: grid; grid-template-rows: auto 1fr auto; }
/* body: header, main, footer */
```

### Tables

```css
table { border: 1px solid silver; border-collapse: collapse; }
table th { background-color: #ddd; }
table th, table td { border: 1px solid silver; padding: 0.5rem; text-align: left; }
```

### Table border

Do not use `border-collapse: collapse;`. Instead set `border-spacing: 0;` & build the collapse yourself:

```css
table { --b: 1px; --r: 6px; }
table { border: var(--b) solid silver; border-spacing: 0; border-radius: var(--r); }
table th { background-color: #ddd; }
table th, table td { padding: 0.5rem; text-align: left; }
th:first-child { border-top-left-radius: calc(var(--r) - var(--b)); }
th:last-child { border-top-right-radius: calc(var(--r) - var(--b)); }
th:not(:last-child), td:not(:last-child) { border-right: var(--b) solid silver; }
th, tr:not(:last-child) > td { border-bottom: var(--b) solid silver; }
```

TODO: since the border gets stacked now, it's actually 2px instead of 1px
(as with border-collapse). Try setting `var(--b)` to 0.5px?

### Navigation vertical bars

```css
nav { display: grid; grid-template-columns: repeat(3, 1fr); padding: 1rem; }
nav > *:not(:last-child) { border-right: 1px solid silver; margin-right: 2rem; }
```
