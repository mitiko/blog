+++
date = 2025-04-28
title = "mitiko.oats instagram <i>deluxe</i>"
aliases = ["/oats/insta"]
+++

<style>
form {
    border: 1px solid rgba(0,0,0,.15);
    border-radius: 6px;
    padding: 1rem;
}
fieldset {
    border-radius: 6px;
    border: 1px solid rgba(0,0,0,.15);
}
fieldset + fieldset { margin-top: 1rem; }
fieldset > legend { /* color: rgba(0,0,0,.3); */ }
fieldset > p {
    margin-block: 0.5rem;
}
</style>

<form onsubmit="event.preventDefault(); handleSubmit(event);">
    <p>
        <label for="summary">Summary:</label>
        <input type="text" id="summary" />
    </p>
    <fieldset id="base">
        <legend>Base</legend>
        <p>
            <input type="radio" name="base" id="yoghurt" value="yoghurt" />
            <label for="yoghurt">Yoghurt</label>
        </p>
        <p>
            <input type="radio" name="base" id="almond-milk" value="almond-milk" />
            <label for="almond-milk">Almond Milk</label>
        </p>
        <p>
            <input type="radio" name="base" id="oat-milk" value="oat-milk" />
            <label for="oat-milk">Oat Milk</label>
        </p>
        <p>
            <input type="radio" name="base" id="coconut-milk" value="coconut-milk" />
            <label for="coconut-milk">Coconut Milk</label>
        </p>
    </fieldset>
    <fieldset id="fruits">
        <legend>Fruits</legend>
        <p>
            <input type="checkbox" id="banana" />
            <label for="banana">Banana</label>
        </p>
        <p>
            <input type="checkbox" id="apple" />
            <label for="apple">Apple</label>
            <!-- green or red apple -->
        </p>
        <p>
            <input type="checkbox" id="pear" />
            <label for="pear">Pear</label>
        </p>
        <p>
            <input type="checkbox" id="blueberries" />
            <label for="blueberries">Blueberries</label>
        </p>
    </fieldset>
    <fieldset id="nuts">
        <legend>Nuts</legend>
        <p>
            <input type="checkbox" id="chia" />
            <label for="chia">Chia</label>
        </p>
        <p>
            <input type="checkbox" id="almond-flakes" />
            <label for="almond-flakes">Almond Flakes</label>
        </p>
        <p>
            <input type="checkbox" id="cocoa-nibs" />
            <label for="cocoa-nibs">Cocoa Nibs</label>
        </p>
    </fieldset>
    <fieldset id="hashtags">
        <legend>Hashtags</legend>
        <!-- TODO: CSS Grid of checkboxes -->
        <p>
            <input type="checkbox" id="hashtag-1" />
            <label for="hashtag-1">#oatlicious</label>
        </p>
        <p>
            <input type="checkbox" id="hashtag-2" />
            <label for="hashtag-2">#oatsforbreakfast</label>
        </p>
        <p>
            <input type="checkbox" id="hashtag-3" />
            <label for="hashtag-3">#breakfastoats</label>
        </p>
        <!-- TODO: add new checkbox entry & save it to local storage? -->
    </fieldset>
    <br>
    <input type="submit">
</form>

### Output:

<pre id="output-box">
🥣 80g oats & 300g yoghurt
🍌 1/2 banana
🍏 1/2 apple
🫐 blueberries
🌰 chia
🌰 almond butter
🧡 cinnamon
</pre>

<script>
let $ = (selector) => document.querySelector(selector);

document.addEventListener("mouseup", (event) => {
    let node = event.target;
    if (node.tagName.toLowerCase() == "label") node = $("#" + node.attributes["for"].value);
    if (node.tagName.toLowerCase() != "input" || node.type != "radio") return;
    if (node.checked == true) setTimeout(() => { node.checked = false; }, 0);
});

// maps input id to emoji
let inputMap = {
    "banana": "🍌",
    "apple": "🍏",
    "blueberry": "🫐",
    "chia": "🌰",
};

// maps quantity value to symbol
let quantityMap = {
    "half": "1/2",
    "three-quarters": "3/4",
    "spoonful": "spoonful",
}

let handleSubmit = (event) => {
    window.s_event = event;
    console.log(event);
    let result = "";
    Array.from(event.target.querySelectorAll("input")).forEach(input => {
        if ((input.type == "radio" || input.type == "checkbox") && input.checked == true) {
            let symbol = inputMap[input.id];
            result += `${symbol} ${input.id}\n`;
        }
    });

    $("pre#output-box").innerText = result;
};
</script>

