/**
 * PodCast AI - JavaScript Controller
 * Handles file upload, API interactions, and UI updates
 */

// State management
const state = {
    file: null,
    filename: null,
    script: null,
    audioFile: null,
    currentStep: 1
};

// DOM Elements
const elements = {
    uploadZone: document.getElementById('upload-zone'),
    fileInput: document.getElementById('file-input'),
    fileInfo: document.getElementById('file-info'),
    fileName: document.getElementById('file-name'),
    fileSize: document.getElementById('file-size'),
    removeFile: document.getElementById('remove-file'),
    uploadBtn: document.getElementById('upload-btn'),

    previewSection: document.getElementById('preview-section'),
    previewContent: document.getElementById('preview-content'),
    generateScriptBtn: document.getElementById('generate-script-btn'),

    scriptSection: document.getElementById('script-section'),
    scriptTitle: document.getElementById('script-title'),
    scriptSummary: document.getElementById('script-summary'),
    conversation: document.getElementById('conversation'),
    generateAudioBtn: document.getElementById('generate-audio-btn'),

    audioSection: document.getElementById('audio-section'),
    audioPlayer: document.getElementById('audio-player'),
    audioSource: document.getElementById('audio-source'),
    audioVisualization: document.getElementById('audio-visualization'),
    downloadBtn: document.getElementById('download-btn'),
    newPodcastBtn: document.getElementById('new-podcast-btn'),

    loadingOverlay: document.getElementById('loading-overlay'),
    loadingTitle: document.getElementById('loading-title'),
    loadingMessage: document.getElementById('loading-message'),
    progressBar: document.getElementById('progress-bar'),

    steps: document.querySelectorAll('.step')
};

// Initialize event listeners
function init() {
    // Upload zone click
    elements.uploadZone.addEventListener('click', () => {
        elements.fileInput.click();
    });

    // File input change
    elements.fileInput.addEventListener('change', handleFileSelect);

    // Drag and drop
    elements.uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        elements.uploadZone.classList.add('dragover');
    });

    elements.uploadZone.addEventListener('dragleave', () => {
        elements.uploadZone.classList.remove('dragover');
    });

    elements.uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        elements.uploadZone.classList.remove('dragover');
        const file = e.dataTransfer.files[0];
        if (file && file.type === 'application/pdf') {
            handleFile(file);
        } else {
            showToast('Please upload a PDF file', 'error');
        }
    });

    // Remove file
    elements.removeFile.addEventListener('click', removeFile);

    // Upload button
    elements.uploadBtn.addEventListener('click', uploadPDF);

    // Generate script button
    elements.generateScriptBtn.addEventListener('click', generateScript);

    // Generate audio button
    elements.generateAudioBtn.addEventListener('click', generateAudio);

    // Download button
    elements.downloadBtn.addEventListener('click', downloadAudio);

    // New podcast button
    elements.newPodcastBtn.addEventListener('click', resetApp);

    // Audio player events
    elements.audioPlayer.addEventListener('play', () => {
        elements.audioVisualization.classList.add('playing');
    });

    elements.audioPlayer.addEventListener('pause', () => {
        elements.audioVisualization.classList.remove('playing');
    });

    elements.audioPlayer.addEventListener('ended', () => {
        elements.audioVisualization.classList.remove('playing');
    });
}

// Handle file selection
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
}

// Process selected file
function handleFile(file) {
    if (file.type !== 'application/pdf') {
        showToast('Please upload a PDF file', 'error');
        return;
    }

    state.file = file;

    // Update UI
    elements.uploadZone.style.display = 'none';
    elements.fileInfo.style.display = 'flex';
    elements.fileName.textContent = file.name;
    elements.fileSize.textContent = formatFileSize(file.size);
    elements.uploadBtn.disabled = false;
}

// Remove selected file
function removeFile() {
    state.file = null;
    elements.fileInput.value = '';
    elements.uploadZone.style.display = 'block';
    elements.fileInfo.style.display = 'none';
    elements.uploadBtn.disabled = true;
}

// Upload PDF to server
async function uploadPDF() {
    if (!state.file) return;

    showLoading('Uploading PDF...', 'Analyzing your document');
    updateProgress(20);

    const formData = new FormData();
    formData.append('pdf', state.file);

    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Upload failed');
        }

        updateProgress(100);

        state.filename = data.filename;

        // Show preview
        elements.previewContent.textContent = data.preview;
        elements.previewSection.style.display = 'block';

        // Update step
        updateStep(2);

        hideLoading();
        showToast('PDF uploaded successfully!', 'success');

        // Scroll to preview
        elements.previewSection.scrollIntoView({ behavior: 'smooth' });

    } catch (error) {
        hideLoading();
        showToast(error.message, 'error');
    }
}

