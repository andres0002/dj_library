function listAuthors(){
    $('#authors_table').DataTable().clear().destroy(); // elimina la instancia de la table in el html.
    $('#authors_table').DataTable({ // crea la instancia de la table in el html.
        "serverSide": true,
        "processing": true,
        "order": [[1, 'asc']],  // <- Orden por defecto: columna 1 (name), ascendente.
        "ajax": (data, callback, settings) => {
            // console.log(data);
            let column_order = (data.order[0].dir === 'asc' ? '' : '-') + data.columns[data.order[0].column].data;
            $.get(
                "/book/authors_table_serve_side_in_datetable/",
                {
                    start: data.start,
                    limit: data.length,
                    search: data.search.value,
                    order: column_order
                },
                (res) => {
                    // console.log(res);
                    callback({
                        recordsTotal: res.length,
                        recordsFiltered: res.length,
                        data: res.objects
                    });
                }
            );
        },
        "columns": [
            {
                "data": "#",
                "orderable": false  // <- Esto desactiva el ordenamiento por esta columna.
            },
            {"data": "name"},
            {"data": "lastname"},
            {"data": "nationality"},
            {"data": "description"},
            {
                "data": null,
                "orderable": false,
                "searchable": false,
                "render": function(data, type, row) {
                    return `
                        <button class="btn btn-sm btn-primary" onclick="open_modal_edition('/book/update_author_serve_side_in_datetable/${row.id}/');">Edit</button>
                        <button class="btn btn-sm btn-danger" onclick="open_modal_elimination('/book/delete_author_serve_side_in_datetable/${row.id}/');">Delete</button>
                    `;
                }
            }
        ]
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
    let data = new FormData($('#form_edition').get(0)); // para imgs.
    $.ajax({
        // url: $('#form_edition').attr('action'), // sin imgs.
        // type: $('#form_edition').attr('method'), // sin imgs.
        // data: $('#form_edition').serialize(), // sin imgs.
        url: $('#form_edition').attr('action'),
        type: $('#form_edition').attr('method'),
        data: data,
        cache: false, // para imgs.
        processData: false, // para imgs.
        contentType: false, // para imgs.
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
        url: '/book/delete_author_serve_side_in_datetable/'+ pk +'/',
        type: 'delete',
        headers: {
            'X-CSRFToken': $("[name='csrfmiddlewaretoken']").val()  // Enviamos el token CSRF en la cabecera
        },
        success: function(response){
            successNotification("Successfully Author elimination.");
            listAuthors();
            close_modal_elimination();
        },
        error: function(error){
            errorNotification("Errorful Author elimination.");
        },
    });
}

$(document).ready(function(){
    listAuthors();
});