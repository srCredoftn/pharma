<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void
    {
        Schema::create('products', function (Blueprint $table) {
            $table->id();
            $table->string('name');
            $table->string('slug')->unique();
            $table->unsignedBigInteger('brand_id')->nullable();
            $table->text('short_desc')->nullable();
            $table->longText('long_desc')->nullable();
            $table->string('sku')->unique();
            $table->string('ean')->nullable()->unique();
            $table->decimal('price_ht', 12, 2)->default(0);
            $table->decimal('price_ttc', 12, 2)->default(0);
            $table->decimal('tax_rate', 5, 4)->default(0.20);
            $table->integer('stock')->default(0);
            $table->boolean('is_active')->default(true);
            $table->timestamp('published_at')->nullable();
            $table->timestamps();

            $table->index('slug');
            $table->index('sku');
            $table->index('brand_id');
            $table->index('is_active');
            $table->index('published_at');
            $table->fullText(['name', 'sku', 'ean']);

            $table->foreign('brand_id')->references('id')->on('brands')->nullOnDelete();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('products');
    }
};
