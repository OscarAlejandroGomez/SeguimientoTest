let Id_registro_url_1 = 0;
let Id_gestion_documento_1 = 0;
let Id_tema_1 =0;
function f_visualizar_subtemas_aprobados(Id_tema){
    Id_tema_1 = Id_tema;
    let Lote="";
    $.ajax({
            url: 'f_visualizar_subtemas_aprobados',
            data: {Id_tema :Id_tema },
            type: 'POST',
                success: function (response) {
                    var subtemas = JSON.parse(response);
                    if ((subtemas.status == 0) || (subtemas.data.length ==0)){  
                        let Lote="";
                                let divPanelSubtemas = document.getElementById('divPanelSubtemas');
                                divPanelSubtemas.style["display"] = "none"; 
                                document.getElementById('divPanelSubtemas').innerHTML = Lote;                             
                    }else {
                            for (let i = 0; i < subtemas.data.length; i++) {
                                if (subtemas.data[i][5] == 1) { 
                                    Id_registro_url_1 = subtemas.data[i][6];
                                    Id_gestion_documento_1 = subtemas.data[i][7];
                                    if (subtemas.data.length != i) {  
                                        for (let k = 0; k < 1; k++) {
                                            Lote+=`<div class="col-lg-12 col-md-12 mt-3">
                                                <nav class="nav nav-pills flex-column flex-sm-row">
                                                    <a class="flex-sm-fill nav-link active" href="javascript:f_consulta_documento(${subtemas.data[i][1]},${subtemas.data[i][2]})" style="background: linear-gradient(179deg, rgba(3,43,87,1) 25%, rgb(0 106 141) 62%) !important;">${subtemas.data[i][3]}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp${subtemas.data[i][4]}</a>
                                                </nav>
                                            </div>`;
                                        }
                                        f_tabla_onsevaciones_documento(Id_registro_url_1);
                                        let divPanelSubtemas = document.getElementById('divPanelSubtemas');
                                        divPanelSubtemas.style["display"] = "block"; 
                                        document.getElementById('divPanelSubtemas').innerHTML = Lote; 
                                        Swal.fire({ title: "Señor funcionario...", text: "...tiene documentos aprobados en esta sección.", type: "success"});
                                      
                                    }   
                                } else{
                                    if (subtemas.data.length != i) {  
                                        for (let k = 0; k < 1; k++) {
                                            Lote+=`<div class="col-lg-12 col-md-12 mt-3">
                                                <nav class="nav nav-pills flex-column flex-sm-row">
                                                    <a class="flex-sm-fill nav-link active" href="javascript:f_consulta_documento(${subtemas.data[i][1]},${subtemas.data[i][2]})" style="background: linear-gradient(179deg, rgba(219, 223, 228) 25%, rgb(87, 125, 138) 62%) !important;">${subtemas.data[i][3]}</a>
                                                </nav>
                                            </div>`;
                                        }
                                        let divPanelSubtemas = document.getElementById('divPanelSubtemas');
                                        divPanelSubtemas.style["display"] = "block"; 
                                        document.getElementById('divPanelSubtemas').innerHTML = Lote;   
                                    }   

                                }                             
                            }
                    }
                },
                error: function (error) {
                console.log(error);
            }
        });
}



