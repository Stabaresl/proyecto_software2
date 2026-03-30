from bson import ObjectId
from datetime import datetime, timezone
from app.utils.db import mongo


def _serialize(doc):
    if doc:
        doc['_id'] = str(doc['_id'])
    return doc


def listar_formaciones(filtros=None):
    query = {}
    if filtros:
        if filtros.get('tipo'):
            query['tipo'] = filtros['tipo']
        if filtros.get('modalidad'):
            query['modalidad'] = filtros['modalidad']
        if filtros.get('universidad_user_id'):
            query['universidad_user_id'] = int(filtros['universidad_user_id'])
        if filtros.get('estado'):
            query['estado'] = filtros['estado']

    docs = list(mongo.db.formaciones.find(query).sort('created_at', -1))
    return [_serialize(d) for d in docs]


def obtener_formacion(formacion_id):
    try:
        doc = mongo.db.formaciones.find_one({'_id': ObjectId(formacion_id)})
        return _serialize(doc)
    except Exception:
        return None


def crear_formacion(data, universidad_user_id):
    data['universidad_user_id'] = universidad_user_id
    data['estado']     = 'borrador'
    data['created_at'] = datetime.now(timezone.utc)
    data['updated_at'] = datetime.now(timezone.utc)

    result = mongo.db.formaciones.insert_one(data)
    return obtener_formacion(str(result.inserted_id))


def actualizar_formacion(formacion_id, data, universidad_user_id):
    formacion = obtener_formacion(formacion_id)
    if not formacion:
        return None, 'Programa no encontrado.'
    if formacion['universidad_user_id'] != universidad_user_id:
        return None, 'No tienes permiso para editar este programa.'

    data['updated_at'] = datetime.now(timezone.utc)
    mongo.db.formaciones.update_one(
        {'_id': ObjectId(formacion_id)},
        {'$set': data}
    )
    return obtener_formacion(formacion_id), None


def registrar_certificacion(data):
    data['created_at'] = datetime.now(timezone.utc)
    result = mongo.db.certificaciones.insert_one(data)
    data['_id'] = str(result.inserted_id)
    return data


def listar_certificaciones_estudiante(estudiante_user_id):
    docs = list(mongo.db.certificaciones.find(
        {'estudiante_user_id': estudiante_user_id}
    ).sort('created_at', -1))
    return [_serialize(d) for d in docs]