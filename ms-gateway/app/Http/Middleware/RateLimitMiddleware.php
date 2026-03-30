<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Cache;

class RateLimitMiddleware
{
    private int $maxRequests = 60;
    private int $decaySeconds = 60;

    public function handle(Request $request, Closure $next)
    {
        $key = 'rate_limit:' . $request->ip();

        $requests = Cache::get($key, 0);

        if ($requests >= $this->maxRequests) {
            return response()->json([
                'success' => false,
                'message' => 'Demasiadas solicitudes. Intenta de nuevo en un minuto.',
            ], 429);
        }

        Cache::put($key, $requests + 1, $this->decaySeconds);

        return $next($request);
    }
}