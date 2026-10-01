<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Photo extends Model
{
    //
    /**
     * A photo is made of a name, metadata/exif data, image file (JPEG, PNG, etc), date taken, date modified, new description,
     * 
     * 
     * TODO:
     * create class attributes
     * create base methods to show, set, etc
     * create methods to modify the attributes
     */

    public $name = ""; // default value is empty
    private $exifData = []; // empty array or object?
    private $imageFile = null;
    private $newDescr = "";

    /**
     * Construct a photo object
     */
    public function Photo($name, $exif, $file){
        $this->name = $name;
        $this->exifData = $exif;
        $this->imageFile = $file;
    }


    



}
