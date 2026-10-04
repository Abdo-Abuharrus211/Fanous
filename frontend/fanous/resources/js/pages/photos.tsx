import { Head } from '@inertiajs/react';
import { useCallback, useState } from 'react';
import DropZone, { type UploadedPhoto } from '@/components/drop-zone';
import PhotoCard from '@/components/photo-card';
import { Button } from '@/components/ui/button';

export interface PagePhoto extends UploadedPhoto {
    selected: boolean;
}

interface PhotosProps {
    sessionId: string;
    photos?: UploadedPhoto[];
}

export default function Photos({ photos: initialPhotos }: PhotosProps) {
    // state vars
    const [photos, setPhotos] = useState<PagePhoto[]>(
        (initialPhotos ?? []).map((p) => ({ ...p, selected: false })),);
    const [isProcessing, setIsProcessing] = useState(false);


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
        setPhotos((prev) =>
            prev.filter((p) => p.id !== photoID));
    }, []);


    const selectedPhotos = photos.filter((p) => p.selected);



    // TODO: implement the logic for sending to controller
    const handleAnalyze = () => {
        if (selectedPhotos.length === 0) return;
        setIsProcessing(true);
        console.log('Analyzing:', selectedPhotos.map((p) => p.id));
    };

    // TODO: download the received images from controller
    const handleDownload = () => {
        if (selectedPhotos.length === 0) return;
        console.log('Downloading:', selectedPhotos.map((p) => p.id));
    };

    return (
        <>
            <Head title="Photos" />

            <div className="flex flex-col gap-8">
                <div className="flex items-center justify-between">
                    <div>
                        <h1 className="text-2xl font-semibold">Upload & Analyze Your Photos</h1>
                        <p>This will generate human-friends, and memorable, filenames based on what they depict.</p>
                    </div>
                    <div className="flex gap-2">
                        <Button
                            onClick={handleAnalyze}
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
