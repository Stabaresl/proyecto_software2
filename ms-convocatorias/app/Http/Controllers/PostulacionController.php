<?php

namespace App\Http\Controllers;

use App\Models\Convocatoria;
use App\Models\DocumentoPostulacion;
use App\Models\Postulacion;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;

class PostulacionController extends Controller
{
    public function store(Request $request, int $convocatoriaId): JsonResponse
    {
        if ($request->auth_user_role !== 'student') {
            return response()->json(['success' => false, 'message' => 'Solo estudiantes pueden postularse.'], 403);
        }

        $convocatoria = Convocatoria::find($convocatoriaId);

        if (!$convocatoria) {
            return response()->json(['success' => false, 'message' => 'Convocatoria no encontrada.'], 404);
        }

        if (!$convocatoria->isActiva()) {
            return response()->json(['success' => false, 'message' => 'La convocatoria no está activa.'], 400);
        }

        if ($convocatoria->cuposDisponibles() === 0) {
            return response()->json(['success' => false, 'message' => 'No hay cupos disponibles.'], 400);
        }

        $yaPostulado = Postulacion::where('convocatoria_id', $convocatoriaId)
            ->where('estudiante_user_id', $request->auth_user_id)
            ->exists();

        if ($yaPostulado) {
            return response()->json(['success' => false, 'message' => 'Ya te postulaste a esta convocatoria.'], 409);
        }

        $validator = Validator::make($request->all(), [
            'carta_presentacion' => 'nullable|string|max:2000',
            'documentos'         => 'nullable|array',
            'documentos.*.nombre' => 'required_with:documentos|string',
            'documentos.*.url'    => 'required_with:documentos|url',
            'documentos.*.tipo'   => 'required_with:documentos|in:cv,carta,certificado,otro',
        ]);

        if ($validator->fails()) {
            return response()->json(['success' => false, 'errors' => $validator->errors()], 422);
        }

        $postulacion = Postulacion::create([
            'convocatoria_id'    => $convocatoriaId,
            'estudiante_user_id' => $request->auth_user_id,
            'carta_presentacion' => $request->carta_presentacion,
            'estado'             => 'en_revision',
        ]);

        if ($request->has('documentos')) {
            foreach ($request->documentos as $doc) {
                DocumentoPostulacion::create([
                    'postulacion_id' => $postulacion->id,
                    'nombre'         => $doc['nombre'],
                    'url'            => $doc['url'],
                    'tipo'           => $doc['tipo'],
                ]);
            }
        }

        return response()->json([
            'success' => true,
            'message' => 'Postulación enviada correctamente.',
            'data'    => $postulacion->load('documentos'),
        ], 201);
    }

    public function misPostulaciones(Request $request): JsonResponse
    {
        $postulaciones = Postulacion::where('estudiante_user_id', $request->auth_user_id)
            ->with(['convocatoria', 'documentos'])
            ->orderByDesc('fecha_postulacion')
            ->get();

        return response()->json(['success' => true, 'data' => $postulaciones]);
    }

    public function postulacionesPorConvocatoria(Request $request, int $convocatoriaId): JsonResponse
    {
        $convocatoria = Convocatoria::find($convocatoriaId);

        if (!$convocatoria) {
            return response()->json(['success' => false, 'message' => 'Convocatoria no encontrada.'], 404);
        }

        if ($convocatoria->publicador_user_id != $request->auth_user_id) {
            return response()->json(['success' => false, 'message' => 'No tienes permiso.'], 403);
        }

        $postulaciones = Postulacion::where('convocatoria_id', $convocatoriaId)
            ->with('documentos')
            ->orderByDesc('fecha_postulacion')
            ->get();

        return response()->json(['success' => true, 'data' => $postulaciones]);
    }

    public function cambiarEstado(Request $request, int $postulacionId): JsonResponse
    {
        $postulacion = Postulacion::with('convocatoria')->find($postulacionId);

        if (!$postulacion) {
            return response()->json(['success' => false, 'message' => 'Postulación no encontrada.'], 404);
        }

        if ($postulacion->convocatoria->publicador_user_id != $request->auth_user_id) {
            return response()->json(['success' => false, 'message' => 'No tienes permiso.'], 403);
        }

        $validator = Validator::make($request->all(), [
            'estado' => 'required|in:en_revision,preseleccionado,seleccionado,rechazado',
        ]);

        if ($validator->fails()) {
            return response()->json(['success' => false, 'errors' => $validator->errors()], 422);
        }

        $postulacion->update(['estado' => $request->estado]);

        return response()->json(['success' => true, 'message' => "Estado actualizado a {$request->estado}.", 'data' => $postulacion]);
    }
}