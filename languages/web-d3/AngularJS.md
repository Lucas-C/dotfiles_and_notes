"The scope is not the model, the scope refers to the model"
"Whenever you have ng-model there's gotta be a dot in there somewhere. If you don't have a dot, you're doing it wrong"
  -> Misko Hevery's talk on AngularJS Best Practices

"Use the scope option to create isolate scopes when making **components** that you want to **reuse** throughout your app."

    var scope = angular.element($('div.vboardPinboard')).scope()
    var $rootScope = angular.element(document.body).scope() // if <body> has the 'ng-app' attribute
    angular.element($('div.vboardPinboard')).controller()
    scope.$$watchers // useful to debug ng-repeat perf issues

    var injector = angular.element(document.body).injector()
    injector.get('serviceName')

http://www.thoughtworks.com/insights/blog/using-page-objects-overcome-protractors-shortcomings

ui-router debug: http://tech.endeepak.com/blog/2014/05/03/debugging-angular-ui-router/

One-time bindings: {{::color}}
.on() -> .one() // Once lony !

href="javascript:$.noop"

    var deferred = $q.defer();
    deferred.promise.then(function (input) {
        throw new Error(input); // Will be logged in chrome console, AND be caught below
        return 'INITIAL PROMISE OK: ' + input;
    }).catch(function (error) {
        console.log('ERROR', error);
        return 'ERROR CAUGHT: ' + error;
    }).then(function (result) {
        console.log('END RESULT:', result);
    });
    deferred.resolve('START');
    //deferred.reject(new Error('REJECTED'));

Returning several values from `then` (so that you can chain it with `then(function (a, b) {...})`):

    }).then(function (data) {
        return $q(function (resolve) { resolve(data[0], data[1]); });
    }).then (function (d0, d1) { ...


Testing $resource-based services (from http://stackoverflow.com/a/18523642/636849) using jasmine-jquery to load fixtures without $http:

    describe("MyServiceTest", function () {
        jasmine.getJSONFixtures().fixturesPath = 'base/src/test/specs/testdata/';

        beforeEach(module('myApp'));

        var $httpBackend, MyService;
        beforeEach(inject(function ($injector) {
            $httpBackend = $injector.get('$httpBackend');
            MyService = $injector.get('MyService');
        }));

        it("can query the backend", function (done) {
            $httpBackend.whenGET('/offers').respond(getJSONFixture('all_offers.json'));
            NsrOffersService.getAllOffers().then(function (offers) {
                expect(offers.length).toEqual(12);
                done();
            });
            $httpBackend.flush();
        });
    });

With only jQuery:

    var $httpBackend, NsrOffersService, allTestOffers, someSpecificTestOffers;
    beforeEach(function (done) {
        module('myApp');

        inject(function ($injector) {
            $httpBackend = $injector.get('$httpBackend');
            MyService = $injector.get('MyService');
        });

        // Loading fixtures
        $.when(
            $.getJSON('base/src/test/specs/testdata/all_offers.json', function (data) { allTestOffers = data; }),
            $.getJSON('base/src/test/specs/testdata/some_specific_offers.json', function (data) { someSpecificTestOffers = data; })
        ).then(done);
    });


### Protractor

Pros: http://pascalprecht.github.io/slides/e2e-testing-with-protractor
Cons: http://googletesting.blogspot.fr/2015/04/just-say-no-to-more-end-to-end-tests.html
