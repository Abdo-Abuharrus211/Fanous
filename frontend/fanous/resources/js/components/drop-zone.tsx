import { useCallback, useRef, useState } from 'react';
import { router } from '@inertiajs/react';
import { Upload } from 'lucide-react';

export interface UploadedPhoto {
    id: string;
    originalName: string;
    mimeType: string;
    size: number;
    exifData: Record<string, unknown>;
    newName: string | null;
    newDescription: string | null;
    status: string;
    previewUrl: string;
}

export default function DropZone({
    onPhotosUploaded,
}: {
    onPhotosUploaded?: (photos: UploadedPhoto[]) => void;
}) {
    const [isDragging, setIsDragging] = useState(false);
    const [isUploading, setIsUploading] = useState(false);
    const fileInputRef = useRef<HTMLInputElement>(null);


    // Drag and drop event handlers
    const handleDragOver = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(true);
    }, []);

    const handleDragLeave = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(false);
    }, []);

    const handleDrop = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(false);

        // file transfer happens here
        const files = Array.from(e.dataTransfer.files).filter((f) =>
            f.type.startsWith('image/'),
        );

        if (files.length > 0) {
            void uploadImages(files);
        }
    }, []);

    const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
        const files = Array.from(e.target.files ?? []);

        if (files.length > 0) {
            void uploadImages(files);
        }

        if (fileInputRef.current) {
            fileInputRef.current.value = '';
        }
    };


    /**
     * Upload the photos to the Laravel server for processing
     * @param files array of files - images of JPEG, JPG, and PNG file types
     */
    const uploadImages = async (files: File[]) => {
        setIsUploading(true);

        const formData = new FormData();
        files.forEach((file) => formData.append('photos[]', file));

        try {
            // Using inertia router to post
            router.post(
                '/photos/upload',
                formData,
                {
                    onSuccess: (page) => {
                        const response = page.props as unknown as {
                            photos?: UploadedPhoto[];
                        };
                        if (response.photos && onPhotosUploaded) {
                            onPhotosUploaded(response.photos);
                        }
                    },
                    onError: (errors) => {
                        console.error('Upload failed:', errors);
                    },
                    forceFormData: true,
                    preserveScroll: true,
                },
            );
        } catch (error) {
            console.error('Upload error:', error);
        } finally {
            setIsUploading(false);
        }
    };

    return (
        <div className="flex flex-col items-center gap-4">
            <div
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
                className={`
                    flex w-full cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed px-6 py-12 transition-colors
                    ${
                        isDragging
                            ? 'border-primary bg-primary/10'
                            : 'border-border hover:border-primary/50 hover:bg-muted/50'
                    }
                `}
            >
                <Upload
                    className={`mb-3 size-8 ${isDragging ? 'text-primary' : 'text-muted-foreground'}`}
                />
                <p className="mb-1 text-sm font-medium">
                    {isDragging
                        ? 'Drop your photos here'
                        : 'Drag & drop photos here'}
                </p>
                <p className="mb-4 text-xs text-muted-foreground">
                    or click to browse
                </p>
                <input
                    ref={fileInputRef}
                    type="file"
                    multiple
                    accept="image/*"
                    onChange={handleFileSelect}
                    className="hidden"
                />
                {isUploading && (
                    <p className="text-sm text-muted-foreground">
                        Uploading...
                    </p>
                )}
            </div>
        </div>
    );
}
