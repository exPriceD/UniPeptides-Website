window.onload = Animation;

function openPopup(popupName, requestId) {
    var popup = document.getElementById(popupName);
    popup.classList.add(requestId);
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
        function(e) {
            if (e.target === popup && popup.hasAttribute("closable")) {
                popupStyle.display = "none";
            }
        };
    popup.addEventListener("click", onClick);
};

function selectDatabase() {
    database_container = document.getElementById("database_container");
    requests_container = document.getElementById("requests_container");
    database_btn = document.getElementById("database_btn");
    requests_btn = document.getElementById("requests_btn");
    database_container.style.display = "flex";
    requests_container.style.display = "none";
    database_btn.classList.add("small-btn1");
    database_btn.classList.remove("small-btn2");
    requests_btn.classList.remove("small-btn1");
    requests_btn.classList.add("small-btn2");

};

function selectRequests() {
    database_container = document.getElementById("database_container");
    requests_container = document.getElementById("requests_container");
    database_btn = document.getElementById("database_btn");
    requests_btn = document.getElementById("requests_btn");
    database_container.style.display = "none";
    requests_container.style.display = "flex";
    requests_btn.classList.add("small-btn1");
    requests_btn.classList.remove("small-btn2");
    database_btn.classList.remove("small-btn1");
    database_btn.classList.add("small-btn2");

};

function acceptRequest() {
    modal = document.getElementById("modalAcceptPopup");
    let request_id = modal.classList[1];
    modal.classList.remove(request_id);
    closePopup('modalAcceptPopup');
    var form_data = new FormData();
    form_data.append('id', request_id);
    form_data.append('sequence', $(`#sequence_${request_id}`).val());
    form_data.append('scientific_name', $(`#scientific_name_${request_id}`).val());
    form_data.append('common_name', $(`#common_name_${request_id}`).val());
    form_data.append('activity', $(`#activity_${request_id}`).val());
    form_data.append('protein_source', $(`#protein_source_${request_id}`).val());
    form_data.append('massDa', $(`#massDa_${request_id}`).val());
    form_data.append('tissue_source', $(`#tissue_source_${request_id}`).val());
    form_data.append('pmid', $(`#pmid_${request_id}`).val());
    form_data.append('reference', $(`#reference_${request_id}`).val());
    $.ajax({
        type: 'POST',
        dataType: 'json',
        url: '/panel/accept',
        data: form_data,
        contentType: false,
        cache: false,
        processData: false,
        success: function(data) {
            console.log("success");
        }
    });
    let status = document.getElementById(`status_${request_id}`);
    status.innerHTML = 'Accepted';
    status.style.color = "#15FF1E";

    let message = document.getElementById(`message_${request_id}`);
    message.style.opacity = '1';

    let acceptButton = document.getElementById(`acceptButton_${request_id}`);
    let cancelButton = document.getElementById(`cancelButton_${request_id}`);

    acceptButton.setAttribute("disabled", "disabled");
    acceptButton.style.opacity = '0.7';
    cancelButton.setAttribute("disabled", "disabled");
    cancelButton.style.opacity = '0.7';

};

function cancelRequest() {
    modal = document.getElementById("modalCancelPopup");
    let request_id = modal.classList[1];
    modal.classList.remove(request_id);
    closePopup('modalCancelPopup');
    var form_data = new FormData();
    form_data.append('id', request_id);
    $.ajax({
        type: 'POST',
        dataType: 'json',
        url: '/panel/cancel',
        data: form_data,
        contentType: false,
        cache: false,
        processData: false,
        success: function(data) {
            console.log("success");
        }
    });
    let status = document.getElementById(`status_${request_id}`);
    status.innerHTML = 'Canceled';
    status.style.color = "#FF4141";

    let message = document.getElementById(`message_${request_id}`);
    message.innerHTML = "The application was canceled"
    message.style.opacity = '1';

    let acceptButton = document.getElementById(`acceptButton_${request_id}`);
    let cancelButton = document.getElementById(`cancelButton_${request_id}`);

    acceptButton.setAttribute("disabled", "disabled");
    acceptButton.style.opacity = '0.7';
    cancelButton.setAttribute("disabled", "disabled");
    cancelButton.style.opacity = '0.7';
};

function addPeptide() {
    var form_data = new FormData();
    form_data.append('sequence', $(`#sequence_addPeptide`).val());
    form_data.append('scientific_name', $(`#scientific_name_addPeptide`).val());
    form_data.append('common_name', $(`#common_name_addPeptide`).val());
    form_data.append('activity', $(`#activity_addPeptide`).val());
    form_data.append('protein_source', $(`#protein_source_addPeptide`).val());
    form_data.append('massDa', $(`#massDa_addPeptide`).val());
    form_data.append('tissue_source', $(`#tissue_source_addPeptide`).val());
    form_data.append('pmid', $(`#pmid_addPeptide`).val());
    form_data.append('reference', $(`#reference_addPeptide`).val());
    $.ajax({
        type: 'POST',
        dataType: 'json',
        url: '/panel/add_peptide',
        data: form_data,
        contentType: false,
        cache: false,
        processData: false,
        success: function(data) {
            console.log("success");
        }
    });

    let message = document.getElementById("addMsg");
    message.style.opacity = "1";

}

