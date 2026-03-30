from bson import ObjectId
from datetime import datetime, timezone
from app.utils.db import mongo


def _serialize(doc):
    if doc:
        doc['_id'] = str(doc['_id'])
    return doc


def crear_solicitud(data, empresa_user_id):
    data['empresa_user_id'] = empresa_user_id
    data['estado']     = 'pendiente'
    data['created_at'] = datetime.now(timezone.utc)
    data['updated_at'] = datetime.now(timezone.utc)

    result = mongo.db.acuerdos.insert_one(data)
    doc = mongo.db.acuerdos.find_one({'_id': result.inserted_id})
    return _serialize(doc)


def listar_acuerdos_empresa(empresa_user_id):
    docs = list(mongo.db.acuerdos.find(
        {'empresa_user_id': empresa_user_id}
    ).sort('created_at', -1))
    return [_serialize(d) for d in docs]


def listar_acuerdos_universidad(universidad_user_id):
    docs = list(mongo.db.acuerdos.find(
        {'universidad_user_id': universidad_user_id}
    ).sort('created_at', -1))
    return [_serialize(d) for d in docs]


def responder_acuerdo(acuerdo_id, accion, respuesta, universidad_user_id):
    try:
        acuerdo = mongo.db.acuerdos.find_one({'_id': ObjectId(acuerdo_id)})
    except Exception:
        return None, 'ID inválido.'

    if not acuerdo:
        return None, 'Acuerdo no encontrado.'
    if acuerdo['universidad_user_id'] != universidad_user_id:
        return None, 'No tienes permiso.'
    if acuerdo['estado'] != 'pendiente':
        return None, 'Este acuerdo ya fue respondido.'

    nuevo_estado = 'aceptado' if accion == 'aceptar' else 'rechazado'

    mongo.db.acuerdos.update_one(
        {'_id': ObjectId(acuerdo_id)},
        {'$set': {
            'estado':     nuevo_estado,
            'respuesta':  respuesta,
            'updated_at': datetime.now(timezone.utc),
        }}
    )
    doc = mongo.db.acuerdos.find_one({'_id': ObjectId(acuerdo_id)})
    return _serialize(doc), None