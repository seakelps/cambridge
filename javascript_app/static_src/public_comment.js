function createTable() {
  var dt = new DataTable("#public-comment-table", {
    ordering: true,
    paging: true,
    searching: true,
    dom: "frtip",
    pageLength: 15,
    columnDefs: [
      {
        className: "dt-nowrap",
        target: 0,
        sortable: true,
      },
      {
        className: "dt-nowrap",
        target: 1,
        render: comment_link,
        sortable: true,
      },
      {
        target: 2,
        sortable: false,
      },
      {
        target: 3,
        visible: false,
      },
    ]
  });
}

function comment_link( data, type, row ) {
    return `<a target="_blank" rel="noopener" href="${row[3]}">${data}</a>`;
}

// export { createTable } uh couldn't get this working
createTable();