function removePeptide() {
    var form_data = new FormData();
    form_data.append('sequence', $(`#sequence_remove`).val());
    form_data.append('activity', $(`#activity_remove`).val());
    $.ajax({
        type: 'POST',
        dataType: 'json',
        url: '/panel/remove_peptide',
        data: form_data,
        contentType: false,
        cache: false,
        processData: false,
        success: function(data) {
            console.log("success");
        }
    });
    let message = document.getElementById("removeMsg");
    message.style.opacity = "1";

};

function editPeptide() {
    var form_data = new FormData();
    form_data.append('sequence', $(`#sequence_editPeptide`).val());
    form_data.append('activity', $(`#activity_editPeptide`).val());
    form_data.append('scientific_name', $(`#scientific_name_editPeptide`).val());
    form_data.append('common_name', $(`#common_name_editPeptide`).val());
    form_data.append('protein_source', $(`#protein_source_editPeptide`).val());
    form_data.append('massDa', $(`#massDa_editPeptide`).val());
    form_data.append('tissue_source', $(`#tissue_source_editPeptide`).val());
    form_data.append('pmid', $(`#pmid_editPeptide`).val());
    form_data.append('reference', $(`#reference_editPeptide`).val());
    $.ajax({
        type: 'POST',
        dataType: 'json',
        url: '/panel/edit_peptide',
        data: form_data,
        contentType: false,
        cache: false,
        processData: false,
        success: function(data) {
            console.log("success");
        }
    });
    let message = document.getElementById("editMsg");
    message.style.opacity = "1";
}

function openCard(elements) {
    card = document.getElementById(elements);
    if (card.style.display === "none") {
        card.style.display = "flex";
    } else {
        card.style.display = "none";
    }
}

function checkFields(sequence_id, reference_id) {
    let flag = true;
    sequenceInput = document.getElementById(sequence_id);
    referenceInput = document.getElementById(reference_id);
    if (!sequenceInput.value) {
        sequenceInput.style.border = "2px solid var(--color-red)";
        flag = false;
        sequenceInput.onfocus = function() {
            sequenceInput.style.border = "2px solid var(--color-silver)";
        }
    };
    if (!referenceInput.value) {
        referenceInput.style.border = "2px solid var(--color-red)";
        flag = false;
        referenceInput.onfocus = function() {
            referenceInput.style.border = "2px solid var(--color-silver)";
        }
    };

    return flag;
}

function findPeptide() {
    let sequence = document.getElementById("sequence_editPeptide");
    let activity = document.getElementById("activity_editPeptide");
    $.getJSON('http://127.0.0.1:5000/api/database', function(data) {
        list = data["data"];
        for (let peptide in list) {
            console.log(peptide);
            if (list[peptide]["sequence"] === sequence.value && list[peptide]["activity"] === activity.value) {
                document.getElementById("scientific_name_editPeptide").value = list[peptide]["scientificName"];
                document.getElementById("common_name_editPeptide").value = list[peptide]["commonName"];
                document.getElementById("protein_source_editPeptide").value = list[peptide]["proteinSource"];
                document.getElementById("massDa_editPeptide").value = list[peptide]["massDa"];
                document.getElementById("tissue_source_editPeptide").value = list[peptide]["tissueSource"];
                document.getElementById("pmid_editPeptide").value = list[peptide]["pmid"];
                document.getElementById("reference_editPeptide").value = list[peptide]["pmid"];
                return;
            }
        }
    });
}

function clearFields(form_id) {
    if (form_id === "removePeptides") {
        document.getElementById("sequence_remove").value = '';
        document.getElementById("activity_remove").value = '';
        return;
    };
    document.getElementById(`sequence_${form_id}`).value = '';
    document.getElementById(`scientific_name_${form_id}`).value = '';
    document.getElementById(`common_name_${form_id}`).value = '';
    document.getElementById(`activity_${form_id}`).value = '';
    document.getElementById(`protein_source_${form_id}`).value = '';
    document.getElementById(`tissue_source_${form_id}`).value = '';
    document.getElementById(`massDa_${form_id}`).value = '';
    document.getElementById(`pmid_${form_id}`).value = '';
    document.getElementById(`reference_${form_id}`).value = '';
}

$(document).on('click', '#addPeptidesBtn', function(e) {
    e.preventDefault();
    if (checkFields("sequence_addPeptide", "reference_addPeptide")) {
        addPeptide();
    };
});

$(document).on('click', '#editPeptidesBtn', function(e) {
    e.preventDefault();
    if (checkFields("sequence_editPeptide", "activity_editPeptide")) {
        editPeptide();
    };
});

$(document).on('click', '#removePeptidesBtn', function(e) {
    e.preventDefault();
    if (checkFields("sequence_remove", "activity_remove")) {
        removePeptide();
    };
});

$(document).on('click', '#addPeptideClear', function(e) {
    e.preventDefault();
    clearFields('addPeptide');
});

$(document).on('click', '#editPeptideClear', function(e) {
    e.preventDefault();
    clearFields('editPeptide');
});

$(document).on('click', '#removePeptideClear', function(e) {
    e.preventDefault();
    clearFields('removePeptides');
});
