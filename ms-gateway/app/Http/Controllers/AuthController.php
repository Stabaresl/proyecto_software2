<?php

namespace App\Http\Controllers;

use App\Models\PasswordResetToken;
use App\Models\TokenBlacklist;
use App\Models\User;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Validator;
use Illuminate\Support\Str;
use Tymon\JWTAuth\Facades\JWTAuth;
use Tymon\JWTAuth\Exceptions\JWTException;

class AuthController extends Controller
{
    // ─── LOGIN ────────────────────────────────────────────────
    public function login(Request $request): JsonResponse
    {
        $validator = Validator::make($request->all(), [
            'email'    => 'required|email',
            'password' => 'required|string|min:6',
        ]);

        if ($validator->fails()) {
            return response()->json([
                'success' => false,
                'errors'  => $validator->errors(),
            ], 422);
        }

        $credentials = $request->only('email', 'password');

        try {
            if (!$token = JWTAuth::attempt($credentials)) {
                return response()->json([
                    'success' => false,
                    'message' => 'Credenciales incorrectas.',
                ], 401);
            }
        } catch (JWTException $e) {
            return response()->json([
                'success' => false,
                'message' => 'No se pudo generar el token.',
            ], 500);
        }

        $user = JWTAuth::user();

        if ($user->status !== 'active') {
            JWTAuth::invalidate($token);
            return response()->json([
                'success' => false,
                'message' => 'Tu cuenta no está activa.',
            ], 403);
        }

        return response()->json([
            'success' => true,
            'message' => 'Login exitoso.',
            'token'   => $token,
            'user'    => [
                'id'     => $user->id,
                'email'  => $user->email,
                'role'   => $user->role,
                'status' => $user->status,
            ],
        ]);
    }

    // ─── LOGOUT ───────────────────────────────────────────────
    public function logout(Request $request): JsonResponse
    {
        try {
            $token = JWTAuth::getToken();

            if (!$token) {
                return response()->json([
                    'success' => false,
                    'message' => 'Token no proporcionado.',
                ], 400);
            }

            $payload    = JWTAuth::getPayload($token);
            $user       = JWTAuth::user();
            $expiresAt  = now()->setTimestamp($payload->get('exp'));

            TokenBlacklist::create([
                'user_id'    => $user->id,
                'token'      => $token->get(),
                'expires_at' => $expiresAt,
            ]);

            JWTAuth::invalidate($token);

            return response()->json([
                'success' => true,
                'message' => 'Sesión cerrada correctamente.',
            ]);
        } catch (JWTException $e) {
            return response()->json([
                'success' => false,
                'message' => 'Error al cerrar sesión.',
            ], 500);
        }
    }

    // ─── SOLICITAR RECUPERACIÓN DE CONTRASEÑA ─────────────────
    public function forgotPassword(Request $request): JsonResponse
    {
        $validator = Validator::make($request->all(), [
            'email' => 'required|email|exists:users,email',
        ]);

        if ($validator->fails()) {
            return response()->json([
                'success' => false,
                'errors'  => $validator->errors(),
            ], 422);
        }

        $user = User::where('email', $request->email)->first();

        // Invalidar tokens anteriores pendientes
        PasswordResetToken::where('user_id', $user->id)
            ->where('status', 'pending')
            ->update(['status' => 'expired']);

        $token = Str::random(64);

        PasswordResetToken::create([
            'user_id'    => $user->id,
            'token'      => hash('sha256', $token),
            'status'     => 'pending',
            'expires_at' => now()->addMinutes(30),
        ]);

        // Aquí se enviaría el email — se implementará con el ms-notificaciones
        // Mail::to($user->email)->send(new PasswordResetMail($token));

        return response()->json([
            'success' => true,
            'message' => 'Si el correo existe, recibirás instrucciones para restablecer tu contraseña.',
            // Solo en desarrollo devolvemos el token directamente
            'dev_token' => app()->environment('local') ? $token : null,
        ]);
    }

    // ─── RESTABLECER CONTRASEÑA ────────────────────────────────
    public function resetPassword(Request $request): JsonResponse
    {
        $validator = Validator::make($request->all(), [
            'token'                 => 'required|string',
            'email'                 => 'required|email|exists:users,email',
            'password'              => 'required|string|min:8|confirmed',
            'password_confirmation' => 'required|string',
        ]);

        if ($validator->fails()) {
            return response()->json([
                'success' => false,
                'errors'  => $validator->errors(),
            ], 422);
        }

        $user = User::where('email', $request->email)->first();

        $resetToken = PasswordResetToken::where('user_id', $user->id)
            ->where('token', hash('sha256', $request->token))
            ->where('status', 'pending')
            ->first();

        if (!$resetToken) {
            return response()->json([
                'success' => false,
                'message' => 'Token inválido o no encontrado.',
            ], 400);
        }

        if ($resetToken->isExpired()) {
            $resetToken->update(['status' => 'expired']);
            return response()->json([
                'success' => false,
                'message' => 'El token ha expirado. Solicita uno nuevo.',
            ], 400);
        }

        $user->update([
            'password' => Hash::make($request->password),
        ]);

        $resetToken->update(['status' => 'used']);

        return response()->json([
            'success' => true,
            'message' => 'Contraseña restablecida correctamente.',
        ]);
    }

    // ─── PERFIL DEL USUARIO AUTENTICADO ───────────────────────
    public function me(Request $request): JsonResponse
    {
        $user = JWTAuth::user();

        return response()->json([
            'success' => true,
            'user'    => [
                'id'         => $user->id,
                'email'      => $user->email,
                'role'       => $user->role,
                'status'     => $user->status,
                'created_at' => $user->created_at,
            ],
        ]);
    }

    // ─── REGISTER ─────────────────────────────────────────────────
    public function register(Request $request): JsonResponse
    {
        $validator = Validator::make($request->all(), [
            'email'    => 'required|email|unique:users,email',
            'password' => 'required|string|min:8|confirmed',
            'password_confirmation' => 'required|string',
            'role'     => 'required|in:student,university,company,state',
        ]);

        if ($validator->fails()) {
            return response()->json([
                'success' => false,
                'errors'  => $validator->errors(),
            ], 422);
        }

        try {
            $user = User::create([
                'email'    => $request->email,
                'password' => Hash::make($request->password),
                'role'     => $request->role,
                'status'   => 'pending',
            ]);

            $token = JWTAuth::fromUser($user);

            return response()->json([
                'success' => true,
                'message' => 'Usuario registrado correctamente.',
                'token'   => $token,
                'user'    => [
                    'id'     => $user->id,
                    'email'  => $user->email,
                    'role'   => $user->role,
                    'status' => $user->status,
                ],
            ], 201);

        } catch (\Exception $e) {
            return response()->json([
                'success' => false,
                'message' => 'Error al registrar el usuario.',
                'error'   => app()->environment('local') ? $e->getMessage() : null,
            ], 500);
        }
    }
}