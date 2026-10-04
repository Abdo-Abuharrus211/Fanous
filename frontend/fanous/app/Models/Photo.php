<?php

namespace App\Models;

use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Str;

/**
 * Represents a photo during the upload → process → download flow.
 * Not an Eloquent model, state lives in temp storage.
 *
 * @property-read string $id
 * @property-read string $originalName
 * @property-read string $mimeType
 * @property-read int $size
 * @property-read string $tempPath
 * @property-read array<string, mixed> $exifData
 * @property-read string|null $newName
 * @property-read string|null $newDescription
 * @property-read string $status
 */
class Photo
{
    public function __construct(
        public readonly string $id,
        public readonly string $originalName,
        public readonly string $mimeType,
        public readonly int $size,
        public readonly string $tempPath,
        public readonly array $exifData = [],
        public readonly ?string $newName = null,
        public readonly ?string $newDescription = null,
        public readonly string $status = 'pending', // pending, ready
    ) {}

    /**
     * Create a Photo from an uploaded file and saves to temp storage.
     */
    public static function fromUpload(UploadedFile $file, string $sessionId): self
    {
        $id = Str::ulid()->toString();
        $extension = $file->getClientOriginalExtension() ?: $file->guessExtension();
        $tempPath = "temp/{$sessionId}/{$id}.{$extension}";

        // store the file as 'temp/sessionId/photoId.extension'
        // so each session has a directory
        Storage::putFileAs(
            "temp/{$sessionId}",
            $file,
            "{$id}.{$extension}",
        );

        // save metadata for later retrieval
        Storage::put(
            "temp/{$sessionId}/{$id}.meta.json",
            json_encode([
                'originalName' => $file->getClientOriginalName(),
            ]),
        );

        // extract the data
        $exifData = self::extractExif(Storage::path($tempPath));

        // this implicityly invokes the constructor 
        return new self(
            id: $id,
            originalName: $file->getClientOriginalName(),
            mimeType: $file->getMimeType(),
            size: $file->getSize(),
            tempPath: $tempPath,
            exifData: $exifData,
        );
    }


    // TODO: consider making fields mutable and just update...? This is probably cleaner for packaging later for download
    /**
     * Return a new Photo instance with analysis results applied.
     */
    public function withAnalysis(string $newName, ?string $description = null): self
    {
        return new self(
            id: $this->id,
            originalName: $this->originalName,
            mimeType: $this->mimeType,
            size: $this->size,
            tempPath: $this->tempPath,
            exifData: $this->exifData,
            newName: $newName,
            newDescription: $description,
            status: 'ready',
        );
    }

    /**
     * Convert to array for JSON serialization to the frontend.
     *
     * @return array{
     *     id: string,
     *     originalName: string,
     *     mimeType: string,
     *     size: int,
     *     exifData: array<string, mixed>,
     *     newName: string|null,
     *     newDescription: string|null,
     *     status: string,
     *     previewUrl: string,
     * }
     */
    public function toArray(): array
    {
        return [
            'id' => $this->id,
            'originalName' => $this->originalName,
            'mimeType' => $this->mimeType,
            'size' => $this->size,
            'exifData' => $this->exifData,
            'newName' => $this->newName,
            'newDescription' => $this->newDescription,
            'status' => $this->status,
            'previewUrl' => route('photos.preview', ['id' => $this->id]),
        ];
    }

    /**
     * Read the file contents from temp storage.
     */
    public function contents(): string|false
    {
        return Storage::get($this->tempPath);
    }

    /**
     * Get the file extension, excluding the dot.
     */
    public function extension(): string
    {
        return pathinfo($this->tempPath, PATHINFO_EXTENSION);
    }

  
    //// Static helpers ////

    /**
     * Ensure the temp directory exists for a session.
     */
    public static function ensureSessionDir(string $sessionId): bool
    {
        return Storage::makeDirectory("temp/{$sessionId}");
    }

