// API Base URL
const API_URL = window.location.origin;

// Load voices on page load
document.addEventListener('DOMContentLoaded', () => {
    loadVoices();
    loadStats();
    setupEventListeners();
});

// Load available voices
async function loadVoices() {
    try {
        const response = await fetch(`${API_URL}/api/voices`);
        const data = await response.json();
        
        const voiceSelect = document.getElementById('voice-select');
        voiceSelect.innerHTML = '';
        
        if (data.voices && data.voices.length > 0) {
            data.voices.forEach(voice => {
                const option = document.createElement('option');
                option.value = voice.voice_id;
                option.textContent = `${voice.name} (${voice.category})`;
                voiceSelect.appendChild(option);
            });
        } else {
            voiceSelect.innerHTML = '<option value="">No voices available</option>';
        }
    } catch (error) {
        console.error('Error loading voices:', error);
        document.getElementById('voice-select').innerHTML = '<option value="">Error loading voices</option>';
    }
}

// Load stats
async function loadStats() {
    try {
        const response = await fetch(`${API_URL}/`);
        const data = await response.json();
        
        if (data.tokens_loaded !== undefined) {
            document.getElementById('active-tokens').textContent = data.tokens_loaded;
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Setup event listeners
function setupEventListeners() {
    // Generate button
    document.getElementById('generate-btn').addEventListener('click', generateSpeech);
    
    // Tab switching
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const tab = btn.dataset.tab;
            
            // Update buttons
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Update content
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            document.querySelector(`.tab-content[data-tab="${tab}"]`).classList.add('active');
        });
    });
    
    // Download button
    document.getElementById('download-btn').addEventListener('click', downloadAudio);
}

// Generate speech
async function generateSpeech() {
    const text = document.getElementById('text-input').value.trim();
    const voiceId = document.getElementById('voice-select').value;
    const modelId = document.getElementById('model-select').value;
    
    if (!text) {
        showError('Please enter some text');
        return;
    }
    
    if (!voiceId) {
        showError('Please select a voice');
        return;
    }
    
    const generateBtn = document.getElementById('generate-btn');
    const btnText = generateBtn.querySelector('.btn-text');
    const btnLoader = generateBtn.querySelector('.btn-loader');
    const resultContainer = document.getElementById('result-container');
    const errorMessage = document.getElementById('error-message');
    
    // Show loading state
    generateBtn.disabled = true;
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline';
    resultContainer.style.display = 'none';
    errorMessage.style.display = 'none';
    
    try {
        const response = await fetch(`${API_URL}/api/tts`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: text,
                voice_id: voiceId,
                model_id: modelId
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to generate speech');
        }
        
        const audioBlob = await response.blob();
        const audioUrl = URL.createObjectURL(audioBlob);
        
        // Store for download
        window.currentAudioBlob = audioBlob;
        
        // Play audio
        const audioPlayer = document.getElementById('audio-player');
        audioPlayer.src = audioUrl;
        
        // Show result
        resultContainer.style.display = 'block';
        
        // Update stats
        const currentRequests = parseInt(document.getElementById('total-requests').textContent);
        document.getElementById('total-requests').textContent = currentRequests + 1;
        
    } catch (error) {
        showError(error.message);
    } finally {
        // Reset button state
        generateBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
}

// Download audio
function downloadAudio() {
    if (!window.currentAudioBlob) {
        showError('No audio to download');
        return;
    }
    
    const url = URL.createObjectURL(window.currentAudioBlob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `speech_${Date.now()}.mp3`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Show error message
function showError(message) {
    const errorMessage = document.getElementById('error-message');
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    
    setTimeout(() => {
        errorMessage.style.display = 'none';
    }, 5000);
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});
