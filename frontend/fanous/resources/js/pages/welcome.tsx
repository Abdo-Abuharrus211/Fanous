// This is the landing page, welcomes the user and redirects to '/photos'

import Footer from '@/components/ui/footer';
import { Head, Link } from '@inertiajs/react';
import { Underline } from 'lucide-react';

export default function Welcome() {
    return (
        <>
            <Head title="Welcome" />
            <section
                id="welcome-section"
                className="flex items-center justify-center p-4 mt-64"
            >
                {/* TODO: add some video animation (loop) of how it works as the hook */}
                {/* <img src='/amber-rings.svg' className='absolute inset-0 h-full w-full object-cover'
                aria-hidden="true"
                ></img> */}
                <div className="flex flex-col">
                    <h1
                        className="mb-4 tracking-tight"
                        style={{ font: 'var(--h1)' }}
                    >
                        Fanous
                    </h1>
                    <h2 style={{ color: 'var(--secondary)' }}>
                        Never lose a photo!
                    </h2>

                    <p
                        className="mx-auto mb-8 max-w-xlg text-muted-foreground"
                        style={{ font: 'var(--p)' }}
                    >
                        No more <span><a href="https://en.wikipedia.org/wiki/Design_rule_for_Camera_File_system" 
                        style={{ textDecoration: 'Underline' }}>DCF</a></span> file names by your
                        camera;
                        <br />
                        rename your photos with human-friendly names instead
                    </p>
                    <Link
                        href="/photos"
                        className="w-fit rounded-md bg-primary px-8 py-3 text-base text-primary-foreground transition-colors hover:bg-primary/90"
                        style={{ borderRadius: '4px' }}
                    >
                        Get Started
                    </Link>
                </div>
            </section>
        </>
    );
}
