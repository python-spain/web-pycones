import { SpeakersController } from "./proposals.controller"


let speakersTemplate = [
      '<div>',
        '<input id="[[$ctrl.fieldId]]" name="[[$ctrl.fieldName]]" type="hidden" value=\'[[$ctrl.speakersSerialized]]\'>',
        '<div class="row" ng-repeat="speaker in $ctrl.speakers">',
          '<div ng-class="{\'col-12\': $index == 0, \'col-11\': $index != 0}">',
            '<input type="text" ng-model="speaker.name" placeholder="[[$ctrl.nameLabel]]" class="form-control" style="margin-bottom: 5px">',
            '<input type="email" ng-model="speaker.email" placeholder="[[$ctrl.emailLabel]]" class="form-control" style="margin-bottom: 5px">',
          '</div>',
          '<div class="col-1" ng-hide="$index == 0">',
            '<a href="javascript:void(0);" ng-click="$ctrl.deleteSpeaker($index)" aria-hidden="true">&times;</a>',
          '</div>',
        '</div>',
        '<div class="row">',
          '<div class="col-12">',
            '<a href="javascript:void(0);" ng-click="$ctrl.addNewSpeaker()">[[$ctrl.addMoreLabel]]</a>',
          '</div>',
        '</div>',
      '</div>'
    ].join('');

const SpeakersComponent = {
  controller: SpeakersController,
  template: speakersTemplate,
  bindings: {
    value: '@',
    fieldName: '@',
    fieldId: '@',
    addMoreLabel: '@',
    nameLabel: '@',
    emailLabel: '@',
  }
};

export {SpeakersComponent};
