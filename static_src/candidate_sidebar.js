/* global: allCandidates */
import { isEqual } from 'underscore'

/* Cookie handler from https://docs.djangoproject.com/en/1.11/ref/csrf/ */
var csrftoken;

ko.bindingHandlers.sortable.strategyMove = true;

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});


/* Slider reveal logic */
$(document).ready(function() {
  csrftoken = $("[name=csrfmiddlewaretoken]").val();
  view_model.loadFromServer();

  $('#candidateRankerSidebar').slideReveal({
    overlay: true,
    push: false,
    position: "right",
    trigger: $("#rankCandidates,#grippy"),
    show: function() {
      $("#candidateRankerSidebar").css("visibility", "visible");
      view_model.startPolling();
    },
    hide: function() { view_model.stopPolling(); },
  });

  $("#candidateRankerSidebar .close").click(function() {
    $("#candidateRankerSidebar").slideReveal("hide")
  });
});


/* Within sidebar lists */
class Candidate {
  constructor(candidate, sidebar) {
    this.sidebar = sidebar;
    this.slug = candidate.slug;
    this.name = candidate.name;
    this.blurb = candidate.blurb;
    this.img_url = candidate.img_url;
    this.img_alt = candidate.img_alt;

    this.comment = ko.observable(candidate.comment);  // TODO should this already be observable?

    // was hoping to imply the order by position in array, but I think this
    // will be easier
    this.order = ko.observable(candidate.order);  // TODO should this already be observable?
  }

  updateComment() {
    var candidate = this;
    $.post({
      url: `/ranking/notes/${candidate.slug}/`,
      data: { comment: candidate.comment() },
    }).done(function() {
      $(`#candidate_${candidate.slug} .modal`).modal("hide");
    }).fail(function() {
      alert("Couldn't save");
    });
  }

  remove() {
    const candidate = this;

    if (confirm("Deleting is permanent. Delete this note and rank?")) {
      $(".commentModal.in").modal("hide");
      // hack due to knockout changing containing element
      $('body').removeClass('modal-open');
      $('.modal-backdrop').remove();

      return $.post({
        url: `/ranking/delete/${candidate.slug}/`,
      }).done(function(response, status){
        candidate.sidebar.loadFromServer();
      });
    }
  }
}


class Sidebar {
  addCandidate(candidate) {
    // Add candidate to "on" list
    this.candidates.push(candidate);
  }

  updateFromResponse(candidates) {
    // Update full data structure from server data
    const sidebar = this;

    // stop polling while updating
    sidebar.stopPolling();
    sidebar.serverUpdate(true);

    let replacement = candidates.map(slug => {
      return sidebar.allCandidates.find(c => c.slug == slug)
    })

    // knockout will trigger update even if nothing's changed, but that screws up the draggable
    if (!isEqual(sidebar.candidates(), replacement)) {
      console.log('replacing');
      sidebar.candidates(replacement);
    }

    sidebar.candidates().forEach(function(candidate, order) {
      candidate.order(order + 1);
    })

    sidebar.serverUpdate(false);
    sidebar.startPolling();
  }

  startPolling() {
    // refresh from server every 1 second
    const sidebar = this;

    // returns id of interval for later cancelling
    sidebar.pollingId = setInterval(() => {
      if (!document.hidden) {
        sidebar.loadFromServer()
      }
    }, 1000);
  }

  stopPolling() {
    const sidebar = this;
    if (sidebar.pollingId) {
      clearInterval(sidebar.pollingId);
      sidebar.pollingId = undefined;
    }
  }

  save(new_value) {
    /* save list ordering */
    const sidebar = this;
    $.post({
      url: "/ranking/mine/",
      data: {
        candidates: new_value.map(x => x.slug).join(',')
      },
    }).done(function(response){
      sidebar.updateFromResponse(response.candidates)
    });
  }

  loadFromServer() {
    const sidebar = this;

    return $.get({
      url: "/ranking/mine/",
      ifModified: true,
    }).done(function(response, status){
      // don't update when not modified
      if (status == "success") {
        sidebar.updateFromResponse(response.candidates);
      }
    });
  }

  constructor() {
    const sidebar = this;

    sidebar.allCandidates = allCandidates.map(x => new Candidate(x, sidebar));

    // Using this to avoid re-saving from server update. Couldn't find a better way
    sidebar.serverUpdate = ko.observable(false);
    sidebar.selectedCandidate = ko.observable();
    sidebar.selectedCandidate.subscribe((new_value) => {
      // also gets triggered on clearing the input
      if (new_value) {
        sidebar.addCandidate(new_value);
      }
    })

    sidebar.candidates = ko.observableArray()
    sidebar.candidates.subscribe(new_value => {
      if (!sidebar.serverUpdate()) {
        sidebar.save(new_value);
      }
    });

    sidebar.remainingCandidates = ko.computed(() => {
      let candidates = [];
      for (let candidate of sidebar.allCandidates) {
        if (!sidebar.candidates().find(x => x.slug == candidate.slug)) {
          candidates.push(candidate);
        }
      }
      return candidates;
    });
  }
}

const view_model = new Sidebar();
export default view_model;
