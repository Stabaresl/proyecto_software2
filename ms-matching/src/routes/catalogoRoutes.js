const router = require('express').Router();
const ctrl   = require('../controllers/catalogoController');
const { authMiddleware, roleMiddleware } = require('../middlewares/authMiddleware');

router.get('/estudiantes',                     authMiddleware, roleMiddleware('company', 'state', 'university'), ctrl.listarEstudiantes);
router.get('/estudiantes/:userId',             authMiddleware, ctrl.obtenerPerfil);
router.post('/perfil',                         authMiddleware, ctrl.crearOActualizarPerfil);
router.post('/favoritos',                      authMiddleware, roleMiddleware('company'), ctrl.agregarFavorito);
router.get('/favoritos',                       authMiddleware, roleMiddleware('company'), ctrl.listarFavoritos);
router.delete('/favoritos/:estudianteId',      authMiddleware, roleMiddleware('company'), ctrl.eliminarFavorito);

module.exports = router;