<?php

namespace App\Enums;

enum PrescriptionStatus: string
{
    case RECEIVED = 'received';
    case VALIDATED = 'validated';
    case REJECTED = 'rejected';
    case PROCESSED = 'processed';

    public function label(): string
    {
        return match($this) {
            self::RECEIVED => 'Reçue',
            self::VALIDATED => 'Validée',
            self::REJECTED => 'Rejetée',
            self::PROCESSED => 'Traitée',
        };
    }

    public function color(): string
    {
        return match($this) {
            self::RECEIVED => 'blue',
            self::VALIDATED => 'green',
            self::REJECTED => 'red',
            self::PROCESSED => 'emerald',
        };
    }

    public function isPending(): bool
    {
        return $this === self::RECEIVED;
    }

    public function isCompleted(): bool
    {
        return in_array($this, [self::VALIDATED, self::PROCESSED]);
    }

    public function isRejected(): bool
    {
        return $this === self::REJECTED;
    }
}
