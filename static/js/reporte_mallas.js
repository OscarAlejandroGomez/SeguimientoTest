$(document).ready(function () {
    f_consulta_periodos();
    f_visualiza_anios();
    f_consulta_materias();
    f_listar_grado_escolar();
});

function f_consulta_periodos() {
    let Estado = 1;
    $.ajax({
        url: 'f_consulta_periodos',
        data: { Estado: Estado },
        type: 'POST',
        success: function (response) {
            var Periodos_escolares = JSON.parse(response);
            console.log(response);
            var opt = 0;
            var opt1 = "No hay datos";
            var auxArr = [];
            if (Periodos_escolares.data.length == 0) {
                auxArr = ""
                $('#Id_periodo').empty(0);
                $('#Id_periodo').change(0);
            } else {
                for (let i = 0; i <= Periodos_escolares.data.length; i++) {
                    if (Periodos_escolares.data.length != i) {
                        for (let k = 0; k <= Periodos_escolares.data[i].length; k++) {
                            if (k == 0) {
                                opt = Periodos_escolares.data[i][k];
                            }
                            else if (k == 1) {
                                opt1 = Periodos_escolares.data[i][k];
                            }
                        }
                        auxArr[i + 1] = "<option value='" + opt + "'>" + opt1 + "</option>";
                    } else {
                        auxArr[0] = "<option value='0'> Seleccione... </option>";
                    }
                }
                $('#Id_periodo').empty();
                $('#Id_periodo').append(auxArr.join(''));
                $('#Id_periodo').change();
            }
        },
        error: function (error) {
            console.log(error);
        }
    });
    return false;
}

function f_visualiza_anios() {
    let Estado = 1;
    $.ajax({
        url: 'f_visualiza_anios',
        data: { Estado: Estado },
        type: 'POST',
        success: function (response) {
            var anios = JSON.parse(response);
            console.log(response);
            var opt = 0;
            var auxArr = [];
            if (anios.data.length == 0) {
                auxArr = ""
                $('#Anio').empty(0);
                $('#Anio').change(0);
            }else{
                for (let i = 0; i <= anios.data.length; i++) {
                    if (anios.data.length != i) {
                        opt = anios.data[i];  
                        auxArr[i + 1] = "<option value='" + opt + "'>" + opt + "</option>";
                    } 
                    else{
                        auxArr[0] = "<option value='0'> Seleccione... </option>";
                    }
                }
                $('#Anio').empty();
                $('#Anio').append(auxArr.join(''));
                $('#Anio').change();
            }
        },
        error: function (error) {
            console.log(error);
        }
    });
    return false;
}

function f_consulta_materias() {
    let Estado = 1;
    $.ajax({
        url: 'f_consulta_materias',
        data: { Estado: Estado },
        type: 'POST',
        success: function (response) {
            var Materias = JSON.parse(response);
            console.log(response);
            var opt = 0;
            var opt1 = "No hay datos";
            var auxArr = [];
            if (Materias.data.length == 0) {
                auxArr = ""
                $('#Id_materia').empty(0);
                $('#Id_materia').change(0);
            } else {
                for (let i = 0; i <= Materias.data.length; i++) {
                    if (Materias.data.length != i) {
                        for (let k = 0; k <= Materias.data[i].length; k++) {
                            if (k == 0) {
                                opt = Materias.data[i][k];
                            }
                            else if (k == 1) {
                                opt1 = Materias.data[i][k];
                            }
                        }
                        auxArr[i + 1] = "<option value='" + opt + "'>" + opt1 + "</option>";
                    } else {
                        auxArr[0] = "<option value='0'> Seleccione... </option>";
                    }
                }
                $('#Id_materia').empty();
                $('#Id_materia').append(auxArr.join(''));
                $('#Id_materia').change();
            }
        },
        error: function (error) {
            console.log(error);
        }
    });
    return false;
}

function f_listar_grado_escolar() {
    let Vigente = 1;
    $.ajax({
        url: 'f_listar_grados',
        data: { data: Vigente },
        type: 'POST',
        success: function (response) {
            var grado_E = JSON.parse(response);
            console.log(response);
            var opt = 0;
            var opt1 = "No hay datos";
            var auxArr = [];
            if (grado_E.data.length == 0) {
                auxArr = ""
                $('#Id_grado_escolar').empty(0);
                $('#Id_grado_escolar').change(0);
            } else {
                for (let i = 0; i <= grado_E.data.length; i++) {
                    if (grado_E.data.length != i) {
                        for (let k = 0; k <= grado_E.data[i].length; k++) {
                            if (k == 0) {
                                opt = grado_E.data[i][k];
                            }
                            else if (k == 1) {
                                opt1 = grado_E.data[i][k];
                            }
                        }
                        auxArr[i + 1] = "<option value='" + opt + "'>" + opt1 + "</option>";
                    } else {
                        auxArr[0] = "<option value='0'> Seleccione... </option>";
                    }
                }
                $('#Id_grado_escolar').empty();
                $('#Id_grado_escolar').append(auxArr.join(''));
                $('#Id_grado_escolar').change();
            }
        },
        error: function (error) {
            console.log(error);
        }
    });
    return false;
}

$(function () {
    $('#Btn_generar_reporte_mallas').click(function(){
        let Anio =  parseInt($('#Anio').val());
        let Id_periodo = parseInt($('#Id_periodo').val());
        let Id_materia = parseInt($('#Id_materia').val());
        let Id_grado_escolar = parseInt($('#Id_grado_escolar').val());
        if (Anio == "0") {
            Swal.fire({ title: "Señor(a) docente", text: "por favor seleccione el año", type: "error", target: document.getElementById('living-room') });
            return true;
        }
        if (Id_periodo == "0") {
            Swal.fire({ title: "Señor(a) docente", text: "por favor seleccione periodo", type: "error", target: document.getElementById('living-room') });
            return true;
        }
        if (Id_materia == "0") {
            Swal.fire({ title: "Señor(a) docente", text: "por favor seleccione el área", type: "error", target: document.getElementById('living-room') });
            return true;
        }
        if (Id_grado_escolar == "0") {
            Swal.fire({ title: "Señor(a) docente", text: "por favor seleccione el grado", type: "error", target: document.getElementById('living-room') });
            return true;
        }
        $.ajax({
                url: 'Generar_reporte_mallas',
                data: {Anio:Anio, Id_periodo:Id_periodo, Id_materia:Id_materia, Id_grado_escolar:Id_grado_escolar},
                type: 'POST',
                    success: function (response) {
                        let Rta = JSON.parse(response);
                        console.log(response); 
                        if(Rta.data == 1){
                            Swal.fire({ title: "Señor(a) docente", text: "el reporte fue generado exitosamente", type: "success", target: document.getElementById('living-room') });
                            return true;
                        }else{
                            Swal.fire({ title: "Señor(a) docente", text: "no hay información para generar éste reporte", type: "warning", target: document.getElementById('living-room') });
                            return true;
                        }
                    },
                    error: function (error) {
                    console.log(error);
                }
        });
    });
});

function e(q) {
    document.body.appendChild( document.createTextNode(q) );
    document.body.appendChild( document.createElement("BR") );
}
function inactividad() {
    window.location.href = "/logout"
}
var t=null;
function contadorInactividad() {
    t=setTimeout("inactividad()",180000);
}
window.onblur=window.onmousemove=function() {
    if(t) clearTimeout(t);
    contadorInactividad();
} 