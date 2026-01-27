/**
 * YouTube MP3 Downloader - Frontend JavaScript
 */

// DOM Elements
const urlInput = document.getElementById('urlInput');
const fetchBtn = document.getElementById('fetchBtn');
const downloadBtn = document.getElementById('downloadBtn');
const newDownloadBtn = document.getElementById('newDownloadBtn');
const tryAgainBtn = document.getElementById('tryAgainBtn');

// Sections
const videoInfo = document.getElementById('videoInfo');
const progressSection = document.getElementById('progressSection');
const successSection = document.getElementById('successSection');
const errorSection = document.getElementById('errorSection');

// Video info elements
const thumbnail = document.getElementById('thumbnail');
const videoTitle = document.getElementById('videoTitle');
const uploader = document.getElementById('uploader');
const views = document.getElementById('views');
const duration = document.getElementById('duration');

// Progress elements
const progressFill = document.getElementById('progressFill');
const progressPercent = document.getElementById('progressPercent');

// Error elements
const errorTitle = document.getElementById('errorTitle');
const errorMessage = document.getElementById('errorMessage');

// State
let currentVideoUrl = '';
let currentVideoInfo = null;

/**
 * Format number with commas
 */
function formatNumber(num) {
    if (!num) return '0';
    return num.toLocaleString();
}

/**
 * Format duration from seconds to MM:SS
 */
function formatDuration(seconds) {
    if (!seconds) return '0:00';
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

/**
 * Get selected quality
 */
function getSelectedQuality() {
    const selected = document.querySelector('input[name="quality"]:checked');
    return selected ? selected.value : '320';
}

/**
 * Show a specific section and hide others
 */
function showSection(section) {
    // Hide all sections
    videoInfo.classList.add('hidden');
    progressSection.classList.add('hidden');
    successSection.classList.add('hidden');
    errorSection.classList.add('hidden');

    // Show requested section
    if (section) {
        section.classList.remove('hidden');
    }
}

/**
 * Show error message
 */
function showError(title, message) {
    errorTitle.textContent = title;
    errorMessage.textContent = message;
    showSection(errorSection);
}

/**
 * Reset to initial state
 */
function resetToInitial() {
    urlInput.value = '';
    currentVideoUrl = '';
    currentVideoInfo = null;
    showSection(null);
    urlInput.focus();
}

/**
 * Fetch video information
 */
async function fetchVideoInfo() {
    const url = urlInput.value.trim();

    if (!url) {
        showError('Error', 'Please enter a YouTube URL');
        return;
    }

    // Show loading state
    fetchBtn.classList.add('loading');
    fetchBtn.disabled = true;

    try {
        const response = await fetch('/api/info', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url }),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to fetch video info');
        }

        // Store current state
        currentVideoUrl = url;
        currentVideoInfo = data.info;

        // Update UI with video info
        thumbnail.src = data.info.thumbnail || '';
        videoTitle.textContent = data.info.title || 'Unknown Title';
        uploader.textContent = data.info.uploader || 'Unknown';
        views.textContent = formatNumber(data.info.view_count) + ' views';
        duration.textContent = formatDuration(data.info.duration);

        // Show video info section
        showSection(videoInfo);

    } catch (error) {
        showError('Error', error.message);
    } finally {
        fetchBtn.classList.remove('loading');
        fetchBtn.disabled = false;
    }
}

/**
 * Download the video as MP3
 */
async function downloadVideo() {
    if (!currentVideoUrl) {
        showError('Error', 'No video selected');
        return;
    }

    // Show loading state
    downloadBtn.classList.add('loading');
    downloadBtn.disabled = true;

    // Show progress section
    showSection(progressSection);

    // Animate progress bar (fake progress since we don't have real-time updates)
    let progress = 0;
    const progressInterval = setInterval(() => {
        progress += Math.random() * 10;
        if (progress > 90) progress = 90;
        progressFill.style.width = `${progress}%`;
        progressPercent.textContent = `${Math.round(progress)}%`;
    }, 500);

    try {
        const response = await fetch('/api/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                url: currentVideoUrl,
                quality: getSelectedQuality(),
            }),
        });

        const data = await response.json();

        clearInterval(progressInterval);

        if (!response.ok) {
            throw new Error(data.error || 'Download failed');
        }

        // Complete progress
        progressFill.style.width = '100%';
        progressPercent.textContent = '100%';

        // Wait a moment then trigger file download
        setTimeout(() => {
            // Create download link
            const downloadLink = document.createElement('a');
            downloadLink.href = `/api/get-file/${encodeURIComponent(data.filename)}`;
            downloadLink.download = data.filename;
            document.body.appendChild(downloadLink);
            downloadLink.click();
            document.body.removeChild(downloadLink);

            // Show success section
            showSection(successSection);
        }, 500);

    } catch (error) {
        clearInterval(progressInterval);
        showError('Download Failed', error.message);
    } finally {
        downloadBtn.classList.remove('loading');
        downloadBtn.disabled = false;
    }
}

// Event Listeners
fetchBtn.addEventListener('click', fetchVideoInfo);

urlInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        fetchVideoInfo();
    }
});

downloadBtn.addEventListener('click', downloadVideo);

newDownloadBtn.addEventListener('click', resetToInitial);

tryAgainBtn.addEventListener('click', () => {
    if (currentVideoInfo) {
        showSection(videoInfo);
    } else {
        resetToInitial();
    }
});

// Auto-focus input on load
urlInput.focus();
