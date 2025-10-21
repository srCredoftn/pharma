<?php

namespace App\Enums;

enum PaymentStatus: string
{
    case PENDING = 'pending';
    case SUCCESSFUL = 'successful';
    case FAILED = 'failed';
    case REFUNDED = 'refunded';
    case CANCELLED = 'cancelled';

    public function label(): string
    {
        return match($this) {
            self::PENDING => 'En attente',
            self::SUCCESSFUL => 'Réussi',
            self::FAILED => 'Échoué',
            self::REFUNDED => 'Remboursé',
            self::CANCELLED => 'Annulé',
        };
    }

    public function color(): string
    {
        return match($this) {
            self::PENDING => 'yellow',
            self::SUCCESSFUL => 'green',
            self::FAILED => 'red',
            self::REFUNDED => 'orange',
            self::CANCELLED => 'gray',
        };
    }

    public function isCompleted(): bool
    {
        return in_array($this, [self::SUCCESSFUL, self::FAILED, self::REFUNDED, self::CANCELLED]);
    }
}
