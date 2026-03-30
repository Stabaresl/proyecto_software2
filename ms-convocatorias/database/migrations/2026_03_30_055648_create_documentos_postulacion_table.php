<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('documentos_postulacion', function (Blueprint $table) {
            $table->id();
            $table->foreignId('postulacion_id')->constrained('postulaciones')->onDelete('cascade');
            $table->string('nombre');
            $table->string('url');
            $table->enum('tipo', ['cv', 'carta', 'certificado', 'otro'])->default('otro');
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('documentos_postulacion');
    }
};