function selectAll() {
    const el = document.getElementsByClassName("checkbox");
    if (!mainCheck.checked) {
        for (let i = 1; i < el.length; i++) {
            el[i].checked = false;
        }
    } else {
        for (let i = 1; i < el.length; i++) {
            el[i].checked = true;
        }
    }
}

function checkSelected() {
    const el = document.getElementsByClassName("checkbox");
    let flag = false;
    for (let i = 1; i < el.length; i++) {
        if (el[i].checked === true) {
            flag = true;
            break;
        }
    }
    if (flag) {
        document.getElementById('usePeptides').disabled = false;
    } else {
        document.getElementById('usePeptides').disabled = true;
    }
}

function format(d) {
    return (
        '<table class="dop_info" cellpadding="5" cellspacing="0" border="0" style="padding-left:20px; height:70px;">' +
        '<tbody style="height:auto;">' +
        '<tr>' +
        '<td style="width: 319px;"><b>ID:</b></td>' +
        '<td>' + '<b>' + d.id + '</b>' + '</td>' +
        '</tr>' +
        '<tr>' +
        '<td style="width: 319px;"><b>Sequence:</b></td>' +
        '<td>' + '<b>' + d.sequence + '</b>' + '</td>' +
        '</tr>' +
        '<tr>' +
        '<td style="width: 319px;"><b>Activity:</b></td>' +
        '<td>' + '<b>' + d.activity + '</b>' + '</td>' +
        '</tr>' +
        '<tr>' +
        '<td style="width: 319px;"><b>Length:</b></td>' +
        '<td>' + '<b>' + d.length + '</b>' + '</td>' +
        '</tr>' +
        '<tr>' +
        '<td style="width: 319px;"><b>Mass (Da):</b></td>' +
        '<td>' + '<b>' + d.massDa + '</b>' + '</td>' +
        '</tr>' +
        '<tr>' +
        '<td style="width: 319px;"><b>Organism (scientific name):</b></td>' +
        '<td>' + '<b>' + d.scientificName + '</b>' + '</td>' +
        '</tr>' +
        '<tr>' +
        '<td style="width: 319px;"><b>Organism (common name):</b></td>' +
        '<td>' + '<b>' + d.commonName + '</b>' + '</td>' +
        '</tr>' +
        '<tr>' +
        '<td style="width: 319px;"><b>Tissue source or synthetic:</b></td>' +
        '<td>' + '<b>' + d.tissueSource + '</b>' + '</td>' +
        '</tr>' +
        '<tr>' +
        '<td style="width: 319px;"><b>Protein source:</b></td>' +
        '<td>' + '<b>' + d.proteinSource + '</b>' + '</td>' +
        '</tr>' +
        '<tr>' +
        '<td style="width: 319px;"><b>PMID:</b></td>' +
        '<td>' + '<b>' + d.pmid + '</b>' + '</td>' +
        '</tr>' +
        '<tr>' +
        '<td style="width: 319px;"><b>Reference:</b></td>' +
        '<td>' + '<b>' + d.reference + '</b>' + '</td>' +
        '</tr>' +
        '</tbody>' +
        '</table>'
    );
};

$(document).ready(function() {
    var table = $('#table').DataTable({
        ajax: '../api/database',
        columns: [{
                className: 'checkbox-control',
                orderable: false,
                data: null,
                defaultContent: '<input class="checkbox" type="checkbox"/>',
            },
            {
                className: 'main-info width80',
                data: 'id'
            },
            {
                className: 'main-info sequence-bold',
                data: 'sequence',
            },
            {
                className: 'main-info width80',
                data: 'length'
            },
            {
                className: 'main-info',
                data: 'scientificName'
            },
            {
                className: 'main-info',
                data: 'commonName'
            },
            {
                className: 'main-info color-state',
                data: 'activity'
            },
        ],
        autoWidth: false,
        fixedHeader: true,
        fixedColumns: true,
        responsive: true,
        paging: false,
        order: [
            [1, 'asc']
        ],
    });
    // Add event listener for opening and closing details
    $('#table tbody').on('click', 'td.main-info', function() {
        var tr = $(this).closest('tr');
        var row = table.row(tr);

        if (row.child.isShown()) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        } else {
            // Open this row
            row.child(format(row.data())).show();
            tr.addClass('shown');
        }
    });
});

function stateColor() {
    const states = document.getElementsByClassName("color-state");
    search = document.querySelector("#table_filter > label > input[type=search]").style
    search.width = '300px';
    search.height = '35px';
    for (let i = 0; i < states.length; i++) {
        if (states[i].innerHTML === 'Yes') {
            states[i].innerHTML = '<b>Yes</b>';
            states[i].style.color = '#00FF08';
        } else if (states[i].innerHTML === 'No') {
            states[i].innerHTML = '<b>No</b>';
            states[i].style.color = '#FE3A3A';
        }
    }
}
function func() {
    const checkbox_list = document.getElementsByClassName("checkbox");
    const sequence_list = document.getElementsByClassName("sequence-bold");
    let checked_seq = [];
    for (let i = 1; i < checkbox_list.length; i++) {
        if (checkbox_list[i].checked) {
            checked_seq.push(sequence_list[i].innerHTML);
        }
    }
    let peptides = checked_seq.join("?");
    console.log(peptides);
    window.location.href = `/search?peptides=${peptides}`;
}