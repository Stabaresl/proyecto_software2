const Notificacion = require('../models/Notificacion');
const Preferencia  = require('../models/Preferencia');
const { enviarEmail } = require('./emailService');

const crear = async ({ destinatario_user_id, tipo, titulo, mensaje, metadata = {}, email = null }) => {
    const notificacion = await Notificacion.create({
        destinatario_user_id,
        tipo,
        titulo,
        mensaje,
        metadata,
    });

    const preferencia = await Preferencia.findOne({ user_id: destinatario_user_id });

    const emailActivo = !preferencia || preferencia.email_activo;
    const tipoActivo  = !preferencia || preferencia.tipos_activos.includes(tipo);

    if (emailActivo && tipoActivo && email) {
        await enviarEmail({
            to:      email,
            subject: titulo,
            html:    `<h2>${titulo}</h2><p>${mensaje}</p>`,
        });
    }

    return notificacion;
};

const listarPorUsuario = async (userId, soloNoLeidas = false) => {
    const query = { destinatario_user_id: parseInt(userId) };
    if (soloNoLeidas) query.leida = false;
    return await Notificacion.find(query).sort({ createdAt: -1 });
};

const marcarLeida = async (notificacionId, userId) => {
    return await Notificacion.findOneAndUpdate(
        { _id: notificacionId, destinatario_user_id: parseInt(userId) },
        { leida: true },
        { new: true }
    );
};

const marcarTodasLeidas = async (userId) => {
    await Notificacion.updateMany(
        { destinatario_user_id: parseInt(userId), leida: false },
        { leida: true }
    );
};

const contarNoLeidas = async (userId) => {
    return await Notificacion.countDocuments({
        destinatario_user_id: parseInt(userId),
        leida: false,
    });
};

const obtenerPreferencia = async (userId) => {
    let pref = await Preferencia.findOne({ user_id: parseInt(userId) });
    if (!pref) {
        pref = await Preferencia.create({ user_id: parseInt(userId) });
    }
    return pref;
};

const actualizarPreferencia = async (userId, data) => {
    return await Preferencia.findOneAndUpdate(
        { user_id: parseInt(userId) },
        data,
        { new: true, upsert: true }
    );
};

module.exports = {
    crear,
    listarPorUsuario,
    marcarLeida,
    marcarTodasLeidas,
    contarNoLeidas,
    obtenerPreferencia,
    actualizarPreferencia,
};