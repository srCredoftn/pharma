<?php

namespace App\Enums;

enum Role: string
{
    case ADMIN = 'admin';
    case PHARMACIST = 'pharmacien';
    case CLIENT = 'client';

    public function label(): string
    {
        return match($this) {
            self::ADMIN => 'Administrateur',
            self::PHARMACIST => 'Pharmacien',
            self::CLIENT => 'Client',
        };
    }

    public function description(): string
    {
        return match($this) {
            self::ADMIN => 'Accès complet à l\'administration',
            self::PHARMACIST => 'Gestion des ordonnances et commandes',
            self::CLIENT => 'Accès client standard',
        };
    }
}
