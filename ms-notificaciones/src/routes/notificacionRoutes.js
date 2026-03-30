const router = require('express').Router();
const ctrl   = require('../controllers/notificacionController');
const { authMiddleware } = require('../middlewares/authMiddleware');

router.post('/',                    ctrl.crear);
router.get('/',                     authMiddleware, ctrl.listar);
router.get('/no-leidas/count',      authMiddleware, ctrl.contarNoLeidas);
router.patch('/marcar-todas',       authMiddleware, ctrl.marcarTodasLeidas);
router.patch('/:id/leer',           authMiddleware, ctrl.marcarLeida);
router.get('/preferencias',         authMiddleware, ctrl.obtenerPreferencia);
router.put('/preferencias',         authMiddleware, ctrl.actualizarPreferencia);

module.exports = router;