// Load the Visualization API and the corechart package.
google.charts.load('current', {'packages':['corechart']});

// Set a callback to run when the Google Visualization API is loaded.
google.charts.setOnLoadCallback(drawChart);

// Callback that creates and populates a data table,
// instantiates the pie chart, passes in the data and
// draws it.

function drawChart() {

    crimes_category = JSON.parse(total_crimes_category);
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Crime category');
    data.addColumn('number', 'Times');
    for (const [category, times] of Object.entries(crimes_category)){
        data.addRows([
            [category, times],
        ]);
    }  
    // Set chart options
    var options = {
                    'title':'Crimes per category, first last month with crimes ('+month+')',
                    pieHole: 0.4, };

    // Instantiate and draw our chart, passing in some options.
    var chart = new google.visualization.PieChart(document.getElementById('chart'));
    chart.draw(data, options);
}