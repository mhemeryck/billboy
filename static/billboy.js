$(function() {
	$( ".form-control.datepicker" ).datepicker({
		format: "yyyy-mm-dd",
		todayHighlight: true,
	});
	
	// hide all edit by default
	$( "tr.edit" ).hide();
	
	// edit buttons
	$( "button[value^='edit']" ).click( function() {
	    var pk = $( this ).attr("value").replace(/.*\[|\]/gi, '');
	    // switch other edit to view
		$( "tr[id!='bill-edit[" + pk + "]'].edit" ).hide();
		$( "tr[id!='bill-view[" + pk + "]'].view" ).show();
		// switch current view to edit
		$( "tr[id='bill-view[" + pk + "]'].view" ).hide();
		$( "tr[id='bill-edit[" + pk + "]'].edit" ).show();
    });
    
    // switch to view
	$( "button[value^='cancel']" ).click( function() {
	    var pk = $( this ).attr("value").replace(/.*\[|\]/gi, '');
	    // switch edit back to view
	    $( "tr[id='bill-edit[" + pk + "]'].edit" ).hide();
	    $( "tr[id='bill-view[" + pk + "]'].view" ).show()
    });
});

