<?php

namespace App\Models;

use App\Enums\ShipmentStatus;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Shipment extends Model
{
    use HasFactory;

    protected $fillable = [
        'order_id',
        'carrier',
        'tracking_number',
        'tracking_url',
        'status',
        'shipped_at',
        'delivered_at',
    ];

    protected $casts = [
        'status' => ShipmentStatus::class,
        'shipped_at' => 'datetime',
        'delivered_at' => 'datetime',
    ];

    // Relations
    public function order()
    {
        return $this->belongsTo(Order::class);
    }

    // Methods
    public function markAsShipped()
    {
        $this->update([
            'status' => ShipmentStatus::SHIPPED,
            'shipped_at' => now(),
        ]);
    }

    public function markAsInTransit()
    {
        $this->update(['status' => ShipmentStatus::IN_TRANSIT]);
    }

    public function markAsDelivered()
    {
        $this->update([
            'status' => ShipmentStatus::DELIVERED,
            'delivered_at' => now(),
        ]);
        $this->order->markAsDelivered();
    }

    public function markAsFailed($reason = null)
    {
        $this->update(['status' => ShipmentStatus::FAILED]);
    }
}
