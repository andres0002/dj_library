function listBooks(){
    $.ajax({
        url: "/book/books_table/",
        type: "get",
        dataType: "json",
        success: function(response){
            if ($.fn.DataTable.isDataTable('#books_table')){
                $('#books_table').DataTable().destroy();
            }
            $('#books_table tbody').html("");
            for (let i = 0;i < response.length;i++){
                let row = '<tr>';
                row += '<td>' + (i + 1) + '</td>';
                row += '<td>' + response[i]['fields']['title'] + '</td>';
                row += '<td>' + response[i]['fields']['publication_date'] + '</td>';
                if (response[i]['fields']['authors'] == '') {
                    row += '<td>Anonymous</td>';
                } else {
                    row += '<td>' + response[i]['fields']['authors'] + '</td>';
                }
                row += '<td>' + response[i]['fields']['create_date'] + '</td>';
                row += '<td>' + response[i]['fields']['update_date'] + '</td>';
                row += '<td>';
                row += '<button class="btn btn-primary"';
                row += ' onclick="open_modal_edition(\'/book/update_book/' + response[i]['pk'] + '/\');">';
                row += '<i class="fa fa-pencil"></i> Edit</button>';
                row += ' <button class="btn btn-danger"';
                row += ' onclick="open_modal_elimination(\'/book/delete_book/' + response[i]['pk'] + '/\');">';
                row += '<i class="fa fa-eraser"></i> Delete</button>';
                row += '</td>';
                row += '</tr>';
                $('#books_table tbody').append(row);
            }
            $('#books_table').DataTable({});
        },
        error: function(error){
            console.log(error);
        }
    });
}

function register(){
    activeButtonCreation();
    let data = new FormData($('#form_creation').get(0)); // para imgs.
	$.ajax({
        // url: $('#form_creacion').attr('action'), // sin imgs.
        // type: $('#form_creacion').attr('method'), // sin imgs.
        // data: $('#form_creacion').serialize(), // sin imgs.
		url: $('#form_creation').attr('action'),
		type: $('#form_creation').attr('method'),
        data: data,
        cache: false, // para imgs.
        processData: false, // para imgs.
        contentType: false, // para imgs.
		success: function(response){
            successNotification(response.message);
			listBooks();
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
    let data = new FormData($('#form_edition').get(0)); // para imgs.
    $.ajax({
        // url: $('#form_edition').attr('action'), // sin imgs.
        // type: $('#form_edition').attr('method'), // sin imgs.
        // data: $('#form_edition').serialize(), // sin imgs.
        url: $('#form_edition').attr('action'),
        type: $('#form_edition').attr('method'),
        data: data, // para imgs.
        cache: false, // para imgs.
        processData: false, // para imgs.
        contentType: false, // para imgs.
        success: function(response){
            successNotification(response.message);
            listBooks();
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
        url: '/book/delete_book/'+ pk +'/',
        type: 'delete',
        headers: {
            'X-CSRFToken': $("[name='csrfmiddlewaretoken']").val()  // Enviamos el token CSRF en la cabecera
        },
        success: function(response){
            successNotification("Successfully Book elimination.");
            listBooks();
            close_modal_elimination();
        },
        error: function(error){
            errorNotification("Errorful Book elimination.");
        },
    });
}

$(document).ready(function(){
    listBooks();
});