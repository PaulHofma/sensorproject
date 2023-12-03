var timestamps = [1700, 1750, 1800, 1850, 1900, 1950, 2000, 2050];
var temperatureData = [106, 106, 107, 111, 133, 221, 783, 2478];


var temperatureChartInput = {
    labels: timestamps,
    datasets: [
        {
            label: "Temperature",
            borderColor: "rgba(220,180,0,1)",
            pointColor: "rgba(220,180,0,1)",
            lineTension: 0,
            fill: false,
            data: temperatureData
        }
    ]
};
 
 
var populationChart;
 
document.addEventListener('DOMContentLoaded', function(event) {
    var context = document.getElementById('temp').getContext('2d');
    console.log(context);
    populationChart = new Chart(
        context,
        {
            type: 'line',
            data: temperatureChartInput,
        }
    ); 
}); 

function updateFunction(inputObj) {
    var chart = Chart.getChart('temp');
    console.log('updating: ', inputObj.tmp);
    console.log(temperatureData);
    var newTemp = inputObj.tmp;
    var newHmd = inputObj.hmd;
    var newTime = inputObj.timestamp;
    if(newTemp && newHmd && newTime) {
        chart.data.datasets[0].data.shift();
        chart.data.datasets[0].data.push(newTemp);
        chart.data.labels.shift();
        chart.data.labels.push(newTime);
    }
    chart.update();
}