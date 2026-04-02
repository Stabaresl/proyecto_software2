<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;

class Convocatoria extends Model
{
    use HasFactory;
    protected $table = 'convocatorias';

    protected $fillable = [
        'publicador_user_id',
        'publicador_tipo',
        'titulo',
        'descripcion',
        'tipo',
        'requisitos',
        'cupos',
        'fecha_inicio',
        'fecha_cierre',
        'estado',
        'condiciones',
    ];

    protected $casts = [
        'requisitos'   => 'array',
        'condiciones'  => 'array',
        'fecha_inicio' => 'date',
        'fecha_cierre' => 'date',
    ];

    public function postulaciones()
    {
        return $this->hasMany(Postulacion::class);
    }

    public function isActiva(): bool
    {
        return $this->estado === 'activa' && $this->fecha_cierre->isFuture();
    }

    public function cuposDisponibles(): int
    {
        $ocupados = $this->postulaciones()
            ->whereIn('estado', ['preseleccionado', 'seleccionado'])
            ->count();
        return max(0, $this->cupos - $ocupados);
    }
}