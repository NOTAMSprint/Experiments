$(document).ready(function(){
    
    $("#submit").click(function(e){
        e.preventDefault()
        var data={}
        $("input").each(function(i,v){
            data[$(v).attr("name")]=$(v).val().trim()
        })
        console.log(data)
        $("#printzone").text("I get you that, please wait a few seconds ...")
        $.get("ENDPOINTGOESHERE",
            data,
            function(res){
                $("#printzone").text(JSON.stringify(res))
            }
        
        )
    })
    
})