// static/js/camera.js
// Handles live camera capture: opens the webcam, lets the user snap 
// a photo, and instantly uploads it to our /upload route - the same 
// pipeline used for file uploads (YOLOv8 + EasyOCR + database save)

const startCameraBtn = document.getElementById("start-camera-btn");
const captureBtn = document.getElementById("capture-btn");
const cameraVideo = document.getElementById("camera-video");
const cameraCanvas = document.getElementById("camera-canvas");
const cameraStatus = document.getElementById("camera-status");

let activeStream = null;

// When the user clicks "Start Camera", ask the browser for camera access
startCameraBtn.addEventListener("click", async () => {
    try {
        // facingMode: "environment" prefers the BACK camera on phones 
        // (better for scanning food than the front selfie camera)
        activeStream = await navigator.mediaDevices.getUserMedia({
            video: { facingMode: "environment" }
        });

        cameraVideo.srcObject = activeStream;
        cameraVideo.style.display = "block";
        captureBtn.style.display = "inline-block";
        startCameraBtn.style.display = "none";
        cameraStatus.textContent = "Camera is live. Point at the food item and capture.";
    } catch (error) {
        cameraStatus.textContent = "Could not access camera: " + error.message;
    }
});

// When the user clicks "Capture & Scan"
captureBtn.addEventListener("click", () => {
    // Draw the current video frame onto our hidden canvas
    const context = cameraCanvas.getContext("2d");
    cameraCanvas.width = cameraVideo.videoWidth;
    cameraCanvas.height = cameraVideo.videoHeight;
    context.drawImage(cameraVideo, 0, 0, cameraCanvas.width, cameraCanvas.height);

    // Convert the canvas image into a file-like "Blob" object (JPEG format)
    cameraCanvas.toBlob(async (blob) => {
        cameraStatus.textContent = "Scanning... please wait (this can take a few seconds)";
        captureBtn.disabled = true;

        // Build form data exactly like a normal file upload form would
        const formData = new FormData();
        const filename = "camera_capture_" + Date.now() + ".jpg";
        formData.append("food_image", blob, filename);

        try {
            // Send it to our existing /upload route using fetch()
            const response = await fetch("/upload", {
                method: "POST",
                body: formData
            });

            if (response.ok || response.redirected) {
                stopCamera();
                window.location.href = "/";
            } else {
                cameraStatus.textContent = "Upload failed. Please try again.";
                captureBtn.disabled = false;
            }
        } catch (error) {
            cameraStatus.textContent = "Error uploading: " + error.message;
            captureBtn.disabled = false;
        }
    }, "image/jpeg", 0.9);
});

// Stops the camera stream and resets the UI back to its starting state
function stopCamera() {
    if (activeStream) {
        activeStream.getTracks().forEach(track => track.stop());
    }
    cameraVideo.style.display = "none";
    captureBtn.style.display = "none";
    startCameraBtn.style.display = "inline-block";
}
