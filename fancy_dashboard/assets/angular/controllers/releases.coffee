class ReleasesController
  constructor: (Releases)->
    @resource = Releases
    @releases = @resource.query()

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
