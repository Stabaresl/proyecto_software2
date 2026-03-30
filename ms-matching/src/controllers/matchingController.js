const matchingService = require('../services/matchingService');

const sugerirCandidatos = async (req, res) => {
    try {
        const requisitos = req.body;
        if (!requisitos || Object.keys(requisitos).length === 0) {
            return res.status(422).json({ success: false, message: 'Debes enviar al menos un criterio de matching.' });
        }
        const resultados = await matchingService.sugerirCandidatos(requisitos);
        res.json({ success: true, total: resultados.length, data: resultados });
    } catch (err) {
        res.status(500).json({ success: false, message: err.message });
    }
};

module.exports = { sugerirCandidatos };