<?php

namespace Database\Factories;

use App\Models\Convocatoria;
use Illuminate\Database\Eloquent\Factories\Factory;

class ConvocatoriaFactory extends Factory
{
    protected $model = Convocatoria::class;

    public function definition(): array
    {
        return [
            'publicador_user_id' => fake()->numberBetween(1, 100),
            'publicador_tipo'    => fake()->randomElement(['company', 'state']),
            'titulo'             => fake()->sentence(4),
            'descripcion'        => fake()->paragraph(),
            'tipo'               => fake()->randomElement(['practica', 'empleo', 'proyecto', 'beca']),
            'cupos'              => fake()->numberBetween(1, 10),
            'fecha_inicio'       => now()->addDay()->format('Y-m-d'),
            'fecha_cierre'       => now()->addMonths(2)->format('Y-m-d'),
            'estado'             => 'borrador',
            'requisitos'         => [],
            'condiciones'        => [],
        ];
    }
}