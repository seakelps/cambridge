/* global: LOGGED_IN */


/* Cookie handler from https://docs.djangoproject.com/en/1.11/ref/csrf/ */

const csrftoken = $("[name=csrfmiddlewaretoken]").val();
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

$('#candidateRankerSidebar').slideReveal({
  overlay: true,
  push: false,
  position: "right",
  trigger: $("#rankCandidates")
});

$("#candidateRankerSidebar .close").click(function() {
  $("#candidateRankerSidebar").slideReveal("hide")
});

$('#candidateRankerSidebar').slideReveal("show");


/* Within sidebar lists */
class Candidate {

}


class Sidebar {
  addCandidate(candidate) {
    // Add candidate to "on" list
    this.candidates.push(candidate);
  }

  updateFromResponse(candidates) {
    // Update full data structure from server data
    const sidebar = this;

    if (sidebar.pollingId) {
      // stop polling while updating
      clearInterval(sidebar.pollingId);
      sidebar.pollingId = undefined;
    }
    sidebar.serverUpdate(true);

    let replacement = candidates.map(slug => {
      return sidebar.allCandidates.find(c => c.slug == slug)
    })

    // knockout will trigger update even if nothing's changed, but that screws up the draggable
    if (!_.isEqual(sidebar.candidates(), replacement)) {
      console.log('replacing');
      sidebar.candidates(replacement);
    }

    sidebar.serverUpdate(false);
    sidebar.startPolling();
  }

  startPolling() {
    // refresh from server every 1 second
    const sidebar = this;

    // returns id of interval for later cancelling
    sidebar.pollingId = setInterval(() => sidebar.loadFromServer(), 1000);
  }

  save(new_value) {
    /* save list ordering */
    const sidebar = this;
    if (LOGGED_IN) {
      $.post({
        url: "/ranking/mine/",
        data: {
          candidates: new_value.map(x => x.slug).join(',')
        },
      }).done(function(response){
        sidebar.updateFromResponse(response.candidates)
      });
    } else {
      localStorage.setItem('candidateList', JSON.stringify((
        new Date(),
        new_value.map(x => x.slug)
      )));
    }
  }

  loadFromServer() {
    const sidebar = this;

    if (LOGGED_IN) {
      return $.get({
        url: "/ranking/mine/",
        ifModified: true,
      }).done(function(response, status){
        // don't update when not modified
        if (status == "success") {
          sidebar.updateFromResponse(response.candidates);
        }
      });
    } else {
      let candidates;
      try {
        candidates = JSON.parse(localStorage.getItem('candidateList'));
      } catch(err) {

      }

      if (!candidates) {
        candidates = [];
      }

      // triggers update regardless of whether there is a change for now
      sidebar.updateFromResponse(candidates);
    }
  }

  constructor() {
    const sidebar = this;
    sidebar.allCandidates = allCandidates;

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

    this.startPolling();
  }
}

var view_model = new Sidebar();
