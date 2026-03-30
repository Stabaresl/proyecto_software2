const sequelize = require('../config/database');
const Perfil    = require('./Perfil');
const Favorito  = require('./Favorito');

const syncDatabase = async () => {
    await sequelize.sync({ alter: true });
    console.log('Base de datos sincronizada.');
};

module.exports = { sequelize, Perfil, Favorito, syncDatabase };