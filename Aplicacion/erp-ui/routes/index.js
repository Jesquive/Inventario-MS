var express = require('express');
var router = express.Router();

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

router.get('/signin', function(req, res, next) {
  res.render('signin', { params:
    {
    }
  });
});

module.exports = router;
