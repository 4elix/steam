function openFullscreen(img) {
    var overlay = document.createElement("div");
    overlay.style.position = "fixed";
    overlay.style.top = "0";
    overlay.style.left = "0";
    overlay.style.width = "100%";
    overlay.style.height = "100%";
    overlay.style.backgroundColor = "rgba(0, 0, 0, 0.8)";
    overlay.style.zIndex = "9998";
    document.body.appendChild(overlay);

    var fullscreenImg = document.createElement("img");
    fullscreenImg.src = img.src;
    fullscreenImg.style.position = "fixed";
    fullscreenImg.style.top = "50%";
    fullscreenImg.style.left = "50%";
    fullscreenImg.style.transform = "translate(-50%, -50%)";
    fullscreenImg.style.maxWidth = "90%";
    fullscreenImg.style.maxHeight = "90%";
    fullscreenImg.style.zIndex = "9999";
    document.body.appendChild(fullscreenImg);

    var closeButton = document.createElement("span");
    closeButton.style.position = "fixed";
    closeButton.style.top = "20px";
    closeButton.style.right = "30px";
    closeButton.style.fontSize = "40px";
    closeButton.style.color = "white";
    closeButton.style.cursor = "pointer";
    closeButton.style.zIndex = "10000";
    closeButton.innerHTML = "&times;";
    closeButton.onclick = closeFullscreen;
    document.body.appendChild(closeButton);
}

function closeFullscreen() {
    var fullscreenImg = document.querySelector("img[style*='position: fixed']");
    if (fullscreenImg) {
        fullscreenImg.parentNode.removeChild(fullscreenImg);
    }

    var overlay = document.querySelector("div[style*='background-color: rgba(0, 0, 0, 0.8)']");
    if (overlay) {
        overlay.parentNode.removeChild(overlay);
    }

    var closeButton = document.querySelector("span[style*='cursor: pointer']");
    if (closeButton) {
        closeButton.parentNode.removeChild(closeButton);
    }
}


document.addEventListener("DOMContentLoaded", function() {
    document.body.classList.add("loading");
});

document.addEventListener("DOMContentLoaded", function() {
    setTimeout(function() {
        document.body.classList.remove("loading");
        document.querySelector(".content").style.display = "block";
    }, 2500);
});