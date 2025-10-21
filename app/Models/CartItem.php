<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class CartItem extends Model
{
    use HasFactory;

    protected $fillable = [
        'cart_id',
        'product_id',
        'quantity',
        'unit_price',
    ];

    protected $casts = [
        'quantity' => 'integer',
        'unit_price' => 'decimal:2',
    ];

    protected $appends = ['total'];

    // Relations
    public function cart()
    {
        return $this->belongsTo(Cart::class);
    }

    public function product()
    {
        return $this->belongsTo(Product::class);
    }

    // Accessors
    public function getTotalAttribute()
    {
        return $this->quantity * $this->unit_price;
    }

    // Mutators
    protected static function boot()
    {
        parent::boot();

        static::created(function ($item) {
            $item->cart->recalculateTotals();
        });

        static::updated(function ($item) {
            $item->cart->recalculateTotals();
        });

        static::deleted(function ($item) {
            $item->cart->recalculateTotals();
        });
    }
}
