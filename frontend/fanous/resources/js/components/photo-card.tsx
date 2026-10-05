import { Badge } from '@/components/ui/badge';
import { Spinner } from '@/components/ui/spinner';
import { cn } from '@/lib/utils';
import { X } from 'lucide-react';

export interface PhotoCardProps {
    id: string;
    originalName: string;
    newName: string | null;
    newDescription: string | null;
    status: string;
    previewUrl: string;
    size: number;
    selected: boolean;
    onSelect: (id: string) => void;
    onRemove: (id: string) => void;
}

export default function PhotoCard({
    id,
    originalName,
    newName,
    newDescription,
    status,
    previewUrl,
    size,
    selected,
    onSelect,
    onRemove,
}: PhotoCardProps) {
    const statusColor: Record<string, string> = {
        pending: 'bg-yellow-500/20 text-yellow-600 dark:text-yellow-400',
        processing: 'bg-blue-500/20 text-blue-600 dark:text-blue-400',
        ready: 'bg-green-500/20 text-green-600 dark:text-green-400',
        error: 'bg-red-500/20 text-red-600 dark:text-red-400',
    };

    const formatSize = (bytes: number): string => {
        if (bytes < 1024) return `${bytes} B`;
        if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
        return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
    };

    return (
        <div
            className={cn(
                'group relative overflow-hidden rounded-lg border bg-card transition-colors hover:border-primary/50',
                selected && 'border-primary ring-2 ring-primary/20',
            )}
        >
            <div
                className="relative aspect-square cursor-pointer overflow-hidden bg-muted"
                onClick={() => onSelect(id)}
            >
                <img
                    src={previewUrl}
                    alt={originalName}
                    className="h-full w-full object-cover transition-transform group-hover:scale-105"
                />
                {status === 'processing' && (
                    <div className="absolute inset-0 flex items-center justify-center bg-black/50 backdrop-blur-sm">
                        <div className="flex flex-col items-center gap-2 text-white">
                            <Spinner className="size-8" />
                            <span className="text-xs font-medium">
                                Processing...
                            </span>
                        </div>
                    </div>
                )}
                <button
                    onClick={(event) => {
                        event.stopPropagation();
                        onRemove(id);
                    }}
                    className="absolute right-2 top-2 z-10 flex size-7 items-center justify-center rounded-full bg-background/80 text-muted-foreground opacity-0 backdrop-blur-sm transition-all hover:bg-destructive hover:text-destructive-foreground group-hover:opacity-100"
                >
                    <X className="size-4" />
                </button>
            </div>

            <div className="p-3">
                <div className="mb-1 flex items-center justify-between gap-2">
                    <p className="truncate text-sm font-medium">
                        {originalName}
                    </p>
                    <Badge
                        className={cn(
                            'rounded-full px-2 py-0 text-xs',
                            statusColor[status] ?? '',
                        )}
                    >
                        {status}
                    </Badge>
                </div>

                {newName && (
                    <p className="text-s text-muted-foreground">
                        → {newName}
                    </p>
                )}

                {newDescription && (
                    <p className="mt-1 line-clamp-2 text-xs text-muted-foreground">
                        {newDescription}
                    </p>
                )}

                <p className="mt-1 text-xs text-muted-foreground">
                    {formatSize(size)}
                </p>
            </div>
        </div>
    );
}
