<?php

namespace Tests\Feature;

use App\Models\Convocatoria;
use App\Models\Postulacion;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class PostulacionTest extends TestCase
{
    use RefreshDatabase;

    private function authHeaders(string $role = 'student', int $userId = 1): array
    {
        return [
            'X-User-Id'   => $userId,
            'X-User-Role' => $role,
        ];
    }

    private function convocatoriaActiva(): Convocatoria
    {
        return Convocatoria::factory()->create([
            'estado'             => 'activa',
            'publicador_user_id' => 10,
            'publicador_tipo'    => 'company',
            'cupos'              => 5,
            'fecha_inicio'       => now()->subDay()->format('Y-m-d'),
            'fecha_cierre'       => now()->addMonths(2)->format('Y-m-d'),
        ]);
    }

    public function test_postularse_exitosamente(): void
    {
        $convocatoria = $this->convocatoriaActiva();

        $response = $this->withHeaders($this->authHeaders())
                         ->postJson("/api/convocatorias/{$convocatoria->id}/postular", [
                             'carta_presentacion' => 'Mi carta de presentación.',
                         ]);

        $response->assertStatus(201)
                 ->assertJson(['success' => true]);
    }

    public function test_postularse_falla_si_no_es_estudiante(): void
    {
        $convocatoria = $this->convocatoriaActiva();

        $response = $this->withHeaders($this->authHeaders('company'))
                         ->postJson("/api/convocatorias/{$convocatoria->id}/postular", []);

        $response->assertStatus(403);
    }

    public function test_postularse_falla_convocatoria_inactiva(): void
    {
        $convocatoria = Convocatoria::factory()->create(['estado' => 'borrador']);

        $response = $this->withHeaders($this->authHeaders())
                         ->postJson("/api/convocatorias/{$convocatoria->id}/postular", []);

        $response->assertStatus(400);
    }

    public function test_postularse_falla_duplicado(): void
    {
        $convocatoria = $this->convocatoriaActiva();

        Postulacion::factory()->create([
            'convocatoria_id'    => $convocatoria->id,
            'estudiante_user_id' => 1,
        ]);

        $response = $this->withHeaders($this->authHeaders())
                         ->postJson("/api/convocatorias/{$convocatoria->id}/postular", []);

        $response->assertStatus(409);
    }

    public function test_mis_postulaciones(): void
    {
        $convocatoria1 = $this->convocatoriaActiva();
        $convocatoria2 = $this->convocatoriaActiva();

        Postulacion::factory()->create([
            'convocatoria_id'    => $convocatoria1->id,
            'estudiante_user_id' => 1,
        ]);
        Postulacion::factory()->create([
            'convocatoria_id'    => $convocatoria2->id,
            'estudiante_user_id' => 1,
        ]);

        $response = $this->withHeaders($this->authHeaders())
                        ->getJson('/api/mis-postulaciones');

        $response->assertStatus(200)
                ->assertJson(['success' => true]);
    }

    public function test_cambiar_estado_postulacion(): void
    {
        $convocatoria = Convocatoria::factory()->create([
            'publicador_user_id' => 10,
            'estado'             => 'activa',
            'fecha_inicio'       => now()->subDay()->format('Y-m-d'),
            'fecha_cierre'       => now()->addMonths(2)->format('Y-m-d'),
        ]);

        $postulacion = Postulacion::factory()->create([
            'convocatoria_id'    => $convocatoria->id,
            'estudiante_user_id' => 1,
            'estado'             => 'en_revision',
        ]);

        $response = $this->withHeaders([
                             'X-User-Id'   => 10,
                             'X-User-Role' => 'company',
                         ])
                         ->patchJson("/api/postulaciones/{$postulacion->id}/estado", [
                             'estado' => 'preseleccionado',
                         ]);

        $response->assertStatus(200)
                 ->assertJson(['success' => true]);
    }
}