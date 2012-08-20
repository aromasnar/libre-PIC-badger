/*
Author:  Geoff Anderson, Azhar Sikander
Contains code for AJAX API calls and page display for the sub_template.html
 */

/* toggles license view and agreement controls. */
/* action = show / hide*/
/* previewDiv = the div that contains the HTML / code preview code. */
function togglePreview(previewDiv, action) {
	if (action == "show") {
		$(previewDiv).show();
	} else if (action == "hide") {
		$(previewDiv).hide();
	}
}

/* Reset a particular form */
function clearForm(formID) {
	document.forms[formID].reset();
	if (formID == "form1") {
		$('#piczero_html_preview').html("");
		$('#piczeroAgreement').attr('checked', false);
		$('#piczeroAgreementError').html("");
		togglePreview('#piczero_preview', 'hide');
	} else if (formID == "form2") {
		$('#picccby_html_preview').html("");
		$('#picccbyAgreement').attr('checked', false);
		$('#picccbyAgreementError').html("");
		togglePreview('#picccby_preview', 'hide');
	}
}

var LIBRE = {

	preview1 : function() {
		if (!$('#piczeroAgreement').attr('checked')) {
			$('#errorPICZeroForm').html("Please accept agreement to proceed.");
			return;
		} else {
			$('#errorPICZeroForm').html("");
		}
		// Get the form.
		var form = $('#form1');
		// Serialize to parameter string.
		var params = form.serialize();
		params = params + "&licenseType=pic_cc_zero";
		params = params + "&formID=form1";

		// togglePreview('#piczero_preview', 'show');
		// Get or Post to the service broker.
		$.post("createBadge/", params, function(data) {
			$('#errorPICZeroForm').html("");
			if (data.hasOwnProperty("status")) {
				if (data.status == "license") {
					// Hide the preview area because of the dom manipulations
					togglePreview('#piczero_preview', 'hide');
					
					// Assume that the content is already HTML
					$('#piczero_html_preview').html(data.response);
					$('#piczero_htmlblob').val(data.response);
					
					// If the output type was xml, then extract the HTML portion
					var outputType = $('#form1 :input[name="outputType"] :selected').text();
					if (outputType.toLowerCase() == "xml") {
						var htmlPreview = $('#piczero_html_preview p');
						if ( htmlPreview.length > 0 ) {							
							$('#piczero_html_preview').html(htmlPreview.html())
						} else {						
							// Just in case the selector breaks -- we'll just not show a preview
							$('#piczero_html_preview').html("No Preview for XML");
						}
					}
					// Show the preview again
					togglePreview('#piczero_preview', 'show');
				} else if (data.status == "error") {
					$('#errorPICZeroForm').html(data.response);
				} else if (data.status == "validationError") {
					$('#form1Container').html(data.response);

				}

			}
		});
	},

	preview2 : function() {
		if (!$('#picccbyAgreement').attr('checked')) {
			$('#errorPICCCByForm').html("Please accept agreement to proceed.");
			return;
		} else {
			$('#errorPICCCByForm').html("");
		}

		var form = $('#form2');
		var params = form.serialize();
		params = params + "&licenseType=pic_cc_by";
		params = params + "&formID=form2";

		$.post("createBadge/", params, function(data) {
			$('#errorPICCCByForm').html("");
			if (data.hasOwnProperty("status")) {
				if (data.status == "license") {
					// Hide the preview area because of the dom manipulations
					togglePreview('#picccby_preview', 'hide');
					
					// Assume that the content is already HTML
					$('#picccby_html_preview').html(data.response);
					$('#picccby_htmlblob').val(data.response);
					
					// If the output type was xml, then extract the HTML portion
					var outputType = $('#form2 :input[name="outputType"] :selected').text();
					if (outputType.toLowerCase() == "xml") {
						var htmlPreview = $('#picccby_html_preview p');
						if ( htmlPreview.length > 0 ) {							
							$('#picccby_html_preview').html(htmlPreview.html())
						} else {						
							// Just in case the selector breaks -- we'll just not show a preview
							$('#picccby_html_preview').html("No Preview for XML");
						}
					}
					// Show the preview again
					togglePreview('#picccby_preview', 'show');					
				} else if (data.status == "error") {
					$('#errorPICCCByForm').html(data.response);
				} else if (data.status == "validationError") {
					$('#form2Container').html(data.response);
				}

			}
		});
	},

	showForm1 : function() {
		$('#form_2').hide();
		$('#form_1').fadeIn('fast');
		isLicensePreviewed = false
	},
	showForm2 : function() {
		$('#form_1').hide();
		$('#form_2').fadeIn('fast');
		isLicensePreviewed = false
	}
}

function init() {

}
