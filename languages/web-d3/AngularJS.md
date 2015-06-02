"The scope is not the model, the scope refers to the model"
"Whenever you have ng-model there’s gotta be a dot in there somewhere. If you don’t have a dot, you’re doing it wrong"
  -> Miško Hevery’s talk on AngularJS Best Practices

"Use the scope option to create isolate scopes when making **components** that you want to **reuse** throughout your app."

    var scope = $('div.vboardPinboard').scope()
    $('div.vboardPinboard').controller()
    scope.$$watchers // useful to debug ng-repeat perf issues

    var injector = $(document.body).injector()
    injector.get('serviceName')

http://www.thoughtworks.com/insights/blog/using-page-objects-overcome-protractors-shortcomings

ui-router debug: http://tech.endeepak.com/blog/2014/05/03/debugging-angular-ui-router/

One-time bindings: {{::color}}
.on() -> .one() // Once lony !

href="javascript:$.noop"

    var deferred = $q.defer();
    deferred.promise.then(function () {
        throw new Error('then: DAMN! ' + arguments); // Will be logged in chrome console, AND be caught below
    }).catch(function () {
        console.log('FAILURE', arguments);
    });
    deferred.resolve();
    //deferred.reject(new Error('REJECTED'));