function f_consulta_documento(Id_tema,Id_subtema){
    let divPaneldocumnt="";
    let divPaneldatosdocument="";
    $.ajax({
        url: 'visualiza_documento',
        data: {Id_tema:Id_tema, Id_subtema:Id_subtema},
        type: 'POST',
            success: function (response) {
                let url = JSON.parse(response);
                // console.log(response); 
                if(url.status == 1){
                    if (url.data.length > 0) {
                        for (let i = 0; i < url.data.length; i++) {
                            $("#contexto_documento").val(url.data[i][2])
                            Id_registro_url_1 = url.data[i][0];
                            f_tabla_onsevaciones_documento(Id_registro_url_1);
                            divPaneldatosdocument = `<div style="color:black;" class="form-control-label mb-3" id="tema"><strong>${url.data[i][3]}</strong></div><div  class="form-control-label" style="color:black;" id="subtema"><strong>${url.data[i][4]}</strong></div>`;
                            divPaneldocumnt = `<div class="col-md-12">
                            <embed id="viewer" style="width: 100%; height: 500px;" class="pdfViewer" src="${url.data[i][1]}"></embed>
                            </div>`;
                        }
                        let divPaneldatosdocumento = document.getElementById('divPaneldatosdocumento');
                        divPaneldatosdocumento.style["display"] = "block"; 
                        document.getElementById('divPaneldatosdocumento').innerHTML = divPaneldatosdocument;
                        let divPaneldocumento = document.getElementById('divPaneldocumento');
                        divPaneldocumento.style["display"] = "block"; 
                        document.getElementById('divPaneldocumento').innerHTML = divPaneldocumnt;
                        $("#basic-modal").modal("show"); 
                    }
                }else{
                    $("#basic-modal1").modal("show"); 
                }
            },
            error: function (error) {
            console.log(error);
        }
    });
}



$(function () {
    $('#btn_aprobar_documento').click(function() {
        $.ajax({
            url: 'p_aprobar_documento_aprobado',
            data: {Id_registro_url_1:Id_registro_url_1, Id_gestion_documento_1:Id_gestion_documento_1},
            type: 'POST',
                success: function (response) {
                    let Rta = JSON.parse(response);
                    if(Rta.status == 'OK'){
                        f_visualizar_subtemas_aprobados(Id_tema_1);
                        Id_tema_1 =0;
                        Swal.fire({ title: "Señor funcionario", text: "el documento fue aprobado exitosamente, por tanto, será visible al Director General de la Policía Nacional.", type: "success", target: document.getElementById('basic-modal')});
                        let t=setTimeout("redirecciona()",1000); 
                        return true;
                    }else{
                        Swal.fire({ title: "Señor funcionario", text: "el documento no pudo ser aprobado por favor presiones f5 e intente nuevamento.", type: "warning", target: document.getElementById('basic-modal')});
                        return true;
                    }
                },
                error: function (error) {
                console.log(error);
            }
        });
    });
});

function redirecciona(){
    $('#basic-modal').modal('hide');  
    location.href ="/revisar_documentos"; 
}

function f_devolver_documento() {
    $('#modal_devolver_documento').modal('show');
}


// $(function () {
//     $('#btn_devolver_documento').click(function() 
    
    function f_devolver_aprobado_aprobado(){
        let Mensaje_revisor = $('#Mensaje_revisor').val()
        $.ajax({
            url: 'p_devolver_documento_aprobado',
            data: {Id_registro_url_1:Id_registro_url_1, Id_gestion_documento_1:Id_gestion_documento_1, Mensaje_revisor:Mensaje_revisor},
            type: 'POST',
                success: function (response) {
                    let Rta = JSON.parse(response);
                    if(Rta.status == 'OK'){
                        f_visualizar_subtemas_aprobados(Id_tema_1);
                        Id_tema_1 =0;
                        Swal.fire({ title: "Señor funcionario", text: "el documento fue devuelto, por tanto, será visible al funcionario responsable del cargue de la información..", type: "success", target: document.getElementById('modal_devolver_documento')});
                        let t=setTimeout("redirecciona()",1000); 
                        return true;
                    }else{
                        Swal.fire({ title: "Señor funcionario", text: "el documento no pudo ser aprobado por favor presiones f5 e intente nuevamento.", type: "warning", target: document.getElementById('modal_devolver_documento')});
                        return true;
                    }
                },
                error: function (error) {
                console.log(error);
            }
        });
    }

    function redirecciona(){
        $('#basic-modal').modal('hide');  
        location.href ="/documentos_aprobados"; 
    }



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
    