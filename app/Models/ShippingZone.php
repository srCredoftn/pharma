<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class ShippingZone extends Model
{
    use HasFactory;

    protected $fillable = [
        'name',
        'cities',
        'min_weight',
        'max_weight',
        'base_cost',
        'per_kg_cost',
        'min_order_for_free',
        'delivery_days',
        'is_active',
    ];

    protected $casts = [
        'cities' => 'array',
        'min_weight' => 'integer',
        'max_weight' => 'integer',
        'base_cost' => 'decimal:2',
        'per_kg_cost' => 'decimal:4',
        'min_order_for_free' => 'decimal:2',
        'delivery_days' => 'integer',
        'is_active' => 'boolean',
    ];

    // Scopes
    public function scopeActive($query)
    {
        return $query->where('is_active', true);
    }

    public function scopeByCity($query, $city)
    {
        return $query->whereJsonContains('cities', $city);
    }

    // Methods
    public function calculateShippingCost($weight, $orderTotal)
    {
        // Si la commande est au-dessus du minimum gratuit, livraison gratuite
        if ($orderTotal >= $this->min_order_for_free) {
            return 0;
        }

        // Calcul : coût de base + coût par kg
        $cost = $this->base_cost + ($weight * $this->per_kg_cost);

        return max(0, (int) $cost);
    }

    public function includesCity($city)
    {
        return in_array($city, $this->cities ?? []);
    }
}
