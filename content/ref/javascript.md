+++
title = "Javascript"
date = 2024-10-18
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