function themeChange(page) {
    let globalTheme = document.getElementById("global-theme");
    let indexTheme = document.getElementById("index-theme");
    let logo = document.getElementById("logoIconId");
    console.log(globalTheme.getAttribute("href"));
    if (indexTheme.getAttribute("href") === `./static/css/${page}/index-light.css`) {
        indexTheme.href = `./static/css/${page}/index-dark.css`;
        logo.src = "./static/images/header/dark/logo-greentransformed-1@2x.png";
    } else {
        indexTheme.href = `./static/css/${page}/index-light.css`;
        logo.src = "./static/images/header/light/logo-blue-1@2x.png";
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
    if (elementsId === "modalPopup") {
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

function startPopup(popupName) {
    if (popupName === "loading") {
        let proteinInput = document.getElementById("proteins-input");
        let peptidesInput = document.getElementById("peptides-input");
        if (!proteinInput.value && document.getElementById("userProteinsFile").value == "") {
            openMessage("errorMessagePopup");
            return;
        }
        if (!peptidesInput.value && document.getElementById("userPeptidesFile").value == "") {
            openMessage("errorMessagePopup");
            return;
        }
        let popup = document.getElementById("modalPopup");
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
    } else {
          var popup = document.getElementById(popupName);
          if (!popup) return;
          var popupStyle = popup.style;
          if (popupStyle) {
            popupStyle.display = "flex";
            popupStyle.zIndex = 100;
            popupStyle.backgroundColor = "rgba(113, 113, 113, 0.3)";
            popupStyle.alignItems = "center";
            popupStyle.justifyContent = "center";
          }
          popup.removeAttribute("closable");

          var onClick =
            popup.onClick ||
            function (e) {
              if (e.target === popup && popup.hasAttribute("closable")) {
                popupStyle.display = "none";
              }
            };
          popup.addEventListener("click", onClick);
      }

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

var lang = "ENG";
function changeLang() {
    hStep1 = document.getElementById("h-step1");
    hStep2 = document.getElementById("h-step2");
    hStep3 = document.getElementById("h-step3");
    hStep4 = document.getElementById("h-step4");
    actionStep1 = document.getElementById("action-step1");
    actionStep2 = document.getElementById("action-step2");
    or = document.getElementsByClassName("enter-one-or");
    text = document.getElementById("step4-text");
    imports = document.getElementsByClassName("import-txt-file");
    selectBtns = document.getElementsByClassName("js-fileName");
    filters = document.getElementsByClassName("text-filters");
    startBtn = document.getElementById("run-btn");
    if (lang === "ENG") {
        lang = "RUS";
        hStep1.innerHTML = "Шаг 1";
        hStep2.innerHTML = "Шаг 2";
        hStep3.innerHTML = "Шаг 3";
        hStep4.innerHTML = "Шаг 4";
        or[1].innerHTML = "ИЛИ";
        or[2].innerHTML = "ИЛИ";
        actionStep1.innerHTML = "Введите белки (один или более)";
        actionStep2.innerHTML = "Введите пептиды";
        imports[0].innerHTML = "Выберите TXT файл";
        imports[1].innerHTML = "Выберите TXT файл";
        selectBtns[0].innerHTML = "Выбрать";
        selectBtns[1].innerHTML = "Выбрать";
        startBtn.innerHTML = "Создать";
        imports[0].style.width='185px';
        imports[1].style.width='185px';
        selectBtns[0].style.fontSize = "18px";
        selectBtns[1].style.fontSize = "18px";
        text.innerHTML = "Процесс поиска пептидов и создания Excel таблиц требует времени, в зависимости от количества белков,пептидов, качества интернет-соединения, работоспособности uniprot.org";
        filters[0].innerHTML = "Индетификатор";
        filters[1].innerHTML = "Статус";
        filters[2].innerHTML = "Имя белка";
        filters[3].innerHTML = "Научное название";
        filters[4].innerHTML = "Распространенное название";
        filters[5].innerHTML = "Название гена";
        filters[6].innerHTML = "Существование (на каком уровне)";
        filters[7].innerHTML = "Длина";
        filters[8].innerHTML = "Масса (Da)";
        filters[9].innerHTML = "Категория";
        filters[10].innerHTML = "Номер пептида";
        filters[11].innerHTML = "Последовательность";
        filters[12].innerHTML = "Длина последовательности";
        filters[13].innerHTML = "Количество пептида";
        filters[14].innerHTML = "Позиция";
        filters[15].innerHTML = "Соседняя аминокислота с С-конца";
        filters[16].innerHTML = "Соседняя аминокислота с N-конца";
        filters[17].innerHTML = "Встречаемость (на 1000)";
    } else {
        lang = "ENG";
        hStep1.innerHTML = "Step 1";
        hStep2.innerHTML = "Step 2";
        hStep3.innerHTML = "Step 3";
        hStep4.innerHTML = "Step 4";
        or[1].innerHTML = "OR";
        or[2].innerHTML = "OR";
        actionStep1.innerHTML = "Enter one or more protein";
        actionStep2.innerHTML = "Enter one or more peptides";
        imports[0].innerHTML = "import TXT file";
        imports[1].innerHTML = "import TXT file";
        selectBtns[0].innerHTML = "Select";
        selectBtns[1].innerHTML = "Select";
        imports[0].style.width='130px';
        imports[1].style.width='130px';
        selectBtns[0].style.fontSize = "20px";
        selectBtns[1].style.fontSize = "20px";
        startBtn.innerHTML = "Create";
        text.innerHTML = "The process of searching for peptides and creating Excel spreadsheets takes time, depending on the number of proteins, peptides, the quality of the Internet connection, efficiency uniprot.org";
        filters[0].innerHTML = "Entry name";
        filters[1].innerHTML = "Status";
        filters[2].innerHTML = "Protein name";
        filters[3].innerHTML = "Organism (scientific name)";
        filters[4].innerHTML = "Organism (common name)";
        filters[5].innerHTML = "Gene name";
        filters[6].innerHTML = "Protein existence";
        filters[7].innerHTML = "Length";
        filters[8].innerHTML = "Mass (Da)";
        filters[9].innerHTML = "Category";
        filters[10].innerHTML = "Peptide ID";
        filters[11].innerHTML = "Sequence";
        filters[12].innerHTML = "Sequence length";
        filters[13].innerHTML = "Occurrence";
        filters[14].innerHTML = "Position";
        filters[15].innerHTML = "Amino acid from the C-terminus";
        filters[16].innerHTML = "Amino acid from the N-terminus";
        filters[17].innerHTML = "Relative (per 1000)";
    }
}
