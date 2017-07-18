class PullRequestsController
  constructor: (PullRequests)->
    @resource = PullRequests
    @pullrequests = @resource.query()
    @checkAll = {}

  getPullRequestColor: (pull_request) ->
    now = moment new Date()
    console.log now
    last_update = moment pull_request.updated_on
    console.log last_update
    duration = moment.duration(now.diff last_update)
    console.log duration
    hours = duration.asHours()
    color = ''
    if hours > 16
      # color = '#ce3e3e'
      color = 'pullrequest-extremely-due'
    else if hours > 8
      # color = '#e8ae38'
      color = 'pullrequest-due'
    else if hours > 4
      # color = '#ede54f'
      color = 'pullrequest-very-idle'
    else if hours > 2
      # color = '#afce3e'
      color = 'pullrequests-idle'
    else
      # color = '#3cd358'
      color = 'pullrequests-created'
    color


PullRequestsController.$inject = [
  "PullRequests",
]

angular.module("fancyDashboard")
  .controller 'PullRequestsController', PullRequestsController
