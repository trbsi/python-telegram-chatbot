/* ---------------- PWA site - install website on phone -----------------  */
if ("serviceWorker" in navigator) {
    //serviceWorkerFile is defined in js.html
    navigator.serviceWorker.register(serviceWorkerFile);
}

let deferredPrompt = null;

// =========================
// Do NOT show if installed
// =========================

// Android / Chrome
window.addEventListener("appinstalled", () => {
    localStorage.setItem("pwaInstalled", "yes");
});

const isIOS = /iphone|ipad|ipod/i.test(navigator.userAgent);
const isInStandalone = window.navigator.standalone === true;

// If already installed → don't show again
if (localStorage.getItem("pwaInstalled") === "yes" || isInStandalone) {
    console.log("PWA is installed, no popup shown.");
} else {
    // Continue logic
    setupBannerLogic();
}

function setupBannerLogic() {

    // ===============================
    // Hide for 1 hour after closing
    // ===============================

    const lastClose = localStorage.getItem("installPopupClosedAt");
    if (lastClose && Date.now() - Number(lastClose) < 3600 * 1000) {
        console.log("Install popup suppressed (within 1 hour).");
        return;
    }

    // ===============================
    // Android / Chrome install prompt
    // ===============================
    window.addEventListener("beforeinstallprompt", (e) => {
        e.preventDefault();
        deferredPrompt = e;

        if (!isIOS) {
            $("#installBanner").removeClass("hidden");
        }
    });


    // ===============================
    // iOS manual A2HS guide
    // ===============================
    if (isIOS && !isInStandalone) {
        $("#iosInstallHint").removeClass("hidden");
    }
}


// ===============================
// Install Button Click (Android)
// ===============================
$("#installBtn").on("click", async function () {
    if (!deferredPrompt) return;

    deferredPrompt.prompt();
    const choice = await deferredPrompt.userChoice;

    if (choice.outcome === "accepted") {
        localStorage.setItem("pwaInstalled", "yes");
        $("#installBanner").addClass("hidden");
    }

    deferredPrompt = null;
});


// ===============================
// CLOSE BUTTONS
// ===============================

$("#closeInstallBanner").on("click", function () {
    $("#installBanner").addClass("hidden");
    localStorage.setItem("installPopupClosedAt", Date.now());
});

$("#closeIosHint").on("click", function () {
    $("#iosInstallHint").addClass("hidden");
    localStorage.setItem("installPopupClosedAt", Date.now());
});