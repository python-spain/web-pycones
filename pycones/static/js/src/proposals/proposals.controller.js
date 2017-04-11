
// Controller for the speakers widget, used in the creation
// of a new proposal.
class SpeakersController {

  constructor($scope) {
    this.scope = $scope;
  }

  $onInit() {
    // List of speakers
    this.speakers = [];
    this.speakersSerialized = "";
    if (this.value !== undefined && this.value !== "None" && this.value !== "" ) {
      this.speakersSerialized = this.value;
      this.speakers = JSON.parse(this.value);
    } else {
      // Adds new speaker
      this.addNewSpeaker();
    }
    // Watch changes on speakers
    this.scope.$watch("$ctrl.speakers", (value) => {
      this.serializeSpeakers();
    }, true);
  }

  addNewSpeaker() {
    this.speakers.push({name: "", email: ""});
  }

  deleteSpeaker(index) {
    this.speakers.splice(index, 1);
  }

  serializeSpeakers() {
    this.speakersSerialized = JSON.stringify(this.speakers);
  }

}

SpeakersController.$inject = ['$scope'];

export {SpeakersController};
