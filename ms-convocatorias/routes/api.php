<?php

use App\Http\Controllers\ConvocatoriaController;
use App\Http\Controllers\PostulacionController;
use Illuminate\Support\Facades\Route;

// ─── Rutas públicas ───────────────────────────────────────────
Route::get('/convocatorias', [ConvocatoriaController::class, 'index']);
Route::get('/convocatorias/{id}', [ConvocatoriaController::class, 'show']);

// ─── Rutas protegidas ─────────────────────────────────────────
Route::middleware(['jwt.auth'])->group(function () {

    // Convocatorias
    Route::post('/convocatorias', [ConvocatoriaController::class, 'store']);
    Route::put('/convocatorias/{id}', [ConvocatoriaController::class, 'update']);
    Route::patch('/convocatorias/{id}/estado', [ConvocatoriaController::class, 'cambiarEstado']);
    Route::get('/mis-convocatorias', [ConvocatoriaController::class, 'misConvocatorias']);

    // Postulaciones
    Route::post('/convocatorias/{id}/postular', [PostulacionController::class, 'store']);
    Route::get('/mis-postulaciones', [PostulacionController::class, 'misPostulaciones']);
    Route::get('/convocatorias/{id}/postulaciones', [PostulacionController::class, 'postulacionesPorConvocatoria']);
    Route::patch('/postulaciones/{id}/estado', [PostulacionController::class, 'cambiarEstado']);
});