<?php

use Illuminate\Support\Facades\Route;

Route::inertia('/', 'welcome')->name('home');

Route::middleware(['auth', 'verified'])->group(function () {
    Route::inertia('dashboard', 'dashboard')->name('dashboard');
});



// Route::get("/photos") // the home page is this, since React SPA
Route::post("/photos/upload", 'upload'); // uploads from React (client browser)
Route::post("/photos/process", 'process'); // ship to server for processing
Route::post("/photos/download", 'package'); // renampe, zip, download on client machine

require __DIR__.'/settings.php';
