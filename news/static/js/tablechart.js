// Load the Visualization API and the corechart package.
google.charts.load('current', {'packages':['table']});

// Set a callback to run when the Google Visualization API is loaded.
google.charts.setOnLoadCallback(drawChart);

// Callback that creates and populates a data table,
// instantiates the pie chart, passes in the data and
// draws it.

function drawChart() {

    current_url = window.location.href;
    details_force = current_url.replace('forces','details_force/');
    console.log(details_force);


    console.log(window.location.href);
    table_forces = JSON.parse(forces);
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Force ID');
    data.addColumn('string', 'Force Name');
    for (const [id, name] of Object.entries(table_forces)){
        data.addRows([
            ['<a href="'+details_force+id+'">'+id+'</a>', name],
        ]);
    }  
    // Set chart options
    var options = {
                    'title': 'Forces',
                    'allowHtml': 'true'
                     };

    // Instantiate and draw our chart, passing in some options.
    var chart = new google.visualization.Table(document.getElementById('chart'));
    chart.draw(data, options);
}