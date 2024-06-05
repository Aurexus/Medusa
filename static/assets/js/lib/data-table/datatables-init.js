(function ($) {
    //    "use strict";


    /*  Data Table
    -------------*/

 	// $('#bootstrap-data-table').DataTable();


    $('#bootstrap-data-table').DataTable({
        lengthMenu: [[10, 20, 50, -1], [10, 20, 50, "All"]],
		
		 
    });
    $('#bootstrap-data-table-export').DataTable({
        dom: 'lBfrtip',
		columnDefs: [
			//hide the 2nd column. it's index is "1"
			{ 'visible': false,
			'targets': [6,7] ,
			'searchable': true
			} /// COLUMN INDEX HERE
		]   ,
        lengthMenu: [[10, 25, 50, -1], [10, 25, 50, "All"]],
        buttons: [
            'csv', 'excel', 'pdf'
        ]          
    });
	$('#table-export').DataTable({
        lengthMenu: [[10, 20, 50, -1], [10, 20, 50, "All"]],
		
		 
    });	


	  $('.dataTables_filter input[type="search"]').css(
		{'width':'350px','display':'inline-block'}
		 )
	$('#row-select').DataTable( {
			initComplete: function () {
				this.api().columns().every( function () {
					var column = this;
					var select = $('<select class="form-control"><option value=""></option></select>')
						.appendTo( $(column.footer()).empty() )
						.on( 'change', function () {
							var val = $.fn.dataTable.util.escapeRegex(
								$(this).val()
							);
	 
							column
								.search( val ? '^'+val+'$' : '', true, false )
								.draw();
						} );
	 
					column.data().unique().sort().each( function ( d, j ) {
						select.append( '<option value="'+d+'">'+d+'</option>' )
					} );
				} );
			}
		} );






})(jQuery);