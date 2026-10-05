<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class PhotoUploadRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'photos' => 'required|array',
            'photos.*' => 'required|file|mimes:jpg,jpeg,png,tiff,tif,webp|max:51200',
        ];
    }

    public function messages(): array
    {
        return [
            'photos.required' => 'At least one photo is required.',
            'photos.array' => 'Photos must be provided as an array.',
            'photos.*.file' => 'Each item must be a valid file.',
            'photos.*.mimes' => 'Only JPG, JPEG, PNG, TIFF, and WebP files are allowed.',
            'photos.*.max' => 'Each photo must be less than 50MB.',
        ];
    }
}
