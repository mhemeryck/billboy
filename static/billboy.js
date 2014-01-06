/**
function copyFieldNames(pk) {

	var fieldNames = ["datepicker", "description", "amount", "paid_by"];
	for (var i = 0; i < fieldNames.length; i++) {
		var v = $( "#view-" + fieldNames[i] + "-" + pk ).html();
		$( "#edit-" + fieldNames[i] + "-" + pk ).val(v);
	}
}
**/

$(function() {
	$( ".form-control.datepicker" ).datepicker({
		format: "yyyy-mm-dd",
		todayHighlight: true,
	});

    // validation
    // $( "input" ).jqBootstrapValidation();
	
	// hide all edit by default
	$( "tr.bill.edit" ).hide();
	
	// submit button
	/*
	$( "button[value=submit]" ).click( function() {
		$.post($SCRIPT_ROOT + '/submit', {
		    date: $( ".panel-body > div > input[name=date]" ).val(),
	        description: $( ".panel-body > div > input[name=description]" ).val(),
	        amount: $( ".panel-body > div > input[name=amount]" ).val(),
		    paid_by: $( ".panel-body > div > select[name=paid_by]" ).val()
		});
	});
	*/
	
	// edit buttons
	$( "button[value=edit].bill.view" ).click( function() {
		var pk = $( this ).attr("pk");
		// switch other edit to view
		$( "tr[pk!=" + pk + "].bill.edit" ).hide();
		$( "tr[pk!=" + pk + "].bill.view" ).show	();
		// switch current view to edit
		$( "tr[pk=" + pk + "].bill.view" ).hide();
		$( "tr[pk=" + pk + "].bill.edit" ).show();
	});
	
	// delete buttons
	/*
	$( "button[value=delete].bill.view" ).click( function() {
		var pk = $( this ).attr("pk");
		alert("do delete for " + pk);
	});
	*/

	// cancel buttons
	$( "button[value=cancel].bill.edit" ).click( function() {
		var pk = $( this ).attr("pk");
		// switch edit back to view
		$( "tr[pk=" + pk + "].bill.edit" ).hide();
		$( "tr[pk=" + pk + "].bill.view" ).show();
	});

});

