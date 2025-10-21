<?php

return [
    'default' => env('PAYMENT_PROVIDER_DEFAULT', 'stripe'),
    
    'providers' => [
        'stripe' => [
            'driver' => 'stripe',
            'public_key' => env('STRIPE_PUBLIC_KEY'),
            'secret_key' => env('STRIPE_SECRET_KEY'),
            'webhook_secret' => env('WEBHOOK_SECRET_STRIPE'),
            'enabled' => true,
        ],
        
        'fedapay' => [
            'driver' => 'fedapay',
            'api_key' => env('FEDAPAY_API_KEY'),
            'public_key' => env('FEDAPAY_PUBLIC_KEY'),
            'webhook_secret' => env('WEBHOOK_SECRET_FEDAPAY'),
            'sandbox' => env('APP_ENV') !== 'production',
            'enabled' => env('FEDAPAY_API_KEY') !== null,
        ],
        
        'uba' => [
            'driver' => 'uba',
            'merchant_id' => env('UBA_MERCHANT_ID'),
            'api_key' => env('UBA_API_KEY'),
            'webhook_secret' => env('WEBHOOK_SECRET_UBA'),
            'sandbox' => env('APP_ENV') !== 'production',
            'enabled' => env('UBA_MERCHANT_ID') !== null,
        ],
    ],
    
    'webhook' => [
        'timeout' => 10,
        'retry_attempts' => 3,
        'retry_delay' => 300, // 5 minutes
    ],
    
    'currency' => env('DEFAULT_CURRENCY', 'XOF'),
];
