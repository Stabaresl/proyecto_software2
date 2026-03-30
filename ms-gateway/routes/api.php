<?php

use App\Http\Controllers\AuthController;
use Illuminate\Support\Facades\Route;

// ─── Rutas públicas ───────────────────────────────────────────
Route::prefix('auth')->group(function () {
    Route::post('/login',           [AuthController::class, 'login']);
    Route::post('/forgot-password', [AuthController::class, 'forgotPassword']);
    Route::post('/reset-password',  [AuthController::class, 'resetPassword']);
});

// ─── Rutas protegidas ─────────────────────────────────────────
Route::middleware(['jwt.auth'])->prefix('auth')->group(function () {
    Route::post('/logout', [AuthController::class, 'logout']);
    Route::get('/me',      [AuthController::class, 'me']);
});