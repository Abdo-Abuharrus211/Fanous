// This is the landing page, welcomes the user and redirects to '/photos'

import Footer from '@/components/ui/footer';
import { Head, Link } from '@inertiajs/react';

export default function Welcome() {
    return (
        <>
            <Head title="Welcome" />
            <section className="relative overflow-hidden">
                {/* TODO: add some video animation (loop) of how it works as the hook */}
                {/* <img src='/amber-rings.svg' className='absolute inset-0 h-full w-full object-cover'
                aria-hidden="true"
                ></img> */}
                <div className="flex min-h-screen flex-col items-center justify-center px-4 text-center">
                    <h1
                        className="mb-4 tracking-tight"
                        style={{ font: 'var(--h1)' }}
                    >
                        Fanous
                    </h1>

                    <p className="mx-auto mb-8 max-w-xlg text-muted-foreground" style={{ font: 'var(--p)' }}>
                        No more forgettable file names deteremined by your camera!<br/>
                        Rename your photos with human-friendly names instead
                    </p>
                    <Link
                        href="/photos"
                        className="rounded-md bg-primary px-8 py-3 text-base font-medium text-primary-foreground transition-colors hover:bg-primary/90"
                        style={{ borderRadius: '4px' }}
                    >
                        Get Started
                    </Link>
                </div>
            </section >
        </>
    );
}
