function listAuthors(){
    $.ajax({
        url: "/book/authors_table/",
        type: "get",
        dataType: "json",
        success: function(response){
            if ($.fn.DataTable.isDataTable('#authors_table')){
                $('#authors_table').DataTable().destroy();
            }
            $('#authors_table tbody').html("");
            for (let i = 0;i < response.length;i++){
                let row = '<tr>';
                row += '<td>' + (i + 1) + '</td>';
                row += '<td>' + response[i]['fields']['nameAuthor'] + '</td>';
                row += '<td>' + response[i]['fields']['lastNameAuthor'] + '</td>';
                row += '<td>' + response[i]['fields']['nationalityAuthor'] + '</td>';
                row += '<td>' + response[i]['fields']['descriptionAuthor'] + '</td>';
                row += '<td>' + response[i]['fields']['createDateAuthor'] + '</td>';
                row += '<td>' + response[i]['fields']['updateDateAuthor'] + '</td>';
                row += '<td>';
                row += '<button class="btn btn-primary" type="button"';
                row += ' onclick="open_modal_edition(\'/book/update_author/' + response[i]['pk'] + '/\');">';
                row += '<i class="fa fa-pencil"></i> Edit</button>';
                row += ' <button class="btn btn-danger" type="button"';
                row += ' onclick="open_modal_elimination(\'/book/delete_author/' + response[i]['pk'] + '/\');">';
                row += '<i class="fa fa-eraser"></i> Delete</button>';
                row += '</td>';
                row += '</tr>';
                $('#authors_table tbody').append(row);
            }
            $('#authors_table').DataTable({});
        },
        error: function(error){
            console.log(error);
        }
    });
}

function register(){
    activeButtonCreation();
    var data = new FormData($('#form_creation').get(0));
	$.ajax({
		url: $('#form_creation').attr('action'),
		type: $('#form_creation').attr('method'),
        data: data,
        cache: false,
        processData: false,
        contentType: false,
		success: function(response){
            successNotification(response.message);
			listAuthors();
            close_modal_creation();
		},
		error: function(error){
            errorNotification(error.responseJSON.message);
			showCreationErrors(error);
            activeButtonCreation();
		}
	});
}

function edition(){
    activeButtonEdition();
    var data = new FormData($('#form_edition').get(0));
    $.ajax({
        url: $('#form_edition').attr('action'),
        type: $('#form_edition').attr('method'),
        data: data,
        cache: false,
        processData: false,
        contentType: false,
        success: function(response){
            successNotification(response.message);
            listAuthors();
            close_modal_edition();
        },
        error: function(error){
            errorNotification(error.responseJSON.message);
            showEditionErrors(error);
            activeButtonEdition();
        }
    });
}

function elimination(pk){
    $.ajax({
        data: {
            csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val()
        },
        url: '/book/delete_author/'+ pk +'/',
        type: 'post',
        success: function(response){
            successNotification(response.message);
            listAuthors();
            close_modal_elimination();
        },
        error: function(error){
            errorNotification(error.responseJSON.message);
        }
    });
}

$(document).ready(function(){
    listAuthors();
});