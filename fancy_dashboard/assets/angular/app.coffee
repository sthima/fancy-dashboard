app = angular.module "fancyDashboard", [
  "ngResource",
  "ui.router",
  "ui.bootstrap",
]

app.config ($stateProvider) ->
  $stateProvider.state
    name: 'pullrequests'
    url: '/pullrequests'
    templateUrl: "/static/angular/partials/pullrequests.html"
  $stateProvider.state
    name: 'releases'
    url: '/releases'
    templateUrl: "/static/angular/partials/releases.html"
  return
