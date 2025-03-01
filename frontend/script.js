// script.js
document.getElementById('mediaForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const url = document.getElementById('urlInput').value;
    const mediaContainer = document.getElementById('mediaContainer');
    
    mediaContainer.innerHTML = '<p>Cargando...</p>';
    
    try {
        // NOTA: Esto requiere un backend para funcionar
        const response = await fetch('/get-media-info', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url })
        });
        
        if (!response.ok) {
            throw new Error('Error al obtener información');
        }
        
        const data = await response.json();
        mostrarMedia(data);
        
    } catch (error) {
        mediaContainer.innerHTML = '<p style="color: red;">Ocurrió un error</p>';
        console.error(error);
    }
});

function mostrarMedia(data) {
    const mediaContainer = document.getElementById('mediaContainer');
    mediaContainer.innerHTML = `
        <h2>${data.title}</h2>
        <div class="media-info">
            ${data.audio_url ? `
                <div class="media-item">
                    <h3>Audio</h3>
                    <audio controls>
                        <source src="${data.audio_url}" type="audio/mp4">
                    </audio>
                </div>
            ` : ''}
            
            ${data.video_url ? `
                <div class="media-item">
                    <h3>Video</h3>
                    <video controls>
                        <source src="${data.video_url}" type="video/mp4">
                    </video>
                </div>
            ` : ''}
        </div>
    `;
}