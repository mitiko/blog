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
table th, table td { border: 1px solid silver; padding: 0.5rem; text-align: left; }
```

### Navigation vertical bars

```css
nav { display: grid; grid-template-columns: repeat(3, 1fr); padding: 1rem; }
nav > *:not(:last-child) { border-right: 1px solid silver; margin-right: 2rem; }
```
