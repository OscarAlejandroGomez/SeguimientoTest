
$(document).ready(function () {
    f_consultar_perfil();
    f_consultar_opcion_habilitar();
    f_visualiza_temas();
});


var Id_Perfil_1=0;
function f_consultar_perfil() {
        let Estado = 1;
        $.ajax({
            url: 'f_consultar_perfil',
            data: { Estado: Estado },
            type: 'POST',
            success: function (response) {
                let perfiles = JSON.parse(response);
                // console.log(response);
                let opt = 0;
                let opt1 = "No hay datos";
                let auxArr = [];
                if (perfiles.data.length == 0) {
                    auxArr = ""
                    $('#Id_Perfil').empty(0);
                    $('#Id_Perfil').change(0);
                } else {
                    for (let i = 0; i <= perfiles.data.length; i++) {
                        if (perfiles.data.length != i) {
                            for (let k = 0; k <= perfiles.data[i].length; k++) {
                                if (k == 0) {
                                    opt = perfiles.data[i][k];
                                }
                                else if (k == 1) {
                                    opt1 = perfiles.data[i][k];
                                }
                            }
                            auxArr[i + 1] = "<option value='" + opt + "'>" + opt1 + "</option>";
                        } else {
                            auxArr[0] = "<option value='0'> Seleccione... </option>";
                        }
                    }
                    $('#Id_Perfil').empty();
                    $('#Id_Perfil').append(auxArr.join(''));
                    $('#Id_Perfil').change();
                    if(Id_Perfil_1!==0){
                        $('#Id_Perfil').val(Id_Perfil_1);
                    }
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
        return false;
}


var Id_habilitar_1=0;
function f_consultar_opcion_habilitar() {
        let Estado = 1;
        $.ajax({
            url: 'f_consultar_opcion_habilitar',
            data: { Estado: Estado },
            type: 'POST',
            success: function (response) {
                let habilitar = JSON.parse(response);
                // console.log(response);
                let opt = 0;
                let opt1 = "No hay datos";
                let auxArr = [];
                if (habilitar.data.length == 0) {
                    auxArr = ""
                    $('#Id_habilitar').empty(0);
                    $('#Id_habilitar').change(0);
                } else {
                    for (let i = 0; i <= habilitar.data.length; i++) {
                        if (habilitar.data.length != i) {
                            for (let k = 0; k <= habilitar.data[i].length; k++) {
                                if (k == 0) {
                                    opt = habilitar.data[i][k];
                                }
                                else if (k == 1) {
                                    opt1 = habilitar.data[i][k];
                                }
                            }
                            auxArr[i + 1] = "<option value='" + opt + "'>" + opt1 + "</option>";
                        } else {
                            auxArr[0] = "<option value='0'> Seleccione... </option>";
                        }
                    }
                    $('#Id_habilitar').empty();
                    $('#Id_habilitar').append(auxArr.join(''));
                    $('#Id_habilitar').change();
                    if(Id_habilitar_1!==0){
                        $('#Id_habilitar').val(Id_habilitar_1);
                    }
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
        return false;
}


var Id_tema_1=0;
function f_visualiza_temas() {
        let Estado = 1;
        $.ajax({
            url: 'f_visualiza_temas',
            data: { Estado: Estado },
            type: 'POST',
            success: function (response) {
                let temas = JSON.parse(response);
                // console.log(response);
                let opt = 0;
                let opt1 = "No hay datos";
                let auxArr = [];
                if (temas.data.length == 0) {
                    auxArr = ""
                    $('#Id_tema').empty(0);
                    $('#Id_tema').change(0);
                } else {
                    for (let i = 0; i <= temas.data.length; i++) {
                        if (temas.data.length != i) {
                            for (let k = 0; k <= temas.data[i].length; k++) {
                                if (k == 0) {
                                    opt = temas.data[i][k];
                                }
                                else if (k == 1) {
                                    opt1 = temas.data[i][k];
                                }
                            }
                            auxArr[i + 1] = "<option value='" + opt + "'>" + opt1 + "</option>";
                        } else {
                            auxArr[0] = "<option value='0'> Seleccione... </option>";
                        }
                    }
                    $('#Id_tema').empty();
                    $('#Id_tema').append(auxArr.join(''));
                    $('#Id_tema').change();
                    if(Id_tema_1!==0){
                        $('#Id_tema').val(Id_tema_1);
                    }
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
        return false;
}


let Id_subtema_1=0;
function f_visualiza_subtemas() {
        let auxArr = [], _options;
        let Id_tema = $('#Id_tema').val();
        if (Id_tema==0){
            _options="";
            Id_tema = Id_tema_1;
            $('#Id_subtema').html(_options);
            $('#Id_subtema').selectpicker('refresh');
        }
            $.ajax({
                url: 'f_visualiza_subtemas',
                data: { Id_tema: Id_tema },
                type: 'POST',
                success: function (response) {
                    let subtemas = JSON.parse(response);
                    // console.log(response);
                    let opt = 0;
                    let opt1 = "No hay datos";
                    if (subtemas.data.length == 0) {
                        _options="";
                        $('#Id_subtema').html(_options);
                        $('#Id_subtema').selectpicker('refresh');
                    } else {
                        for (let i = 0; i <= subtemas.data.length; i++) {
                            if (subtemas.data.length != i) {
                                for (let k = 0; k <= subtemas.data[i].length; k++) {
                                    if (k == 0) {
                                        opt = subtemas.data[i][k];
                                    }
                                    else if (k == 1) {
                                        opt1 = subtemas.data[i][k];
                                    }
                                }
                                auxArr[i + 1] = "<option value='" + opt + "'>" + opt1 + "</option>";
                            } else {
                                auxArr[0] = "<option value='0'> Seleccione... </option>";
                            }
                        }

                        _options = auxArr.join('');
                        $('#Id_subtema').html(_options).selectpicker('refresh'); 
                        if (Id_subtema_1.val!== 0) {
                                $('select[name=Id_subtema]').val(Id_subtema_1);
                                $('.selectpicker').selectpicker('val', Id_subtema_1);
                               
                        }else{
                            $('#Id_subtema').html(_options).selectpicker('refresh');
                        }
                    }
                },
                error: function (error) {
                    console.log(error);
                }
            });
            return false;
}


let Id_codigo_cargo=0;
let correo_electronico=0;
$(function () {
        $('#Btnbuscar').click(function(){
            let Identificacion = ($('#Texto_buscar').val());
            if(Identificacion ==""){ 
                document.getElementById("Texto_buscar").focus();
                Swal.fire('Señor(@) funcionario', '¡por favor escriba el número de identificación', 'error');
                return false;
            }else if(isNaN(Identificacion)){
                Swal.fire('Señor(@) funcionario', 'el dato ingresado no corresponde a un número', 'warning' );
                return false;
            }
            f_permisos(Identificacion);
            $.ajax({
                url: 'p_identificacion',
                data: { Identificacion:Identificacion },
                type: 'POST',
                success: function (response) {
                    let HB = JSON.parse(response);
                    // console.log(response);
                    if ((HB.status == 1) && (HB.data.Codigo == 4)){
                        $('#Funcionario').val( HB.data.Respuesta['GRAD_ALFABETICO'] +' '+ HB.data.Respuesta['NOMBRES'] +' '+ HB.data.Respuesta['APELLIDOS']);
                        $('#Unidad').val(HB.data.Respuesta['FISICA'] );  
                        $('#Cargo').val(HB.data.Respuesta['CARGO_ACTUAL'] );
                        Id_codigo_cargo = HB.data.Respuesta['CODIGO_CARGO'];  
                        $('#Situacion_actual').val(HB.data.Respuesta['SITUACION_LABORAL']);
                        $('#Usuario').val(HB.data.Respuesta['USUARIO_EMPRESARIAL']);
                        correo_electronico = HB.data.Respuesta['CORREO_ELECTRONICO'];
                        $('#Id_habilitar').val(0);
                        $('#Id_Perfil').val(0);
                        $('#Fecha_fin_rol').val("");
                        $('#Id_tema').val(0);
                        _options = "";
                        $('#Id_subtema').html(_options);
                        $('#Id_subtema').selectpicker('refresh')
                        $('#Justificacion').val("");
                        Id_usuario = 0;
                        Id_usuario_1 = 0;

                        Swal.fire('Señor(@) funcionario', 'la consulta fue exitosa', 'success' );
                        return false;
                    }else{
                        Swal.fire('Señor(@) funcionario', 'la consulta no fue exitosa, por favor verifique el número de identificación.', 'error' );
                        return false;
                    } 
                },
                error: function (error) {
                    console.log(error);
                }
            });
            return false;      
        });
});




let Id_usuario_1 =0;
let _options;
let Id_codigo_cargo_1=0;
//let Identificacion_1 = 0;
$(function () {
        $('#btn_regitro_permisos_usuario').click(function(){
            let Identificacion = ($('#Texto_buscar').val())
            if(Identificacion == ""){
                Swal.fire({ title: "Señor(a) funcionario", text: "por favor indique un número de identificación.", type: "warning" });
                return true;  
            }
            let Id_habilitar = ($('#Id_habilitar').val())
            if(Id_habilitar == 0){
                Swal.fire({ title: "Señor(a) funcionario", text: "por favor indique si va estar habilitado el permiso.", type: "warning" });
                return true;  
            }
            let Id_Perfil = ($('#Id_Perfil').val())
            if(Id_Perfil == 0){
                Swal.fire({ title: "Señor(a) funcionario", text: "por favor seleccione el perfil.", type: "warning" });
                return true;  
            }
            let Fecha_fin_rol = ($('#Fecha_fin_rol').val())
            if(Fecha_fin_rol == ""){
                Swal.fire({ title: "Señor(a) funcionario", text: "por favor indique fecha fin rol .", type: "warning" });
                return true;  
            }
            let Id_tema = ($('#Id_tema').val())
            if(Id_tema == 0){
                Swal.fire({ title: "Señor(a) funcionario", text: "por favor seleccione un tema.", type: "warning" });
                return true;  
            }
            let Id_subtema = $("#Id_subtema").val();
            if (Id_subtema.length == "0"){
                    Swal.fire({ title: "Señor(a) funcionario", text: "por favor seleccione un subtema", type: "warning" });
                    return true;  
                }
            else{
                let lstId_subtema = [];
                for (let i = 0; i < Id_subtema.length; i++) {
                    lstId_subtema.push(Id_subtema[i]);
                }
                subm = JSON.stringify(lstId_subtema)
            }
            Justificacion =  ($('#Justificacion').val())
            if(Justificacion == ""){
                Swal.fire({ title: "Señor(a) funcionario", text: "por favor escriba la justificación de asignación del rol.", type: "warning" });
                return true;  
            }
            let obj = {
                Identificacion : ($('#Texto_buscar').val()),
                Funcionario : ($('#Funcionario').val()),
                Unidad : ($('#Unidad').val()),
                Id_codigo_cargo: Id_codigo_cargo,
                Cargo : ($('#Cargo').val()),
                Situacion_actual : ($('#Situacion_actual').val()),
                Usuario : ($('#Usuario').val()),
                Id_habilitar : ($('#Id_habilitar').val()),
                Id_Perfil : ($('#Id_Perfil').val()),
                Fecha_fin_rol : ($('#Fecha_fin_rol').val()),
                Id_tema : ($('#Id_tema').val()),
                Id_subtema : subm,
                Justificacion :  ($('#Justificacion').val()),
                Id_usuario :  Id_usuario_1,
                Correo_electronico : correo_electronico
            };
            $.ajax({
                url: 'p_registro_permisos_funcionario',
                data: { obj:obj },
                type: 'POST',
                success: function (response) {
                    let HB = JSON.parse(response);
                    // console.log(response);
                    if (HB.status == 1){
                        f_permisos($('#Texto_buscar').val());
                        // $('#Texto_buscar').val("");
                        $('#Funcionario').val("");
                        $('#Unidad').val();
                        Id_codigo_cargo_1: Id_codigo_cargo;
                        $('#Cargo').val("");
                        $('#Situacion_actual').val("");
                        $('#Usuario').val("");
                        $('#Id_habilitar').val(0);
                        $('#Id_Perfil').val(0);
                        $('#Fecha_fin_rol').val("");
                        $('#Id_tema').val(0);
                        _options = "";
                        $('#Id_subtema').html(_options);
                        $('#Id_subtema').selectpicker('refresh')
                        $('#Justificacion').val("");
                        Id_usuario :  Id_usuario_1;
                        $('#Unidad').val(""),
                        Swal.fire('Señor(@) funcionario', 'el registro fue exitoso', 'success' );
                        return false;
                    }
                    else if(HB.status == 2){
                        $('#Id_habilitar').val(0);
                        $('#Id_Perfil').val(0);
                        $('#Fecha_fin_rol').val("");
                        $('#Id_tema').val(0);
                        _options = "";
                        $('#Id_subtema').html(_options);
                        $('#Id_subtema').selectpicker('refresh')
                        $('#Justificacion').val("");
                        Id_usuario =0;
                        Id_usuario_1 = 0;
                        f_permisos($('#Texto_buscar').val());
                        Swal.fire('Señor(@) funcionario', 'el registro fue actualizado satisfactoriamente', 'success' );
                        return false;
                    }else{
                        Swal.fire('Señor(@) funcionario', 'el registro no fue exitoso', 'error' );
                        return false;
                    }
                },
                error: function (error) {
                    console.log(error);
                }
            });
            return false;      
        });
});


function f_permisos(Identificacion){
    $("#mytable_permisos").DataTable({
        destroy: true,
        paging: true,
        ajax: {
                "url": 'f_permisos',
                "type": 'POST',
                "datatype": "json",
                "data": { Identificacion : Identificacion },
            },
            "columnDefs": [
                { orderable: false, targets: 0 }
            ],
            "columns": [
                { title: "N°", data: 0 },
                { title: "Identificación", data: 16, class:"form-control-label" },
                { title: "Funcionario", data: 2, class:"form-control-label" },  
                { title: "Cargo", data: 4, class:"form-control-label" },
                { title: "Unidad", data: 5, class:"form-control-label" },
                { title: "Habilitado", data: 7, class:"form-control-label" },
                { title: "Perfil", data: 9, class:"form-control-label" },
                { title: "Tema", data: 11, class:"form-control-label" },
                { title: "Subtema", data: 13, class:"form-control-label" },
                { title: "Justificación", data: 14, class:"form-control-label" },
                { title: "Fecha fin rol", data: 15, class:"form-control-label" },
                { title: "Editar", "data": null, "responsive": true,  "scrollY": "10000px", "render": function (data, type, row) {return `<button id="Btn_editar_habilidad" onclick="f_editar_permiso(${data[1]})" data-type="button" class="btn btn-secondary ripple">Editar</button>`;}}, 
                { title: "Eliminar", "data": null, "responsive": true,  "scrollY": "10000px", "render": function (data, type, row) {return `<button id="Btn_eliminar_habilidad" onclick="f_eliminar_permiso(${data[1]})" data-type="button" class="btn btn-danger">Eliminar</button>`;}},     
            ],
            lengthMenu: [
                [5, 10, 50, -1],
                ['5', '10', '50', 'Todos']
            ],
        });
}


function f_editar_permiso(Id_usuario){
    $.ajax({
            url: 'f_editar_permiso',
            data: {Id_usuario:Id_usuario},
            type: 'POST',
                success: function (response) {
                    let HB = JSON.parse(response);
                    // console.log(response); 
                    if((HB.status == 1) && (HB.data1.Codigo == 4)){
                        $('#Funcionario').val( HB.data1.Respuesta['GRAD_ALFABETICO'] +' '+ HB.data1.Respuesta['NOMBRES'] +' '+ HB.data1.Respuesta['APELLIDOS']);
                        $('#Unidad').val(HB.data1.Respuesta['FISICA'] );  
                        $('#Cargo').val(HB.data1.Respuesta['CARGO_ACTUAL'] );
                        Id_codigo_cargo = HB.data1.Respuesta['CODIGO_CARGO'];  
                        $('#Situacion_actual').val(HB.data1.Respuesta['SITUACION_LABORAL']);
                        $('#Usuario').val(HB.data1.Respuesta['USUARIO_EMPRESARIAL']);
                        correo_electronico = HB.data1.Respuesta['CORREO_ELECTRONICO'];

                        Id_usuario_1 = HB.data[0][1];    
                        Id_habilitar_1 = HB.data[0][2];
                        f_consultar_opcion_habilitar();
                        Id_Perfil_1 = HB.data[0][4];
                        f_consultar_perfil();
                        Id_tema_1 = HB.data[0][6];
                        f_visualiza_temas();              
                        Id_subtema_1 = HB.data[0][8];
                        f_visualiza_subtemas();
                        $('#Justificacion').val(HB.data[0][10]); 
                        $('#Fecha_fin_rol').val(HB.data[0][11]);
                        f_permisos(HB.data[0][12]);
                       
                        Swal.fire({ title: "Señor funcionario", text: "ahora puede editar el documento", type: "success"});
                        return true;
                    }
                    
                },
                error: function (error) {
                console.log(error);
            }
        });
}

function f_eliminar_permiso(Id_usuario){
    $.ajax({
        url: 'f_eliminar_permiso',
        data: {Id_usuario:Id_usuario},
        type: 'POST',
            success: function (response) {
                let Rta = JSON.parse(response);
                // console.log(response); 
                if(Rta.status == 'OK'){
                    f_permisos($('#Texto_buscar').val());
                    Swal.fire({ title: "Señor funcionario", text: "el documento fue eliminado exitosamente", type: "success"});
                    return true;
                }
            },
            error: function (error) {
            console.log(error);
        }
    });
}


$(function () {
    $('#btn_limpiar_campos').click(function() {
        $('#Texto_buscar').val("");
        $('#Funcionario').val("");
        $('#Unidad').val();
        Id_codigo_cargo_1: Id_codigo_cargo;
        $('#Cargo').val("");
        $('#Situacion_actual').val("");
        $('#Usuario').val("");
        $('#Id_habilitar').val(0);
        $('#Id_Perfil').val(0);
        $('#Fecha_fin_rol').val("");
        $('#Id_tema').val(0);
        _options = "";
        $('#Id_subtema').html(_options);
        $('#Id_subtema').selectpicker('refresh');
        $('#Justificacion').val("");
        Id_usuario :  Id_usuario_1;
        $('#Unidad').val("");
    });
});