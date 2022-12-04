const g_data = document.getElementsByClassName("data");
const g_count = document.getElementsByClassName("count");
const g_ctx = document.querySelectorAll("pre > span.aux > span.ctx");
const g_sym = document.querySelectorAll("pre > span.aux > span.next");
const g_l1 = document.getElementsByClassName("l1");
const text = g_data[0].innerText;

const historyExample = (data, count, sym) => {
    let i = 0;

    setInterval(() => {
        let highlight = text.slice(0, i);
        let nextSym = text.slice(i, i+1);
        let rest = text.slice(i+1);
        data.innerHTML = `<span class="highlight">${highlight}</span><span class="next">${nextSym}</span>${rest}`
        count.innerText = i;
        sym.innerText = nextSym.replace("\n", "\\n");

        if (++i >= text.length) i = 0;
    }, 200);
};

const ctxExample = (data, count, ctx, sym) => {
    // let i = text.length >> 1;
    let i = 0;

    const func = () => {
        const history = text.slice(0, i);
        let highlight = history.slice(0, -2);
        let context = history.slice(-2);
        let nextSym = text.slice(i, i+1);
        let rest = text.slice(i+1);

        count.innerText = i;
        sym.innerText = nextSym.replace("\n", "\\n");
        ctx.innerText = context.replace("\n", "\\n");

        const regex = new RegExp(`${context}`, 'g');
        highlight = highlight.replace(regex, `<span class="ctx">${context}</span>`);
        data.innerHTML = `<span class="highlight">${highlight}</span><span class="ctx">${context}</span><span class="next">${nextSym}</span>${rest}`;

        // if (++i >= text.length) i = text.length >> 1;
        if (++i >= text.length) i = 0;
    };

    // func();
    setInterval(func, 400);
};

const l1Example = (data, count, ctx, sym) => {
    let l1 = document.getElementsByClassName("l1")[0];
    // let i = text.length >> 1;
    let i = 0;

    const func = () => {
        const history = text.slice(0, i);
        let highlight = history.slice(0, -2);
        let context = history.slice(-2);
        let nextSym = text.slice(i, i+1);
        let rest = text.slice(i+1);

        count.innerText = i;
        sym.innerText = nextSym.replace("\n", "\\n");
        ctx.innerText = context.replace("\n", "\\n");

        let regex = new RegExp(`${context}(.)`, 'g');
        highlight = highlight.replace(regex, `<span class="ctx">${context}</span><span class="l1">$1</span>`);
        data.innerHTML = `<span class="highlight">${highlight}</span><span class="ctx">${context}</span><span class="next">${nextSym}</span>${rest}`;

        regex = new RegExp(`(?=${context}(.))`, 'g')
        l1.innerText = Array.from(history.matchAll(regex))
            .map(x => x[1])
            .join("")
            .replace("\n", "\\n");

            // if (++i >= text.length) i = text.length >> 1;
            if (++i >= text.length) i = 0;
    };

    // func();
    setInterval(func, 100);
};

historyExample(g_data[0], g_count[0], g_sym[0]);
ctxExample(g_data[1], g_count[1], g_ctx[0], g_sym[1]);
l1Example(g_data[2], g_count[2], g_ctx[1], g_sym[2], g_l1[0]);
