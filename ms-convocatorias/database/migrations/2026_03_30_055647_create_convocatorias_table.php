<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('convocatorias', function (Blueprint $table) {
            $table->id();
            $table->unsignedBigInteger('publicador_user_id');
            $table->enum('publicador_tipo', ['company', 'state']);
            $table->string('titulo');
            $table->text('descripcion');
            $table->enum('tipo', [
                'practica',
                'empleo',
                'proyecto',
                'beca',
                'reto_nacional',
                'investigacion',
            ]);
            $table->json('requisitos')->nullable();
            $table->unsignedInteger('cupos')->default(1);
            $table->date('fecha_inicio');
            $table->date('fecha_cierre');
            $table->enum('estado', ['borrador', 'activa', 'pausada', 'cerrada'])->default('borrador');
            $table->json('condiciones')->nullable();
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('convocatorias');
    }
};