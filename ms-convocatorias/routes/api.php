<?php

use App\Http\Controllers\ConvocatoriaController;
use App\Http\Controllers\PostulacionController;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| API Routes - Microservicio Convocatorias
|--------------------------------------------------------------------------
*/

// 1. RUTAS ESPECÍFICAS — sin prefijo (acceso directo)
Route::get('/mis-convocatorias', [ConvocatoriaController::class, 'misConvocatorias']);
Route::get('/mis-postulaciones', [PostulacionController::class, 'misPostulaciones']);

// 2. RUTAS ESPECÍFICAS — con prefijo convocatorias (acceso desde gateway)
Route::get('/convocatorias/mis-convocatorias', [ConvocatoriaController::class, 'misConvocatorias']);
Route::get('/convocatorias/mis-postulaciones', [PostulacionController::class, 'misPostulaciones']);

// 3. RUTAS DE RECURSOS GENERALES
Route::get('/convocatorias',  [ConvocatoriaController::class, 'index']);
Route::post('/convocatorias', [ConvocatoriaController::class, 'store']);

// 4. RUTAS CON PARÁMETROS DINÁMICOS (Van al final)
Route::get('/convocatorias/{id}',               [ConvocatoriaController::class, 'show']);
Route::put('/convocatorias/{id}',               [ConvocatoriaController::class, 'update']);
Route::patch('/convocatorias/{id}/estado',      [ConvocatoriaController::class, 'cambiarEstado']);

// 5. POSTULACIONES
Route::post('/convocatorias/{id}/postular',     [PostulacionController::class, 'store']);
Route::get('/convocatorias/{id}/postulaciones', [PostulacionController::class, 'postulacionesPorConvocatoria']);
Route::patch('/postulaciones/{id}/estado',      [PostulacionController::class, 'cambiarEstado']);
Route::patch('/convocatorias/postulaciones/{id}/estado', [PostulacionController::class, 'cambiarEstado']);