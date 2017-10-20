class Sprints
  constructor: ($resource) ->
    @api = $resource '/v1/sprint/',

  query: (group_id)->
    @api.query()

Sprints.$inject = [
  '$resource',
]

angular.module("fancyDashboard")
  .service 'Sprints', Sprints
