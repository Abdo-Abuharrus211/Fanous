import { Link } from '@inertiajs/react';
import Footer from '@/components/ui/footer';

export default function SimpleLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="flex min-h-screen flex-col bg-background text-foreground">
            <header className="border-b px-6 py-4">
                <div className="mx-auto flex max-w-7xl items-center justify-between">
                    <Link href="/" className="text-3xl flex items-center gap-2">
                        Fanous
                    </Link>
                </div>
            </header>
            <main className="mx-auto max-w-7xl px-6 py-8">
                {children}
            </main>
            <Footer />
        </div>
    );
}
