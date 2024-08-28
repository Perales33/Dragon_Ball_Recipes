let countdown, isPaused = false, remainingTime = 0;

// Actualiza la pantalla con el tiempo restante en formato MM:SS
const updateDisplay = (time) => {
    const minutes = Math.floor(time / 60).toString().padStart(2, '0');
    const seconds = (time % 60).toString().padStart(2, '0');
    document.getElementById('timeDisplay').textContent = `${minutes}:${seconds}`;
};

// Inicia el temporizador
const startTimer = (duration) => {
    const end = Date.now() + duration * 1000;
    countdown = setInterval(() => {
        remainingTime = Math.max(Math.ceil((end - Date.now()) / 1000), 0);
        updateDisplay(remainingTime);
        if (remainingTime === 0) clearInterval(countdown); // Detener cuando el tiempo se agota
    }, 1000);
};

// Maneja el clic en el botón de inicio
document.getElementById('startButton').addEventListener('click', () => {
    remainingTime = (parseInt(document.getElementById('minutes').value) || 0) * 60 +
                    (parseInt(document.getElementById('seconds').value) || 0);

    if (remainingTime > 0) startTimer(remainingTime); // Inicia si se ha ingresado tiempo
    else alert("Por favor, establece un tiempo válido."); // Alerta si no se ingresa tiempo
});

// Maneja el clic en el botón de pausa/reanudación
document.getElementById('pauseButton').addEventListener('click', () => {
    isPaused ? startTimer(remainingTime) : clearInterval(countdown); // Pausar o reanudar
    isPaused = !isPaused; // Alternar el estado de pausa
});

// Maneja el clic en el botón de reinicio
document.getElementById('resetButton').addEventListener('click', () => {
    clearInterval(countdown);
    updateDisplay(0); // Restablecer la pantalla a 00:00
    document.getElementById('minutes').value = ""; // Limpiar los campos de entrada
    document.getElementById('seconds').value = "";
    isPaused = false;
});
