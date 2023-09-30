function createTable() {
  var dt = new DataTable("#myTable", {
    paging: false,
    searching: false,
    info: false,
    ordering: false,
    columnDefs: [
      {
        targets: 0,
        visible: false,  // not yet done
        render: (data, type, row) => {
          return `
            <a class="btn btn-dark btn-sm" href="${data}">
              <i class="fa fa-plus"></i>
            </a>`;
        }
      },
      {
        targets: 1,
        render: (data, type, row) => {
          return `<a href=${row[2]}>${data}</a>`;
        }
      },
      {
        targets: "col-organization",
        render: (data, type, row) => {
          switch (data) {
            case "True": 
              return '<i class="fa fa-check text-success"></i>';
            case "False": 
              return '<i class="fa fa-ban text-danger"></i>';
            default: 
              return value;
          }
        },
      },
      {
        // detail url
        targets: [2],
        visible: false,
      },
    ],
  });

  document.querySelectorAll('#org-toggle > label').forEach((el) => {
    el.addEventListener('click', function (e) {
      e.preventDefault();

      let columnName = e.target.getAttribute('data-column');
      let column = dt.column(`:contains("${columnName}")`);

      // Toggle the visibility
      column.visible(!column.visible());
    });
  });

  window.dt = dt;

  /* table-responsive must wrap the table, but data-tables adds a div
       before and after the table, so we have to do this after DataTables is
       applied so the table controls don't also scroll */
  $("#myTable").wrap("<div class='table-responsive'></div>");

  $("[data-toggle=tooltip]").tooltip();
}

export { createTable }
