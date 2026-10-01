<?php

use App\Http\Controllers\PhotoController;
use Illuminate\Support\Facades\Route;

Route::inertia('/', 'welcome')->name('home');

Route::middleware(['auth', 'verified'])->group(function () {
    Route::inertia('dashboard', 'dashboard')->name('dashboard');
});
// Syntax convention: `route::httpMethod(url, [controller::class, method])->name(routeName)`
Route::get('photos', [PhotoController::class, 'index'])->name('photos.index');
Route::get('photos/preview/{id}', [PhotoController::class, 'preview'])->name('photos.preview');
Route::post('photos/upload', [PhotoController::class, 'upload'])->name('photos.upload');
Route::post('photos/process', [PhotoController::class, 'process'])->name('photos.process');
Route::post('photos/download', [PhotoController::class, 'download'])->name('photos.download');

require __DIR__ . '/settings.php';
