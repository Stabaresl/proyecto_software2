const { Perfil } = require('../models');

const calcularScore = (perfil, requisitos) => {
    let score = 0;

    if (requisitos.habilidades && Array.isArray(perfil.habilidades)) {
        const matches = requisitos.habilidades.filter(h =>
            perfil.habilidades.map(p => p.toLowerCase()).includes(h.toLowerCase())
        );
        score += (matches.length / requisitos.habilidades.length) * 50;
    }

    if (requisitos.disponibilidad && perfil.disponibilidad === requisitos.disponibilidad) {
        score += 20;
    }

    if (requisitos.semestre_minimo && perfil.semestre >= requisitos.semestre_minimo) {
        score += 15;
    }

    if (requisitos.promedio_minimo && parseFloat(perfil.promedio) >= requisitos.promedio_minimo) {
        score += 15;
    }

    return Math.round(score);
};

const sugerirCandidatos = async (requisitos) => {
    const perfiles = await Perfil.findAll({ where: { role: 'student', visible: true } });

    const scored = perfiles
        .map(p => ({ perfil: p, score: calcularScore(p, requisitos) }))
        .filter(p => p.score > 0)
        .sort((a, b) => b.score - a.score)
        .slice(0, 10);

    return scored;
};

module.exports = { sugerirCandidatos };