// Generate podcast script
async function generateScript() {
    if (!state.filename) return;

    showLoading('Creating Your Podcast Script...', 'AI is transforming your content into an engaging conversation');

    // Simulate progress
    let progress = 0;
    const progressInterval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress > 90) progress = 90;
        updateProgress(progress);
    }, 500);

    try {
        const language = document.getElementById('language-select').value;
        const response = await fetch('/api/generate-script', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ filename: state.filename, language: language })
        });

        const data = await response.json();

        clearInterval(progressInterval);

        if (!response.ok) {
            throw new Error(data.error || 'Script generation failed');
        }

        updateProgress(100);

        state.script = data.script;

        // Display script
        displayScript(state.script);

        // Update step
        updateStep(3);

        hideLoading();
        showToast('Script generated successfully!', 'success');

        // Scroll to script
        elements.scriptSection.scrollIntoView({ behavior: 'smooth' });

    } catch (error) {
        clearInterval(progressInterval);
        hideLoading();
        showToast(error.message, 'error');
    }
}

// Display the generated script
function displayScript(script) {
    elements.scriptTitle.textContent = `🎙️ ${script.title || 'Your Podcast'}`;
    elements.scriptSummary.textContent = script.summary || '';

    // Clear existing conversation
    elements.conversation.innerHTML = '';

    // Add each dialogue
    script.conversation.forEach((dialogue, index) => {
        const div = document.createElement('div');
        div.className = `dialogue ${dialogue.speaker}`;
        div.style.animationDelay = `${index * 0.1}s`;

        div.innerHTML = `
            <div class="dialogue-speaker">${dialogue.speaker === 'teacher' ? '👨‍🏫 Teacher' : '👨‍🎓 Student'}</div>
            <p class="dialogue-text">${dialogue.text}</p>
        `;

        elements.conversation.appendChild(div);
    });

    elements.scriptSection.style.display = 'block';
}

// Generate audio from script
async function generateAudio() {
    if (!state.script) return;

    showLoading('Generating Your Podcast Audio...', 'Converting the conversation to natural speech');

    // Simulate progress for longer operation
    let progress = 0;
    const totalDialogues = state.script.conversation.length;
    const progressPerDialogue = 90 / totalDialogues;

    const progressInterval = setInterval(() => {
        progress += Math.random() * 5;
        if (progress > 90) progress = 90;
        updateProgress(progress);
    }, 1000);

    try {
        const language = document.getElementById('language-select').value;
        const response = await fetch('/api/generate-audio', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                script: state.script,
                filename: state.filename,
                language: language
            })
        });

        const data = await response.json();

        clearInterval(progressInterval);

        if (!response.ok) {
            throw new Error(data.error || 'Audio generation failed');
        }

        updateProgress(100);

        state.audioFile = data.audio_file;

        // Set up audio player
        elements.audioSource.src = `/api/stream/${state.audioFile}`;
        elements.audioPlayer.load();

        // Show audio section
        elements.audioSection.style.display = 'block';

        hideLoading();
        showToast('🎉 Your podcast is ready!', 'success');

        // Scroll to audio
        elements.audioSection.scrollIntoView({ behavior: 'smooth' });

    } catch (error) {
        clearInterval(progressInterval);
        hideLoading();
        showToast(error.message, 'error');
    }
}

// Download audio file
function downloadAudio() {
    if (!state.audioFile) return;

    const link = document.createElement('a');
    link.href = `/api/download/${state.audioFile}`;
    link.download = state.audioFile;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    showToast('Download started!', 'success');
}

// Reset application
function resetApp() {
    // Reset state
    state.file = null;
    state.filename = null;
    state.script = null;
    state.audioFile = null;
    state.currentStep = 1;

    // Reset UI
    elements.fileInput.value = '';
    elements.uploadZone.style.display = 'block';
    elements.fileInfo.style.display = 'none';
    elements.uploadBtn.disabled = true;
    elements.previewSection.style.display = 'none';
    elements.scriptSection.style.display = 'none';
    elements.audioSection.style.display = 'none';
    elements.conversation.innerHTML = '';
    elements.audioPlayer.pause();
    elements.audioVisualization.classList.remove('playing');

    // Reset steps
    updateStep(1);

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Update step indicator
function updateStep(step) {
    state.currentStep = step;

    elements.steps.forEach((stepEl, index) => {
        const stepNum = index + 1;

        stepEl.classList.remove('active', 'completed');

        if (stepNum < step) {
            stepEl.classList.add('completed');
        } else if (stepNum === step) {
            stepEl.classList.add('active');
        }
    });
}

// Show loading overlay
function showLoading(title, message) {
    elements.loadingTitle.textContent = title;
    elements.loadingMessage.textContent = message;
    elements.progressBar.style.width = '0%';
    elements.loadingOverlay.classList.add('active');
}

// Hide loading overlay
function hideLoading() {
    elements.loadingOverlay.classList.remove('active');
}

// Update progress bar
function updateProgress(percent) {
    elements.progressBar.style.width = `${Math.min(percent, 100)}%`;
}

// Show toast notification
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;

    const icon = type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️';

    toast.innerHTML = `
        <span class="toast-icon">${icon}</span>
        <span class="toast-message">${message}</span>
    `;

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'slideIn 0.3s ease reverse';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', init);
