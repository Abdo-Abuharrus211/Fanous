<?php

namespace App\Http\Controllers;

use App\Http\Requests\PhotoDownloadRequest;
use App\Http\Requests\PhotoProcessRequest;
use App\Http\Requests\PhotoUploadRequest;
use App\Models\Photo;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Str;
use Inertia\Inertia;
use Inertia\Response as InertiaResponse;
use Symfony\Component\HttpFoundation\StreamedResponse;

class PhotoController extends Controller
{
    /**
     * Show the photo upload page.
     */
    public function index(Request $request): InertiaResponse
    {
        $sessionId = $this->sessionId($request);

        $photos = Photo::listForSession($sessionId);

        return Inertia::render('photos', [
            'sessionId' => $sessionId,
            'photos' => array_map(fn (Photo $p) => $p->toArray(), $photos),
        ]);
    }

    /**
     * Accept uploaded files and save to temp storage.
     *
     * @return JsonResponse
     */
    public function upload(PhotoUploadRequest $request)
    {
        $sessionId = $this->sessionId($request);
        $_seshDirExists = Photo::ensureSessionDir($sessionId);

        $files = $request->file('photos');

        if (! is_array($files)) {
            $files = [$files];
        }

        // create Photo objects and store them
        $photos = array_map(
            fn ($file) => Photo::fromUpload($file, $sessionId)->toArray(),
            $files,
        );

        return response()->json(['photos' => $photos]);
    }

    /**
     * Send photos to the backend API for analysis, then update with results.
     *
     * @return JsonResponse
     */
    public function process(PhotoProcessRequest $request)
    {
        $sessionId = $this->sessionId($request);
        $photoIds = $request->input('photo_ids', []);

        if (empty($photoIds)) {
            return response()->json(['error' => 'No photos selected'], 422);
        }

        $backendUrl = config('services.fanous_backend.url');

        if (! $backendUrl) {
            return response()->json([
                'error' => 'Backend server URL not configured. Set FANOUS_SERVER_URL in .env',
            ], 500);
        }

        $results = [];

        foreach ($photoIds as $photoId) {
            $photos = Photo::listForSession($sessionId);
            $photo = collect($photos)->first(fn (Photo $p) => $p->id === $photoId);

            if (! $photo) {
                $results[] = [
                    'id' => $photoId,
                    'status' => 'error',
                    'error' => 'Photo not found',
                ];

                continue;
            }

            // get the acutal photo files from storage
            $contents = $photo->contents();

            if ($contents === false) {
                $results[] = [
                    'id' => $photoId,
                    'status' => 'error',
                    'error' => 'Could not read photo file',
                ];

                continue;
            }

            try {
                $response = Http::timeout(80)
                    ->attach('image', $contents, basename($photo->tempPath))
                    ->post("{$backendUrl}/caption");

                if ($response->successful()) {
                    $data = $response->json();
                    $newName = $data['name'] ?? $data['caption'] ?? $photo->originalName;
                    $description = $data['description'] ?? $data['caption'] ?? null;

                    $updated = $photo->withAnalysis($newName, $description);
                    $results[] = $updated->toArray();

                    // Save updated metadata to session storage for later
                    Storage::put(
                        "temp/{$sessionId}/{$photoId}.meta.json",
                        json_encode([
                            'newName' => $newName,
                            'newDescription' => $description,
                        ]),
                    );
                } else {
                    $results[] = [
                        'id' => $photoId,
                        'status' => 'error',
                        'error' => $response->body(),
                    ];
                }
            } catch (\Exception $e) {
                $results[] = [
                    'id' => $photoId,
                    'status' => 'error',
                    'error' => $e->getMessage(),
                ];
            }
        }

        return response()->json(['results' => $results]);
    }

    /**
     * Rename photos, create a zip, and stream it to the user for download.
     */
    public function download(PhotoDownloadRequest $request): StreamedResponse
    {
        $sessionId = $this->sessionId($request);
        $photoIds = $request->input('photo_ids', []);

        $photos = Photo::listForSession($sessionId);
        $selected = collect($photos)->filter(fn (Photo $p) => in_array($p->id, $photoIds));

        if ($selected->isEmpty()) {
            abort(404, 'No photos found for download');
        }

        $zipPath = "temp/{$sessionId}/fanous-{$sessionId}.zip";
        $zip = new \ZipArchive;
        $zip->open(Storage::path($zipPath), \ZipArchive::CREATE | \ZipArchive::OVERWRITE);

        foreach ($selected as $photo) {
            $contents = $photo->contents();

            if ($contents === false) {
                continue;
            }

            // Load metadata if it exists
            $metaPath = "temp/{$sessionId}/{$photo->id}.meta.json";
            $newName = $photo->originalName;

            if (Storage::exists($metaPath)) {
                $meta = json_decode(Storage::get($metaPath), true);
                if (! empty($meta['newName'])) {
                    $newName = $meta['newName'];
                }
            }

            $extension = $photo->extension();
            $zipFileName = "{$newName}.{$extension}";

            $zip->addFromString($zipFileName, $contents);
        }

        $zip->close();

        return response()->streamDownload(function () use ($zipPath) {
            echo Storage::get($zipPath);
            Storage::delete($zipPath);
            Photo::cleanupSession($this->sessionId(request()));
        }, 'fanous-photos.zip', [
            'Content-Type' => 'application/zip',
            'Content-Disposition' => 'attachment; filename="fanous-photos.zip"',
        ]);
    }

    /**
     * Serve a photo file for preview in the browser.
     */
    public function preview(Request $request, string $id): Response
    {
        $sessionId = $this->sessionId($request);
        $photos = Photo::listForSession($sessionId);
        $photo = collect($photos)->first(fn (Photo $p) => $p->id === $id);

        if (! $photo) {
            abort(404);
        }

        $contents = $photo->contents();

        if ($contents === false) {
            abort(404);
        }

        return response($contents, 200, [
            'Content-Type' => $photo->mimeType,
            'Cache-Control' => 'no-store, private',
        ]);
    }

    /**
     * Get or create a session identifier for temp file grouping.
     */
    private function sessionId(Request $request): string
    {
        $sessionId = $request->session()->get('photo_session_id');

        if (! $sessionId) {
            $sessionId = Str::ulid()->toString();
            $request->session()->put('photo_session_id', $sessionId);
        }

        return $sessionId;
    }
}
