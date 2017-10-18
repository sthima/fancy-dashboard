class SprintsController
  constructor: (Sprints)->
    @resource = Sprints
    @loaded = false
    @issues = @resource.query()
    @issues.$promise.then(=> @loaded = true)
    @columns = [
      "Open",
      "WIP",
      "Review",
      "Validation",
      "Done",
    ]


SprintsController.$inject = [
  "Sprints",
]

angular.module("fancyDashboard")
  .controller 'SprintsController', SprintsController
