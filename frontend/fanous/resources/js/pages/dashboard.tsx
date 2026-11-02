import { Head, Link } from '@inertiajs/react';
import photos  from '@/routes/photos';
import { dashboard } from '@/routes';
export default function Dashboard() {
    return (
        <>
            <Head title="Dashboard" />
            <div className="flex h-full flex-1 flex-col gap-6 overflow-x-auto rounded-xl p-4">
                <h2 className="text-2xl font-semibold">Welcome to Fanous</h2>
                <p className="text-muted-foreground">
                    Rename your photos with human-friendly names using AI.
                </p>
                <Link
                    href={photos.index()}
                    className="rounded-md bg-primary px-6 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 w-fit"
                >
                    Get Started
                </Link>
            </div>
        </>
    );
}

Dashboard.layout = {
    breadcrumbs: [
        {
            title: 'Dashboard',
            href: dashboard(),
        },
    ],
};
