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
