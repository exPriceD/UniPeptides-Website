window.onload = Animation;

let params = (new URL(document.location)).searchParams;
let peptides = params.get("peptides");
if (peptides) {
    for (let i = 0; i < peptides.length; i++) {
        if (peptides[i] === '?') {
            peptides = peptides.replace('?', ',');
        }
    }
    input = document.getElementById("peptides-input");
    input.value = peptides;
};

$('#peptides-input').focus(function() {
    var that = this;
    setTimeout(function() {
        that.selectionStart = that.selectionEnd = 10000;
    }, 0);
});

$('#userProteinsFile').on('click touchstart', function() {
    $(this).val('');
});
$("#userProteinsFile").change(function(e) {
    openMessage("okMessagePopup");
});

$('#userPeptidesFile').on('click touchstart', function() {
    $(this).val('');
});
$("#userPeptidesFile").change(function(e) {
    openMessage("okMessagePopup");
});

$(document).on('submit', '#post-form', function(e) {
    e.preventDefault();
    var form_data = new FormData();
    console.log($('#userProteinsFile').prop('files')[0]);
    form_data.append('userProteins', $('#userProteinsFile').prop('files')[0]);
    form_data.append('userPeptides', $('#userPeptidesFile').prop('files')[0]);
    form_data.append('proteins_value', $("#proteins-input").val());
    form_data.append('peptides_value', $("#peptides-input").val());
    form_data.append('entryName', $("#entry_name").is(':checked'));
    form_data.append('entryType', $("#status").is(':checked'));
    form_data.append('fullName', $("#protein_name").is(':checked'));
    form_data.append('scientificName', $("#scientific_name").is(':checked'));
    form_data.append('commonName', $("#common_name").is(':checked'));
    form_data.append('genes', $("#gene").is(':checked'));
    form_data.append('proteinExistence', $("#protein_existence").is(':checked'));
    form_data.append('length', $("#sequence_length").is(':checked'));
    form_data.append('massDa', $("#mass_da").is(':checked'));
    form_data.append('category', $("#category").is(':checked'));
    form_data.append('id', $("#peptide_id").is(':checked'));
    form_data.append('sequence', $("#sequence").is(':checked'));
    form_data.append('sequence_length', $("#peptide_length").is(':checked'));
    form_data.append('occurrence', $("#occurrence").is(':checked'));
    form_data.append('position', $("#position").is(':checked'));
    form_data.append('cter', $("#cterm").is(':checked'));
    form_data.append('nter', $("#nterm").is(':checked'));
    form_data.append('relative', $("#relative").is(':checked'));

    $.ajax({
        type: 'POST',
        dataType: 'json',
        url: '/search',
        data: form_data,
        contentType: false,
        cache: false,
        processData: false,
        success: function(data) {
            console.log(data);
            updateModal(data);
        }
    })
});

function updateModal(data) {
    filename = data['filename']
    let downloadLink = document.getElementById("downloadLink");
    let downloadButton = document.getElementById("downloadBtn");
    let downloadButtonStyle = downloadButton.style;
    let popupPreloaderStyle = document.getElementById("popupPreloader").style;
    let popupText = document.getElementById("popupText");
    if (downloadButtonStyle) {
        downloadLink.href = `/uploads/outputs/${filename}`
        downloadButtonStyle.display = "flex";
    }
    if (popupPreloaderStyle) {
        popupPreloaderStyle.display = "none";
    }
    if (popupText) {
        popupText.innerHTML = "File was created";
    }
    message_title = data['message_title'];
    message = data['message'];
    if (message_title) {
        title = document.getElementById('message_title');
        msg = document.getElementById('message');
        title.innerHTML = message_title;
        msg.innerHTML = message;
        title.style.display = 'flex';
        msg.style.display = 'flex';
    }
}