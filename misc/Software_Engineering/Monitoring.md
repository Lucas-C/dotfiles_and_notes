## Service monitoring
cf. https://github.com/ripienaar/free-for-dev#monitoring

- Errors monitoring:
  * https://sentry.io : has a free plan (10k events/month, 7 days history), clients in many languages, [email notifications](https://docs.sentry.io/learn/notifications/), server is open source
  * https://rollbar.com : has a free plan (5k events/month, 30 days retention), clients in many languages, [email notifications](https://rollbar.com/blog/notification-types-how-to-use-them/#notifications-for-email), server is closed source
  * https://www.bugsnag.com : has a free plan (7.5k events/month), clients in many languages, [email notifications](https://docs.bugsnag.com/product/email/), server is closed source
- SAAS status pages:
  * https://exana.io : has a free plan, but also has limits: no HTTP API + no way to delete an incident, can only update/close it (stays public)
  * https://www.statuspage.io : [REST API doc](http://doers.statuspage.io/api/v1/incidents/)
  * https://www.sorryapp.com : [REST API doc](https://docs.sorryapp.com/api/v1/reference/pages/notices/)
  * https://status.io : [REST API doc](https://statusio.docs.apiary.io)
  * https://statusy.co : [REST API doc](https://api.statusy.co/?uid=161a00cdc946ef-0b341c9832c015-d35346d-1fa400-161a00cdc961475#create-an-incident)
- OSS status pages:
  * https://cachethq.io (PHP) -> [recipe](https://www.reddit.com/r/sysadmin/comments/6r5rzq/xpost_from_rhomelab_is_there_something_similar_to/dl304ed/) to setup a CentOS7 EC2 AMI on AWS
  * https://github.com/jayfk/statuspage (Python, using Github issues for incidents & Github Pages for hosting)
  * https://lambstatus.github.io (NodeJS, hosted on AWS Lambda)
  * https://sourcegraph.github.io/checkup/ (Go)
  * https://github.com/adamcooke/staytus (Ruby)
- active healthcheck monitoring:
  * https://healthchecks.io : "Get Notified When Your Cron Jobs Fail"
  * https://deadmanssnitch.com : "Kiss Silent Failures Goodbye"
- passive public server external monitoring:
  * https://www.checkiton.us
  * https://www.pingdom.com
  * http://www.sixnines.io
- receive notifications on mobile:
  * https://pushover.net : KISS, SAAS, not open source, the app is 5$ and that's it.
  Require a device configured, else error: "no active devices to send to"
  * http://docs.pushjet.io : open source
- distributed tracing systems & Application Performance Monitoring (APM)
  * https://sentry.io/for/javascript/ : open source, backend in Python+Django (+ Celery, PostgreSQL, Redis), easily deployable on premise with Docker, JS client: Raven
  * https://github.com/errbit/errbit : open source, in Ruby, deployable on premise
  * https://opbeat.com -> joined [Elastic APM](https://www.elastic.co/solutions/apm)
  * https://opencensus.io : backed by Google, metric collection and tracing, supports Prometheus, SignalFX, Stackdriver, Zipkin, Datadog, and Azure App Insights
  * https://github.com/apache/incubator-skywalking : distributed tracing system & APM, high performance Java agent, OpenTracing
