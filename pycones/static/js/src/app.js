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
import Proposals from './proposals';

angular
  .module('pycones', [
    Proposals.name
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
    let description = $("#slot-description-" + $(event.target).data("slot"));
    description.fadeToggle();
    let ad = $(event.target).find(".fa-angle-down");
    let au = $(event.target).find(".fa-angle-up");
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
