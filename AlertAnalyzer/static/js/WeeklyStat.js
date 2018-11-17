function plotColumnChart (data_series) {
    $('#EventAppPanel').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: 'Top events group by Event and App'
        },
        xAxis: {
            type: 'category',
            labels: {
                rotation: -45,
                style: {
                    fontSize: '13px',
                    fontFamily: 'Verdana, sans-serif'
                }
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Weekly Alerts (By EventAppName)'
            }
        },
        legend: {
            enabled: false
        },
        tooltip: {
            pointFormat: 'Count: <b>{point.y}</b>'
        },
        series: [{
            name: 'Alert Count per week',
            data: data_series,
            dataLabels: {
                enabled: true,
                rotation: -90,
                color: '#FFFFFF',
                align: 'right',
                format: '{point.y}', // one decimal
                y: 10, // 10 pixels down from the top
                style: {
                    fontSize: '13px',
                    fontFamily: 'Verdana, sans-serif'
                }
            }
        }]
    });
}

function plotStackAreaChart (days,data_series) {
    $('#WeeklyTop10Panel').highcharts({
        chart: {
            type: 'area',
            zoomType: 'x',
            events: {
                click: function (e) {
                    // find the clicked values and the series
                    var x = e.xAxis[0].value,
                    y = e.yAxis[0].value;
                    alert(""+x+" "+y);
                }
            }
        },
        title: {
            text: 'Weekly Event Stat'
        },
        subtitle: {
            text: 'To be implemented'
        },
        credits: {
            enabled : false
        },
        xAxis: {
            categories: days,
            tickmarkPlacement: 'on',
            title: {
                enabled: false
            }
        },
        yAxis: {
            title: {
                text: 'Count'
            },
            labels: {
                formatter: function () {
                    return this.value;
                }
            }
        },
        tooltip: {
            shared: true,
            valueSuffix: ''
        },
        plotOptions: {
            area: {
                stacking: 'normal',
                lineColor: '#666666',
                lineWidth: 1,
                marker: {
                    lineWidth: 1,
                    lineColor: '#666666'
                },
            }
        },
        series: data_series
    });
}

function plotByEvent (StartDay,EndDay) {
    $.getJSON("StatByEvent.json",{"StartDay":StartDay,"EndDay":EndDay}, function(json_data) {
        plotStackAreaChart(json_data.days,json_data.data_series)
    });
}

function plotByAppEvent (StartDay,EndDay) {
    $.getJSON("StatByAppEvent.json",{"StartDay":StartDay,"EndDay":EndDay}, function(json_data) {
        plotColumnChart(json_data);
    });
}

$(document).ready(function() {
    var StartDay = $('#StartDay').val();
    var EndDay = $('#EndDay').val();
    plotByEvent(StartDay,EndDay);
    plotByAppEvent(StartDay,EndDay);
});
