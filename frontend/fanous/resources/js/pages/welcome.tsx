// This is the landing page, welcomes the user and redirects to '/photos'

import { Head, Link } from '@inertiajs/react';

export default function Welcome() {
    return (
        <>
            <Head title="Welcome" />
            <div className="flex min-h-screen flex-col items-center justify-center gap-6 bg-background text-foreground">
                <h1 className="text-4xl font-bold">Fanous</h1>
                <p className="text-muted-foreground">
                    No more file-system names defined by your camera, rename your photos with human-friendly names
                </p>
                <Link
                    href="/photos"
                    className="rounded-md bg-primary px-6 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90"
                >
                    Get Started
                </Link>
            </div>
        </>
    );
}
