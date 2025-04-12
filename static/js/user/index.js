function listUsers(){
    $.ajax({
        url: "/user/users_table/",
        type: "get",
        dataType: "json",
        success: function(response){
            if ($.fn.DataTable.isDataTable('#users_table')){
                $('#users_table').DataTable().destroy();
            }
            $('#users_table tbody').html("");
            for (let i = 0;i < response.length;i++){
                let row = '<tr>';
                row += '<td>' + (i + 1) + '</td>';
                row += '<td>' + response[i]['fields']['username'] + '</td>';
                row += '<td>' + response[i]['fields']['name'] + '</td>';
                row += '<td>' + response[i]['fields']['lastname'] + '</td>';
                row += '<td>' + response[i]['fields']['email'] + '</td>';
                row += '<td>';
                row += '<button class="btn btn-primary" type="button"';
                row += ' onclick="open_modal_edition(\'/user/update_user/' + response[i]['pk'] + '/\');">';
                row += '<i class="fa fa-pencil"></i> Edit</button>';
                row += ' <button class="btn btn-danger" type="button"';
                row += ' onclick="open_modal_elimination(\'/user/delete_user/' + response[i]['pk'] + '/\');">';
                row += '<i class="fa fa-eraser"></i> Delete</button>';
                row += '</td>';
                row += '</tr>';
                $('#users_table tbody').append(row);
            }
            $('#users_table').DataTable({
                language: {
                    "decimal": "",
                    "emptyTable": "No hay información",
                    "info": "Mostrando _START_ a _END_ de _TOTAL_ Entradas",
                    "infoEmpty": "Mostrando 0 to 0 of 0 Entradas",
                    "infoFiltered": "(Filtrado de _MAX_ total entradas)",
                    "infoPostFix": "",
                    "thousands": ",",
                    "lengthMenu": "Mostrar _MENU_ Entradas",
                    "loadingRecords": "Cargando...",
                    "processing": "Procesando...",
                    "search": "Buscar:",
                    "zeroRecords": "Sin resultados encontrados",
                    "paginate": {
                        "first": "Primero",
                        "last": "Ultimo",
                        "next": "Siguiente",
                        "previous": "Anterior"
                    },
                },
            });
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
			listUsers();
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
            listUsers();
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
        url: '/user/delete_user/'+ pk +'/',
        type: 'post',
        success: function(response){
            successNotification(response.message);
            listUsers();
            close_modal_elimination();
        },
        error: function(error){
            errorNotification(error.responseJSON.message);
        }
    });
}

$(document).ready(function(){
    listUsers();
});