$(document).ready(function(){

    console.log(data.url);

    $("#providerData").click(function(){
        $.ajax({
            url: data.url,
            type:"GET",
            success: function(result){
                $.notify({
                    icon: 'nc-air-baloon',
                    message: "Provider Loaded correctly"
                    },{
                      type: 'info',
                      timer: 4000
                    });
                $('#ProviderCard').css('display','inline-block');
                console.log(result);
            },
            error: function(err){
                $.notify({
                    icon: 'nc-simple-remove',
                    message: "Ups!, an error has ocurred. Please wait and try again"
                    },{
                      type: 'danger',
                      timer: 4000
                    });
                console.log("error "+err);
            }
        });
    });
});