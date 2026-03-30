const service = require('../services/notificacionService');

const crear = async (req, res) => {
    try {
        const { destinatario_user_id, tipo, titulo, mensaje, metadata, email } = req.body;

        if (!destinatario_user_id || !tipo || !titulo || !mensaje) {
            return res.status(422).json({ success: false, message: 'Faltan campos requeridos: destinatario_user_id, tipo, titulo, mensaje.' });
        }

        const notificacion = await service.crear({ destinatario_user_id, tipo, titulo, mensaje, metadata, email });
        res.status(201).json({ success: true, message: 'Notificación creada.', data: notificacion });
    } catch (err) {
        res.status(500).json({ success: false, message: err.message });
    }
};

const listar = async (req, res) => {
    try {
        const soloNoLeidas = req.query.no_leidas === 'true';
        const data = await service.listarPorUsuario(req.authUserId, soloNoLeidas);
        res.json({ success: true, data });
    } catch (err) {
        res.status(500).json({ success: false, message: err.message });
    }
};

const marcarLeida = async (req, res) => {
    try {
        const notificacion = await service.marcarLeida(req.params.id, req.authUserId);
        if (!notificacion) return res.status(404).json({ success: false, message: 'Notificación no encontrada.' });
        res.json({ success: true, message: 'Marcada como leída.', data: notificacion });
    } catch (err) {
        res.status(500).json({ success: false, message: err.message });
    }
};

const marcarTodasLeidas = async (req, res) => {
    try {
        await service.marcarTodasLeidas(req.authUserId);
        res.json({ success: true, message: 'Todas las notificaciones marcadas como leídas.' });
    } catch (err) {
        res.status(500).json({ success: false, message: err.message });
    }
};

const contarNoLeidas = async (req, res) => {
    try {
        const total = await service.contarNoLeidas(req.authUserId);
        res.json({ success: true, total });
    } catch (err) {
        res.status(500).json({ success: false, message: err.message });
    }
};

const obtenerPreferencia = async (req, res) => {
    try {
        const data = await service.obtenerPreferencia(req.authUserId);
        res.json({ success: true, data });
    } catch (err) {
        res.status(500).json({ success: false, message: err.message });
    }
};

const actualizarPreferencia = async (req, res) => {
    try {
        const data = await service.actualizarPreferencia(req.authUserId, req.body);
        res.json({ success: true, message: 'Preferencias actualizadas.', data });
    } catch (err) {
        res.status(500).json({ success: false, message: err.message });
    }
};

module.exports = { crear, listar, marcarLeida, marcarTodasLeidas, contarNoLeidas, obtenerPreferencia, actualizarPreferencia };