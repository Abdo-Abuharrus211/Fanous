const year = new Date().getFullYear();

export default function Footer() {
    return (
        <footer className="mt-auto border-t border-border bg-background px-6 py-8">
            <div className="mx-auto flex max-w-7xl flex-col gap-64 md:flex-row md:items-start md:justify-center">
                <div>
                    <p className="text-sm font-medium text-foreground">Fanous</p>
                    <p className="mt-1 text-s text-muted-foreground">
                        Abdulqadir Abuharrus © {year}
                    </p>
                </div>

                <div>
                    <h3 className="mb-2 text-sm font-semibold text-foreground">
                        Links
                    </h3>
                    <ul className="flex flex-col gap-2">
                        <li>
                            <a
                                href="https://aabuharrus.dev/"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-sm text-muted-foreground transition-colors hover:text-foreground"
                            >
                                Abdu's
                            </a>
                        </li>
                        <li>
                            <a
                                href="https://github.com/Abdo-Abuharrus211/Fanous"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-sm text-muted-foreground transition-colors hover:text-foreground"
                            >
                                GitHub
                            </a>
                        </li>
                        <li>
                            <span className="text-sm text-muted-foreground">
                                Docs Coming Soon...
                            </span>
                        </li>
                    </ul>
                </div>
            </div>
        </footer>
    );
}