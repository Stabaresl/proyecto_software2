const catalogoService = require('../services/catalogoService');

const listarEstudiantes = async (req, res) => {
    try {
        const data = await catalogoService.listarEstudiantes(req.query);
        res.json({ success: true, data });
    } catch (err) {
        res.status(500).json({ success: false, message: err.message });
    }
};

const obtenerPerfil = async (req, res) => {
    try {
        const perfil = await catalogoService.obtenerPerfil(req.params.userId);
        if (!perfil) return res.status(404).json({ success: false, message: 'Perfil no encontrado.' });
        res.json({ success: true, data: perfil });
    } catch (err) {
        res.status(500).json({ success: false, message: err.message });
    }
};

const crearOActualizarPerfil = async (req, res) => {
    try {
        const data = { ...req.body, gateway_user_id: req.authUserId, role: req.authUserRole };
        const perfil = await catalogoService.crearOActualizarPerfil(data);
        res.status(201).json({ success: true, message: 'Perfil sincronizado.', data: perfil });
    } catch (err) {
        res.status(500).json({ success: false, message: err.message });
    }
};

const agregarFavorito = async (req, res) => {
    try {
        const { estudiante_user_id, nota } = req.body;
        if (!estudiante_user_id) return res.status(422).json({ success: false, message: 'estudiante_user_id es requerido.' });
        const fav = await catalogoService.agregarFavorito(req.authUserId, estudiante_user_id, nota);
        res.status(201).json({ success: true, message: 'Favorito guardado.', data: fav });
    } catch (err) {
        res.status(500).json({ success: false, message: err.message });
    }
};

const listarFavoritos = async (req, res) => {
    try {
        const data = await catalogoService.listarFavoritos(req.authUserId);
        res.json({ success: true, data });
    } catch (err) {
        res.status(500).json({ success: false, message: err.message });
    }
};

const eliminarFavorito = async (req, res) => {
    try {
        const deleted = await catalogoService.eliminarFavorito(req.authUserId, req.params.estudianteId);
        if (!deleted) return res.status(404).json({ success: false, message: 'Favorito no encontrado.' });
        res.json({ success: true, message: 'Favorito eliminado.' });
    } catch (err) {
        res.status(500).json({ success: false, message: err.message });
    }
};

module.exports = { listarEstudiantes, obtenerPerfil, crearOActualizarPerfil, agregarFavorito, listarFavoritos, eliminarFavorito };