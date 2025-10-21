<?php

return [
    'country_code' => 'BJ',
    'country_name' => 'République du Bénin',
    'locale' => 'fr_BJ',
    'timezone' => 'Africa/Porto-Novo',
    
    'currency' => [
        'code' => 'XOF',
        'name' => 'Franc CFA',
        'symbol' => 'F CFA',
        'decimal_separator' => ',',
        'thousands_separator' => ' ',
        'decimal_places' => 0,
    ],
    
    'company' => [
        'name' => env('COMPANY_NAME', 'Pharmacie Camp Guézo'),
        'address' => env('COMPANY_ADDRESS', 'Cotonou, République du Bénin'),
        'phone' => env('COMPANY_PHONE', '+229 0121 31 35 55'),
        'email' => env('COMPANY_EMAIL', 'info@pharmaciecampguezo.net'),
        'website' => env('APP_URL', 'https://pharmacie.benin'),
    ],
    
    'taxes' => [
        'default_rate' => (float) env('DEFAULT_TAX_RATE', 0.20),
        'variable_by_category' => [
            'medicines' => 0.00,
            'parapharmacy' => 0.20,
            'cosmetics' => 0.20,
        ],
    ],
    
    'shipping' => [
        'default_cost' => (int) env('DEFAULT_SHIPPING_COST', 5000),
        'free_above' => 50000,
        'zones' => [
            'cotonou' => [
                'name' => 'Cotonou',
                'cities' => ['Cotonou'],
                'min_cost' => 2000,
                'max_cost' => 5000,
                'delivery_days' => 1,
            ],
            'abomey-calavi' => [
                'name' => 'Abomey-Calavi',
                'cities' => ['Abomey-Calavi', 'Sèmè-Kpodji', 'Ouidah'],
                'min_cost' => 3000,
                'max_cost' => 7000,
                'delivery_days' => 2,
            ],
            'porto-novo' => [
                'name' => 'Porto-Novo',
                'cities' => ['Porto-Novo'],
                'min_cost' => 3500,
                'max_cost' => 7500,
                'delivery_days' => 2,
            ],
            'other' => [
                'name' => 'Autres régions',
                'cities' => ['Parakou', 'Natitingou', 'Djougou', 'Lokossa'],
                'min_cost' => 8000,
                'max_cost' => 15000,
                'delivery_days' => 3,
            ],
        ],
    ],
    
    'phone' => [
        'country_code' => '+229',
        'regex' => '/^\+229\d{8}$/',
        'mask' => '+229 9999 9999',
    ],
    
    'payment_providers' => [
        'primary' => 'stripe',
        'secondary' => ['fedapay', 'uba'],
        'enabled' => ['stripe', 'fedapay', 'uba'],
    ],
    
    'contact' => [
        'admin_email' => env('ADMIN_EMAIL', 'admin@pharmaciecampguezo.net'),
        'admin_phone' => env('ADMIN_PHONE', '+229 0121 31 35 55'),
        'support_email' => env('MAIL_FROM_ADDRESS', 'info@pharmaciecampguezo.net'),
        'support_phone' => env('COMPANY_PHONE', '+229 0121 31 35 55'),
    ],
];
