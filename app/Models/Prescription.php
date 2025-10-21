<?php

namespace App\Models;

use App\Enums\PrescriptionStatus;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Prescription extends Model
{
    use HasFactory;

    protected $fillable = [
        'order_id',
        'user_id',
        'status',
        'file_path',
        'file_disk',
        'file_name_original',
        'uploaded_by',
        'verified_by',
        'verified_at',
        'rejected_by',
        'rejected_at',
        'rejection_reason',
        'notes_internal',
    ];

    protected $casts = [
        'status' => PrescriptionStatus::class,
        'verified_at' => 'datetime',
        'rejected_at' => 'datetime',
    ];

    // Relations
    public function order()
    {
        return $this->belongsTo(Order::class);
    }

    public function user()
    {
        return $this->belongsTo(User::class);
    }

    public function uploadedByUser()
    {
        return $this->belongsTo(User::class, 'uploaded_by');
    }

    public function verifiedByUser()
    {
        return $this->belongsTo(User::class, 'verified_by');
    }

    public function rejectedByUser()
    {
        return $this->belongsTo(User::class, 'rejected_by');
    }

    // Scopes
    public function scopeByStatus($query, $status)
    {
        return $query->where('status', $status);
    }

    public function scopePending($query)
    {
        return $query->where('status', PrescriptionStatus::RECEIVED);
    }

    public function scopeByUser($query, $userId)
    {
        return $query->where('user_id', $userId);
    }

    public function scopeRecent($query)
    {
        return $query->orderBy('created_at', 'desc');
    }

    // Methods
    public function validate($verifiedBy)
    {
        $this->update([
            'status' => PrescriptionStatus::VALIDATED,
            'verified_by' => $verifiedBy,
            'verified_at' => now(),
        ]);
    }

    public function reject($rejectionReason, $rejectedBy)
    {
        $this->update([
            'status' => PrescriptionStatus::REJECTED,
            'rejection_reason' => $rejectionReason,
            'rejected_by' => $rejectedBy,
            'rejected_at' => now(),
        ]);
    }

    public function markAsProcessed()
    {
        $this->update(['status' => PrescriptionStatus::PROCESSED]);
    }

    public function getFileUrl()
    {
        return \Storage::disk($this->file_disk)->url($this->file_path);
    }

    public function getSignedFileUrl($expiresInMinutes = 60)
    {
        return \Storage::disk($this->file_disk)->temporaryUrl(
            $this->file_path,
            now()->addMinutes($expiresInMinutes)
        );
    }
}
