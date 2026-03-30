const { Op } = require('sequelize');
const { Perfil, Favorito } = require('../models');

const listarEstudiantes = async (filtros) => {
    const where = { role: 'student', visible: true };

    if (filtros.universidad)    where.universidad    = { [Op.like]: `%${filtros.universidad}%` };
    if (filtros.carrera)        where.carrera        = { [Op.like]: `%${filtros.carrera}%` };
    if (filtros.disponibilidad) where.disponibilidad = filtros.disponibilidad;
    if (filtros.ubicacion)      where.ubicacion      = { [Op.like]: `%${filtros.ubicacion}%` };
    if (filtros.semestre_min)   where.semestre       = { [Op.gte]: parseInt(filtros.semestre_min) };
    if (filtros.promedio_min)   where.promedio       = { [Op.gte]: parseFloat(filtros.promedio_min) };

    const perfiles = await Perfil.findAll({ where, order: [['created_at', 'DESC']] });

    if (filtros.habilidad) {
        return perfiles.filter(p =>
            Array.isArray(p.habilidades) &&
            p.habilidades.some(h => h.toLowerCase().includes(filtros.habilidad.toLowerCase()))
        );
    }

    return perfiles;
};

const obtenerPerfil = async (gatewayUserId) => {
    return await Perfil.findOne({ where: { gateway_user_id: gatewayUserId } });
};

const crearOActualizarPerfil = async (data) => {
    const [perfil, created] = await Perfil.findOrCreate({
        where: { gateway_user_id: data.gateway_user_id },
        defaults: data,
    });
    if (!created) {
        await perfil.update(data);
    }
    return perfil;
};

const agregarFavorito = async (empresaUserId, estudianteUserId, nota) => {
    const [fav, created] = await Favorito.findOrCreate({
        where: { empresa_user_id: empresaUserId, estudiante_user_id: estudianteUserId },
        defaults: { nota },
    });
    if (!created) {
        await fav.update({ nota });
    }
    return fav;
};

const listarFavoritos = async (empresaUserId) => {
    return await Favorito.findAll({
        where: { empresa_user_id: empresaUserId },
        order: [['created_at', 'DESC']],
    });
};

const eliminarFavorito = async (empresaUserId, estudianteUserId) => {
    const deleted = await Favorito.destroy({
        where: { empresa_user_id: empresaUserId, estudiante_user_id: estudianteUserId },
    });
    return deleted > 0;
};

module.exports = {
    listarEstudiantes,
    obtenerPerfil,
    crearOActualizarPerfil,
    agregarFavorito,
    listarFavoritos,
    eliminarFavorito,
};