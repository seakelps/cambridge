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

  // Using this to avoid re-saving from server update. Couldn't find a better way
  self.serverUpdate = ko.observable(false);

  self.candidates = ko.observableArray()
  self.candidates.subscribe(new_value => {
    if (!self.serverUpdate()) {
      self.save(new_value);
    }
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

    console.log("updating with " + candidates.join(','));
    self.candidates(candidates.map(x => {
      return {
        slug: x,
        name: x,
      }
    }));
    self.serverUpdate(false);
    self.startPolling();
  };

  self.save = function(new_value) {
    console.log("saving        " + new_value.map(x => x.slug).join(','));
    $.post({
      url: "/ranking/mine/",
      data: {
        candidates: new_value.map(x => x.slug).join(',')
      },
    }).done(function(response){
      self.updateFromResponse(response.candidates)
    });
  };

  self.loadFromServer = function(){
    return $.get({
      url: "/ranking/mine/",
      ifModified: true,
    }).done(function(response, status){
      // don't update when not modified
      if (status == "success") {
        self.updateFromResponse(response.candidates);
      }
    });
  }

  self.loadFromServer();

  // refresh from server every 1 second
  self.startPolling = function() {
    // returns id of interval
    self.pollingId = setInterval(() => {
      console.log('ping');
      self.loadFromServer();
    }, 1000);
  }
}


/* Add button */

$("#addCandidate").chosen({
  width: "100%",
  // inherit_select_class: true,
  classes: "btn btn-primary",
}).change(function(_event, selected) {
  view_model.addCandidate({
    slug: selected.selected,
    name: selected.selected,
  });
  $("#addCandidate").val('').trigger("chosen:updated");
});
