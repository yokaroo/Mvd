// Section 1: Sunburst Chart (COICOP)
fetch('../../data/food_expenditure_by_category.json')
    .then(response => response.json())
    .then(data => {
        // Dummy: treat all as root category, for real COICOP add subcategory property in JSON
        const labels = data.map(d => d.Category);
        const parents = Array(data.length).fill("");
        const values = data.map(d => d.Share);
        const sunburstData = [{
            type: 'sunburst',
            labels: labels,
            parents: parents,
            values: values,
            branchvalues: 'total',
            hovertemplate: '<b>%{label}</b><br>Share: %{value}%<extra></extra>',
            marker: {colors: [
                '#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd','#8c564b','#e377c2','#7f7f7f','#bcbd22','#17becf',
                '#f44336','#4caf50','#2196f3','#ffeb3b','#ff9800','#9c27b0','#00bcd4','#8bc34a','#ffc107','#e91e63']}
        }];
        Plotly.newPlot('sunburst-chart', sunburstData, {
            title: 'Food Expenditure by Category (COICOP)',
            width: 420,
            height: 420,
            margin: {t: 60, b: 20, l: 20, r: 20},
        }, {responsive: true});
    });

// Section 2: Diverging Bar Chart (dummy data, adjust as needed)
const foodSecurity = [
    {region: 'Urban', sufficient: 120, insufficient: -30},
    {region: 'Rural', sufficient: 80, insufficient: -50}
];
const traceSufficient = {
    x: foodSecurity.map(d => d.sufficient),
    y: foodSecurity.map(d => d.region),
    name: 'Sufficient',
    orientation: 'h',
    type: 'bar',
    marker: {color: '#43a047'},
    hovertemplate: 'Sufficient: %{x}<extra></extra>'
};
const traceInsufficient = {
    x: foodSecurity.map(d => d.insufficient),
    y: foodSecurity.map(d => d.region),
    name: 'Insufficient',
    orientation: 'h',
    type: 'bar',
    marker: {color: '#e53935'},
    hovertemplate: 'Insufficient: %{x}<extra></extra>'
};
Plotly.newPlot('nutrient-bar-chart', [traceInsufficient, traceSufficient], {
    barmode: 'relative',
    title: 'Household Food Security (Sufficient vs. Insufficient)',
    width: 420,
    height: 350,
    margin: {t: 60, b: 40, l: 60, r: 20},
    legend: {orientation: 'h', x: 0.3, y: 1.1}
}, {responsive: true});

// Section 3: Donut Chart (Food Source)
fetch('../../data/food_source_distribution.json')
    .then(response => response.json())
    .then(data => {
        const labels = data.map(d => d.Source);
        const values = data.map(d => d.Share);
        const donutData = [{
            labels: labels,
            values: values,
            type: 'pie',
            hole: .5,
            marker: {colors: ['#ff9800','#43a047','#2196f3','#e91e63']},
            hovertemplate: '<b>%{label}</b><br>%{percent:.1%} (%{value})<extra></extra>',
            textinfo: 'percent+label',
            textposition: 'inside',
        }];
        Plotly.newPlot('food-source-donut', donutData, {
            title: 'Food Consumption by Source',
            width: 420,
            height: 350,
            margin: {t: 60, b: 20, l: 20, r: 20},
            showlegend: true
        }, {responsive: true});
    });

// Section 4: Bar Chart (Welfare Indicators by Region)
// Dummy data, adjust with your real data if available
const welfareIndicators = {
    indicators: ['Food Expenditure', 'Calorie Intake', 'Protein Intake'],
    Urban: [11.57, 1353, 78.6],
    Rural: [11.79, 1353, 78.6]
};
const barData = [
    {
        x: welfareIndicators.indicators,
        y: welfareIndicators.Urban,
        name: 'Urban',
        type: 'bar',
        marker: {color: '#2196f3'}
    },
    {
        x: welfareIndicators.indicators,
        y: welfareIndicators.Rural,
        name: 'Rural',
        type: 'bar',
        marker: {color: '#e53935'}
    }
];
Plotly.newPlot('regional-bar-chart', barData, {
    barmode: 'group',
    title: 'Welfare Indicators by Region',
    width: 420,
    height: 350,
    xaxis: {title: 'Indicator'},
    yaxis: {title: 'Value'},
    margin: {t: 60, b: 40, l: 60, r: 20},
    legend: {orientation: 'h', x: 0.3, y: 1.1}
}, {responsive: true});
