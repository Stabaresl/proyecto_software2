<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class DocumentoPostulacion extends Model
{
    protected $table = 'documentos_postulacion';

    protected $fillable = [
        'postulacion_id',
        'nombre',
        'url',
        'tipo',
    ];

    public function postulacion()
    {
        return $this->belongsTo(Postulacion::class);
    }
}