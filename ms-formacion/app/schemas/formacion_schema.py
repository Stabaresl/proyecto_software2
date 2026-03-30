from marshmallow import Schema, fields, validate

class FormacionSchema(Schema):
    titulo       = fields.Str(required=True, validate=validate.Length(min=3, max=255))
    descripcion  = fields.Str(required=True)
    tipo         = fields.Str(required=True, validate=validate.OneOf([
        'curso', 'diplomado', 'bootcamp', 'certificacion'
    ]))
    modalidad    = fields.Str(required=True, validate=validate.OneOf([
        'presencial', 'virtual', 'hibrida'
    ]))
    duracion_semanas = fields.Int(required=True, validate=validate.Range(min=1))
    requisitos_ingreso = fields.List(fields.Str(), load_default=[])
    costo        = fields.Float(load_default=0.0)
    condiciones_garantia = fields.List(fields.Str(), load_default=[])
    universidad_user_id  = fields.Int(required=True)

class FormacionUpdateSchema(Schema):
    titulo       = fields.Str(validate=validate.Length(min=3, max=255))
    descripcion  = fields.Str()
    modalidad    = fields.Str(validate=validate.OneOf([
        'presencial', 'virtual', 'hibrida'
    ]))
    duracion_semanas = fields.Int(validate=validate.Range(min=1))
    requisitos_ingreso = fields.List(fields.Str())
    costo        = fields.Float()
    condiciones_garantia = fields.List(fields.Str())
    estado       = fields.Str(validate=validate.OneOf([
        'borrador', 'publicado', 'cerrado'
    ]))