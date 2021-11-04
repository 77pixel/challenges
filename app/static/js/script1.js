$(document).ready(function() {
    
    $('#example_tab').DataTable( {
        "paging":   false,
        columnDefs: [
        { 
            render: function ( data, type, row ) 
            {
                var qt = row[7] - row[8];
                if(qt <= 0)
                {
                    return '<p style="background-color: rgba(255, 0, 0, 0.3);">'+qt+'</p>';
                }
                else
                {
                    return '<p style="background-color: rgba(0, 255, 0, 0.3);">'+qt+'</p>';
                }
            }, 
            targets: [9] 
        }] 
        
    });

} );