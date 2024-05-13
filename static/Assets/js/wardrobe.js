 // Acceso a los elementos de la cámara y canvas
 const video = document.getElementById('videoElement');
 const canvas = document.getElementById('canvas');
 const context = canvas.getContext('2d');
 const captureButton = document.getElementById('captureButton');

 // Solicitar acceso a la cámara
 navigator.mediaDevices.getUserMedia({ video: true })
     .then((stream) => {
         video.srcObject = stream;
     })
     .catch((err) => {
         console.error('Error al acceder a la cámara: ', err);
     });

 // Función para capturar la foto
 captureButton.addEventListener('click', () => {
     context.drawImage(video, 0, 0, canvas.width, canvas.height);
 });