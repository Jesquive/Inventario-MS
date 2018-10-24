$(document).ready(function(){
  $('#products-all').DataTable( {
    /*"language": {
      "url": "//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json"
    },*/
    data: data,
    columns: [
        { data: 'id' },
        { data: 'name' },
        { data: 'stock' },
        { data: 'provider' }

    ]
  });
});
