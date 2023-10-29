function createTable() {
  var dt = new DataTable("#public-comment-table", {
    ordering: true,
    paging: false,
    searching: true,
    dom: "lfrtip",
    pageLength: 15,
    columnDefs: [
      { className: "dt-nowrap", targets: [ 0, 1 ] }
    ]
  });
}

// export { createTable } uh couldn't get this working
createTable();
