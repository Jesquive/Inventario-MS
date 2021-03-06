var express = require('express');
var router = express.Router();
var requestP = require('request-promise');
var session = require('express-session');

var gatewayURI = "http://localhost:8080/products/";


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

router.get('/:id', function(req, res, next) {
  ssn= req.session;
  var providerURL = "http://localhost:3000/providers/name/";
  var jsondata = {};
  var header =
  {
    "Authorization": "Bearer "+ssn.token
  };
  requestP({
    "method":"GET",
    "uri": gatewayURI+req.params.id,
    "headers": header,
    "json": true
  }).then(function(body){
    jsondata=body;
    res.render('single-product', { params:
      {title: 'Products',
      customscript:'single-product.js',
      data: JSON.stringify({url: providerURL+body.provider}),
      data2:jsondata
    } });
  }).catch(function(err){
    //GG
    console.log(err);
    res.render('products-all', { params:
      {title: 'Products',
      customscript:'products.js',
      data:JSON.stringify(jsondata),
      data2:{}
    } });
  });
});


router.post('/add', function(req, res, next) {
  ssn= req.session;
  console.log(ssn.id);
  var sendData = 
  {
    name: req.body.name,
    code: req.body.code,
    stock: req.body.stock,
    patent: req.body.patent,
    provider: req.body.provider,
    aggregated_by: 1
  };
  var header =
  {
    "Authorization": "Bearer "+ssn.token
  };
  requestP({
    "method":"POST",
    "uri": gatewayURI,
    "headers": header,
    "formData": sendData
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
  var sendData = 
  {
    name: req.body.nameP,
    stock: req.body.stockP,
  };
  var idForm = req.body.idp;

  requestP({
    "method":"PUT",
    "uri": gatewayURI+idForm,
    "headers": header,
    "formData": sendData
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
