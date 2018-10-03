var express = require('express');
var router = express.Router();
var session = require('express-session');

/* GET users listing. */
router.get('/', function(req, res, next) {
  res.send('respond with a resource');
});

module.exports = router;
//C:\Users\Jesquive\Documents\Proyectos\Microservicios\Inventario-MS\Aplicacion\erp-ui>set DEBUG=erp-ui:* & npm start
