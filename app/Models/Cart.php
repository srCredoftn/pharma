<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Cart extends Model
{
    use HasFactory;

    protected $fillable = [
        'user_id',
        'session_id',
        'currency',
        'coupon_code',
        'subtotal',
        'tax_total',
        'shipping_total',
        'discount_total',
        'grand_total',
    ];

    protected $casts = [
        'subtotal' => 'decimal:2',
        'tax_total' => 'decimal:2',
        'shipping_total' => 'decimal:2',
        'discount_total' => 'decimal:2',
        'grand_total' => 'decimal:2',
    ];

    // Relations
    public function user()
    {
        return $this->belongsTo(User::class);
    }

    public function items()
    {
        return $this->hasMany(CartItem::class);
    }

    // Scopes
    public function scopeActive($query)
    {
        return $query->whereNull('converted_to_order_at');
    }

    public function scopeForUser($query, $userId)
    {
        return $query->where('user_id', $userId);
    }

    public function scopeForSession($query, $sessionId)
    {
        return $query->where('session_id', $sessionId);
    }

    // Methods
    public function addItem($product, $quantity)
    {
        $existingItem = $this->items()
            ->where('product_id', $product->id)
            ->first();

        if ($existingItem) {
            $existingItem->increment('quantity', $quantity);
            return $existingItem;
        }

        return $this->items()->create([
            'product_id' => $product->id,
            'quantity' => $quantity,
            'unit_price' => $product->price_ttc,
        ]);
    }

    public function updateItem($itemId, $quantity)
    {
        $item = $this->items()->find($itemId);
        if ($item) {
            $item->update(['quantity' => $quantity]);
            $this->recalculateTotals();
        }
        return $item;
    }

    public function removeItem($itemId)
    {
        $this->items()->where('id', $itemId)->delete();
        $this->recalculateTotals();
    }

    public function clear()
    {
        $this->items()->delete();
        $this->update([
            'subtotal' => 0,
            'tax_total' => 0,
            'shipping_total' => 0,
            'grand_total' => 0,
        ]);
    }

    public function recalculateTotals()
    {
        $subtotal = $this->items()->sum('total');
        $taxTotal = $this->items()->sum(fn($item) => $item->product->calculateTax());
        
        $this->update([
            'subtotal' => $subtotal,
            'tax_total' => $taxTotal,
            'grand_total' => $subtotal + $taxTotal + $this->shipping_total,
        ]);
    }

    public function isEmpty()
    {
        return $this->items()->count() === 0;
    }

    public function getItemCount()
    {
        return $this->items()->sum('quantity');
    }
}
