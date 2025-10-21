<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class PostCategory extends Model
{
    use HasFactory;

    protected $table = 'post_categories';
    public $timestamps = false;

    protected $fillable = [
        'name',
        'slug',
        'description',
    ];

    // Relations
    public function posts()
    {
        return $this->belongsToMany(Post::class, 'post_category');
    }

    // Boot
    protected static function boot()
    {
        parent::boot();

        static::creating(function ($model) {
            if (empty($model->slug)) {
                $model->slug = \Illuminate\Support\Str::slug($model->name);
            }
        });
    }

    public function getRouteKeyName()
    {
        return 'slug';
    }
}
