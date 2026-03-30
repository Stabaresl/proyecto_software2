from marshmallow import Schema, fields, validate

class SolicitudAcuerdoSchema(Schema):
    universidad_user_id  = fields.Int(required=True)
    titulo               = fields.Str(required=True, validate=validate.Length(min=3, max=255))
    descripcion          = fields.Str(required=True)
    habilidades_requeridas = fields.List(fields.Str(), load_default=[])
    duracion_semanas     = fields.Int(required=True, validate=validate.Range(min=1))
    perfil_estudiante    = fields.Str(required=True)
    condiciones          = fields.List(fields.Str(), load_default=[])

class RespuestaAcuerdoSchema(Schema):
    accion    = fields.Str(required=True, validate=validate.OneOf(['aceptar', 'rechazar']))
    respuesta = fields.Str(load_default='')