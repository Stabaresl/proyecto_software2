from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app.schemas.acuerdo_schema import SolicitudAcuerdoSchema, RespuestaAcuerdoSchema
from app.services import acuerdo_service
from app.utils.auth import token_required, role_required

acuerdo_bp = Blueprint('acuerdos', __name__)


@acuerdo_bp.route('/', methods=['POST'])
@token_required
@role_required('company')
def solicitar():
    schema = SolicitudAcuerdoSchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as e:
        return jsonify({'success': False, 'errors': e.messages}), 422

    doc = acuerdo_service.crear_solicitud(data, int(request.auth_user_id))
    return jsonify({'success': True, 'message': 'Solicitud enviada.', 'data': doc}), 201


@acuerdo_bp.route('/mis-solicitudes', methods=['GET'])
@token_required
@role_required('company')
def mis_solicitudes():
    data = acuerdo_service.listar_acuerdos_empresa(int(request.auth_user_id))
    return jsonify({'success': True, 'data': data})


@acuerdo_bp.route('/recibidos', methods=['GET'])
@token_required
@role_required('university')
def recibidos():
    data = acuerdo_service.listar_acuerdos_universidad(int(request.auth_user_id))
    return jsonify({'success': True, 'data': data})


@acuerdo_bp.route('/<acuerdo_id>/responder', methods=['PATCH'])
@token_required
@role_required('university')
def responder(acuerdo_id):
    schema = RespuestaAcuerdoSchema()
    try:
        body = schema.load(request.get_json())
    except ValidationError as e:
        return jsonify({'success': False, 'errors': e.messages}), 422

    doc, error = acuerdo_service.responder_acuerdo(
        acuerdo_id, body['accion'], body.get('respuesta', ''), int(request.auth_user_id)
    )
    if error:
        return jsonify({'success': False, 'message': error}), 400
    return jsonify({'success': True, 'message': f"Acuerdo {body['accion']}do.", 'data': doc})