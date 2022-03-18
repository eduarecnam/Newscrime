// Load the Visualization API and the corechart package.
google.charts.load('current', {'packages':['corechart']});

// Set a callback to run when the Google Visualization API is loaded.
google.charts.setOnLoadCallback(drawChart);

// Callback that creates and populates a data table,
// instantiates the pie chart, passes in the data and
// draws it.

function drawChart() {
    my_seniors = JSON.parse(seniors);
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Force');
    data.addColumn('number', 'Number of Seniors');
    for (const [force, number_seniors] of Object.entries(my_seniors)){
        data.addRows([
            [force, number_seniors],
        ]);
    }  
    // Set chart options
    var options = {
                    'title':'Number of seniors per Force'
                };

    // Instantiate and draw our chart, passing in some options.
    var chart = new google.visualization.PieChart(document.getElementById('chart'));
    chart.draw(data, options);
}