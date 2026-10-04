import { Link } from '@inertiajs/react';

export default function SimpleLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="min-h-screen bg-background text-foreground">
            <header className="border-b px-6 py-4">
                <div className="mx-auto flex max-w-7xl items-center justify-between">
                    <Link href="/" className="flex items-center gap-2">
                        Fanous
                    </Link>
                </div>
            </header>
            <main className="mx-auto max-w-7xl px-6 py-8">
                {children}
            </main>
        </div>
    );
}
