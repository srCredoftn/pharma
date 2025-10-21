<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Category extends Model
{
    use HasFactory;

    protected $fillable = [
        'name',
        'slug',
        'parent_id',
        'depth',
        'description',
        'image_media_id',
        'is_active',
        'path',
    ];

    protected $casts = [
        'is_active' => 'boolean',
        'depth' => 'integer',
    ];

    // Relations
    public function parent()
    {
        return $this->belongsTo(Category::class, 'parent_id');
    }

    public function children()
    {
        return $this->hasMany(Category::class, 'parent_id');
    }

    public function products()
    {
        return $this->belongsToMany(Product::class, 'product_category');
    }

    public function image()
    {
        return $this->belongsTo(Media::class, 'image_media_id');
    }

    // Scopes
    public function scopeActive($query)
    {
        return $query->where('is_active', true);
    }

    public function scopeRoot($query)
    {
        return $query->whereNull('parent_id');
    }

    public function scopeByDepth($query, $depth)
    {
        return $query->where('depth', $depth);
    }

    // Methods
    public function getAncestorsAttribute()
    {
        return collect(explode('/', trim($this->path, '/')))
            ->filter()
            ->map(fn($id) => Category::find($id))
            ->filter();
    }

    public function getDescendantsAttribute()
    {
        return Category::query()
            ->where('path', 'LIKE', "{$this->path}{$this->id}/%")
            ->get();
    }

    public function isRoot()
    {
        return is_null($this->parent_id);
    }

    // Boot
    protected static function boot()
    {
        parent::boot();

        static::creating(function ($model) {
            if (empty($model->slug)) {
                $model->slug = \Illuminate\Support\Str::slug($model->name);
            }

            if ($model->parent_id) {
                $parent = Category::find($model->parent_id);
                $model->depth = ($parent->depth ?? 0) + 1;
                $model->path = ($parent->path ?? '') . $parent->id . '/';
            } else {
                $model->depth = 0;
                $model->path = '/';
            }
        });
    }

    public function getRouteKeyName()
    {
        return 'slug';
    }
}
