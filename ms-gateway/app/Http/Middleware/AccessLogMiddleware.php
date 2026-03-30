<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;

class AccessLogMiddleware
{
    public function handle(Request $request, Closure $next)
    {
        $start    = microtime(true);
        $response = $next($request);
        $duration = round((microtime(true) - $start) * 1000, 2);

        Log::channel('daily')->info('ACCESS', [
            'method'   => $request->method(),
            'url'      => $request->fullUrl(),
            'ip'       => $request->ip(),
            'status'   => $response->getStatusCode(),
            'duration' => "{$duration}ms",
            'user'     => $request->input('auth_user_id', 'guest'),
        ]);

        return $response;
    }
}