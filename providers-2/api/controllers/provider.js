'use strict'

// Cargamos los modelos para usarlos posteriormente
var Provider = require('../models/provider');


// Conseguir datos de un usuario

exports.getAllProviders=function(req, res){
    Provider.find(function (err, providers) {
        if (err) return next(err);
        res.send(providers);
    })
};

//PUT
exports.createProvider=function(req, res, next){
    let provider = new Provider(
        {
            name: req.body.name,
            contact: {
                contact1: req.body.contact1,
                contact2: req.body.contact1,
                contact3: req.body.contact1

            }
        }
    );
    provider.save(function (err) {
        if (err) {
            return next(err);
        }
        res.send('Provider Created successfully')
    })
};

//GET :ID
exports.providerDetails = function (req, res) {
    Provider.findById(req.params.id, function (err, provider) {
        if (err) return next(err);
        res.send(provider);
    })
};

//GET BY NAME
exports.providerDetailsByName = function (req, res) {
    Provider.find({name: req.params.name}, function (err, provider) {
        console.log("gerer");
        if (err) return next(err);
        res.send(provider);
    })
};

//UPDATE
exports.providerUpdate = function (req, res) {
    Provider.findByIdAndUpdate(req.params.id, {$set: req.body}, function (err, provider) {
        if (err) return next(err);
        res.send('Product udpated.');
    });
};

//DELETE
exports.providerDelete = function (req, res) {
    Provider.findByIdAndRemove(req.params.id, function (err) {
        if (err) return next(err);
        res.send('Deleted successfully!');
    })
};