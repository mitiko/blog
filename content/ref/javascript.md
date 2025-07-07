+++
title = "Javascript"
date = 2024-10-18
aliases = ["/ref/js"]
+++

### Generate UUID

This is pretty hacker-ish, I love it, it's smart.
Found in the source code of [FM](https://explorer.futurememory.app/?viewer=small-matrix).

```js
function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        const r = Math.random() * 16 | 0, v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}
```

### Uncheck radio buttons

This is also pretty tricky with the `setTimeout`. Everyone on the web suggests
adding a "no choice" option but tbh I find this more intuitive.
TODO: test on mobile

```js
let $ = (selector) => document.querySelector(selector);

document.addEventListener("mouseup", (event) => {
    let node = event.target;
    if (node.tagName.toLowerCase() == "label") node = $("#" + node.attributes["for"].value);
    if (node.tagName.toLowerCase() != "input" || node.type != "radio") return;
    if (node.checked == true) setTimeout(() => { node.checked = false; }, 0);
});
```
