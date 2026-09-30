<?php
/**
 * TODO:
 * 
 * - store(Request $request) → accepts uploaded files, saves to storage/app/temp/{session_id}/, extracts EXIF
 *   (using PHP's exif_read_data), returns photo list with preview URL
 * - analyze(Request $request) → sends photos to backend API, stores results
 * - download(Request $request) → renames files, zips, streams download, cleans up
 */