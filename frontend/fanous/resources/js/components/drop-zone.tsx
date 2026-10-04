import { useEffect, useState } from "react"


export default function DropZone() {
    // State and variables
    const zone: HTMLElement = document.getElementById("drop-zone");
    const [images, setImages] = useState([]);


    useEffect(() => {
        const images = zone.addEventListener("drop", dropZoneHandler);
        setImages(images);
    }, []);

    function dropZoneHandler() {

    }

    /**
     * 
     */
    function uploadImages(images: File[]) {

        try {
            // make HTTP request to the Laravel backend sending the images
        } catch (error) {

        }
    }



    return (
        <section>
            <h1>Dropzone</h1>
            <div id="drop-zone">
                <p>Drop Image Files Here</p>
                <input type="file" id="file-drop-input"
                    multiple
                    accept="image/*" />
            </div>
            <button onClick={()=> {uploadImages}}>Analyze</button>
        </section>

    )
}