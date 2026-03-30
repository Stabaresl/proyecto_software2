const mongoose = require('mongoose');

const notificacionSchema = new mongoose.Schema({
    destinatario_user_id: { type: Number, required: true },
    tipo: {
        type: String,
        required: true,
        enum: [
            'postulacion_estado',
            'nueva_convocatoria',
            'perfil_visitado',
            'acuerdo_respuesta',
            'grupo_seleccionado',
            'convocatoria_por_cerrar',
            'certificacion_registrada',
            'general',
        ],
    },
    titulo:   { type: String, required: true },
    mensaje:  { type: String, required: true },
    leida:    { type: Boolean, default: false },
    metadata: { type: mongoose.Schema.Types.Mixed, default: {} },
}, { timestamps: true });

module.exports = mongoose.model('Notificacion', notificacionSchema);