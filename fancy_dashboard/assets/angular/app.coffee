app = angular.module "fancyDashboard", [
  "ngResource",
  "ngAnimate",
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
  $stateProvider.state
    name: 'sprint'
    url: '/sprint'
    templateUrl: "/static/angular/partials/sprints.html"
  return
