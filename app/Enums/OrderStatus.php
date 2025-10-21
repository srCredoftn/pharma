<?php

namespace App\Enums;

enum OrderStatus: string
{
    case DRAFT = 'draft';
    case PENDING_PAYMENT = 'pending_payment';
    case PAID = 'paid';
    case PROCESSING = 'processing';
    case SHIPPED = 'shipped';
    case DELIVERED = 'delivered';
    case CANCELED = 'canceled';
    case REFUNDED = 'refunded';

    public function label(): string
    {
        return match($this) {
            self::DRAFT => 'Brouillon',
            self::PENDING_PAYMENT => 'En attente de paiement',
            self::PAID => 'Payée',
            self::PROCESSING => 'En traitement',
            self::SHIPPED => 'Expédiée',
            self::DELIVERED => 'Livrée',
            self::CANCELED => 'Annulée',
            self::REFUNDED => 'Remboursée',
        };
    }

    public function color(): string
    {
        return match($this) {
            self::DRAFT => 'gray',
            self::PENDING_PAYMENT => 'yellow',
            self::PAID => 'green',
            self::PROCESSING => 'blue',
            self::SHIPPED => 'indigo',
            self::DELIVERED => 'emerald',
            self::CANCELED => 'red',
            self::REFUNDED => 'orange',
        };
    }

    public function isCompleted(): bool
    {
        return in_array($this, [self::DELIVERED, self::CANCELED, self::REFUNDED]);
    }

    public function isPending(): bool
    {
        return $this === self::PENDING_PAYMENT;
    }
}
