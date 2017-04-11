import angular from 'angular';

import {SpeakersComponent} from  './proposals.component';


// Proposals module
const proposals = angular
  .module('proposals', [])
  .component('speakers', SpeakersComponent);

export default proposals;

