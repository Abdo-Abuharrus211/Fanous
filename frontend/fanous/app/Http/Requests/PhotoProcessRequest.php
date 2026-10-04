<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class PhotoProcessRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'photo_ids' => 'required|array|min:1',
            'photo_ids.*' => 'required|string',
        ];
    }

    public function messages(): array
    {
        return [
            'photo_ids.required' => 'At least one photo must be selected for processing.',
            'photo_ids.array' => 'Photo IDs must be provided as an array.',
            'photo_ids.*.string' => 'Each photo ID must be a valid string.',
        ];
    }
}
