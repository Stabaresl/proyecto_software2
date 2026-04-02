<?php

namespace Database\Factories;

use App\Models\Postulacion;
use Illuminate\Database\Eloquent\Factories\Factory;

class PostulacionFactory extends Factory
{
    protected $model = Postulacion::class;

    public function definition(): array
    {
        return [
            'convocatoria_id'    => 1,
            'estudiante_user_id' => fake()->numberBetween(1, 100),
            'estado'             => 'en_revision',
            'carta_presentacion' => fake()->paragraph(),
        ];
    }
}