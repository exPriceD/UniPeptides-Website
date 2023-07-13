window.onload = Animation;

new DataTable('#table', {
    ajax: '../api/database',
    paging: false,
    scrollCollapse: true,
    scrollY: '50vh',
    order: [
        [1, 'asc']
    ],
    "columnDefs": [{
        responsivePriority: 1,
        targets: 3
    }, ],
    columns: [{
            orderable: false,
            data: null,
            defaultContent: ''
        },
        {
            className: 'checkbox-control',
            orderable: false,
            data: null,
            defaultContent: '<input class="checkbox" type="checkbox"/>',
        },
        {
            data: 'id'
        },
        {
            className: "sequence-bold",
            data: 'sequence'
        },
        {
            data: 'length'
        },
        {
            data: 'scientificName'
        },
        {
            data: 'commonName'
        },
        {
            data: 'activity'
        },
        {
            data: 'tissueSource'
        },
        {
            data: 'proteinSource'
        },
        {
            className: 'display_none',
            data: 'pmid'
        },
        {
            className: 'display_none',
            data: 'reference'
        },
    ],
    responsive: {
        details: {
            renderer: function(api, rowIdx, columns) {
                let data = columns.map((col, i) => {
                    if (col.columnIndex != 1 && col.columnIndex != 0) {
                        return '<tr data-dt-row="' +
                            col.rowIndex +
                            '" data-dt-column="' +
                            col.columnIndex +
                            '">' +
                            '<td>' + '<b>' +
                            col.title + '</b>' +
                            ':' +
                            '</td> ' +
                            '<td>' + '<b>' +
                            col.data +
                            '</td>' + '</b>' +
                            '</tr>'
                    }
                }).join('');

                let table = document.createElement('table');
                table.innerHTML = data;

                return data ? table : false;
            }
        }
    }
});
var inter = setInterval(function() {
    let table = document.getElementById('table');
    table.classList.add("collapsed");
}, 100);
setTimeout(function() {
    clearInterval(inter);
}, 5000);

setInterval(checkSelected, 100);

function pepInSearch() {
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