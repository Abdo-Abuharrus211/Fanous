<?php

namespace App\Providers;

use Carbon\CarbonImmutable;
use Illuminate\Support\Facades\Date;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\ServiceProvider;
use Illuminate\Validation\Rules\Password;
use Illuminate\Http\Request;
use Illuminate\Cache\RateLimiter;
use Illuminate\Cache\RateLimiting\Limit;


class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        //
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        $this->configureDefaults();

        // Rate limiter - upload
        RateLimiter::for('photos.upload', function (Request $request) {

            return Limit::perMinute(50)->by('ip' . $request->ip());
        });

        // Rate limiter - Processing
        RateLimiter::for('photos.process', function (Request $request) {
            // TODO: Future placeholder for whne implement Auth
            // if ($request->authUser()) {
            //     return Limit::perMinute(5)->by('ip' . $request->ip());
            // }

            if ($request->sessionId()) {
                return Limit::perMinute(5)->by('ip' . $request->ip());
            }

            return Limit::perMinute(2)->by('ip' . $request->ip());
        });


        // Rate limiter - upload
        RateLimiter::for('photos.upload', function (Request $request) {

            return Limit::perMinute(50)->by('ip' . $request->ip());
        });

        // Rate limiter - download
        RateLimiter::for('photos.download', function (Request $request) {

            return Limit::perMinute(20)->by('ip' . $request->ip());
        });
    }

    /**
     * Configure default behaviors for production-ready applications.
     */
    protected function configureDefaults(): void
    {
        Date::use(CarbonImmutable::class);

        DB::prohibitDestructiveCommands(
            app()->isProduction(),
        );

        Password::defaults(
            fn(): ?Password => app()->isProduction()
                ? Password::min(12)
                ->mixedCase()
                ->letters()
                ->numbers()
                ->symbols()
                ->uncompromised()
                : null,
        );
    }
}
