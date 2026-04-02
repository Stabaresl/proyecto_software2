<?php

namespace Tests\Feature;

use App\Models\Convocatoria;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class ConvocatoriaTest extends TestCase
{
    use RefreshDatabase;

    private function authHeaders(string $role = 'company', int $userId = 1): array
    {
        return [
            'X-User-Id'   => $userId,
            'X-User-Role' => $role,
        ];
    }

    private function convocatoriaData(array $overrides = []): array
    {
        return array_merge([
            'titulo'       => 'Práctica de Prueba',
            'descripcion'  => 'Descripción de prueba',
            'tipo'         => 'practica',
            'cupos'        => 3,
            'fecha_inicio' => now()->addDay()->format('Y-m-d'),
            'fecha_cierre' => now()->addMonths(2)->format('Y-m-d'),
        ], $overrides);
    }

    public function test_listar_convocatorias(): void
    {
        Convocatoria::factory()->count(3)->create();

        $response = $this->getJson('/api/convocatorias');

        $response->assertStatus(200)
                 ->assertJson(['success' => true])
                 ->assertJsonStructure(['success', 'data']);
    }

    public function test_crear_convocatoria_exitosa(): void
    {
        $response = $this->withHeaders($this->authHeaders())
                         ->postJson('/api/convocatorias', $this->convocatoriaData());

        $response->assertStatus(201)
                 ->assertJson(['success' => true])
                 ->assertJsonStructure(['data' => ['id', 'titulo', 'estado']]);
    }

    public function test_crear_convocatoria_falla_sin_auth(): void
    {
        $response = $this->postJson('/api/convocatorias', $this->convocatoriaData());
        $response->assertStatus(401);
    }

    public function test_crear_convocatoria_falla_role_student(): void
    {
        $response = $this->withHeaders($this->authHeaders('student'))
                         ->postJson('/api/convocatorias', $this->convocatoriaData());

        $response->assertStatus(403);
    }

    public function test_crear_convocatoria_falla_campos_requeridos(): void
    {
        $response = $this->withHeaders($this->authHeaders())
                         ->postJson('/api/convocatorias', []);

        $response->assertStatus(422);
    }

    public function test_ver_convocatoria(): void
    {
        $convocatoria = Convocatoria::factory()->create();

        $response = $this->getJson("/api/convocatorias/{$convocatoria->id}");

        $response->assertStatus(200)
                 ->assertJson(['success' => true, 'data' => ['id' => $convocatoria->id]]);
    }

    public function test_ver_convocatoria_no_existente(): void
    {
        $response = $this->getJson('/api/convocatorias/9999');
        $response->assertStatus(404);
    }

    public function test_cambiar_estado_convocatoria(): void
    {
        $convocatoria = Convocatoria::factory()->create([
            'publicador_user_id' => 1,
            'estado'             => 'borrador',
        ]);

        $response = $this->withHeaders($this->authHeaders())
                         ->patchJson("/api/convocatorias/{$convocatoria->id}/estado", [
                             'estado' => 'activa',
                         ]);

        $response->assertStatus(200)
                 ->assertJson(['success' => true]);
    }

    public function test_cambiar_estado_falla_sin_permiso(): void
    {
        $convocatoria = Convocatoria::factory()->create([
            'publicador_user_id' => 99,
        ]);

        $response = $this->withHeaders($this->authHeaders('company', 1))
                         ->patchJson("/api/convocatorias/{$convocatoria->id}/estado", [
                             'estado' => 'activa',
                         ]);

        $response->assertStatus(403);
    }

    public function test_mis_convocatorias(): void
    {
        Convocatoria::factory()->count(2)->create(['publicador_user_id' => 1]);
        Convocatoria::factory()->count(2)->create(['publicador_user_id' => 99]);

        $response = $this->withHeaders($this->authHeaders())
                         ->getJson('/api/mis-convocatorias');

        $response->assertStatus(200)
                 ->assertJson(['success' => true]);

        $this->assertCount(2, $response->json('data'));
    }
}