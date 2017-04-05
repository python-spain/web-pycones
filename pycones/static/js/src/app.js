// Include bootstrap 4
// -----------------------------------------------------------------------------
import tether from 'tether';
window.Tether = tether;
let bootstrap = require('bootstrap');

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
