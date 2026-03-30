<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('postulaciones', function (Blueprint $table) {
            $table->id();
            $table->foreignId('convocatoria_id')->constrained('convocatorias')->onDelete('cascade');
            $table->unsignedBigInteger('estudiante_user_id');
            $table->enum('estado', [
                'en_revision',
                'preseleccionado',
                'seleccionado',
                'rechazado',
            ])->default('en_revision');
            $table->text('carta_presentacion')->nullable();
            $table->timestamp('fecha_postulacion')->useCurrent();
            $table->timestamps();

            $table->unique(['convocatoria_id', 'estudiante_user_id']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('postulaciones');
    }
};