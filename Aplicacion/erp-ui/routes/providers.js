var express = require('express');
var router = express.Router();
var requestP = require('request-promise');
var session = require('express-session');

var gatewayURI = "http://localhost:8080/providers/";


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

router.get('/name/:name',function(req,res,next){
    ssn= req.session;
    var jsondata = {};
    var header =
    {
      "Authorization": "Bearer "+ssn.token
    };
    requestP({
      "method":"POST",
      "uri": gatewayURI+'read/name/'+req.params.name,
      "headers": header,
      "json": true
    }).then(function(body){
    console.log("geeeeeeeeeeeeeeeeeeeeeeeeeee");
    console.log(body);

      jsondata=body;
      res.send(jsondata);
    }).catch(function(err){
      //GG
    console.log("ASDGSDFHGSDFH");

      console.log(err);
      res.send(jsondata);
    });
});

router.post('/add', function(req, res, next) {
  ssn= req.session;
  var contactOBJ = {
    contact1: req.body.contact1,
    contact2: req.body.contact2,
    contact3: req.body.contact3
  };
  var sendData = 
  {
    name: req.body.name,
    contact: contactOBJ,
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
