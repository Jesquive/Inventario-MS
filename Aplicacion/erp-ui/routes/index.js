var express = require('express');
var router = express.Router();
var session = require('express-session');
var ssn;


/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { params:
    {
    title: 'Dashboard' ,
    customscript: 'index.js',
    data:JSON.stringify({casa:'gg'})
    }
  });
});

module.exports = router;
