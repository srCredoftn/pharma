<?php

namespace App\Models;

use App\Enums\OrderStatus;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Order extends Model
{
    use HasFactory;

    protected $fillable = [
        'user_id',
        'number',
        'status',
        'currency',
        'subtotal',
        'tax_total',
        'shipping_total',
        'discount_total',
        'grand_total',
        'paid_at',
        'shipped_at',
        'delivered_at',
        'notes',
    ];

    protected $casts = [
        'status' => OrderStatus::class,
        'subtotal' => 'decimal:2',
        'tax_total' => 'decimal:2',
        'shipping_total' => 'decimal:2',
        'discount_total' => 'decimal:2',
        'grand_total' => 'decimal:2',
        'paid_at' => 'datetime',
        'shipped_at' => 'datetime',
        'delivered_at' => 'datetime',
    ];

    // Relations
    public function user()
    {
        return $this->belongsTo(User::class);
    }

    public function items()
    {
        return $this->hasMany(OrderItem::class);
    }

    public function shippingAddress()
    {
        return $this->hasOne(Address::class)->where('type', 'shipping');
    }

    public function billingAddress()
    {
        return $this->hasOne(Address::class)->where('type', 'billing');
    }

    public function payment()
    {
        return $this->hasOne(Payment::class);
    }

    public function shipment()
    {
        return $this->hasOne(Shipment::class);
    }

    public function prescriptions()
    {
        return $this->hasMany(Prescription::class);
    }

    // Scopes
    public function scopeByStatus($query, $status)
    {
        return $query->where('status', $status);
    }

    public function scopeByUser($query, $userId)
    {
        return $query->where('user_id', $userId);
    }

    public function scopePaid($query)
    {
        return $query->where('paid_at', '!=', null);
    }

    public function scopeUnpaid($query)
    {
        return $query->where('paid_at', null);
    }

    public function scopeRecent($query)
    {
        return $query->orderBy('created_at', 'desc');
    }

    // Methods
    public function markAsPaid()
    {
        $this->update([
            'status' => OrderStatus::PAID,
            'paid_at' => now(),
        ]);
    }

    public function markAsProcessing()
    {
        $this->update(['status' => OrderStatus::PROCESSING]);
    }

    public function markAsShipped($trackingNumber = null)
    {
        $this->update([
            'status' => OrderStatus::SHIPPED,
            'shipped_at' => now(),
        ]);

        if ($trackingNumber && !$this->shipment) {
            $this->shipment()->create([
                'tracking_number' => $trackingNumber,
                'status' => 'shipped',
            ]);
        }
    }

    public function markAsDelivered()
    {
        $this->update([
            'status' => OrderStatus::DELIVERED,
            'delivered_at' => now(),
        ]);
    }

    public function cancel()
    {
        $this->update(['status' => OrderStatus::CANCELED]);
    }

    public function getOrderNumberAttribute()
    {
        return $this->attributes['number'] ?? "ORD-{$this->id}";
    }

    // Boot
    protected static function boot()
    {
        parent::boot();

        static::creating(function ($order) {
            if (empty($order->number)) {
                $order->number = 'ORD-' . strtoupper(uniqid());
            }
            if (empty($order->status)) {
                $order->status = OrderStatus::DRAFT;
            }
            if (empty($order->currency)) {
                $order->currency = config('benin.currency.code', 'XOF');
            }
        });
    }
}
