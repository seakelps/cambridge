import 'bootstrap'
import './stylesheets/application.sass'

$(document).ready(function() {
  $('[data-toggle="popover"]').popover();
  $('[data-toggle="tooltip"]').tooltip();
});
