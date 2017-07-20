class ReleasesController
  constructor: (Releases)->
    @resource = Releases
    @loaded = false
    @releases = @resource.query()
    @releases.$promise.finally(=> @loaded = true)


  getIssuesCount: (release) ->
    issuesCount = 0
    for release_status in release.statuses
      issuesCount = issuesCount + release_status.count
    issuesCount

ReleasesController.$inject = [
  "Releases",
]

angular.module("fancyDashboard")
  .controller 'ReleasesController', ReleasesController
