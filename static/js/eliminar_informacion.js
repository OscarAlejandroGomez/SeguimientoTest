
function p_eliminar_documento(Id_documento){
    $.ajax({
        url: 'p_eliminar_documento',
        data: {Id_documento:Id_documento},
        type: 'POST',
            success: function (response) {
                let Rta = JSON.parse(response);
                console.log(response); 
                if(Rta.status == 'OK'){
                    Swal.fire({ title: "Señor funcionario", text: "el documento fue eliminado exitosamente", type: "success"});
                    let t=setTimeout("redirecciona()",2000);   
                    return true;
                }
            },
            error: function (error) {
            console.log(error);
        }
});

    Swal.fire('Señor(@) funcionario', 'ha descargado el documento xxxx, y se registra en la auditoría. Gracias', 'success' );
    return false;

}


function redirecciona(){
location.href ="/documento_registrado";   
}

