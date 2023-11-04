import marked from 'marked'
import debounce from 'lodash/debounce'


function childText( d ) {
	/* text (can be html) for foldout row when main row is clicked */
		var child = `<h5>${d.title} (<a target="_blank" rel="noopener" href="http://cambridgema.iqm2.com/Citizens/Detail_LegiFile.aspx?ID=${d.id}">view</a>)</h5>`;
	if (d.text) {
		return child + marked(d.text);
	} else {
		return child;
	}
}

function make_vote_split( d ) {
	let councillors = [
		"dennis_j_carlone",
		"e_denise_simmons",
		"marc_c_mcgovern",
		"burhan_azeem",
		"alanna_mallon",
		"patricia_nolan",
		"paul_toner",
		"sumbul_siddiqui",
		"quinton_zondervan",
	];

	for (let i = 0; i < councillors.length; i++) {
		if (d[councillors[i]] == 'NAYS') {
			return 'contested';
		}
	}

	return 'unanimous';
}

function as_date(d) {
	if (d === null) {
		return null;
	} else {
    	return (new Date(d)).toLocaleDateString();
	}
}

function vote( data, type, row ) {
    data = data || "";
    return `<span class=${data.replace(" ", "_")}>${data.replace(/s$/, "")}</span>`;
}

function searchValues() {
    return $("#voteSearch").val().split(/\s+/).map($.trim);
}

function markOpenChildren() {
  console.log('hi');
  let search_value = $("#voteSearch").val();

  this.api().rows({ page: "current" }).every(function() {
    if (this.child()) { // if folded out
      if (search_value.length == 0) {
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
    drawCallback: markOpenChildren,
    columns: [
      { data: "id", visible: false },
      { orderable: false, data: "text", visible: false },
      {
		  title: "Date",
		  render: as_date,
		  width: "20ch",
		  orderable: true,
		  type: "date",
		  data: "date",
		  visible: true
      },

      {
		  title: "Title",
		  orderable: false,
		  data: "title"
      },
      { searchable: true, visible: false, orderable: false, name: "vote_split", data: make_vote_split },

      { render:vote, orderable: false, searchable: false, data: "dennis_j_carlone", title: "Carlone" },
      { render:vote, orderable: false, searchable: false, data: "e_denise_simmons", title: "Simmons" },
      { render:vote, orderable: false, searchable: false, data: "marc_c_mcgovern", title: "McGovern" },
      { render:vote, orderable: false, searchable: false, data: "burhan_azeem", title: "Azeem" },
      { render:vote, orderable: false, searchable: false, data: "alanna_mallon", title: "Mallon" },
      { render:vote, orderable: false, searchable: false, data: "patricia_nolan", title: "Nolan" },
      { render:vote, orderable: false, searchable: false, data: "paul_toner", title: "Toner" },
      { render:vote, orderable: false, searchable: false, data: "sumbul_siddiqui", title: "Siddiqui" },
      { render:vote, orderable: false, searchable: false, data: "quinton_zondervan", title: "Zondervan" },
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
      row.child().mark(searchValues());
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
  $('#myTable thead').addClass('thead-dark');
}

export { createTable }
