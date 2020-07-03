var chart;

function requestData() {
    $.ajax({
        url: '/live-chart',
        success: function(point) {
            var series = chart.series[0],
                shift = series.data.length > 20; // shift if the series is

                chart.series[0].setData(point, true, shift);
                chart.redraw();
                setTimeout(requestData, 1000)
        },
        cache: false
    });
}



$(document).ready(function() {
    chart = new Highcharts.Chart({
        chart: {
            renderTo: 'container',
            defaultSeriesType: 'column',
            events: {
                load: requestData
            }
        },
        title: {
            text: 'Most Popular Languages'
        },
        xAxis: {
            type: 'category',
            categories: [
                "JavaScript",
                "Python",
                "Java",
                "Golang",
                "C++",
                "Ruby",
                "PHP",
                "C#",
                "Scala",
                "Rust",
                "Swift",
                "Node.js",
                "React"
            ],
            min: 0,
            max: 12,

        },
        yAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                text: 'Job Count',
                margin: 80
            }
        },
        series: [{
            name: 'Jobs',
            data: [],
            enablePolling: true,
            dataRefreshRate: 1,
            pointInterval: 1,
            pointStart: 0,
        }]
    });
});