    /**
     * Remove a photo from storage - basically delete if user wants removed
     */
    public static function removePhoto(string $photoId, string $sessionId): void
    {
        $dir = "temp/{$sessionId}";
        $files = Storage::files($dir);

        // reads as for each path in files...wth php?!
        foreach ($files as $path) {
            $fileName = pathinfo($path, PATHINFO_FILENAME);

            if ($fileName === $photoId) {
                Storage::delete($path);
                Storage::delete("{$dir}/{$photoId}.meta.json");

                break;
            }
        }
    }

    /**
     * Delete all temp files for a session.
     */
    public static function cleanupSession(string $sessionId): void
    {
        if (Storage::exists("temp/{$sessionId}")) {
            Storage::deleteDirectory("temp/{$sessionId}");
        }
    }

    /**
     * Get all photos stored for a session.
     *
     * @return list<Photo>
     */
    public static function listForSession(string $sessionId): array
    {
        $dir = "temp/{$sessionId}";

        if (! Storage::exists($dir)) {
            return [];
        }

        $files = Storage::files($dir);
        $photos = [];

        foreach ($files as $path) {
            if (str_ends_with($path, '.meta.json')) {
                continue;
            }

            $id = pathinfo($path, PATHINFO_FILENAME);
            $exifData = self::extractExif(Storage::path($path));
            $metaPath = "temp/{$sessionId}/{$id}.meta.json";
            $originalName = basename($path);

            if (Storage::exists($metaPath)) {
                $meta = json_decode(Storage::get($metaPath), true);
                if (! empty($meta['originalName'])) {
                    $originalName = $meta['originalName'];
                }
            }

            $photos[] = new self(
                id: $id,
                originalName: $originalName,
                mimeType: Storage::mimeType($path) ?: 'application/octet-stream',
                size: Storage::size($path),
                tempPath: $path,
                exifData: $exifData,
            );
        }

        return $photos;
    }

    /**
     * Extract EXIF data from a file path.
     * Returns empty array if the file doesn't support EXIF or the extension isn't loaded.
     *
     * @return array<string, mixed>
     */
    private static function extractExif(string $filePath): array
    {
        if (! function_exists('exif_read_data')) {
            return [];
        }

        $ext = strtolower(pathinfo($filePath, PATHINFO_EXTENSION));

        if (! in_array($ext, ['jpg', 'jpeg', 'tiff', 'png'])) {
            return [];
        }

        $exif = @exif_read_data($filePath, 'EXIF');

        if ($exif === false) {
            return [];
        }

        return [
            'DateTime' => $exif['DateTimeOriginal'] ?? $exif['DateTime'] ?? null,
            'Make' => $exif['Make'] ?? null,
            'Model' => $exif['Model'] ?? null,
            'ExposureTime' => $exif['ExposureTime'] ?? null,
            'FNumber' => $exif['FNumber'] ?? null,
            'ISOSpeedRatings' => $exif['ISOSpeedRatings'] ?? null,
            'FocalLength' => $exif['FocalLength'] ?? null,
            'GPS' => isset($exif['GPSLatitude'], $exif['GPSLongitude'])
                ? [
                    'lat' => self::gpsToDecimal($exif['GPSLatitude'], $exif['GPSLatitudeRef'] ?? 'N'),
                    'lng' => self::gpsToDecimal($exif['GPSLongitude'], $exif['GPSLongitudeRef'] ?? 'E'),
                ]
                : null,
        ];
    }

    /**
     * Convert EXIF GPS coordinates to decimal degrees.
     */
    private static function gpsToDecimal(array $coords, string $ref): float
    {
        $degrees = count($coords) > 0 ? self::fractionToFloat($coords[0]) : 0;
        $minutes = count($coords) > 1 ? self::fractionToFloat($coords[1]) : 0;
        $seconds = count($coords) > 2 ? self::fractionToFloat($coords[2]) : 0;

        $decimal = $degrees + ($minutes / 60) + ($seconds / 3600);

        if (in_array($ref, ['S', 'W'])) {
            $decimal *= -1;
        }

        return $decimal;
    }

    /**
     * Convert an EXIF fraction string (e.g. "1/125") to a float.
     */
    private static function fractionToFloat(string $value): float
    {
        if (str_contains($value, '/')) {
            [$num, $den] = explode('/', $value);

            return $den != 0 ? (float) $num / (float) $den : 0;
        }

        return (float) $value;
    }
}
