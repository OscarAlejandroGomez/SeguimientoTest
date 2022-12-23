function create_room(){
    $.ajax({
        url:'/link_create_room',
        method:'post',
        data:{
            name_room: $("#input-create").text()
        }
    }).done(function(data){
        if(data.state == 'error'){
            let message = data.result;
            alert(message);
        }
        else if(data.state == 'ok'){
            let link = window.location+data.result;  
            let message = "Puedes unirte a la sesion con: " + link;
            alert(message);
            location.href = link
            //location.href = "/link_join_room";
            // location.href ="/revisar_documentos"; 
        }
    });
}

$(".button-create").click(function(){
    create_room();
});

$("#input-create").keyup(function(event){
    if(event.key == 'Enter'){
        if ( $("#input-create").text().trim() == ""){
            $("#input-create").text("")
        }
        else{
            create_room();
            $("#input-create").text("")
        }
    }
    
})
$("#input-create").keydown(function(event){
    if(event.key == 'Enter'){
        $("#input-create").html($("#input-create").text())
    }
})


$(".button-join").click(function(){
    let link = $("#input-join").text();
    location.href = link;
});

$("#input-join").keyup(function(event){
    if(event.key == 'Enter'){
        let link = $("#input-join").text();
        location.href = link;
    }
})