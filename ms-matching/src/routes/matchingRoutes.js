const router = require('express').Router();
const ctrl   = require('../controllers/matchingController');
const { authMiddleware, roleMiddleware } = require('../middlewares/authMiddleware');

router.post('/sugerir', authMiddleware, roleMiddleware('company', 'state'), ctrl.sugerirCandidatos);

module.exports = router;