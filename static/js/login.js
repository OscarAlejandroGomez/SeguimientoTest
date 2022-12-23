$(function () {
    $('#btn_iniciar_sesion').click(function(){
        let Usuario = ($('#Usuario').val());
        let password = ($('#password').val());
        if(Usuario ==""){ 
            Swal.fire('Señor funcionario', '¡por favor escriba su usuario', "error");
            return false;
        }else if(password==""){
            Swal.fire('Señor funcionario', '¡por favor escriba la contraseña', "error");
            return false;
        }
        $.ajax({
            url: 'f_iniciar_sesion',
            data: { Usuario:Usuario, password:password },
            type: 'POST',
            success: function (response) {
                let ET = JSON.parse(response);
                console.log(response);
                if (ET.data == 4){
                    Swal.fire('Señor funcionario(@)', 'los datos fueron validados exitosamente', "error");
                    return true;
                }else if(ET.data == 5){
                    Swal.fire('Señor funcionario(@)', 'sus datos no son válidos', "error");
                    return true; 
                } 
            },
            error: function (error) {
                console.log(error);
            }
        });
        return false;      
    });
});
