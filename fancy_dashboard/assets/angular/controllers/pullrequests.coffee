class PullRequestsController
  constructor: (PullRequests)->
    @resource = PullRequests
    @pullrequests = @resource.query()
    @checkAll = {}

PullRequestsController.$inject = [
  "PullRequests",
]

angular.module("fancyDashboard")
  .controller 'PullRequestsController', PullRequestsController
