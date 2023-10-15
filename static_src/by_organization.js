function createTable() {
  $.fn.dataTable.Buttons.defaults.dom.button.className = 'btn btn-light';
  $.fn.dataTable.Buttons.defaults.dom.split.action.className = 'btn btn-light';
  $.fn.dataTable.Buttons.defaults.dom.split.dropdown.className = 'btn btn-light';
  $.fn.dataTable.Buttons.defaults.dom.container.className = 'btn-group-toggle';

  var dt = new DataTable("#myTable", {
    ordering: false,
    paging: false,
    searching: false,
    buttons: [
      {
        extend: 'spacer',
        style: "d-block h5",
        text: 'Local Organizations'
      },
      {
        extend: "columnsToggle",
        columns: ".col-local-organization",
      },
      {
        extend: 'spacer',
        style: 'd-block h5',
        text: 'Unions'
      },
      {
        extend: "columnsToggle",
        columns: ".col-union-organization",
      },
      {
        text: "All Unions",
        extend: "columnToggle",
        columns: ".col-union-organization",
      },
      {
        extend: 'spacer',
        style: 'd-block h5',
        text: 'Other'
      },
      {
        extend: "columnsToggle",
        columns: ".col-organization",
      },
    ],
    dom: "<'#filterBar.py-4'B>t",
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
        visible: true,
        render: (data, type, row) => {
          return `<a href=${row[2]}>${data}</a>`;
        }
      },
      {
        // detail url
        targets: [2],
        visible: false,
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
        // first few organizations
        targets: [3, 4, 5],
        visible: true,
      },
      {
        // rest of organizations
        targets: "_all",
        visible: false,
      },
    ],
  });

  $("#filterBar").prepend("<label>Click an organization below to show or hide their endorsements in the table.</label>");

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
