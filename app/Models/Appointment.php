<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Appointment extends Model
{
    use HasFactory;

    protected $fillable = [
        'user_id',
        'service_type',
        'starts_at',
        'ends_at',
        'notes_user',
        'notes_admin',
        'status',
    ];

    protected $casts = [
        'starts_at' => 'datetime',
        'ends_at' => 'datetime',
    ];

    // Relations
    public function user()
    {
        return $this->belongsTo(User::class);
    }

    // Scopes
    public function scopeByUser($query, $userId)
    {
        return $query->where('user_id', $userId);
    }

    public function scopeByStatus($query, $status)
    {
        return $query->where('status', $status);
    }

    public function scopeUpcoming($query)
    {
        return $query->where('starts_at', '>', now())
            ->whereIn('status', ['pending', 'confirmed'])
            ->orderBy('starts_at');
    }

    public function scopePast($query)
    {
        return $query->where('starts_at', '<', now())
            ->orderBy('starts_at', 'desc');
    }

    // Methods
    public function confirm()
    {
        $this->update(['status' => 'confirmed']);
    }

    public function cancel()
    {
        $this->update(['status' => 'canceled']);
    }

    public function complete()
    {
        $this->update(['status' => 'completed']);
    }

    public function isUpcoming()
    {
        return $this->starts_at > now();
    }

    public function isPast()
    {
        return $this->starts_at < now();
    }
}
