const sequelize = require('../config/database');
const Perfil    = require('./perfil');
const Favorito  = require('./favorito');

const syncDatabase = async () => {
    await sequelize.sync({ alter: true });
    console.log('Base de datos sincronizada.');
};

module.exports = { sequelize, Perfil, Favorito, syncDatabase };