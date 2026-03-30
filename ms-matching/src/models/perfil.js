const { DataTypes } = require('sequelize');
const sequelize = require('../config/database');

const Perfil = sequelize.define('Perfil', {
    id: {
        type:          DataTypes.BIGINT,
        primaryKey:    true,
        autoIncrement: true,
    },
    gateway_user_id: {
        type:      DataTypes.BIGINT,
        allowNull: false,
        unique:    true,
    },
    role: {
        type:      DataTypes.ENUM('student', 'company', 'state', 'university'),
        allowNull: false,
    },
    universidad: {
        type:         DataTypes.STRING,
        allowNull:    true,
    },
    carrera: {
        type:         DataTypes.STRING,
        allowNull:    true,
    },
    semestre: {
        type:         DataTypes.INTEGER,
        allowNull:    true,
    },
    habilidades: {
        type:         DataTypes.JSON,
        defaultValue: [],
    },
    idiomas: {
        type:         DataTypes.JSON,
        defaultValue: [],
    },
    disponibilidad: {
        type:         DataTypes.STRING,
        allowNull:    true,
    },
    promedio: {
        type:         DataTypes.DECIMAL(3, 2),
        allowNull:    true,
    },
    ubicacion: {
        type:         DataTypes.STRING,
        allowNull:    true,
    },
    certificaciones: {
        type:         DataTypes.JSON,
        defaultValue: [],
    },
    visible: {
        type:         DataTypes.BOOLEAN,
        defaultValue: true,
    },
}, {
    tableName:  'perfiles',
    timestamps: true,
    underscored: true,
});

module.exports = Perfil;