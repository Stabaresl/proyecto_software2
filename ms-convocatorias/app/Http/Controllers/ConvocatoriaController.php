<?php

namespace App\Http\Controllers;

use App\Models\Convocatoria;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;

class ConvocatoriaController extends Controller
{
    private function getAuth(Request $request): array
    {
        return [
            'userId' => $request->header('X-User-Id'),
            'role'   => $request->header('X-User-Role'),
        ];
    }

    private function checkAuth($userId): ?JsonResponse
    {
        if (!$userId) {
            return response()->json([
                'success' => false,
                'message' => 'No autenticado.',
            ], 401);
        }
        return null;
    }

    public function index(Request $request): JsonResponse
    {
        $query = Convocatoria::query();

        if ($request->has('tipo'))           $query->where('tipo', $request->tipo);
        if ($request->has('estado'))         $query->where('estado', $request->estado);
        if ($request->has('publicador_tipo')) $query->where('publicador_tipo', $request->publicador_tipo);

        $convocatorias = $query->withCount('postulaciones')
            ->orderByDesc('created_at')
            ->get();

        return response()->json(['success' => true, 'data' => $convocatorias]);
    }

    public function show(int $id): JsonResponse
    {
        $convocatoria = Convocatoria::withCount('postulaciones')->find($id);

        if (!$convocatoria) {
            return response()->json(['success' => false, 'message' => 'Convocatoria no encontrada.'], 404);
        }

        return response()->json(['success' => true, 'data' => $convocatoria]);
    }

    public function store(Request $request): JsonResponse
    {
        $auth = $this->getAuth($request);

        if ($res = $this->checkAuth($auth['userId'])) return $res;

        if (!in_array($auth['role'], ['company', 'state'])) {
            return response()->json([
                'success' => false,
                'message' => 'Solo empresas o entidades del Estado pueden publicar convocatorias.',
            ], 403);
        }

        $validator = Validator::make($request->all(), [
            'titulo'       => 'required|string|max:255',
            'descripcion'  => 'required|string',
            'tipo'         => 'required|in:practica,empleo,proyecto,beca,reto_nacional,investigacion',
            'cupos'        => 'required|integer|min:1',
            'fecha_inicio' => 'required|date|after_or_equal:today',
            'fecha_cierre' => 'required|date|after:fecha_inicio',
            'requisitos'   => 'nullable|array',
            'condiciones'  => 'nullable|array',
        ]);

        if ($validator->fails()) {
            return response()->json(['success' => false, 'errors' => $validator->errors()], 422);
        }

        $convocatoria = Convocatoria::create([
            'publicador_user_id' => $auth['userId'],
            'publicador_tipo'    => $auth['role'],
            'titulo'             => $request->titulo,
            'descripcion'        => $request->descripcion,
            'tipo'               => $request->tipo,
            'cupos'              => $request->cupos,
            'fecha_inicio'       => $request->fecha_inicio,
            'fecha_cierre'       => $request->fecha_cierre,
            'estado'             => 'borrador',
            'requisitos'         => $request->requisitos ?? [],
            'condiciones'        => $request->condiciones ?? [],
        ]);

        return response()->json([
            'success' => true,
            'message' => 'Convocatoria creada.',
            'data'    => $convocatoria,
        ], 201);
    }

    public function update(Request $request, int $id): JsonResponse
    {
        $auth = $this->getAuth($request);

        if ($res = $this->checkAuth($auth['userId'])) return $res;

        $convocatoria = Convocatoria::find($id);

        if (!$convocatoria) {
            return response()->json(['success' => false, 'message' => 'Convocatoria no encontrada.'], 404);
        }

        if ($convocatoria->publicador_user_id != $auth['userId']) {
            return response()->json(['success' => false, 'message' => 'No tienes permiso para editar esta convocatoria.'], 403);
        }

        $validator = Validator::make($request->all(), [
            'titulo'       => 'sometimes|string|max:255',
            'descripcion'  => 'sometimes|string',
            'cupos'        => 'sometimes|integer|min:1',
            'fecha_inicio' => 'sometimes|date',
            'fecha_cierre' => 'sometimes|date|after:fecha_inicio',
            'estado'       => 'sometimes|in:borrador,activa,pausada,cerrada',
            'requisitos'   => 'nullable|array',
            'condiciones'  => 'nullable|array',
        ]);

        if ($validator->fails()) {
            return response()->json(['success' => false, 'errors' => $validator->errors()], 422);
        }

        $convocatoria->update($request->only([
            'titulo', 'descripcion', 'cupos',
            'fecha_inicio', 'fecha_cierre', 'estado',
            'requisitos', 'condiciones',
        ]));

        return response()->json(['success' => true, 'message' => 'Convocatoria actualizada.', 'data' => $convocatoria]);
    }

    public function cambiarEstado(Request $request, int $id): JsonResponse
    {
        $auth = $this->getAuth($request);

        if ($res = $this->checkAuth($auth['userId'])) return $res;

        $convocatoria = Convocatoria::find($id);

        if (!$convocatoria) {
            return response()->json(['success' => false, 'message' => 'Convocatoria no encontrada.'], 404);
        }

        if ($convocatoria->publicador_user_id != $auth['userId']) {
            return response()->json(['success' => false, 'message' => 'No tienes permiso.'], 403);
        }

        $validator = Validator::make($request->all(), [
            'estado' => 'required|in:borrador,activa,pausada,cerrada',
        ]);

        if ($validator->fails()) {
            return response()->json(['success' => false, 'errors' => $validator->errors()], 422);
        }

        $convocatoria->update(['estado' => $request->estado]);

        return response()->json([
            'success' => true,
            'message' => "Estado cambiado a {$request->estado}.",
            'data'    => $convocatoria,
        ]);
    }

    public function misConvocatorias(Request $request): JsonResponse
    {
        $auth = $this->getAuth($request);

        if ($res = $this->checkAuth($auth['userId'])) return $res;

        $data = Convocatoria::where('publicador_user_id', $auth['userId'])
            ->withCount('postulaciones')
            ->orderByDesc('created_at')
            ->get();

        return response()->json(['success' => true, 'data' => $data]);
    }
}