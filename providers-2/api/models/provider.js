'use strict'

// Cargamos el módulo de mongoose
var mongoose =  require('mongoose');

// Usaremos los esquemas
var Schema = mongoose.Schema;

// Creamos el objeto del esquema y sus atributos
var ProviderSchema = Schema({
    name: String,
    contact:[{
        contact1: String,
        contact2: String,
        contact3: String
    }] ,
    image: String
});

// Exportamos el modelo para usarlo en otros ficheros
module.exports = mongoose.model('Provider', ProviderSchema);