[Software development is a collaborative game](http://blog.codinghorror.com/software-development-as-a-collaborative-game/)

## References
- [MVB] : [Miniumn Viable Bureaucracy](https://speakerdeck.com/lauraxt/minimum-viable-bureaucracy-june-2014-edition)
- [GoodAtOps] : [How to be Good at Ops in 40min](https://adamhjk.github.io/good-at-ops/#/8)
- [ShittyDashboards](http://attackwithnumbers.com/the-laws-of-shitty-dashboard)
- [DieScrum] : [Why Scrum Should Basically Just Die In A Fire](http://gilesbowkett.blogspot.com.au/2014/09/why-scrum-should-basically-just-die-in.html)
- [5EPSQ] : [Five essential phone screen questions](https://sites.google.com/site/steveyegge2/five-essential-phone-screen-questions)
- [PostMortems101](http://tech.blog.box.com/2014/08/a-tale-of-postmortems/)
- [InfiniteHows](http://radar.oreilly.com/2014/11/the-infinite-hows.html)
- [IT Change Management](http://stephaniekdean.wordpress.com/2011/06/17/cm/)
- [Event Management](http://stephaniekdean.wordpress.com/2011/04/04/eventmgmt/)
- [AuthoringStyleGuide](https://github.com/tooling/authoring-styleguide)
- [TeachDontTell](http://stevelosh.com/blog/2013/09/teach-dont-tell/)
- [BeautifulDocs](https://github.com/PharkMillups/beautiful-docs)
- [WriteTheDocs](http://docs.writethedocs.org)
- [WhatToWrite](http://jacobian.org/writing/what-to-write/)
- [FrontendJobInterviewQuestions](https://github.com/h5bp/Front-end-Developer-Interview-Questions)
- [#gamedev Lead Quick Start Guide](http://web.archive.org/web/20140701034212/http://www.altdev.co/2013/11/05/gamedev-lead-quick-start-guide/)
- [What happens when you type google.com into your browser and press enter?](https://github.com/alex/what-happens-when)

## Joining a new team
- talk to a colleague each day (but not for too long, and schedule it) and question him on what he does
- take notes in a file, complete/fix the existing docs & draw diagrams
- quickly get a short-term goal to focus on & follow the 'minimal info' loop:
    * Acquire as little information as possible
    * Acquire information as efficiently as possible
    * Use the information you acquire as effectively as possible
- ask people to have lunch with them (force yourself !)
- ask people for coffee breaks (force yourself !)
- hang cheat-sheets in home toiles to learn stuff

## Leadership
cf. [#gamedev Lead Quick Start Guide]

## Team culture building
- two main tenets: RESPECT & TRUST people.
How to build trust ? Start by trusting others, be trustworthy, build relationships + it takes time [MVB]
- write down team tenets as guidelines for priorities
- define clear team goals with deadlines
- build a team brand: catching name, logo, slogan... [PP]
- small is good: 2-pizzas team
- make decisions based on data
- allocate some hack time
- rotate unwanted responsabilities [MVB]
- whiteboard sessions
- coding style reference, tools to enforce it, code reviews
- regular emails with tips. Or put a one-pager in the toilets, as Google is doing

## Stand-up & meetings
It mush be SHORT (<15min), everybody has to be ponctual, actually **stand-up**, **listen** and **be concise** : [DieScrum]
- What did you do yesterday?
- What are you doing today?
- What is blocking your progress?
- What are your commitments for the week / progression / changes due to blockers or higher priorities

In general, limit meetings by making them informal chats or doing them properly: agenda (skip if empty), few participants, time-boxed, clustered on some days in the week, take notes & record team decisions [MVB]

## Design
- interface design + decoupling >>more critical>> component design [MVB]
- start from a POC / MVP. [MVB]: "come with code" -> proof of concept + momentum + build motivation
- + Diagrams !

## Define team metrics
- customer satisfaction
- performance, output data quality
- availability : measured from the client side
- latency
- to fight it and encourage people reducing it, properly measure the technical debt: time & effort to repair; impact frequency, severity & reach; error rates; capacity/headroom

## Ops
![](http://blog.sei.cmu.edu/assets/content/Traceability-Model.png)

- "**Empathy** allows software makers and operators to help each other deliver the best possible functionality and operability on behalf of their customers." [Katherine Daniels](http://devopsdays.org/events/2014-minneapolis/proposals/Devops%20Is%20Dead/)
- monitor everything ! CPU, openFD, procCount... For services: throughput + delay + completness (% of potential src data processed). And store historical data !
- zero config: config is hard to document, hard to update, hard to set up, its persistent state can overlaps with other data
- emails are evil: no guarantee it will be actioned + no guarantee anyone is subscribed + sense of false security as it works from time to time
- when an alarm is raised, alerting tools should give a maximum of *context* on the system state and what triggered it
- prioritize identifying the root cause of an issue and resolving it
- hold weekly/monthly ops review meetings, including:
    * highlights from previous on-call shift: high severity events, metrics...
    * this week's priorities: deployments, hand-over of burning tickets or tickets failing over SLA
- frequently determine operational excellence goals: eliminate the top root cause of tickets, create a runbook/dashboard for a service...
- CMs: cf. [IT Change Management]
- post-mortems, event management & establishing new processes: cf. [PostMortems101] & [Event Management]
Learning is the goal during post-mortems + questiosn examples : [InfiniteHows]
- use a chatbot for real time alerts

## Documentation:
- Tenets:
    * the key challenge to sustaining a complex system is maintaining our *understanding* of it
    * documentation reduce accidents
    * trouble is, documentation goes out of date -> _instrumentation_ reflects the reality of the system as it exists
    * it is possible to have too little info, or too much, or present it badly
- minimum doc: how to install, how to create and ship changes, roadmap, changelog, glossary, where to get help
- wiki are great !
    * store meeting notes, tasks list, team & members pages, build processes, design docs, software architecture diagrams...
    * + use it to share useful links, and try to encourage using this instead of individual bookmarks
    * ++ Ops Docs !
    * +++ DASHBOARD !! But dont create [ShittyDashboards]
    * include the wiki as part of task processes : sprints, ops, deployments...
    * get a leader whose goal is to motivate & educate others
- use Doxygen / Docurium for code documentation
- cf. [TeachDontTell], [BeautifulDocs], [AuthoringStyleGuide], [WriteTheDocs], [WhatToWrite]

## Recruiting & coaching new hires
- codility.com & cie
- recruiting shared and detailed: what soft/tech competencies to assess, how to evaluate code, loop prebrief/debrief process... cf. [5EPSQ]
- STAR -> Probe -> Chalenge
- some soft skills: teamwork, conflict resolution, listening, coordination...
- sample questions:
    * describe me the organisational methods you used on past project to tackle work efficiently. E.g. todo-list, programming journal, task planning software, time & emails management...
    * cf. [FrontendJobInterviewQuestions]
    * cf. [What happens when you type google.com into your browser and press enter?]
