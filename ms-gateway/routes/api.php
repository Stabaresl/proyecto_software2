<?php

use App\Http\Controllers\AuthController;
use App\Http\Controllers\GatewayController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| AUTH (NO PROXY)
|--------------------------------------------------------------------------
*/

// Públicas
Route::prefix('auth')->group(function () {
    Route::post('/register',         [AuthController::class, 'register']);
    Route::post('/login',            [AuthController::class, 'login']);
    Route::post('/forgot-password',  [AuthController::class, 'forgotPassword']);
    Route::post('/reset-password',    [AuthController::class, 'resetPassword']);
});

// Protegidas
Route::middleware(['jwt.auth'])->prefix('auth')->group(function () {
    Route::post('/logout', [AuthController::class, 'logout']);
    Route::get('/me',      [AuthController::class, 'me']);
});

// ─── Rutas especiales ANTES del proxy dinámico ───────────────
Route::middleware(['jwt.auth', 'rate.limit'])->group(function () {
    Route::get('/mis-convocatorias', function (Request $request) {
        return app(GatewayController::class)->forward($request, 'convocatorias', 'mis-convocatorias');
    });
    Route::get('/mis-postulaciones', function (Request $request) {
        return app(GatewayController::class)->forward($request, 'convocatorias', 'mis-postulaciones');
    });
    Route::patch('/postulaciones/{id}/estado', function (Request $request, $id) {
        return app(GatewayController::class)->forward($request, 'convocatorias', "postulaciones/{$id}/estado");
    });

    // Acuerdos especiales
    Route::get('/mis-solicitudes', function (Request $request) {
        return app(GatewayController::class)->forward($request, 'acuerdos', 'mis-solicitudes');
    });
    Route::get('/recibidos', function (Request $request) {
        return app(GatewayController::class)->forward($request, 'acuerdos', 'recibidos');
    });

    // Notificaciones especiales
    Route::get('/notificaciones/no-leidas/count', function (Request $request) {
        return app(GatewayController::class)->forward($request, 'notificaciones', 'no-leidas/count');
    });
    Route::patch('/notificaciones/marcar-todas', function (Request $request) {
        return app(GatewayController::class)->forward($request, 'notificaciones', 'marcar-todas');
    });
    Route::get('/notificaciones/preferencias', function (Request $request) {
        return app(GatewayController::class)->forward($request, 'notificaciones', 'preferencias');
    });
    Route::put('/notificaciones/preferencias', function (Request $request) {
        return app(GatewayController::class)->forward($request, 'notificaciones', 'preferencias');
    });
});
// ─── Rutas públicas SIN auth ──────────────────────────────────
Route::get('/convocatorias', function (Request $request) {
    return app(GatewayController::class)->forward($request, 'convocatorias', '');
});

Route::get('/convocatorias/{id}', function (Request $request, $id) {
    return app(GatewayController::class)->forward($request, 'convocatorias', $id);
});

Route::get('/formaciones', function (Request $request) {
    return app(GatewayController::class)->forward($request, 'formaciones', '');
});
/*
|--------------------------------------------------------------------------
| PROXY DINÁMICO (SOLO UNO)
|--------------------------------------------------------------------------
*/

Route::middleware(['jwt.auth', 'rate.limit'])
    ->any('/{service}/{path?}', function (Request $request, $service, $path = '') {
        return app(GatewayController::class)->forward($request, $service, $path);
    })
    ->where('path', '.*');