$(document).ready(function () {
  f_estado_documento();
  f_visualiza_gestion_documento();
});
   
$('input[type="file"]').on('change', function(){
    var ext = $( this ).val().split('.').pop();
    if ($( this ).val() != '') {
      if(ext == "pdf"){

      }
      else
      {
        $( this ).val('');
        Swal.fire({ title: "Señor funcionario", text: "la extensión no es permitida: " + ext, type: "warning"});
      }
    }
  });



function p_eliminar_documento(Id_documento){
        $.ajax({
            url: 'p_eliminar_documento',
            data: {Id_documento:Id_documento},
            type: 'POST',
                success: function (response) {
                    let Rta = JSON.parse(response);
                    if(Rta.status == 'OK'){
                        Id_registro_url_1=0;
                        Swal.fire({ title: "Señor funcionario", text: "el documento fue eliminado exitosamente", type: "success"});
                        let t=setTimeout("redirecciona()",1000);   
                        return true;
                    }
                },
                error: function (error) {
                console.log(error);
            }
        });
}
function redirecciona(){
    location.href ="/cargar_archivo";   
}


var Id_estado_documento_1=0;
function f_estado_documento() {
        let Estado = 1;
        $.ajax({
            url: 'f_estado_documento',
            data: { Estado: Estado },
            type: 'POST',
            success: function (response) {
                let documento = JSON.parse(response);
                let opt = 0;
                let opt1 = "No hay datos";
                let auxArr = [];
                if (documento.data.length == 0) {
                    auxArr = ""
                    $('#Id_estado_documento').empty(0);
                    $('#Id_estado_documento').change(0);
                } else {
                    for (let i = 0; i <= documento.data.length; i++) {
                        if (documento.data.length != i) {
                            for (let k = 0; k <= documento.data[i].length; k++) {
                                if (k == 0) {
                                    opt = documento.data[i][k];
                                }
                                else if (k == 1) {
                                    opt1 = documento.data[i][k];
                                }
                            }
                            auxArr[i + 1] = "<option value='" + opt + "'>" + opt1 + "</option>";
                        } else {
                            auxArr[0] = "<option value='0'> Por gestionar... </option>";
                        }
                    }
                    $('#Id_estado_documento').empty();
                    $('#Id_estado_documento').append(auxArr.join(''));
                    $('#Id_estado_documento').change();
                    if(Id_estado_documento_1!==0){
                        $('#Id_estado_documento').val(Id_estado_documento_1);
                    }
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
        return false;
}




// $(function () {
//     $('#btn_envia_documento').click(function() 
    
   function envia_documento(){
        $('#Id_estado_documento').val();
        $('#Numero_gepol').val();
        $('#Contexto_documento').val();
        if ($('#Mensaje_funcionario').val()==""){
            Swal.fire({ title: "Señor funcionario", text: "Por favor escriba una anotación.", type: "error"});
            return false;
        }else{
            envia_menaje();
            let obj = {
                Id_estado_documento : ($('#Id_estado_documento').val()),
                Numero_gepol : ($('#Numero_gepol').val()),
                Contexto_documento : ($('#Contexto_documento').val()),
                Id_gestion_documento : Id_gestion_documento_1
            };
            $.ajax({
                url: 'p_enviar_documento_a_SEPRI',
                data: {obj:obj},
                type: 'POST',
                    success: function (response) {
                        let Rta = JSON.parse(response);
                        if(Rta.status == 'OK'){
                            
                            Swal.fire({ title: "Señor funcionario", text: "el documento fue enviado a revisión exitosamente, por favor, atento en caso de ser necesario una corrección.", type: "success"});
                            let t=setTimeout("redirecciona()",1000); 
                            return true;
                        }else{
                            Swal.fire({ title: "Señor funcionario", text: "la información del documento fue actualizada exitosamente, por favor, verificar recurrentemente ante retorno a corrección.", type: "success"});
                            let t=setTimeout("redirecciona()",1000); 
                            return true;
                        }
                    },
                    error: function (error) {
                    console.log(error);
                }
            });
        }
   }
    // });
// });

function redirecciona(){ 
    f_tabla_onsevaciones_documento(Id_registro_url_1);
    location.href ="/cargar_archivo"; 
}

let Id_registro_url_1=0;
var Id_gestion_documento_1=0;
function f_visualiza_gestion_documento(){
    let Estado= 1;
    $.ajax({
        url: 'f_visualiza_gestion_documento',
        data: {Estado:Estado},
        type: 'POST',
            success: function (response) {
                let Rta = JSON.parse(response);
                if((Rta.status == 'OK') && (Rta.data.length>0)){
                    Id_gestion_documento_1 = Rta.data[0][0];
                    Id_estado_documento_1 = Rta.data[0][1];
                    f_estado_documento();
                    $('#Numero_gepol').val(Rta.data[0][3]);
                    $('#Contexto_documento').val(Rta.data[0][4]);
                    Id_registro_url_1 = Rta.data[0][5];
                    f_tabla_onsevaciones_documento(Id_registro_url_1);
                }
            },
            error: function (error) {
            console.log(error);
        }
    });
}



let Id_observacion_1=0;
// $(function () {
//     $('#btn_mensaje_funcionario').click(function() 
    
  function envia_menaje(){
       
        $('#Mensaje_revisor').val();
        $('#Mensaje_z1').val();

        let obj = {
            Mensaje_funcionario : ($('#Mensaje_funcionario').val()),
            // Mensaje_revisor : ($('#Mensaje_revisor').val()),
            // Mensaje_z1 : ($('#Mensaje_z1').val()),
            Id_observacion : Id_observacion_1
        };
        $.ajax({
            url: 'p_enviar_mensaje',
            data: {obj:obj},
            type: 'POST',
                success: function (response) {
                    let Rta = JSON.parse(response);
                    if(Rta.status == 'OK'){
                        
                        // Swal.fire({ title: "Señor funcionario", text: "el mensaje fue registrado exitosamente.", type: "success"});
                        // return true;
                    }else{
                        Swal.fire({ title: "Señor funcionario", text: "el mensaje no pudo ser registrado.", type: "warning"});
                        return true;
                    }
                },
                error: function (error) {
                console.log(error);
            }
        });
    }
    // });
// });




function f_tabla_onsevaciones_documento(Id_registro_url_1){
    $("#MyTable_Observaciones_documento").DataTable({
        destroy: true,
        paging: true,
        ajax: {
                "url": 'f_tabla_onsevaciones_documento',
                "type": 'POST',
                "datatype": "json",
                "data": { Id_registro_url_1 : Id_registro_url_1 },
            },
            "columnDefs": [
                { orderable: false, targets: 0 }
            ],
            "columns": [
                { title: "N°", data: 0 },
                { title: "Mensaje funcionario", data: 2, class:"form-control-label" },
                { title: "Mensaje revisor", data: 3, class:"form-control-label" },  
                { title: "Mensaje Director", data: 4, class:"form-control-label" },
                { title: "Fecha registro", data: 5, class:"form-control-label" },
                // { title: "Editar", "data": null, "responsive": true,  "scrollY": "10000px", "render": function (data, type, row) {return `<button id="Btn_editar_observacion" onclick="f_editar_observacion(${data[1]})" data-type="button" class="btn btn-secondary ripple">Editar</button>`;}}, 
                //{ title: "Eliminar", "data": null, "responsive": true,  "scrollY": "10000px", "render": function (data, type, row) {return `<button id="Btn_eliminar_observacion" onclick="f_eliminar_observacion(${data[1]})" data-type="button" class="btn btn-danger">Eliminar</button>`;}},     
            ],
            lengthMenu: [
                [5, 10, 50, -1],
                ['5', '10', '50', 'Todos']
            ],
        });
}


function f_eliminar_observacion(Id_observacion){
    $.ajax({
        url: 'f_eliminar_observacion',
        data: {Id_observacion:Id_observacion},
        type: 'POST',
            success: function (response) {
                let Rta = JSON.parse(response);
                // console.log(response); 
                if(Rta.status == 'OK'){
                    f_tabla_onsevaciones_documento(Id_registro_url_1);
                    Swal.fire({ title: "Señor funcionario", text: "la observación fue eliminada exitosamente", type: "success"});
                    return true;
                }
            },
            error: function (error) {
            console.log(error);
        }
    });
}
