FROM php:8.4-fpm AS base

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpng-dev \
    libjpeg-dev \
    libfreetype-dev \
    libonig-dev \
    libxml2-dev \
    libsqlite3-dev \
    libzip-dev \
    default-libmysqlclient-dev \
    zip \
    unzip \
    curl \
    git \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install pdo_mysql pdo_sqlite mbstring exif gd zip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Composer
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

# Copy dependency files first for layer caching
COPY fanous/composer.json fanous/composer.lock ./

RUN composer install --no-dev --no-interaction --prefer-dist --optimize-autoloader --no-scripts

COPY fanous/ .

# Run composer scripts now that artisan exists
RUN composer run-script post-autoload-dump
# Generate Wayfinder types (required by Vite build step)
RUN php artisan wayfinder:generate


# Install Node & build assets
FROM node:22-alpine AS node-builder
WORKDIR /app
COPY --from=base /app/resources ./resources
COPY --from=base /app/routes ./routes
COPY fanous/package.json fanous/package-lock.json fanous/tsconfig.json fanous/vite.config.ts ./
RUN npm ci
RUN npm run build

# Final image
FROM base AS production

COPY fanous/php.ini /usr/local/etc/php/conf.d/fanous.ini
COPY --from=node-builder /app/public/build ./public/build

RUN chown -R www-data:www-data /app/storage /app/bootstrap/cache

ENV APP_ENV=production
ENV APP_DEBUG=false

EXPOSE 8000

CMD ["php", "artisan", "serve", "--host=0.0.0.0", "--port=8000"]
