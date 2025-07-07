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

    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.5rem;
}

section#gradeCharts > div.chart {
    border: 1px solid silver;
    border-radius: 0.4rem;
    padding: 0.4rem;
}

div.chart > div.bar {
    width: 10%;
    height: 3rem;
}

div.bar:nth-child(1) { background-color: limegreen; }
div.bar:nth-child(2) { background-color: gold; }
div.bar:nth-child(3) { background-color: red; }

div.chart:nth-child(1) > div.bar:nth-child(1) { width: 3%; }
div.chart:nth-child(1) > div.bar:nth-child(2) { width: 3%; }
div.chart:nth-child(1) > div.bar:nth-child(3) { width: 95%; }
div.chart:nth-child(2) > div.bar:nth-child(1) { width: 40%; }
div.chart:nth-child(2) > div.bar:nth-child(2) { width: 20%; }
div.chart:nth-child(2) > div.bar:nth-child(3) { width: 40%; }
div.chart:nth-child(3) > div.bar:nth-child(1) { width: 84%; }
div.chart:nth-child(3) > div.bar:nth-child(2) { width: 6%; }
div.chart:nth-child(3) > div.bar:nth-child(3) { width: 10%; }
div.chart:nth-child(4) > div.bar:nth-child(1) { width: 86%; }
div.chart:nth-child(4) > div.bar:nth-child(2) { width: 6%; }
div.chart:nth-child(4) > div.bar:nth-child(3) { width: 8%; }
</style>

<section id="gradeCharts">
<div class="chart">
    <div class="bar"></div>
    <div class="bar"></div>
    <div class="bar"></div>
</div>
<div class="chart">
    <div class="bar"></div>
    <div class="bar"></div>
    <div class="bar"></div>
</div>
<div class="chart">
    <div class="bar"></div>
    <div class="bar"></div>
    <div class="bar"></div>
</div>
<div class="chart">
    <div class="bar"></div>
    <div class="bar"></div>
    <div class="bar"></div>
</div>
</section>

<br><br><br>

<script src="../range-slider.js"></script>

<div id="slider"></div>

<script>
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
    values: [10, 20, 26],
    min: 6,
    max: 31,
    tooltipHandler: gradeIndexToDifficulty,
};
let slider = new RangeSlider('div#slider', sliderOptions);
slider.onChange(values => {
    values.sort();
    console.log(values);
});
</script>
