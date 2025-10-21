<?php

namespace App\Models;

use App\Enums\PaymentStatus;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Payment extends Model
{
    use HasFactory;

    protected $fillable = [
        'order_id',
        'provider',
        'intent_id',
        'status',
        'amount',
        'currency',
        'payload',
        'refund_amount',
        'refunded_at',
    ];

    protected $casts = [
        'status' => PaymentStatus::class,
        'amount' => 'decimal:2',
        'refund_amount' => 'decimal:2',
        'payload' => 'array',
        'refunded_at' => 'datetime',
    ];

    // Relations
    public function order()
    {
        return $this->belongsTo(Order::class);
    }

    // Scopes
    public function scopeByProvider($query, $provider)
    {
        return $query->where('provider', $provider);
    }

    public function scopeByStatus($query, $status)
    {
        return $query->where('status', $status);
    }

    public function scopeSuccessful($query)
    {
        return $query->where('status', PaymentStatus::SUCCESSFUL);
    }

    public function scopeFailed($query)
    {
        return $query->where('status', PaymentStatus::FAILED);
    }

    // Methods
    public function markAsSuccessful()
    {
        $this->update(['status' => PaymentStatus::SUCCESSFUL]);
        $this->order->markAsPaid();
    }

    public function markAsFailed()
    {
        $this->update(['status' => PaymentStatus::FAILED]);
    }

    public function refund($amount = null)
    {
        $refundAmount = $amount ?? $this->amount;
        
        $this->update([
            'status' => PaymentStatus::REFUNDED,
            'refund_amount' => $refundAmount,
            'refunded_at' => now(),
        ]);

        $this->order->update([
            'status' => \App\Enums\OrderStatus::REFUNDED,
        ]);
    }
}
