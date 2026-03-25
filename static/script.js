console.log("JS Loaded");

let currentLocation = null;
let recognition = null;
let isListening = false;

document.addEventListener('DOMContentLoaded', function() {
    getLocation();
    initVoiceRecognition();

    document.getElementById('sosBtn').onclick = sendSOS;
    document.getElementById('voiceBtn').onclick = toggleVoice;
});

// Location
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function(position) {
                currentLocation = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };
                document.getElementById('location-status').innerHTML =
                    `✅ ${currentLocation.lat.toFixed(4)}, ${currentLocation.lng.toFixed(4)}`;
            },
            function() {
                document.getElementById('location-status').innerHTML = '❌ Location unavailable';
            }
        );
    }
}

// SOS
async function sendSOS() {
    if (!currentLocation) {
        alert('Please wait for location detection');
        return;
    }

    try {
        await fetch('/sos', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                location: `${currentLocation.lat},${currentLocation.lng}`,
                message: '🚨 SOS 🚨'
            })
        });

        showSuccessModal();
    } catch {
        alert('Error sending alert');
    }
}

// Voice
function initVoiceRecognition() {
    if (!('webkitSpeechRecognition' in window)) return;

    recognition = new webkitSpeechRecognition();
    recognition.continuous = true;

    recognition.onresult = function(event) {
        let text = event.results[event.results.length - 1][0].transcript;
        document.getElementById("voiceResult").innerText = text;

        if (text.toLowerCase().includes("help")) {
            sendSOS();
        }
    };
}

function toggleVoice() {
    if (!recognition) return;

    if (!isListening) {
        recognition.start();
        isListening = true;
    } else {
        recognition.stop();
        isListening = false;
    }
}

// Modal
function showSuccessModal() {
    document.getElementById("successModal").style.display = "block";
}

function closeModal() {
    document.getElementById("successModal").style.display = "none";
}