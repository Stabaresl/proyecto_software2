const { DataTypes } = require('sequelize');
const sequelize = require('../config/database');

const Favorito = sequelize.define('Favorito', {
    id: {
        type:          DataTypes.BIGINT,
        primaryKey:    true,
        autoIncrement: true,
    },
    empresa_user_id: {
        type:      DataTypes.BIGINT,
        allowNull: false,
    },
    estudiante_user_id: {
        type:      DataTypes.BIGINT,
        allowNull: false,
    },
    nota: {
        type:         DataTypes.TEXT,
        allowNull:    true,
    },
}, {
    tableName:  'favoritos',
    timestamps: true,
    underscored: true,
    indexes: [
        {
            unique: true,
            fields: ['empresa_user_id', 'estudiante_user_id'],
        },
    ],
});

module.exports = Favorito;