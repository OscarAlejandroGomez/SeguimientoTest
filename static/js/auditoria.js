


$(function () {
    $('#secondaryDownload').click(function(){
        let secondaryDownload =  parseInt($('#secondaryDownload').val());
        Swal.fire('Señor(@) funcionario', 'ha descargado el documento xxxx, y se registra en la auditoría. Gracias', 'success' );
        return false;

    });
});
