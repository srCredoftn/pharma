<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void
    {
        Schema::create('categories', function (Blueprint $table) {
            $table->id();
            $table->string('name');
            $table->string('slug')->unique();
            $table->unsignedBigInteger('parent_id')->nullable();
            $table->integer('depth')->default(0);
            $table->text('description')->nullable();
            $table->unsignedBigInteger('image_media_id')->nullable();
            $table->boolean('is_active')->default(true);
            $table->string('path')->default('/');
            $table->timestamps();

            $table->index('slug');
            $table->index('parent_id');
            $table->index('depth');
            $table->index('is_active');
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('categories');
    }
};
