<?php

namespace App\Http\Controllers;

use GuzzleHttp\Client;
use GuzzleHttp\Exception\ConnectException;
use GuzzleHttp\Exception\RequestException;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Tymon\JWTAuth\Facades\JWTAuth;

class GatewayController extends Controller
{
    private Client $client;

    private array $serviceMap = [
        'usuarios'       => 'MS_USUARIOS_URL',
        'convocatorias'  => 'MS_CONVOCATORIAS_URL',
        'formaciones'    => 'MS_FORMACION_URL',
        'acuerdos'       => 'MS_FORMACION_URL',
        'catalogo'       => 'MS_MATCHING_URL',
        'matching'       => 'MS_MATCHING_URL',
        'notificaciones' => 'MS_NOTIFICACIONES_URL',
    ];

    private array $servicePrefixes = [
        'usuarios'       => '',
        'convocatorias'  => 'convocatorias',
        'formaciones'    => 'formaciones',
        'acuerdos'       => 'acuerdos',
        'catalogo'       => 'catalogo',
        'matching'       => 'matching',
        'notificaciones' => 'notificaciones',
    ];

    public function __construct()
    {
        $this->client = new Client(['timeout' => 15]);
    }

    public function forward(Request $request, string $service, string $path = ''): JsonResponse
    {
        $envKey = $this->serviceMap[$service] ?? null;

        if (!$envKey || !env($envKey)) {
            return response()->json([
                'success' => false,
                'message' => "Servicio '{$service}' no encontrado.",
            ], 404);
        }

        $baseUrl   = rtrim(env($envKey), '/');
        $prefix    = $this->servicePrefixes[$service] ?? $service;
        $cleanPath = $path ? "/{$path}" : '';

        $djangoServices = ['usuarios'];
        $slash = in_array($service, $djangoServices) ? '/' : '';

        $targetUrl = $prefix
            ? "{$baseUrl}/api/{$prefix}{$cleanPath}{$slash}"
            : "{$baseUrl}/api{$cleanPath}{$slash}";

        if ($request->getQueryString()) {
            $targetUrl .= '?' . $request->getQueryString();
        }

        $headers = [
            'Content-Type' => 'application/json',
            'Accept'       => 'application/json',
        ];

        try {
            $token = JWTAuth::getToken();
            if ($token) {
                $headers['Authorization'] = 'Bearer ' . $token->get();
                $payload = JWTAuth::getPayload($token);
                $headers['X-User-Id']   = $payload->get('sub');
                $headers['X-User-Role'] = $payload->get('role');
            }
        } catch (\Exception $e) {}

        try {
            $options = [
                'headers'     => $headers,
                'http_errors' => false,
            ];

            if (in_array($request->method(), ['POST', 'PUT', 'PATCH'])) {
                $options['json'] = $request->all();
            }

            $response   = $this->client->request($request->method(), $targetUrl, $options);
            $body       = json_decode($response->getBody()->getContents(), true);
            $statusCode = $response->getStatusCode();

            return response()->json($body, $statusCode);

        } catch (ConnectException $e) {
            return response()->json([
                'success' => false,
                'message' => "No se pudo conectar con el servicio '{$service}'. Verifica que esté corriendo.",
            ], 503);
        } catch (RequestException $e) {
            return response()->json([
                'success' => false,
                'message' => 'Error al procesar la solicitud en el microservicio.',
            ], 500);
        }
    }
}