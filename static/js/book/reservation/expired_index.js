function listExpiredReservations(){
    $.ajax({
        url: "/book/expired-reservations-table/",
        type: "get",
        dataType: "json",
        success: function(response){
            if ($.fn.DataTable.isDataTable('#expired_reservations_table')){
                $('#expired_reservations_table').DataTable().destroy();
            }
            $('#expired_reservations_table tbody').html("");
            for (let i = 0;i < response.length;i++){
                let row = '<tr>';
                row += '<td>' + (i + 1) + '</td>';
                row += '<td>' + response[i]['fields']['book'] + '</td>';
                row += '<td>' + response[i]['fields']['amount_days'] + '</td>';
                row += '<td>' + response[i]['fields']['createDate'] + '</td>';
                row += '<td>' + response[i]['fields']['expirationDate'] + '</td>';
                row += '</tr>';
                $('#expired_reservations_table tbody').append(row);
            }
            $('#expired_reservations_table').DataTable({});
        },
        error: function(error){
            console.log(error);
        }
    });
}

$(document).ready(function(){
    listExpiredReservations();
});