app = angular.module "fancyDashboard", ["ngResource", "ui.router"]

app.config ($stateProvider) ->
  $stateProvider.state
    name: 'pullrequests'
    url: '/pullrequests'
    templateUrl: "/static/angular/partials/pullrequests.html"
  return
    # .when "/releases",
    #   templateUrl: "/static/angular/partials/releases.html"
