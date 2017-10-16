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

var view_model = new function() {
  var self = this;
  self.allCandidates = allCandidates;
  self.trash = ko.observableArray(["Drag here to delete"]);

  // Using this to avoid re-saving from server update. Couldn't find a better way
  self.serverUpdate = ko.observable(false);
  self.selectedCandidate = ko.observable();
  self.selectedCandidate.subscribe((new_value) => {
    // also gets triggered on clearing the input
    if (new_value) {
      self.addCandidate(new_value);
    }
  })

  self.candidates = ko.observableArray()
  self.candidates.subscribe(new_value => {
    if (!self.serverUpdate()) {
      self.save(new_value);
    }
  });

  self.remainingCandidates = ko.computed(() => {
    let candidates = [];
    for (candidate of self.allCandidates) {
      if (!self.candidates().find(x => x.slug == candidate.slug)) {
        candidates.push(candidate);
      }
    }
    return candidates;
  });

  self.addCandidate = function(candidate) {
    self.candidates.push(candidate);
  };

  self.updateFromResponse = function(candidates) {
    if (self.pollingId) {
      clearInterval(self.pollingId);
      self.pollingId = undefined;
    }
    self.serverUpdate(true);

    let replacement = candidates.map(slug => {
			return self.allCandidates.find(c => c.slug == slug)
    })

    // knockout will trigger update even if nothing's changed, but that screws up the draggable
    if (!_.isEqual(self.candidates(), replacement)) {
      console.log('replacing');
      self.candidates(replacement);
    }

    self.serverUpdate(false);
    self.startPolling();
  };

  // refresh from server every 1 second
  self.startPolling = function() {
    // returns id of interval
    self.pollingId = setInterval(() => {
      self.loadFromServer();
    }, 1000);
  }

  self.save = function(new_value) {
    if (LOGGED_IN) {
      $.post({
        url: "/ranking/mine/",
        data: {
          candidates: new_value.map(x => x.slug).join(',')
        },
      }).done(function(response){
        self.updateFromResponse(response.candidates)
      });
    } else {
      localStorage.setItem('candidateList', JSON.stringify((
        new Date(),
        new_value.map(x => x.slug)
      )));
    }
  };

  self.loadFromServer = function(){
    if (LOGGED_IN) {
      return $.get({
        url: "/ranking/mine/",
        ifModified: true,
      }).done(function(response, status){
        // don't update when not modified
        if (status == "success") {
          self.updateFromResponse(response.candidates);
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
      self.updateFromResponse(candidates);
    }
  }

  self.startPolling();
}
