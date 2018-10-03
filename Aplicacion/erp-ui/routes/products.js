var express = require('express');
var router = express.Router();
var requestP = require('request-promise');
var session = require('express-session');

var gatewayURI = "http://localhost:8080/productos/";


router.get('/all', function(req, res, next) {
    ssn= req.session;

    var jsondata = {};
    var header =
    {
      "Authorization": "Bearer "+ssn.token
    };
    requestP({
      "method":"GET",
      "uri": gatewayURI,
      "headers": header,
      "json": true
    }).then(function(body){
      jsondata=body;
      res.render('products-all', { params:
        {title: 'Productos',
        customscript:'products.js',
        data:JSON.stringify(jsondata),
        data2:jsondata
      } });
    }).catch(function(err){
      //GG
      console.log(err);
      res.render('products-all', { params:
        {title: 'Productos',
        customscript:'products.js',
        data:JSON.stringify(jsondata),
        data2:{}
      } });
    });
});

router.get('/add', function(req, res, next) {
  ssn= req.session;
  var header =
  {
    "Authorization": "Bearer "+ssn.token
  };
  var nameForm = req.query.name;
  requestP({
    "method":"POST",
    "uri": gatewayURI,
    "headers": header,
    "formData": {name: nameForm}
  }).then(function(body){
    console.log("exito");
    res.redirect("/products/all");
  });
});

router.post('/upd', function(req, res, next) {
  ssn= req.session;
  var header =
  {
    "Authorization": "Bearer "+ssn.token
  };
  var nameForm = req.body.namep;
  var idForm = req.body.idp;

  requestP({
    "method":"PUT",
    "uri": gatewayURI+idForm,
    "headers": header,
    "formData": {name: nameForm}
  }).then(function(body){
    console.log("exito");
    res.redirect("/products/all");
  });
});

router.post('/del', function(req, res, next) {
  ssn= req.session;
  var header =
  {
    "Authorization": "Bearer "+ssn.token
  };
  var idForm = req.body.idd;
  var url = gatewayURI+idForm;
  console.log(url);
  requestP({
    "method":"DELETE",
    "uri": url,
    "headers": header
  }).then(function(body){
    console.log("exito");
    res.redirect("/products/all");
  });
});

module.exports = router;
