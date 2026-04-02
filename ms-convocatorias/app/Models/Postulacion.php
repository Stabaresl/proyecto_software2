<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Postulacion extends Model
{
    use HasFactory;
    protected $table = 'postulaciones';

    protected $fillable = [
        'convocatoria_id',
        'estudiante_user_id',
        'estado',
        'carta_presentacion',
        'fecha_postulacion',
    ];

    protected $casts = [
        'fecha_postulacion' => 'datetime',
    ];

    public function convocatoria()
    {
        return $this->belongsTo(Convocatoria::class);
    }

    public function documentos()
    {
        return $this->hasMany(DocumentoPostulacion::class);
    }
}