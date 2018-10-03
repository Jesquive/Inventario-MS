$(document).ready(function(){

  if(!(mes === "")){
    $.notify({
        icon: 'pe-7s-gift',
        message: mes,
        },{
          type: 'info',
          timer: 4000
        });
  }

});
