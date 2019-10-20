// Include bootstrap 4
// -----------------------------------------------------------------------------
import tether from 'tether';
window.Tether = tether;
const bootstrap = require('bootstrap');

// General Angular 1.5 App
// -----------------------------------------------------------------------------
import angular from 'angular';

// Project modules
// -----------------------------------------------------------------------------

angular
  .module('pycones', [

  ])
  .config(['$httpProvider', '$interpolateProvider', ($httpProvider, $interpolateProvider) => {
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
  }]);


// Extra scripts
// -----------------------------------------------------------------------------
import $ from 'jquery';

$(document).ready( () => {
  $(".js-slot-expand").on("click", (event) => {
    let _this = event.target;
    if ($(event.target).hasClass("fa")) {
      _this = $(event.target).parent();
    }
    let description = $("#slot-description-" + $(_this).data("slot"));
    description.fadeToggle();
    let ad = $(_this).find(".fa-angle-down");
    let au = $(_this).find(".fa-angle-up");
    if (ad.length > 0) {
        ad.removeClass("fa-angle-down");
        ad.addClass("fa-angle-up");
    }
    if (au.length > 0) {
        au.addClass("fa-angle-down");
        au.removeClass("fa-angle-up");
    }
  });
});
