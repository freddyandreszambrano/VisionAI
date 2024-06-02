document.addEventListener('DOMContentLoaded', () => {
    const videoElement = document.getElementById('videoElement');
    const toggleButton = document.getElementById('toggle_camara');
    const captureButton = document.getElementById('tomar_foto');
    const deleteButtonContainer = document.getElementById('eliminar_button_container');
    const deleteButton = document.getElementById('eliminar_foto');
    const saveButton = document.getElementById('guardar_foto');
    const canvas = document.getElementById('canvas');
    const prendaInput = document.getElementById('id_prenda'); // Cambia esto si tu input de archivo tiene un ID diferente
    let mediaStream = null;

    // Activar o desactivar la cámara
    toggleButton.addEventListener('click', async () => {
        if (!mediaStream) {
            try {
                mediaStream = await navigator.mediaDevices.getUserMedia({ video: true });
                videoElement.srcObject = mediaStream;
                toggleButton.textContent = 'Cancelar';
            } catch (error) {
                console.error('Error accediendo a la cámara', error);
                alert('getUserMedia no es compatible con este navegador o no se pudo acceder a la cámara.');
            }
        } else {
            mediaStream.getTracks().forEach(track => track.stop());
            videoElement.srcObject = null;
            mediaStream = null;
            toggleButton.textContent = 'Activar cámara';
        }
    });

    // Capturar la imagen desde la cámara
    captureButton.addEventListener('click', () => {
        if (mediaStream) {
            const context = canvas.getContext('2d');
            canvas.width = videoElement.videoWidth;
            canvas.height = videoElement.videoHeight;
            context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
            captureButton.style.display = 'none';
            deleteButtonContainer.style.display = 'block';
        } else {
            alert('Primero debes activar la cámara.');
        }
    });

    // Eliminar la imagen capturada
    deleteButton.addEventListener('click', () => {
        const context = canvas.getContext('2d');
        context.clearRect(0, 0, canvas.width, canvas.height);
        captureButton.style.display = 'block';
        deleteButtonContainer.style.display = 'none';
    });

    // Guardar la imagen capturada y asignarla al input file
    saveButton.addEventListener('click', () => {
        if (mediaStream) {
            const imageData = canvas.toDataURL('image/jpeg');

            fetch(imageData)
                .then(res => res.blob())
                .then(blob => {
                    const file = new File([blob], "captured_image.jpg", { type: "image/jpeg" });

                    const dataTransfer = new DataTransfer();
                    dataTransfer.items.add(file);
                    prendaInput.files = dataTransfer.files;

                    alert('Imagen capturada y asignada al formulario.');
                })
                .catch(error => {
                    console.error('Error al crear el archivo:', error);
                    alert('Hubo un error al procesar la imagen.');
                });
        } else {
            alert('Primero debes activar la cámara.');
        }
    });
});
