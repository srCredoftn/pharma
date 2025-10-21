<?php

namespace App\Enums;

enum ShipmentStatus: string
{
    case PENDING = 'pending';
    case SHIPPED = 'shipped';
    case IN_TRANSIT = 'in_transit';
    case DELIVERED = 'delivered';
    case FAILED = 'failed';

    public function label(): string
    {
        return match($this) {
            self::PENDING => 'En attente',
            self::SHIPPED => 'Expédié',
            self::IN_TRANSIT => 'En transit',
            self::DELIVERED => 'Livré',
            self::FAILED => 'Échec de livraison',
        };
    }

    public function color(): string
    {
        return match($this) {
            self::PENDING => 'yellow',
            self::SHIPPED => 'blue',
            self::IN_TRANSIT => 'indigo',
            self::DELIVERED => 'green',
            self::FAILED => 'red',
        };
    }

    public function isCompleted(): bool
    {
        return in_array($this, [self::DELIVERED, self::FAILED]);
    }
}
