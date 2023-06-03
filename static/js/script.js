function themeChange() {
    let globalTheme = document.getElementById("global-theme");
    let indexTheme = document.getElementById("index-theme");
    let logo = document.getElementById("logoIconId");
    console.log(globalTheme.getAttribute("href"));
    if (globalTheme.getAttribute("href") === "./static/css/global-light.css") {
        globalTheme.href = "./static/css/global-dark.css";
        indexTheme.href = "./static/css/index-dark.css";
        logo.src = "./static/images/dark/logo-greentransformed-1@2x.png";
    } else {
        globalTheme.href = "./static/css/global-light.css";
        indexTheme.href = "./static/css/index-light.css";
        logo.src = "./static/images/light/logo-blue-1@2x.png";
    }

}
function Animation() {
    var scrollAnimElements = document.querySelectorAll("[data-animate-on-scroll]");
    var observer = new IntersectionObserver(
        (entries) => {
            for (const entry of entries) {
                if (entry.isIntersecting || entry.intersectionRatio > 0) {
                    const targetElement = entry.target;
                    targetElement.classList.add("animate");
                    observer.unobserve(targetElement);
                }
            }
        },
        {
            threshold: 0.15,
        }
    );
    for (let i = 0; i < scrollAnimElements.length; i++) {
        observer.observe(scrollAnimElements[i]);
    }
}

function closePopup(elementsId) {
    if (elementsId === "modalContentPopup") {
        let downloadLink = document.getElementById("downloadLink");
        let downloadButton = document.getElementById("downloadBtn");
        let downloadButtonStyle = downloadButton.style;
        let popupPreloaderStyle = document.getElementById("popupPreloader").style;
        let popupText = document.getElementById("popupText");
        if (downloadButtonStyle) {
          downloadLink.href = "#";
          downloadButtonStyle.display = "none";
        }
        if (popupPreloaderStyle) {
          popupPreloaderStyle.display = "flex";
        }
        if (popupText) {
          popupText.innerHTML = "Files will be created soon";
        }
    }
    let popup = document.getElementById(elementsId);
    function isOverlay(node) {
        return !!(
            node &&
            node.classList &&
            node.classList.contains("popup-overlay")
        );
    }
    while (popup && !isOverlay(popup)) {
        popup = popup.parentNode;
    }
    if (isOverlay(popup)) {
        popup.style.display = "none";
    }
}

function startLoadingPopup() {
    let proteinInput = document.getElementById("proteins-input");
    let peptidesInput = document.getElementById("peptides-input");
    if (!proteinInput.value || !peptidesInput.value) {
        openMessage("errorMessagePopup");
        return;
    }
    let popup = document.getElementById("modalContentPopup");
    if (!popup) return;
    let popupStyle = popup.style;
    if (popupStyle) {
        popupStyle.display = "flex";
        popupStyle.zIndex = 100;
        popupStyle.backgroundColor = "rgba(0, 0, 0, 0.6)";
        popupStyle.alignItems = "center";
        popupStyle.justifyContent = "center";
    }
    popup.removeAttribute("closable");

    let onClick =
        popup.onClick ||
            function (e) {
                if (e.target === popup && popup.hasAttribute("closable")) {
                    popupStyle.display = "none";
                }
            };
    popup.addEventListener("click", onClick);
}

function openMessage(elementsId) {
    let popup = document.getElementById(elementsId);
    if (!popup) return;
    let popupStyle = popup.style;
    if (popupStyle) {
        popupStyle.display = "flex";
        popupStyle.zIndex = 100;
        popupStyle.backgroundColor = "";
        popupStyle.alignItems = "flex-end";
        popupStyle.justifyContent = "";
    }
    popup.setAttribute("closable", "");

    let onClick =
        popup.onClick ||
        function (e) {
        if (e.target === popup && popup.hasAttribute("closable")) {
            popupStyle.display = "none";
        }
    };
    popup.addEventListener("click", onClick);
}

