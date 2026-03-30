<?php

use App\Http\Controllers\AuthController;
use App\Http\Controllers\GatewayController;
use Illuminate\Support\Facades\Route;

// ─── Auth — rutas públicas ────────────────────────────────────
Route::prefix('auth')->group(function () {
    Route::post('/register',        [AuthController::class, 'register']);
    Route::post('/login',           [AuthController::class, 'login']);
    Route::post('/forgot-password', [AuthController::class, 'forgotPassword']);
    Route::post('/reset-password',  [AuthController::class, 'resetPassword']);
});

// ─── Auth — rutas protegidas ──────────────────────────────────
Route::middleware(['jwt.auth'])->prefix('auth')->group(function () {
    Route::post('/logout', [AuthController::class, 'logout']);
    Route::get('/me',      [AuthController::class, 'me']);
});

// ─── Proxy — rutas públicas (sin auth) ───────────────────────
Route::middleware(['rate.limit'])->group(function () {
    Route::get('/convocatorias',      function (\Illuminate\Http\Request $request) {
        return app(GatewayController::class)->forward($request, 'convocatorias', '');
    });
    Route::get('/convocatorias/{id}', function (\Illuminate\Http\Request $request, $id) {
        return app(GatewayController::class)->forward($request, 'convocatorias', $id);
    });
    Route::get('/formaciones',        function (\Illuminate\Http\Request $request) {
        return app(GatewayController::class)->forward($request, 'formaciones', '');
    });
    Route::get('/formaciones/{id}',   function (\Illuminate\Http\Request $request, $id) {
        return app(GatewayController::class)->forward($request, 'formaciones', $id);
    });
});

// ─── Proxy — rutas protegidas (con auth) ─────────────────────
Route::middleware(['jwt.auth', 'rate.limit'])->group(function () {

    // Usuarios
    Route::any('/usuarios/{path?}', function (\Illuminate\Http\Request $request, $path = '') {
        return app(GatewayController::class)->forward($request, 'usuarios', $path);
    })->where('path', '.*');

    // Convocatorias
    Route::any('/convocatorias/{path?}', function (\Illuminate\Http\Request $request, $path = '') {
        return app(GatewayController::class)->forward($request, 'convocatorias', $path);
    })->where('path', '.*');

    // Formaciones
    Route::any('/formaciones/{path?}', function (\Illuminate\Http\Request $request, $path = '') {
        return app(GatewayController::class)->forward($request, 'formaciones', $path);
    })->where('path', '.*');

    // Acuerdos
    Route::any('/acuerdos/{path?}', function (\Illuminate\Http\Request $request, $path = '') {
        return app(GatewayController::class)->forward($request, 'acuerdos', $path);
    })->where('path', '.*');

    // Matching
    Route::any('/matching/{path?}', function (\Illuminate\Http\Request $request, $path = '') {
        return app(GatewayController::class)->forward($request, 'matching', $path);
    })->where('path', '.*');

    // Catálogo
    Route::any('/catalogo/{path?}', function (\Illuminate\Http\Request $request, $path = '') {
        return app(GatewayController::class)->forward($request, 'catalogo', $path);
    })->where('path', '.*');

    // Notificaciones
    Route::any('/notificaciones/{path?}', function (\Illuminate\Http\Request $request, $path = '') {
        return app(GatewayController::class)->forward($request, 'notificaciones', $path);
    })->where('path', '.*');
});