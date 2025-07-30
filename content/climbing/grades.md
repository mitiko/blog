+++
title = "Категориите в катеренето"
date = 2024-05-31

[extra]
subtitle = "Субективна мярка и гориво за егото"
exclude_meta = true
+++

Статия.

<style>
section#gradeCharts {
    width: 100%;
    border: 1px solid silver;
    border-radius: 0.5rem;
    padding: 0.5rem;
    font-family: monospace;

    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.5rem;
}

div.chart > p { margin-bottom: 0; text-align: center; color: gray; }
div.chart > table { width: 100%; }

div.chart tr:nth-child(1) > td:nth-child(2) > div { background-color: limegreen; }
div.chart tr:nth-child(2) > td:nth-child(2) > div { background-color: gold; }
div.chart tr:nth-child(3) > td:nth-child(2) > div { background-color: red; }
</style>

<section id="gradeCharts">
    <div class="chart">
        <div class="row"><span class="barValue">10</span><div class="bar"></div></div>
        <div class="row"><span class="barValue">10</span><div class="bar"></div></div>
        <div class="row"><span class="barValue">10</span><div class="bar"></div></div>
        <p>Warmup</p>
    </div>
    <div class="chart">
        <table>
            <tr><td>10</td><td><div></div></td></tr>
            <tr><td>10</td><td><div></div></td></tr>
            <tr><td>10</td><td><div></div></td></tr>
        </table>
        <p>Easy</p>
    </div>
    <div class="chart">
        <table>
            <tr><td>10</td><td><div></div></td></tr>
            <tr><td>10</td><td><div></div></td></tr>
            <tr><td>10</td><td><div></div></td></tr>
        </table>
        <p>Medium</p>
    </div>
    <div class="chart">
        <table>
            <tr><td>10</td><td><div></div></td></tr>
            <tr><td>10</td><td><div></div></td></tr>
            <tr><td>10</td><td><div></div></td></tr>
        </table>
        <p>Hard</p>
    </div>
</section>

<br><br><br>

<script src="../range-slider.js"></script>

<div id="slider"></div>

<script>
let data = {
    31: [0,  0,  1],
    30: [0,  0,  4],
    29: [0,  0, 11],
    28: [0,  0,  9],
    27: [1,  1, 10],
    26: [2,  5, 14],
    25: [17, 3, 11],
    24: [5,  5,  7],
    23: [9,  3,  1],
    22: [5,  0,  1],
    21: [7,  0,  2],
    19: [6,  0,  2],
    18: [6,  0,  0],
    17: [6,  1,  0],
    16: [13, 2,  0],
    14: [11, 2,  0],
    12: [10, 0,  2],
    9:  [8,  0,  1],
    7:  [1,  0,  0],
    6:  [1,  0,  0],
};
let gradeIndexToDifficulty = (gradeIndex) => {
    switch (gradeIndex) {
        case 6: return "4a";
        case 7: return "4b";
        case 8: return "4c";
        case 9: case "10":
        case 11: return "5a";
        case 12:
        case 13: return "5b";
        case 14:
        case 15: return "5c";
        case 16: return "6a";
        case 17: return "6a+";
        case 18: return "6b";
        case 19: return "6b+";
        case 20:
        case 21: return "6c";
        case 22: return "6c+";
        case 23: return "7a";
        case 24: return "7a+";
        case 25: return "7b";
        case 26: return "7b+";
        case 27: return "7c";
        case 28: return "7c+";
        case 29: return "8a";
        case 30: return "8a+";
        case 31: return "8b";
    }
    return gradeIndex;
};
let sliderOptions = {
    pointRadius: 10,
    values: [16, 22, 26],
    min: 6,
    max: 31,
    tooltipHandler: gradeIndexToDifficulty,
};
let slider = new RangeSlider('div#slider', sliderOptions);
let setWidths = (values) => {
    let breakpoints = [...values, sliderOptions.min, sliderOptions.max];
    breakpoints.sort((a, b) => a - b);

    for (let rangeIndex = 0; rangeIndex < breakpoints.length - 1; rangeIndex++) {
        let barValues = [0, 0, 0];
        for (let grade = breakpoints[rangeIndex]; grade <= breakpoints[rangeIndex + 1]; grade++) {
            let gradeTries = data[grade] || [0, 0, 0];
            barValues[0] += gradeTries[0];
            barValues[1] += gradeTries[1];
            barValues[2] += gradeTries[2];
        }
        let barValuesSum = barValues[0] + barValues[1] + barValues[2];
        let barWidths = [
            Math.round(100 * barValues[0] / barValuesSum),
            Math.round(100 * barValues[1] / barValuesSum),
            Math.round(100 * barValues[2] / barValuesSum),
        ];

        let chart = document.querySelector(`div.chart:nth-child(${rangeIndex + 1})`);
        console.log(chart.querySelector('tr:nth-child(1) > td:nth-child(2)'));
        console.log(chart.querySelector('tr:nth-child(2) > td:nth-child(2)'));
        console.log(chart.querySelector('tr:nth-child(3) > td:nth-child(2)'));
        chart.querySelector('tr:nth-child(1) > td:nth-child(2) > div').style.width = `${barWidths[0]}%`;
        chart.querySelector('tr:nth-child(2) > td:nth-child(2) > div').style.width = `${barWidths[1]}%`;
        chart.querySelector('tr:nth-child(3) > td:nth-child(2) > div').style.width = `${barWidths[2]}%`;
    }
};
slider.onChange(setWidths);
setWidths(sliderOptions.values);
</script>
