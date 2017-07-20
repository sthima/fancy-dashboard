class DashboardToolbarController
  constructor: (@$state, @$timeout)->
    @rotateSlice = [
      'pullrequests',
      'releases',
    ]
    @rotateTime = '30'
    @currentState = -1
    @setNextRotation()

  getRotateTime: =>
    new Number(@rotateTime)

  rotateState: =>
    @currentState = @currentState + 1
    if @currentState >= @rotateSlice.length
      @currentState = 0
    console.log("Rotating to: #{@rotateSlice[@currentState]}")
    @$state.transitionTo(@rotateSlice[@currentState])
    @setNextRotation()

  setNextRotation: =>
    console.log("Next rotation in: #{@getRotateTime()} seconds")
    @$timeout(@rotateState, @getRotateTime() * 1000)




DashboardToolbarController.$inject = [
  "$state",
  "$timeout",
]

angular.module("fancyDashboard")
  .controller 'DashboardToolbarController', DashboardToolbarController
