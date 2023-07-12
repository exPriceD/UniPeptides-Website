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
            data: 'sequence',
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