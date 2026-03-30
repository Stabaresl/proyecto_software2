<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Tymon\JWTAuth\Facades\JWTAuth;
use Tymon\JWTAuth\Exceptions\JWTException;
use Tymon\JWTAuth\Exceptions\TokenExpiredException;
use Tymon\JWTAuth\Exceptions\TokenInvalidException;

class JwtMiddleware
{
    public function handle(Request $request, Closure $next)
    {
        try {
            $token = JWTAuth::getToken();

            if (!$token) {
                return response()->json([
                    'success' => false,
                    'message' => 'Token no proporcionado.',
                ], 401);
            }

            $payload = JWTAuth::getPayload($token);
            $request->merge([
                'auth_user_id'   => $payload->get('sub'),
                'auth_user_role' => $payload->get('role'),
            ]);

        } catch (TokenExpiredException $e) {
            return response()->json(['success' => false, 'message' => 'Token expirado.'], 401);
        } catch (TokenInvalidException $e) {
            return response()->json(['success' => false, 'message' => 'Token inválido.'], 401);
        } catch (JWTException $e) {
            return response()->json(['success' => false, 'message' => 'Error de autenticación.'], 401);
        }

        return $next($request);
    }
}