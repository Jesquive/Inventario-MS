var express = require('express');
// Cargamos el controlador
var ProviderController = require('../controllers/provider');
var md_auth = require('../middlewares/authenticated');
var router = express.Router();

/* GET  listing. */
router.get('/', ProviderController.getAllProviders);
router.post('/create', ProviderController.createProvider);
router.post('/update/:id', ProviderController.providerUpdate);
router.post('/delete/:id', ProviderController.providerDelete);
router.post('/read/:id', ProviderController.providerDetails);
router.post('/read/name/:name', ProviderController.providerDetailsByName);



module.exports = router;
