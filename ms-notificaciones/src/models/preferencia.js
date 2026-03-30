const mongoose = require('mongoose');

const preferenciaSchema = new mongoose.Schema({
    user_id: { type: Number, required: true, unique: true },
    email_activo:  { type: Boolean, default: true },
    push_activo:   { type: Boolean, default: true },
    tipos_activos: {
        type: [String],
        default: [
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
}, { timestamps: true });

module.exports = mongoose.model('Preferencia', preferenciaSchema);