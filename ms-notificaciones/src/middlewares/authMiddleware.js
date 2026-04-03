const jwt = require('jsonwebtoken');

const authMiddleware = (req, res, next) => {

    if (req.headers['x-user-id'] && req.headers['x-user-role']) {
        req.authUserId   = req.headers['x-user-id'];
        req.authUserRole = req.headers['x-user-role'];
        return next();
    }

    const authHeader = req.headers['authorization'];

    if (!authHeader || !authHeader.startsWith('Bearer ')) {
        return res.status(401).json({ success: false, message: 'Token no proporcionado.' });
    }

    const token = authHeader.split(' ')[1];

    try {
        const payload = jwt.decode(token);
        if (!payload) {
            return res.status(401).json({ success: false, message: 'Token inválido.' });
        }
        req.authUserId   = payload.sub;
        req.authUserRole = payload.role;
        next();
    } catch (err) {
        return res.status(401).json({ success: false, message: 'Error de autenticación.' });
    }
};

module.exports = { authMiddleware };