import marked from 'marked'
import { debounce } from 'lodash'


function childText( d ) {
    /* text (can be html) for foldout row when main row is clicked */
    if (d.aceladescription) {
      return `<h5>${d.resolutionshorttitle} (<a target="_blank" rel="noopener" href="http://cambridgema.iqm2.com/Citizens/Detail_LegiFile.aspx?ID=${d.resolutionid}">view</a>)</h5>` + marked(d.aceladescription);
    } else {
      return ''; // otherwise .show() fails
    }
}

function make_vote_split( d ) {
    let councillors = ["dennis_carlone", "jan_devereux", "craig_kelley", "alanna_mallon", "marc_mcgovern", "sumbul_siddiqui", "denise_simmons", "tim_toomey", "quinton_zondervan"];

    for (let i = 0; i < councillors.length; i++) {
        if (d[councillors[i]] == 'Present' || d[councillors[i]] == 'Nays') {
            return 'contested';
        }
    }

    return 'unanimous';
}

function as_date(d) {
    return (new Date(d)).toLocaleDateString();
}

function vote( data, type, row ) {
    data = data || "";
    return `<span class=${data.replace(" ", "_")}>${data.replace(/s$/, "")}</span>`;
}

function searchValue() {
    return $("#voteSearch").val().split(/\s+/).map($.trim);
}

function markOpenChildren() {
  let search_value = searchValue();
  this.api().rows({ page: "current" }).every(function() {
    if (this.child()) { // if folded out
      if (val.length == 0) {
        // otherwise we leave the last mark() around
        this.child().unmark();
      } else {
        // had some trouble going from $ to $4 without unmarking, but other searches seem to have worked
        this.child().unmark();
        this.child().mark(search_value);
      }
    }
  });
}

function createTable(voter_file_url) {
  var dt;

  $.fn.dataTable.ext.search.push(
    function( settings, data, dataIndex ) {
      var vote_split = $("[name=vote-split]:checked").val();
      if (vote_split == 'all') {
        return true;
      } else {
        // 'vote_split:name', must be a searchable field or else this gets no value
        return data[4] == vote_split;
      }
    }
  );

  dt = $('#myTable').DataTable( {
    mark: true,
    ajax: voter_file_url,
    searching: true,
    lengthChange: false,
    order: [[ 0, "desc" ]],
    // drawCallback: markOpenChildren,
    columns: [
      { data: "resolutionid", visible: false },
      { orderable: false, data: "full_text", visible: false },
      { render: as_date, width: "10ch", orderable: true, data: "meetingdate", visible: true },

      { orderable: false, data: "resolutionshorttitle",  },
      { searchable: true, visible: false, orderable: false, name: "vote_split", data: make_vote_split },

      { render:vote, searchable: false, data: "dennis_carlone", title: "Carlone" },
      { render:vote, searchable: false, data: "jan_devereux", title: "Devereux" },
      { render:vote, searchable: false, data: "craig_kelley", title: "Kelley" },
      { render:vote, searchable: false, data: "alanna_mallon", title: "Mallon" },
      { render:vote, searchable: false, data: "marc_mcgovern", title: "McGovern" },
      { render:vote, searchable: false, data: "sumbul_siddiqui", title: "Siddiqui" },
      { render:vote, searchable: false, data: "denise_simmons", title: "Simmons" },
      { render:vote, searchable: false, data: "tim_toomey", title: "Toomey" },
      { render:vote, searchable: false, data: "quinton_zondervan", title: "Zondervan" }
    ],
  } );

  window.dt = dt;

  $('#myTable tbody').on( 'click', 'tr[role=row]', function () {
    /* toggle child row visibility */
    var tr = $(this);
    var row = dt.row( tr );

    if ( row.child.isShown() ) {
      tr.removeClass( 'details' );
      row.child.hide();
    }
    else {
      tr.addClass( 'details' );
      row.child( childText( row.data() ) ).show();
      row.child().mark(searchValue());
    }
  } );

  /* table-responsive must wrap the table, but data-tables adds a div
       before and after the table, so we have to do this after DataTables is
       applied so the table controls don't also scroll */
  $("#myTable").wrap("<div class='table-responsive'></div>");

  $("[name=vote-split]").on("change", () => dt.draw());

  let searchTable = debounce(function(val) {
    // .columns([x, y]).search() must match all columns and .search()
    // matches any but we need vote_split to be searchable too, so
    // using a hidden concat column
    dt.columns(1).search(val).draw();
  }, 250, { "leading": false });

  $("#voteSearch").on("input", function() {
    let val = $.trim( $(this).val() );
    searchTable(val);
  });

  $("[data-toggle=tooltip]").tooltip();
}

export { createTable }
