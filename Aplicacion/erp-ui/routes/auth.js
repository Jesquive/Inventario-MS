var express = require('express');
var router = express.Router();
var requestP = require('request-promise');
var session = require('express-session');

var gatewayURI = "http://localhost:8080/auth/";
var ssn;

/*var jsdom = require('jsdom');
const { JSDOM } = jsdom;
const { window } = new JSDOM();
const { document } = (new JSDOM('')).window;
global.document = document;
var $ = jQuery = require('jquery')(window);*/

router.get('/signout', function(req, res, next) {
  ssn= req.session;

  var header =
  {
    "Authorization": "Bearer "+ssn.token
  };
  requestP({
    "method":"POST",
    "uri": gatewayURI+"logout",
    "headers": header,
    "json": true
  }).then(function(body){
    ssn.destroy();
    res.render('signin', { params:
      {
        customscript: 'auth.js',
        message: body.message
      }
    });
  });
});

router.use(function(req,res,next){
  ssn= req.session;
  if(ssn.email || ssn.token)
  {
    res.redirect("/dashboard/all");
  } else
  {
    next();
  }
});

router.get('/signin', function(req, res, next) {
  res.render('signin', { params:
    {
      customscript: 'auth.js',
      message: ''
    }
  });
});

router.get('/register', function(req, res, next) {
  res.render('register', { params:
    {
      customscript: 'auth.js',
      message: ''
    }
  });
});

router.post('/authReg', function(req, res, next) {
  var emailForm = req.body.email;
  var passwForm = req.body.password;

  requestP({
    "method":"POST",
    "uri": gatewayURI+"register",
    "formData": {
      email: emailForm,
      password: passwForm
    }
  }).then(function(body){
    var body = JSON.parse(body);
    res.render('register', { params:{
      customscript: 'auth.js',
      message: body.message
      }
    });
  });
});

router.post('/authLog', function(req, res, next) {
  ssn=req.session;
  var emailForm = req.body.email;
  var passwForm = req.body.password;

  requestP({
    "method":"POST",
    "uri": gatewayURI+"login",
    "formData": {
      email: emailForm,
      password: passwForm
    }
  }).then(function(body){
    var body = JSON.parse(body);
    ssn.email = emailForm;
    ssn.token = body.access_token;
    res.redirect("/dashboard/all");
  });
});

module.exports = router;
