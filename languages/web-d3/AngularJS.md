# Angular 2

Config injection:

    @Injectable()
    export class AppConfig {
        endpointUrl: string;

        constructor(private http: Http) {}

        public load() {
            return this.http.get("config.json").toPromise().then(response => {
                let config = response.json();
                this.endpointUrl = config.endpointUrl;
            });
        }
    }

And in `app.module.ts` :

    @NgModule({
        ...
        providers: [AppConfig, { provide: APP_INITIALIZER, useFactory: (config: AppConfig) => () => config.load(), deps: [AppConfig], multi: true }]
    })

Console debug:

    ng.probe($0).componentInstance


# Angular 1.5

http://aosabook.org/en/500L/web-spreadsheet.html : demonstrate interesting ES6 features
- redirect-based graceful degradation to ES5
- `ng-model="sheet[col+row]" ng-change="calc()" ng-model-options="{debounce: 200}" ng-keydown="keydown($event, col, row)`
- `$scope.keydown = ({which}, col, row)=> { ...` : destructuring assignment to assign `$event.which` into the `which` parameter
- `function* range(cur, end) { while (cur <= end) { yield cur; cur++; } }`
- `#${ col }${ row + direction }` : template string
- web worker : why ? sandboxing + user can continue to navigate without getting blocked by computation in the main thread

"The scope is not the model, the scope refers to the model"
"Whenever you have ng-model there's gotta be a dot in there somewhere. If you don't have a dot, you're doing it wrong"
  -> Misko Hevery's talk on AngularJS Best Practices

"Use the scope option to create isolate scopes when making **components** that you want to **reuse** throughout your app."

    var scope = angular.element($0).scope()
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

    $interpolate('Hello {{name | uppercase}}!')({name:'Angular'})

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

    angular.module('myApp').factory('MyAppNavigationHistory', function ($location, $rootScope) {
        var navigationHistory = {
            visited: []
        };
        $rootScope.$on('$locationChangeSuccess', function () {
            navigationHistory.visited.push($location.url());
        });
        navigationHistory.lastStuffUrlVisited = function () {
            return _.last(navigationHistory.visited.filter(function (url) {
                return _.startsWith(url, '/stuff');
            }));
        };
        return navigationHistory;
    });

    /* Enabled with $httpProvider.interceptors.push('NsrErrorInterceptor');
     * The .disableErrorInterceptor flag makes it possible to define $resources that don't trigger the error interceptor:
     * var MyCrudResource = $resource(MY_API_ENDPOINT + '/path/:id/something', {}, {
     *     getWithoutErrorInterceptor: { method: 'GET',  disableErrorInterceptor: true},
     * });
     */
    angular.module('myApp').factory('MyAppErrorInterceptor', function ($q, $location) {
        return {
            responseError: function (rejection) {
                if (rejection.config && !rejection.config.disableErrorInterceptor && rejection.config.url.indexOf(MY_API_ENDPOINT) === 0) {
                    $location.path('/error/' + rejection.status);
                }
                return $q.reject(rejection);
            }
        };
    });


### Protractor

Pros: http://pascalprecht.github.io/slides/e2e-testing-with-protractor
Cons: http://googletesting.blogspot.fr/2015/04/just-say-no-to-more-end-to-end-tests.html

Debug: `protractor debug conf.js` cf. "Using debugger" -> https://github.com/angular/protractor/blob/master/docs/debugging.md#pausing-to-debug
