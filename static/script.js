function startTimer(event) {
    event.preventDefault(); 

    let button = document.getElementById("resendBtn");
    let now = Date.now();
    let endTime = now + 120000; // 2 minuty od teď
    localStorage.setItem("resendEndTime", endTime); // Uložení času konce do localStorage

    disableButton(endTime);

    // Počká 0,5 sekundy, aby uživatel viděl změnu, a pak přesměruje
    setTimeout(() => {
        window.location.href = button.href;
    }, 500);
}

function disableButton(endTime) {
    let button = document.getElementById("resendBtn");
    let timerText = document.getElementById("timerText");

    let interval = setInterval(() => {
        let now = Date.now();
        let timeLeft = Math.max(0, Math.floor((endTime - now) / 1000)); // Zbývající čas v sekundách

        if (timeLeft > 0) {
            button.style.pointerEvents = "none";
            button.style.opacity = "0.5";
            timerText.innerText = ` (${timeLeft}s)`;
        } else {
            clearInterval(interval);
            button.style.pointerEvents = "auto";
            button.style.opacity = "1";
            timerText.innerText = "";
            localStorage.removeItem("resendEndTime"); // Smazání uloženého času
        }
    }, 1000);
}

// Okamžitě při načtení stránky zablokujeme tlačítko
let endTime = localStorage.getItem("resendEndTime");
if (endTime) {
    let now = Date.now();
    if (now < parseInt(endTime)) {
        document.getElementById("resendBtn").style.pointerEvents = "none";
        document.getElementById("resendBtn").style.opacity = "0.5";
    }
}

// Po načtení stránky aktivujeme timer, pokud je třeba
document.addEventListener("DOMContentLoaded", () => {
    if (endTime) {
        disableButton(parseInt(endTime));
    }
});
