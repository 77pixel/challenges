$(document).ready(function() {
    
    $('#table_from_file').DataTable( {
        "paging":   true,
        "ordering": true,
        "info":     false
    });

    let ben_tab = $('#benford_tab').DataTable( {
        "paging":    false,
        "ordering":  false,
        "info":      false,
        "searching": false 
    });
    var s_head = [ 'Benford norm', ...serie[0]["data"]];
    ben_tab.row.add(s_head).draw( false );
    s_head = [ 'File data', ...serie[1]["data"]];
    ben_tab.row.add(s_head).draw( false );
    
    Highcharts.chart('chart', 
    {
        title: {
            text: 'Benford’s Distribution'
        },
        yAxis: {
            opposite: false,
            title: {
                text: 'Percentage'
            }
        },
        xAxis: {
            reversed: false
        },
        legend: {
            layout: 'vertical',
            align: 'left',
            verticalAlign: 'middle'
        },
        series: serie,
        
        responsive: {
            rules: [{
                condition: {
                    maxWidth: 500
                },
                chartOptions: {
                    legend: {
                        layout: 'horizontal',
                        align: 'center',
                        verticalAlign: 'bottom'
                    }
                }
            }]
        }
    });
} );