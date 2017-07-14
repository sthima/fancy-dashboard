class PullRequests
  constructor: ($resource) ->
    @api = $resource '/dashboard/pullrequests/',

  query: (group_id)->
    @api.query()

PullRequests.$inject = [
  '$resource',
]

angular.module("fancyDashboard")
  .service 'PullRequests', PullRequests
