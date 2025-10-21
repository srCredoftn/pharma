<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;
use Spatie\MediaLibrary\HasMedia;
use Spatie\MediaLibrary\InteractsWithMedia;

class Product extends Model implements HasMedia
{
    use HasFactory, Searchable, InteractsWithMedia;

    protected $fillable = [
        'name',
        'slug',
        'brand_id',
        'short_desc',
        'long_desc',
        'sku',
        'ean',
        'price_ht',
        'price_ttc',
        'tax_rate',
        'stock',
        'is_active',
        'published_at',
    ];

    protected $casts = [
        'price_ht' => 'decimal:2',
        'price_ttc' => 'decimal:2',
        'tax_rate' => 'decimal:4',
        'stock' => 'integer',
        'is_active' => 'boolean',
        'published_at' => 'datetime',
    ];

    // Relations
    public function brand()
    {
        return $this->belongsTo(Brand::class);
    }

    public function categories()
    {
        return $this->belongsToMany(Category::class, 'product_category');
    }

    public function cartItems()
    {
        return $this->hasMany(CartItem::class);
    }

    public function orderItems()
    {
        return $this->hasMany(OrderItem::class);
    }

    // Scopes
    public function scopeActive($query)
    {
        return $query->where('is_active', true);
    }

    public function scopePublished($query)
    {
        return $query->where('published_at', '<=', now());
    }

    public function scopeInStock($query)
    {
        return $query->where('stock', '>', 0);
    }

    public function scopeByCategory($query, $categoryId)
    {
        return $query->whereHas('categories', fn($q) => $q->where('category_id', $categoryId));
    }

    public function scopeByBrand($query, $brandId)
    {
        return $query->where('brand_id', $brandId);
    }

    public function scopeByPriceRange($query, $min, $max)
    {
        return $query->whereBetween('price_ttc', [$min, $max]);
    }

    public function scopeSearch($query, $term)
    {
        return $query->where('name', 'LIKE', "%{$term}%")
            ->orWhere('sku', 'LIKE', "%{$term}%")
            ->orWhere('ean', 'LIKE', "%{$term}%");
    }

    // Methods
    public function isAvailable()
    {
        return $this->is_active && $this->published_at <= now() && $this->stock > 0;
    }

    public function isLowStock($threshold = 5)
    {
        return $this->stock <= $threshold;
    }

    public function calculateTax()
    {
        return $this->price_ht * $this->tax_rate;
    }

    // Searchable
    public function toSearchableArray()
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'sku' => $this->sku,
            'ean' => $this->ean,
            'brand' => $this->brand?->name,
            'categories' => $this->categories->pluck('name')->implode(' '),
            'description' => $this->short_desc,
            'price' => (int) $this->price_ttc,
            'is_active' => $this->is_active,
            'stock' => $this->stock,
        ];
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

        static::updating(function ($model) {
            if (empty($model->slug)) {
                $model->slug = \Illuminate\Support\Str::slug($model->name);
            }
        });
    }

    public function getRouteKeyName()
    {
        return 'slug';
    }

    public function registerMediaCollections(): void
    {
        $this->addMediaCollection('gallery')
            ->acceptsMimeTypes(['image/jpeg', 'image/png', 'image/webp']);
    }

    public function registerMediaConversions($media = null): void
    {
        $this->addMediaConversion('thumbnail')
            ->width(300)
            ->height(300)
            ->sharpen(0, 0.5, 1);

        $this->addMediaConversion('medium')
            ->width(600)
            ->height(600)
            ->sharpen(0, 0.5, 1);

        $this->addMediaConversion('large')
            ->width(1200)
            ->height(1200)
            ->sharpen(0, 0.5, 1);
    }
}
