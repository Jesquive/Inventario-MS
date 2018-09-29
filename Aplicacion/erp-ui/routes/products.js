var express = require('express');
var router = express.Router();
var requestP = require('request-promise');

router.get('/all', function(req, res, next) {
    var jsondata = {}

    requestP({
      "method":"GET",
      "uri": "http://127.0.0.1:5000/productos/",
      "json": true
    }).then(function(body){
      jsondata=body;
      res.render('products-all', { params:
        {title: 'Productos',
        customscript:'products.js',
        data:JSON.stringify(jsondata)
      } });
    }).catch(function(err){
      //GG
      console.log(err);
      res.render('products-all', { params:
        {title: 'Productos',
        customscript:'products.js',
        data:JSON.stringify(jsondata)
      } });
    });
});

router.get('/add', function(req, res, next) {
  var nameForm = req.query.name;
  requestP({
    "method":"POST",
    "uri": "http://127.0.0.1:5000/productos/",
    "formData": {name: nameForm}
  }).then(function(body){
    console.log("exito");
    res.redirect("/products/all");
  });
});

router.post('/upd', function(req, res, next) {
  var nameForm = req.body.namep;
  var idForm = req.body.idp;

  requestP({
    "method":"PUT",
    "uri": "http://127.0.0.1:5000/productos/"+idForm,
    "formData": {name: nameForm}
  }).then(function(body){
    console.log("exito");
    res.redirect("/products/all");
  });
});

router.post('/del', function(req, res, next) {
  var idForm = req.body.idd;
  var url = "http://127.0.0.1:5000/productos/"+idForm;
  console.log(url);
  requestP({
    "method":"DELETE",
    "uri": url
  }).then(function(body){
    console.log("exito");
    res.redirect("/products/all");
  });
});




module.exports = router;
