FROM php:8.4-fpm AS base

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpng-dev \
    libjpeg-dev \
    libfreetype-dev \
    libonig-dev \
    libxml2-dev \
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

RUN composer install --no-dev --no-interaction --prefer-dist --optimize-autoloader

COPY fanous/ .

# Install Node & build assets
FROM node:22-alpine AS node-builder
WORKDIR /app
COPY fanous/package.json fanous/package-lock.json fanous/tsconfig.json fanous/vite.config.ts ./
RUN npm ci
COPY fanous/resources ./resources
RUN npm run build

# Final image
FROM base AS production

COPY --from=node-builder /app/public/build ./public/build

RUN chown -R www-data:www-data /app/storage /app/bootstrap/cache

ENV APP_ENV=production
ENV APP_DEBUG=false

EXPOSE 8000

CMD ["php", "artisan", "serve", "--host=0.0.0.0", "--port=8000"]
