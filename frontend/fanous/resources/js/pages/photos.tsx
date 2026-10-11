import { Head, router } from '@inertiajs/react';
import { useCallback, useState } from 'react';
import { toast } from 'sonner';
import DropZone, { type UploadedPhoto } from '@/components/drop-zone';
import PhotoCard from '@/components/photo-card';
import { Button } from '@/components/ui/button';

export interface PagePhoto extends UploadedPhoto {
    selected: boolean;
}

interface PhotosProps {
    sessionId: string;
    photos?: UploadedPhoto[];
    quota?: number;
}

export default function Photos({ photos: initialPhotos }: PhotosProps) {
    // state vars
    const [photos, setPhotos] = useState<PagePhoto[]>(
        (initialPhotos ?? []).map((p) => ({ ...p, selected: false })),);
    const [isProcessing, setIsProcessing] = useState(false);
    const [isRemoving, setIsRemoving] = useState(false);
    const [isDownloading, setIsDownloading] = useState(false);


    // Add uploaded photos to `photos` array
    const handlePhotosUploaded = (uploaded: UploadedPhoto[]) => {
        const newPhotos = uploaded.map((p) => ({
            ...p,
            selected: true,
        }));
        setPhotos((prev) => [...prev, ...newPhotos]);
    };

    // Toggle `selected` boolean when 
    const handleSelect = useCallback((id: string) => {
        setPhotos((prev) =>
            prev.map((p) =>
                p.id === id ? { ...p, selected: !p.selected } : p,
            ),
        );
    }, []);

    // remove the photo from uploads
    const removePhoto = useCallback((photoID: string) => {
        setIsRemoving(true);
        setPhotos((prev) =>
            prev.filter((p) => p.id !== photoID));

        // make call to Laravel to remove from storage

        try {
            router.post('/photos/remove',
                { photoId: photoID }, {
                onSuccess: (page) => {

                },
                onError: (error) => {
                    console.error("Failed to remove photos:", error);
                    const messages = typeof error === 'object'
                        ? Object.values(error).join(', ')
                        : 'Could not remove photo.';
                    toast.error('Remove failed', { description: messages });
                },
                preserveScroll: true,
            },

            )
        } catch (error) {
            console.error("Error making removal request", error);
            toast.error('Remove error', { description: 'Something went wrong while removing the photo.' });

        } finally {
            setIsRemoving(false);
        }
    }, []);


    const selectedPhotos = photos.filter((p) => p.selected);
    const allSelected = photos.length > 0 && photos.every((p) => p.selected);

    const handleSelectAll = () => {
        const newState = !allSelected;
        setPhotos((prev) =>
            prev.map((p) => ({ ...p, selected: newState })),
        );
    };


    const handleProcess = async () => {
        if (selectedPhotos.length === 0) return;
        setIsProcessing(true);

        setPhotos((prev) =>
            prev.map((photo) =>
                selectedPhotos.some((s) => s.id === photo.id)
                    ? { ...photo, status: 'processing' }
                    : photo,
            ),
        );

        try {
            const response = await fetch('/photos/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-TOKEN': document.querySelector<HTMLMetaElement>(
                        'meta[name="csrf-token"]',
                    )?.content ?? '',
                },
                body: JSON.stringify({
                    photo_ids: selectedPhotos.map((p) => p.id),
                }),
            });

            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.error ?? 'Processing failed');
            }

            const data = await response.json();

            setPhotos((prev) =>
                prev.map((photo) => {
                    const result = data.results?.find(
                        (r: { id: string }) => r.id === photo.id,
                    );

                    if (result && result.status !== 'error') {
                        return {
                            ...photo,
                            newName: result.newName ?? photo.newName,
                            newDescription:
                                result.newDescription ?? photo.newDescription,
                            status: result.status ?? photo.status,
                        };
                    }

                    if (result?.status === 'error') {
                        return { ...photo, status: 'error' };
                    }

                    return photo;
                }),
            );
        } catch (error) {
            console.error('Error processing selected photos', error);
            toast.error('Process error', {
                description:
                    error instanceof Error
                        ? error.message
                        : 'Something went wrong while processing photos.',
            });
            setPhotos((prev) =>
                prev.map((photo) =>
                    selectedPhotos.some((s) => s.id === photo.id)
                        ? { ...photo, status: 'pending' }
                        : photo,
                ),
            );
        } finally {
            setIsProcessing(false);
        }
    };

    const handleDownload = async () => {
        if (selectedPhotos.length === 0) return;
        setIsDownloading(true);

        try {
            const response = await fetch('/photos/download', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-TOKEN': document.querySelector<HTMLMetaElement>(
                        'meta[name="csrf-token"]',
                    )?.content ?? '',
                },
                body: JSON.stringify({
                    photo_ids: selectedPhotos.map((p) => p.id),
                }),
            });

            if (!response.ok) {
                const data = await response.json().catch(() => null);
                throw new Error(
                    data?.error ?? 'Download failed',
                );
            }

            // unpacking the images and downloading - important!
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'fanous-photos.zip';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        } catch (error) {
            console.error('Error downloading processed photos', error);
            toast.error('Download error', {
                description:
                    error instanceof Error
                        ? error.message
                        : 'Something went wrong while downloading.',
            });
        } finally {
            setIsDownloading(false);
        }
    };

    return (
        <>
            <Head title="Photos" />

            <div className="flex flex-col gap-16">
                <div className="flex items-center gap-16 justify-between">
                    <div>
                        <h1 className="text-2xl font-semibold">Upload & Analyze Your Photos</h1>
                        <p>This will generate human-friendly, searchable filenames based on what they depict.</p>
                    </div>
                    <div className="flex gap-2">
                        <Button
                            variant="outline"
                            onClick={handleSelectAll}
                            disabled={photos.length === 0}
                        >
                            {allSelected ? 'Deselect All' : 'Select All'}
                        </Button>
                        <Button
                            onClick={handleProcess}
                            disabled={
                                selectedPhotos.length === 0 || isProcessing
                            }
                        >
                            {isProcessing
                                ? 'Analyzing...'
                                : `Analyze (${selectedPhotos.length})`}
                        </Button>
                        <Button
                            onClick={handleDownload}
                            variant="secondary"
                            disabled={selectedPhotos.length === 0}
                        >
                            Download ({selectedPhotos.length})
                        </Button>
                    </div>
                </div>

                <DropZone onPhotosUploaded={handlePhotosUploaded} />

                {/* Mapping the previews in a grid*/}
                {photos.length > 0 && (
                    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
                        {photos.map((photo) => (
                            <PhotoCard
                                key={photo.id}
                                {...photo}
                                selected={photo.selected}
                                onSelect={handleSelect}
                                onRemove={removePhoto}
                            />
                        ))}
                    </div>
                )}
            </div>
        </>
    );
}
