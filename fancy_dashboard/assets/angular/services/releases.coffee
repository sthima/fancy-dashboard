class Releases
  constructor: ($resource) ->
    @api = $resource '/dashboard/releases/',

  query: (group_id)->
    @api.query()

Releases.$inject = [
  '$resource',
]

angular.module("fancyDashboard")
  .service 'Releases', Releases
