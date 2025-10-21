<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Address extends Model
{
    use HasFactory;

    protected $fillable = [
        'user_id',
        'order_id',
        'type',
        'first_name',
        'last_name',
        'address1',
        'address2',
        'zip',
        'city',
        'country',
        'phone',
    ];

    // Relations
    public function user()
    {
        return $this->belongsTo(User::class);
    }

    public function order()
    {
        return $this->belongsTo(Order::class);
    }

    // Methods
    public function getFullAddressAttribute()
    {
        return trim("{$this->address1} {$this->address2}");
    }

    public function getFullNameAttribute()
    {
        return "{$this->first_name} {$this->last_name}";
    }
}
