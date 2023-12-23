var timestamps = [];
var dummyData = [];

var temperatureChartInput = {
    labels: timestamps,
    datasets: [
        {
            label: "Temperature",
            borderColor: "red",
            pointColor: "red",
            lineTension: 0,
            fill: false,
            data: dummyData
        }
    ]
};

var humidityChartInput = {
    labels: timestamps,
    datasets: [
        {
            label: "Humidity",
            borderColor: "blue",
            pointColor: "blue",
            lineTension: 0,
            fill: false,
            data: dummyData
        }
    ]
};

document.addEventListener('DOMContentLoaded', function(event) {
    var context = document.getElementById('temp').getContext('2d');
    var hmd_context = document.getElementById('hmd').getContext('2d');
    
    new Chart(
        hmd_context,
        {
            type: 'line',
            data: humidityChartInput,
            options: {
                scales: {
                    x: {
                        type: 'timeseries',
                        time: {
                            tooltipFormat: 'HH MM SS'
                        }
                    }
                }
            }
        }
    ); 
    
    new Chart(
        context,
        {
            type: 'line',
            data: temperatureChartInput,
            options: {
                scales: {
                    x: {
                        type: 'timeseries',
                        time: {
                            tooltipFormat: 'HH MM SS'
                        }
                    }
                }
            }
        }
    ); 
}); 

function updateFunction(inputObj) {
    var tempchart = Chart.getChart('temp');
    var hmdchart = Chart.getChart('hmd');

    var newTemp = inputObj.tmp;
    var newHmd = inputObj.hmd;
    var newTime = inputObj.timestamp;

    if(newTemp && newHmd && newTime) {
        tempchart.data.datasets[0].data = newTemp;
        tempchart.data.labels = newTime;
        hmdchart.data.datasets[0].data = newHmd;
        hmdchart.data.labels = newTime;
    }
    
    tempchart.update();
    hmdchart.update();
}