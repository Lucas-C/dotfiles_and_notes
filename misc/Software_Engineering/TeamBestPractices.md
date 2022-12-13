# Software development is a collaborative game
cf. http://blog.codinghorror.com/software-development-as-a-collaborative-game/

<!-- To update this Table Of Contents:
    markdown-toc --indent "    " --maxdepth 3 -i TeamBestPractices.md
-->

<!-- toc -->

- [References](#references)
- [Teams organization](#teams-organization)
    * [Open-plan offices](#open-plan-offices)
- [Joining a new team](#joining-a-new-team)
- [Coaching new hires & bringing them up to speed](#coaching-new-hires--bringing-them-up-to-speed)
- [Leadership](#leadership)
- [Team culture building & best practices](#team-culture-building--best-practices)
- [Stand-up & meetings](#stand-up--meetings)
    * [Collective tasks estimation](#collective-tasks-estimation)
- [Retrospectives](#retrospectives)
- [Define team metrics](#define-team-metrics)
- [Ops](#ops)
    * [Post-mortems](#post-mortems)
    * [Chaos Engineering aka Resilience Testing](#chaos-engineering-aka-resilience-testing)
- [Documentation:](#documentation)
- [Recruiting / recrutement](#recruiting--recrutement)
    * [Matrice de compétences](#matrice-de-compétences)
    * [Outils](#outils)
    * [Language-based question](#language-based-question)

<!-- tocstop -->

## References
- [Minimum Viable Bureaucracy](https://speakerdeck.com/lauraxt/minimum-viable-bureaucracy-june-2014-edition)
- [HowToBeGoodAtOps](https://adamhjk.github.io/good-at-ops/#/8)
- [ShittyDashboards](http://attackwithnumbers.com/the-laws-of-shitty-dashboard)
- [Why Scrum Should Basically Just Die In A Fire](http://gilesbowkett.blogspot.com.au/2014/09/why-scrum-should-basically-just-die-in.html)
- [Five essential phone screen questions](https://sites.google.com/site/steveyegge2/five-essential-phone-screen-questions)
- [InfiniteHows](http://radar.oreilly.com/2014/11/the-infinite-hows.html)
- [5WhysWithHumansNotRobots](http://fr.slideshare.net/danmil30/how-to-run-a-5-whys-with-humans-not-robots/27-How_Hindsight_Bias_Shows_up)
- [PostMortemsPIEIndicator](https://www.box.com/blog/a-tale-of-postmortems/)
- [IT Change Management](http://stephaniekdean.wordpress.com/2011/06/17/cm/)
- [Event Management](http://stephaniekdean.wordpress.com/2011/04/04/eventmgmt/) : it "typically covers a brief description of the issue,
major points in the timeline of the event, information on trigger, root cause & resolution, lessons learned and short- & long-term action items.
... Action items must have a clear owner and due date."
- [AuthoringStyleGuide](https://github.com/tooling/authoring-styleguide)
- [TeachDontTell](http://stevelosh.com/blog/2013/09/teach-dont-tell/)
- [BeautifulDocs](https://github.com/PharkMillups/beautiful-docs)
- [WriteTheDocs](https://www.writethedocs.org)
- [WhatToWrite](http://jacobian.org/writing/what-to-write/)
- [FrontendJobInterviewQuestions](https://github.com/h5bp/Front-end-Developer-Interview-Questions) & [Front End Interview Handbook](https://github.com/yangshun/front-end-interview-handbook)
- [#gamedev Lead Quick Start Guide](http://web.archive.org/web/20140701034212/http://www.altdev.co/2013/11/05/gamedev-lead-quick-start-guide/)
- [What happens when you type google.com into your browser and press enter?](https://github.com/alex/what-happens-when)
- [JoeStumpTechnicalInterviewQuestions](http://stu.mp/2012/10/my-patent-pending-3-question-technical-interview.html)
- [TrekOps](https://medium.com/@jpaulreed/trouble-with-devops-try-trekops-fb69f7e554fd)
- [CodeVisualizationTools](https://softvis.wordpress.com/tools/)
- [ThePowerOfStableTeams](http://firstround.com/review/Twitter-Engineering-SVP-Chris-Fry-on-the-Power-of-Stable-Teams/)
- [MAPP] : Management Autonome de la Performance et du Progrès - [MichelinManufacturingWay](https://www.youtube.com/watch?v=ztsGX4YNkQ4)
- [Bringing Novice Developers Up To Speed](https://web.archive.org/web/20181210003120/https://www.mendix.com/blog/tips-for-bringing-novice-developers-up-to-speed/)
- [Criticism and Ineffective Feedback](https://www.kateheddleston.com/blog/criticism-and-ineffective-feedback)
- [Onboarding and the Cost of Team Debt](https://kateheddleston.com/blog/onboarding-and-the-cost-of-team-debt)
- [Things I was unprepared for as a lead developer](https://www.techspot.com/news/62243-things-unprepared-lead-developer.html)
- [DefendingYourTime](https://archive.is/TQOdt)
- [Alarm design: From nuclear power to WebOps](http://humanisticsystems.com/2015/10/16/fit-for-purpose-questions-about-alarm-system-design-from-theory-and-practice/)
- [Climbing out of the software death spiral](http://tinyletter.com/programming-beyond-practices/letters/beginning-to-climb-out-of-the-software-death-spiral)
- [Interviewing is broken](http://www.stilldrinking.org/interviewing-is-broken)
- [What Google Learned From Its Quest to Build the Perfect Team](http://www.nytimes.com/2016/02/28/magazine/what-google-learned-from-its-quest-to-build-the-perfect-team.html)
- [We Hire the Best, Just Like Everyone Else](http://blog.codinghorror.com/we-hire-the-best-just-like-everyone-else/)
- [Google SREs](http://www.wired.com/2016/04/google-ensures-services-almost-never-go/)
- [Learning Through Blameless Reviews](http://fr.slideshare.net/joelchippindale/learning-through-blameless-reviews)
- [Process Hacking](http://fr.slideshare.net/ClaireAgutter/process-hacking)
- [Blameless PostMortems and a Just Culture](https://codeascraft.com/2012/05/22/blameless-postmortems/)
- [HowAProgrammerReadsYourResumeVsARecruiter](http://stevehanov.ca/blog/index.php?id=56)
- [HowFuckedUpIsYourManagement?](https://mfbt.ca/how-fucked-up-is-your-management-8a1086eeb4a9#.3dmqfm2yu)
- [WorkAtDifferentManagementLevels](http://larahogan.me/blog/manager-levels/)
- [SelfFormingTeams](https://blogs.msdn.microsoft.com/bharry/2015/07/24/self-forming-teams-at-scale/)
- [OnFindingRootCauses](https://medium.com/production-ready/on-finding-root-causes-c0ce524bf98b#.fu7ofzcr4)
- [HoneYourProductionIncidentPostmortems](http://tech.shutterstock.com/2016/11/11/5-ways-to-hone-your-production-incident-postmortems/)
- [EtsyDebriefingFacilitationGuide](https://extfiles.etsy.com/DebriefingFacilitationGuide.pdf)
- [HowDoYouMakeAnAwesomeTeam](http://jvns.ca/blog/2017/01/13/how-do-you-make-an-awesome-team/)
- [IncidentManagementAtGoogle](https://cloudplatform.googleblog.com/2017/02/Incident-management-at-Google-adventures-in-SRE-land.html)
- [HowAndWhyToDesignYourTeamsForModernSoftwareSystems](https://www.slideshare.net/matthewskelton/how-and-why-to-design-your-teams-for-modern-software-systems-devopscon-berlin-june-2017)
- [BeingResponsibleForMyProgramsOperationsMakesMeABetterDeveloper](https://jvns.ca/blog/2017/06/18/operate-your-software/)
- [IfCompaniesInterviewedTechRecruitersTheWayTheyInterviewProgrammers](https://medium.com/@NTDF9/if-companies-interviewed-tech-recruiters-the-way-they-interview-programmers-f18e1a980cdd)
- [ProgrammerCompetencyMatrix](http://sijinjoseph.com/programmer-competency-matrix/)
- [3LawsOfConfigDynamics](https://blog.buildo.io/the-three-laws-of-config-dynamics-1e9724593aa9)
- [10WaysToBeABetterInterviewer](http://queue.acm.org/detail.cfm?id=3125635)
- [HiringEngineeringManagers](https://medium.com/@skamille/hiring-engineering-managers-screening-for-potential-1476044604d3)
- [Engineering a culture of psychological safety](https://blog.intercom.com/psychological-safety/)
- [DevOps at Netflix by Josh Evans](https://www.infoq.com/podcasts/Josh-Evans-netflix)
- [HowToMoMonitoringTheSREGoldenSignals](https://www.slideshare.net/OpsStack/how-to-monitoring-the-sre-golden-signals-ebook/)
- [How To Establish a High Severity Incident Management Program](https://www.gremlin.com/how-to-establish-a-high-severity-incident-management-program/)
- [STAR method of behavioral interviewing](https://www.vawizard.org/wiz-pdf/STAR_Method_Interviews.pdf)
- [Liste des émotions & sentiments](http://www.groupeconscientia.com/uploads/DOC_Liste_EmotionsSentiments.pdf)
- [Core Protocols](http://www.mccarthyshow.com/online/)
- [Intro à la Sociodynamique](http://cache.media.eduscol.education.fr/file/Numerique/85/7/3._Presentation_Marc_Smia_427857.pdf)
- [CNV & Agilité par T. Clavier & J. Quille](https://gitlab.com/azae/conferences/cnv-agilite/-/jobs/52813557/artifacts/file/2017agileFrance.pdf)
- [Enable your Devs to do Ops - Runbooks in the DevOps era](https://blog.buildo.io/enable-your-devs-to-do-ops-9a0a870baa1)
- [Why "Agile" and especially Scrum are terrible](https://michaelochurch.wordpress.com/2015/06/06/why-agile-and-especially-scrum-are-terrible/)
- [No, seriously. Root Cause is a Fallacy.](https://willgallego.com/2018/04/02/no-seriously-root-cause-is-a-fallacy/)
- [Some notes on running new software in production](https://jvns.ca/blog/2018/11/11/understand-the-software-you-use-in-production/)
- [CRACKING the CODING INTERVIEW](http://www.crackingthecodinginterview.com/resources.html)
- [Pour que les backlog grooming ne soient plus une corvée](http://www.theobserverself.com/corvee-backlog-grooming/)
- [Weighted Shortest Job First](https://www.scaledagileframework.com/wsjf/)
- [Agile Engineering Fluency - Stages of practice map](https://arlobelshee.github.io/AgileEngineeringFluency/Stages_of_practice_map.html)
- [Faire équipe](https://larlet.fr/david/blog/2019/faire-equipe/)
- [An epic treatise on scheduling, bug tracking, and triage](https://apenwarr.ca/log/20171213)
- [Monitoring Complex Systems: Keeping Your Head on Straight in a Hard World](https://fr.slideshare.net/BrianTroutwine1/erlang-factory-berlin-monitoring-complex-systems-keeping-your-head-on-straight-in-a-hard-world)
- [What is Spike in Scrum?](https://www.visual-paradigm.com/scrum/what-is-scrum-spike/)
- [Rethinking how we interview in Microsoft’s Developer Division](https://blog.usejournal.com/rethinking-how-we-interview-in-microsofts-developer-division-8f404cfd075a)
- [Greg Wilson - What We Actually Know About Software Development, and Why We Believe It's True](https://vimeo.com/9270320)
- [Technical interview exercises](http://www.colinhowe.co.uk/general/2018/05/30/technical-interview-exercises/)
- [Have interviewers practice](https://rework.withgoogle.com/guides/hiring-train-your-interviewers/steps/giving-interviewers-practice/)
- [Valve Handbook For New Employees](https://steamcdn-a.akamaihd.net/apps/valve/Valve_NewEmployeeHandbook.pdf)
- [Survival guide for Odooers](https://www.odoo.com/web/content/31413934?utm_campaign=HR_recruitment&utm_source=annonce+job&unique=495f86cbf17dad7e465ba2b292b62e3c80d09b1a)
- [Using 6 Page and 2 Page Documents To Make Organizational Decisions](https://medium.com/@inowland/using-6-page-and-2-page-documents-to-make-organizational-decisions-3216badde909)
- [Les ADR pour garder une trace de tous les choix d'architecture](https://blog.stack-labs.com/code/adr-to-remember-past-archiectural-decisions/)
- [L1221-6 à L1221-9 du Code du travail (Section 2: Recrutement)](https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006072050/LEGISCTA000006177850/2008-05-01/)
- [Managing developer identities in autonomous teams](https://kislayverma.com/organizations/managing-developer-identities-in-autonomous-teams/)
- [Agile at 20: The Failed Rebellion](https://www.simplethread.com/agile-at-20-the-failed-rebellion/)
- [The DevOps Phenomenon / CALMS framework](https://queue.acm.org/detail.cfm?id=3338532)
- [Why Don’t Tech Companies Pay Their Engineers to Stay?](https://marker.medium.com/why-dont-tech-companies-pay-their-engineers-to-stay-b9c7e4b751e9)
- [Who wrote this shit?](https://www.heltweg.org/posts/who-wrote-this-shit/)
- [You will always have more Problems than Engineers](https://betterprogramming.pub/you-will-always-have-more-problems-than-engineers-aafff94a4623)

## Teams organization
"Organizations which design systems are constrained to produce designs which are copies of the communication structures of these organizations" - Mel Conway, 1968
+ cf. [HowAndWhyToDesignYourTeamsForModernSoftwareSystems] & http://devopstopologies.com
+ https://bonkersworld.net/organizational-charts

[Agile Engineering Fluency - Stages of practice map]:
- Traditional well done
- Work as a team
- Core modern engineering
- Adaptive engineering
- Leverage capabilities
- Eliminate debt and change the rules
- Take advantage of being awesome

Tracks:
- Check your work (TDD, Exploratory Testing)
- Write good code (Refactoring, Design, Recovering legacy code)
- Ship at will (Continuous Integration, Continuous Deployment, Dev Ops)
- Know what to build (Stories, Vertical Decomposition, Planning)
- Discipline and learning (Pairing, Mobbing)
- Improve as a team (Teams, Retrospectives)
- Not hurried (Velocity, Planning to Capacity)

Specifies when:
- Doing A is nearly required to do B
- Doing A helps a lot when doing B

[Faire équipe]:
  * Les rituels
  * Les pratiques
  * Les joies
  > Peut-être est-ce cela faire équipe : partager l’enthousiasme de faire des choses ensemble qui permettent de mieux se connaître.
  * L’arithmétique

[An epic treatise on scheduling, bug tracking, and triage]:
Talk from experience. Explain the benefit of some Agile practices.
  * highlight the importance of non-negotiable work rates, and why setting deadlines is a bad idea and can be avoided
  * highlight the importance of bug triaging and give some practical recommendations (inc. the terible bug bankrupcy & bug clutter)
  * restricted multitasking, how to organize short biweekly team meetings, estimating Stories with points & tracking them using user-visible features...

[Agile at 20: The Failed Rebellion]
> Scrum was invented to function in hostile environments.
> It’s a contract between hard-pushing managers and developers needing time to think and explore.

> When “Agile” ideas are applied poorly, they often lead to more interference with developers,
> less time to do the work, higher pressure, and demands to “go faster”.

### Open-plan offices
Cons from [Why "Agile" and especially Scrum are terrible]:
- it’s hard to concentrate in them
- they’re anti-intellectual, insofar as people become afraid to be caught reading books (or just thinking) on the job. When you force people to play a side game of appearing productive, in addition to their job duties, they become less productive

## Joining a new team
- talk to a colleague each day (but not for too long, and schedule it) and question him on what he does
- take notes in a file, complete/fix the existing docs & draw diagrams
- quickly get a short-term goal to focus on & follow the 'minimal info' loop:
    * Acquire as little information as possible
    * Acquire information as efficiently as possible
    * Use the information you acquire as effectively as possible
- ask people to have lunch with them (force yourself !)
- ask people for coffee breaks (force yourself !)
- grasp the whole architecture using [CodeVisualizationTools]
- get along with HR and plan out-of-the-box projetcs with them that will make your team happier
- [Who wrote this shit?]

## Coaching new hires & bringing them up to speed
- **First**: publicly tell her/him WELCOME + invite them to have launch or have a drink
- [Onboarding and the Cost of Team Debt] = "when employees aren't properly trained, integrated, or managed, they are operating at less than optimal efficiency and "team debt" is accrued"
    * Productivity = Σ of talent * teamwork
    * To improve onboarding:
        - distribute the load of onboarding
        - focus on technical skills, knowledge of company processes, and personal development
- provide a basic map / schema of Where is What ?
- write docs
- assign a "buddy" in the team & a "mentor" in the company
- [Bringing Novice Developers Up To Speed]
    * Key elements: Autonomy / Mastery / Purpose
    * Each novice has a tech mentor to meet with regularly, ideally the team lead
    * Encourage questions, and make it safe to ask anything.
    * Implement a regular pairing schedule
    * Make sure that code is systematically reviewed
    * Junior developers need individual learning goals with self-defined objectives
- cf. also bookmarks on coaching an intern
- organiser un atelier en mode _Event-Sourcing_ pour expliquer le fonctionnement du projet et la terminologie
- initier un wiki que les nouveaux arrivants complèteront au fur et à mesure,
avec des sections "liens utiles" / "à installer sur son poste" / "par où commencer" / "nos méthodos & rituels d'équipe"
- prévoir un court dispositif du type 1h / jour avec un collègue différent pour présenter un sujet
- [Valve Handbook For New Employees]
    * present the team history a bit
    * Your First Month / What To Work On
- [Survival guide for Odooers]
    * Your first days : You'll get a quick tour of the company before starting a 2-week training on the product. You’ll learn this through the eLearning platform by creating your own database and by having fun with our business game. At the end of the training, you’ll have to take the certification to assess your level. After the training, you’ll join your team and a coach will train you
    * Our culture & values
    * It’s ok to fail. It’s ok to ask stupid questions. Please, do it.
    * Be responsible: avoid the “this is not my job” attitude
    * Our Tools
    * Career Path : the tools to help you evolve (in the company)
    * Work Hard, Play Hard: the idea is to have fun after work
    * Our Offices
    * HR Policies: purchase policy, working hours, legal/sick leaves
    * Glossary
- https://walkthrough.dev: step-by-step code walkthroughs to share knowledge and bring developers up to speed - GitHub based, $7/month
  Alt: free VSCode plugin - https://marketplace.visualstudio.com/items?itemName=vsls-contrib.codetour

## Leadership
cf. [#gamedev Lead Quick Start Guide] & [Things I was unprepared for as a lead developer] & TED Talk WhyGoodLeadersMakeYouFeelSafe
"tell people what you want them to do instead of detailing what they’re doing wrong" [Criticism and Ineffective Feedback]
Daniel Pink motivational building blocks from "The puzzle of motivation" :
- autonomy: to direct our own lives
- mastery: to get better and better at something that matters
- purpose: to do what we do in the service of something larger than ourselves

[Amazon Principal Engineering Community Tenets](https://www.amazon.jobs/en/landing_pages/pe-community-tenets) :
- Exemplary Practitioner
- Technically Fearless
- Balanced and Pragmatic
- Illuminate and Clarify
- Flexible in Approach
- Respect What Came Before
- Learn, Educate, and Advocate
- Have Resounding Impact

[Managing developer identities in autonomous teams]
> An autonomous team is a team which is responsible for solving a specific business problem. The members of this team cut across system boundaries to solve business problems
> The challenge of the manager is to get his team to engage with the problem statement. [...] The ability to do this, in my opinion, the hallmark of a great manager/leader

[WorkAtDifferentManagementLevels]
* Managing a team of individual contributors
* Managing individual contributors and managers
* Managing just managers

## Team culture building & best practices
- two main tenets: RESPECT & TRUST people.
How to build trust ? Start by trusting others, be trustworthy, build relationships + it takes time [Minimum Viable Bureaucracy] + [MAPP] on trust, autonomy & Agile methods in Michelin
- [TrekOps]
> Something that is really great about Star Trek, is that when a character notices something is amiss,
> and they are the only one to see it, **the rest of the crew doesn’t just dismiss their concerns offhand**.
> **Their concerns are ALWAYS valid**.
- write down team tenets as guidelines for priorities
- define clear team goals with deadlines
- build a team brand: catchy name, logo, slogan... [PP]
- small is good: 2-pizzas team
- make decisions based on data
- allocate some hack time
- rotate unwanted responsabilities [Minimum Viable Bureaucracy]
- whiteboard sessions
- coding style reference, tools to enforce it, code reviews
- regular emails with tips. Or put a one-pager in the toilets, as Google is doing
- [ThePowerOfStableTeams] :
    - Getting teams to sit together
    - Making someone responsible
    - Clarifying mission
    - Knowing your role as an executive: beeing a support for the team
- [DefendingYourTime] : protect from bad planning and burnout.
  * It tackles two major problems in software companies: bad planning, and burnout.
  * Setting boundaries & defending them
  * Estimates are not deadlines
  * Take your holidays
- [What Google Learned From Its Quest to Build the Perfect Team] :
    * Two behaviors that all the good teams generally shared:
        - First, on the good teams, members spoke in roughly the same proportion. " if only one person or a small group spoke all the time, the collective intelligence declined".
        - Second, the good teams all had high "average social sensitivity".
    * Psychological safety is "a sense of confidence that the team will not embarrass, reject or punish someone for speaking up".
    It describes a team climate characterized by interpersonal trust and mutual respect in which people are comfortable being themselves.
    * Everyone [shared] something personal about themselves. The team found it easier to speak honestly about the things that had been bothering them, their small frictions and everyday annoyances.
    They agreed to adopt some new norms: from now on, [the team leader] would make an extra effort to let the team members know how their work fit into [the company's] larger mission; they agreed to try harder to notice when someone on the team was feeling excluded or down.
    * No one wants to put on a ‘‘work face’’ when they get to the office.
    To be fully present at work, to feel ‘‘psychologically safe,’’ we must know that we can be free enough, sometimes, to share the things that scare us without fear of recriminations. We must be able to talk about what is messy or sad, to have hard conversations with colleagues who are driving us crazy. We can’t be focused just on efficiency.
- [Process Hacking]: process exploration days, rotation days, problem boards, reward participants
- [HowDoYouMakeAnAwesomeTeam]
    * Talk a lot about your work in a public channel
    * Ask a lot of questions in public
    * Scheduling brainstorming meetings
    * When having a discussion, talk like you might be wrong
    * Don’t forget you have power over how your team is
- [Engineering a culture of psychological safety]
    * Make respect part of your team’s culture: It’s essential to challenge lack of respect immediately, politely, and in front of everyone who heard the disrespect.
    * Make space for people to take chances: Create an expectation that everyone on the team should think outside the box
    * Make it obvious when your team is doing well: celebrate glorious failure
    * Make your communication clear, and your expectations explicit: f you expect someone to do something for you, ask for a specific commitment – “When might this be done?”, rather than assuming everyone agrees on its urgency
    * Make your team feel safe
- exercice d'écoute empathique -> cf [Liste des émotions & sentiments]
- [Core Protocols]:
  * pass:  decline to participate in something
  * check-in: indicate your engagement + express feelings
  * check-out: "You must Check Out when you are aware that you cannot maintain the Core Commitments or whenever it would be better for you to be elsewhere."
- [Intro à la Sociodynamique]: socio-passifs B1, hésitants B2, déchirés B3, irréductibles B4, opposants B5, alignés B6, concertatifs B7
- [CNV & Agilité par T. Clavier & J. Quille]

## Stand-up & meetings
It mush be SHORT (<15min), everybody has to be ponctual, actually **stand-up**, **listen** and **be concise** : [Why Scrum Should Basically Just Die In A Fire]
- What did you do yesterday?
- What are you doing today?
- What is blocking your progress?
- What are your commitments for the week / progression / changes due to blockers or higher priorities

In general, limit meetings by making them informal chats or doing them properly: agenda (skip if empty), few participants, time-boxed, clustered on some days in the week, take notes & record team decisions [Minimum Viable Bureaucracy]

Identify what's the main purpose of the meeting: **think & reflect**, **decide** or **inform**

Décision commune par consensus, explitie : demander si quelqu'un a un concern / une objection.
Si personne ne se manifeste -> adopté

[Liberating Structures](http://www.liberatingstructures.com) 33 microstructures to replace more controlling or constraining meetings
\+ problème peut être découpé en plusieurs ateliers pour diverger puis converger
Exemples :
- [1-2-4-All](http://www.liberatingstructures.com/1-1-2-4-all/) - 12min, "autoporté", _parallel processing_ - **Attention**: le choix de question posée est crucial
- [Troika consulting](http://www.liberatingstructures.com/8-troika-consulting%20/) - 30min - by groups of 3 persons - in each round, one participant is the “client”, the others “consultants”

ROTI (_Return On Time Invested_) : vote à main levée de 1 à 5, de excellent à inutile

Dot Voting : une fois les idées listées (sous forme de post-its par exemple) chacun répartit N votes parmi elles (en traçant des bâtons)

### Collective tasks estimation
- [Pour que les backlog grooming ne soient plus une corvée]:
  * des petites séances répétées : en faire 1 court par mois plutôt des très longs 1 à 2 fois par semestre
  * changer de vocabulaire: "atelier" plutôt que "réunion"
  * proposer en début de séance de timeboxer à 5 ou 10min max par US
- planning poker
- spread tasks in 5 columns arbitrarily assigned a 2/3/5/8/13 points value, comparing them in terms of estimate time to completion (with no absolute estimation in man-days), e.g. with RealTimeBoard
- [Weighted Shortest Job First] (WSJF) = _Cost of Delay_ / _Job Duration_, where _Cost of Delay_ = _User-business value_ + _Time criticality_ + _Risk reduction-opportunity enablement value_
and all values can be estimated on a 1-13 scale using planning poker cards
- [What is Spike in Scrum?]
> Spikes are an invention of Extreme Programming (XP), are a special type of user story that is used to gain the knowledge necessary to reduce the risk of a technical approach. A spike has a maximum time-box size [...] A Spike is a great way to mitigate risks early and allows the team ascertain feedback and develop an understanding on an upcoming PBI’s complexity.
- Anchor effect (bias) :
> For a given test software project and a random group of developpers,
> a single sentence in the specs **estimating that it should take** 2 or 20 months to complete,
> is the main statistical drive explaining **why it took, in the end**, 5 or 15 months to produce it,
> **regardless of how much** experience the developpers have in the domain,
> how much experience they have in software development in general,
> what techniques they're using or how familiar they are with the tools.
Experiment by Aranda & Easterbrook (2005)
Source: [Greg Wilson - What We Actually Know About Software Development, and Why We Believe It's True] - 15:55
- If more than 20-25% of a component has to be revised,
it's better to rewrite it from scratch (Thomas et al, 1997)

[You will always have more Problems than Engineers]:
> When you’re overwhelmed with problems, ordering them isn’t the most important skill, filtering them is. The most valuable prioritization skill is simply saying “No. I’m not going to solve that problem right now”.
> Engineers need prioritization skills too.

[J'ai presque fini - David Laizé - DevFest 2021](https://youtube.com/watch?v=ohVd4ugay1o)
* Overconficence effect
* Escalation of commitment (aka _Sunk cost fallacy_ aka "biais des coûts irrécupérables")

Ses solutions : la phase de conception est importante; solliciter des collègues un feedback si on est tombés dans ce biais => psychological safety

## Retrospectives
- Content/Pas content/A améliorer/A continuer/A arrêter/Questions
- Drop/Add/Keep/Improve
- Ecocycle schema of products maturity: https://www.taesch.com/references-cards/ecocycle

Liens utiles:
* http://www.funretrospectives.com
* http://retrospectivewiki.org
* https://retromat.org
* https://www.scrumalliance.org/community/member-articles/699
* https://action.parabol.co : open-source online retrospectives, sprint poker, standup meetings...
* TRUNE: https://www.scrumexpert.com/tools/truly-connect-with-your-team-retros-radars-with-trune/ : online retrospective & health radar tool

| Nom rétrospective                       | Description / Lien                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|-----------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 4L + W³                                 | Liked / Learned / Lacked / Longed for + [What / So What / Now What ?](https://www.liberatingstructures.com/9-what-so-what-now-what-w/)                                                                                                                                                                                                                                                                                                                                    |
| TRIZ                                    | Stop Counterproductive Activities and Behaviors to Make Space for Innovation - http://www.everydaykanban.com/2015/06/18/shake-up-retrospective-with-triz/                                                                                                                                                                                                                                                                                                                 |
| STARFISH                                | Start Stop Continue More Less                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| DAKI                                    | Drop Add Keep Improve - http://www.funretrospectives.com/daki-drop-add-keep-improve/                                                                                                                                                                                                                                                                                                                                                                                      |
| SPEED BOAT                              | http://blog.xebia.fr/2015/03/20/la-retrospective-le-format-speed-boat/                                                                                                                                                                                                                                                                                                                                                                                                    |
| Worked well, kinda Worked, didn’t Work  | http://www.funretrospectives.com/www-activity-worked-well-kinda-worked-didnt-work/                                                                                                                                                                                                                                                                                                                                                                                        |
| UPS & DOWNS                             | Similaire à la retro Dixit, on utilise les cartes de facilitation Ups And Downs représentant un personnage nu navigant sur la mer dans sa baignoire (?!) On étale les cartes et pose une question à l'équipe (comment vous vous sentez..) et on demande à chacun de choisir une carte adaptée et de raconter au groupe ce que l'on ressent http://innovativeresources.org/resources/card-sets/ups-and-downs/                                                              |
| JEOPARDY                                | Comme le jeu télé : trouver les questions aux réponses données http://talondagile.fr/2013/02/un-oeil-dans-la-retro-33-jeopardy/http://jeopardyretro.blogspot.fr/2012/11/jeopardy-retrospective-plan.html                                                                                                                                                                                                                                                                  |
| CELEBRATION GRID                        | Un format qui permet de prendre du recul sur nos FAIL et aussi de promouvoir les expérimentations. http://noop.nl/2014/07/my-best-diagram-ever-the-celebration-grid.html                                                                                                                                                                                                                                                                                                  |
| STAR WARS                               | Chaque participant pose ses post-it d'un coté (Light/Dark), ensuite chacun prend une (ou zéro) action pour le sprint prochain http://blog.octo.com/retrospective-agile-sur-le-theme-star-wars/                                                                                                                                                                                                                                                                            |
| GYSHIDO                                 | http://www.areyouagile.com/2015/03/festival-de-retrospectives/ Rétro Get Your Shit Done : Les choses chiantes Les choses inutiles Les choses brouillonnes Qui et comment avez vous aidé ? Quelles actions avez vous menées ? (j’ai aidé)Qui et comment avez vous perturbé ? (j’ai foiré)Niveau de confiance important nécessaire dans la team pour jouer ce genre de rétro.                                                                                               |
| TURN THE TABLES                         | http://retrospectives-agiles.fr/post/46705782065/la-r%C3%A9trospective-turn-the-tables Très bien pour faire parler des gens qui ont des métiers et visions différentes sur un projet (typiquement les FTs). Très bons impacts la première fois qu'on la joue.                                                                                                                                                                                                             |
| SPEED CAR                               | It is a mix of retrospective and futurespective, which uncovers risks - http://www.funretrospectives.com/speed-car-abyss/                                                                                                                                                                                                                                                                                                                                                 |
| HOT AIR BALOON                          | It is a mix of retrospective and futurespective, which uncovers risks - http://www.funretrospectives.com/hot-air-balloon-bad-weather                                                                                                                                                                                                                                                                                                                                      |
| SQUAD HEALTH CHECK                      | Mesure la santé de l’équipe https://jp-lambert.me/r%C3%A9tro-squad-health-check-94d3fed9997                                                                                                                                                                                                                                                                                                                                                                               |
| DESSINEZ LE SPRINT                      | On distribue de grande feuille blanche et des marqueurs dans chacune des 3 équipes Les participants dessinent certains aspects du sprint. Exemples de sujet : Comment avez-vous vécu le sprint ? Quel a été le moment le plus marquant ? Quel a été le plus gros problème ? Qu'auriez-vous désiré ? Chaque équipe réalise son œuvre On colle tous les dessins au mur. Pour chaque dessin, laissez les gens deviner ce qu'il représente avant que les auteurs ne le fasse. |
| LES 3 PETITS COCHONS                    | http://www.funretrospectives.com/three-little-pigs/ Les petits +: Faire dessiner chaque petit cochon par un membre de l'équipe, attribuer un vote au meilleur dessins Attribution d'un cochon à l'image du sprint                                                                                                                                                                                                                                                         |
| RETRO MARTINE                           | Chaque personne réalise une ou plusieurs couvertures de Martine en reflétant son état d'esprit ou le sprint qui vient de se terminerimprimer et afficher sur le mur pour générer des discussions & actions http://www.retourdemartine.free.fr/create.phphttp://www.nintendo-town.fr/martine/create.php Dans le même genre avec les livres oreilly : https://korben.info/generateur-de-couvertures-oreilly.html                                                            |
| Jour de lessive !                       | La rétrospective, c'est un peu laver son linge sale (en famille bien sur). Chaque équipe rédige ses post-its "linge propre" ou "linge sale", et les accroche sur un fil à linge : côté "linge propre" (les points positifs du sprint) ou "linge sale" (les points négatifs du sprint). Puis les équipes tournent et analysent les post-its sur le fil à linge de l'équipe précédente, et propose des actions d'amélioration.                                              |
| Le rétro dont vous êtes le héros        | http://blog.octo.com/la-retrospective-dont-vous-etes-le-heros/                                                                                                                                                                                                                                                                                                                                                                                                            |
| FunRetro                                | http://funretro.github.io -> en ligne, nécessite de préparer des questions à l'avance                                                                                                                                                                                                                                                                                                                                                                                     |
| Problem Solving Tree                    | Got a big goal? Find the steps that lead to it https://retromat.org/en/?id=96                                                                                                                                                                                                                                                                                                                                                                                             |
| Strengths-Based Retrospective           | Do more of the things that you are already doing and which you are good at. http://retrospectivewiki.org/index.php?title=Strengths-Based_Retrospective                                                                                                                                                                                                                                                                                                                    |
| Force Field Analysis                    | List all the supporting/driving factors for the topic, then the inhibiting/restraining ones http://retrospectivewiki.org/index.php?title=Force_Field_Analysis                                                                                                                                                                                                                                                                                                             |
| FLAT                                    | Future direction, Lessons learned, Accomplishments and Thank you                                                                                                                                                                                                                                                                                                                                                                                                          |


## Define team metrics
- customer satisfaction
- performance, output data quality
- availability : measured from the client side
- latency
- to fight it and encourage people reducing it, properly measure the technical debt: time & effort to repair; impact frequency, severity & reach; error rates; capacity/headroom

## Ops
![](http://blog.sei.cmu.edu/assets/content/Traceability-Model.png)

![](/Agile_vs_CI_vs_CD_vs_DevOps.jpg)

- [HowToBeGoodAtOps]
- "**Empathy** allows software makers and operators to help each other deliver the best possible functionality and operability on behalf of their customers." [Jeff Sussna & Katherine Daniels](http://blog.ingineering.it/post/72964480807/empathy-the-essence-of-devops)
- monitor everything ! CPU, openFD, procCount... For services: throughput + delay + completness (% of potential src data processed). And store historical data ! Distributed tracing tools: Twitter’s Zipkin and compatible Apache HTrace, Google’s Dapper
- zero config: config is hard to document, hard to update, hard to set up, its persistent state can overlaps with other data
- the [3LawsOfConfigDynamics] : tl.dr "have at least one default configuration that is committed to the repo and is enough to start the app successfully in a local dev environment"
  * Config values can be transformed from one form to another, but can be neither created nor destroyed.
  * The total length of a config file can only increase over time.
  * The length of a perfect config file in a development environment is exactly equal to zero.
- emails are evil: no guarantee it will be actioned + no guarantee anyone is subscribed + sense of false security as it works from time to time
- when an alarm is raised, alerting tools should give a maximum of *context* on the system state and what triggered it
- prioritize identifying the root cause of an issue and resolving it
- hold weekly/monthly ops review meetings, including:
    * highlights from previous on-call shift: high severity events, metrics...
    * this week's priorities: deployments, hand-over of burning tickets or tickets failing over SLA
- frequently determine operational excellence goals: eliminate the top root cause of tickets, create a runbook/dashboard for a service...
- CMs: cf. [IT Change Management]
- event management: cf. [Event Management]
- use a chatbot for real time alerts (e.g. Hubot in Node.js, can integrate with Jenkins via Janky - Also: Slack, Lita for Ruby, Err or Zulip for Python, cog for Slack / HipChat)
- useful questions to ask yourself when designing an alarms system : [Alarm design: From nuclear power to WebOps]
- [Climbing out of the software death spiral] -> either :
    * comprehensive backlog audit
    * issue bankruptcy
    * new dev "work queue"
- [Google SRE] : "no SRE could spent more than 50 percent of his or her time on traditional operations as opposed to coding"
- keep Ops playbooks
- [BeingResponsibleForMyProgramsOperationsMakesMeABetterDeveloper]
- [DevOps at Netflix by Josh Evans] key takeaways:
    * There are many interpretations of the term DevOps, it is a useful shorthand for a wide variety of technologies and approaches
    * “You build it, you run it” is the concrete application of the freedom and responsibility culture
    * When building a platform tool make it so easy to use that the product teams are not tempted to try and build something for themselves
    * Product teams are free to experiment and learn, which can feel chaotic and is a valuable part of the freedom and responsibility culture
    * The value of blameless and safe incident reviews – the goal is to learn and find patterns and use that information to present whole classes of failure from happening in the future
    * Don't view the value stream in a fragmented way – see the whole end to end system with all its interactions and dependencies and optimize the system as a cohesive whole rather than different tools and domains
- [HowToMoMonitoringTheSREGoldenSignals] the "golden signals" are, from Google SRE book and the USE/RED methods:
    * Rate
    * Errors
    * Latency
    * Saturation
    * Utilization
- [Enable your Devs to do Ops - Runbooks in the DevOps era] aka "Collaborative Ops FAQ":
    * IHMO: sometimes better than automation: faster + foster knowledge sharing
    * "Actually, you should be able to do it yourself. Here’s a link to the documentation."
    * define a template
    * "scripts longer than two lines are better treated as code; thus they should be versioned"
    * "If you find something that is outdated, but don’t have time to fix it immediately, leave a quick note or add a task for someone to update it"
    * "make sure every runbook has a clear owner and write it at the top of the document."
- [Some notes on running new software in production]:
    * Start using [your software] in production in a non-critical capacity (by sending a small percentage of traffic to it, on a less critical service, etc)
    * try to have each incident only once
    * Understand what is ok to break and isn’t
- [The DevOps Phenomenon / CALMS]:
    * **Culture**: mutual trust, willingness to learn and continuous improvement, constant flow of information, open-mindedness to changes and experimentation
    * **Automation**: deployment pipelines (CI/CD), comprehensive test automation
    * **Lean**: minimize WIP state, shorten and amplify feedback loops, look for opportunities to remove waste, fix errors as they are discovered
    * **Measurement**: monitoring, system metrics, KPIs
    * **Sharing**: sharing knowledge & practices, including successes & failures, learn from each other's experiences, proactively communicate, shadowing & pairing on tasks

### Post-mortems
- trying to organize it THE DAY AFTER THE EVENT, when it is fresh in people's minds
- PIE = Probability of recurrence * Impact of recurrence * Ease of addressing - cf. [PostMortemsPIEIndicator]
- planning for a future where we're as stupid as we are today [5WhysWithHumansNotRobots]
- [No, seriously. Root Cause is a Fallacy.]: because our systems are complex, there is never really a single unique root cause
- if we made an incremental improvment in area A or area B, which would prevent the broadest class of problems going ahead ? [5WhysWithHumansNotRobots]
- human error is NEVER a root cause [OnFindingRootCauses] : You can’t fix people, but you can fix systems and processes to better support them.
Learning is the goal during post-mortems (cf. [Learning Through Blameless Reviews] for a nice quick slideshow) + questions examples : [InfiniteHows]
- share your postmortem in an accessible, standardized way : [HoneYourProductionIncidentPostmortems] & [EtsyDebriefingFacilitationGuide]
- tooling: https://github.com/etsy/morgue : PHP based web application to help manage your postmortems, made by Etsy
- FTA = Fault Tree method = Arbre des défaillances : ~ méthode des "5 whys" avec une mindmap
- train people to handle those situations : [IncidentManagementAtGoogle]
- [How To Establish a High Severity Incident Management Program]
- DOs:
  * Ne discuter que d'états, de faits et d’enchaînements d'événements
  * Agréger au maximum les informations
  * Restreindre le périmètre de l'événement de départ
  * S'arrêter de descendre dans une branche dès qu'on a plus de prise sur l'événement concerné
  * Un arbre pour les gros incidents coûteux
- DON'Ts:
  * Parler de solutions. Discuter de pistes d'analyse.
  * Etre pointilleux et chercher à détailler au maximum
  * Partir d'une défaillance trop générale
  * Modéliser ce qui n'est pas de son ressort
  * En faire à chaque fois
- cf. [PostMortemTemplate.md](PostMortemTemplate.md)

### Chaos Engineering aka Resilience Testing
Présentation par Sylvain Hellegouarch:
- Steady State Hypothesis
- devenir familier avec l'échec, l'erreur dans votre système
- Game Days / Days Of Chaos
- Tools:
  * Chaos Monkey / Kong (AWS...)
  * Chaos Kub, Kube Monkey (Kubernetes)
  * PowerfulSeal (AWS, OpenStack, Kubernetes)
  * Pumba (Docker, Kubernetes)
  * Gremlin (Docker) - payant
  * ChaoSlingr (AWS)
  * Chaos Spring Boot : Latency / Exception / AppKiller Assaults
  * Byte Monkey
  * [toxiproxy](https://github.com/Shopify/toxiproxy): Ruby framework for simulating network conditions
    Alt: community-libs/vaurien in Python (not much maintained); kffl/speedbump in Go
- [ChaosToolKit](https://chaostoolkit.org)

## Documentation:
- Operational doc Tenets:
    * the key challenge to sustaining a complex system is maintaining our *understanding* of it (cf. [Monitoring Complex Systems: Keeping Your Head on Straight in a Hard World])
    * documentation reduce accidents
    * trouble is, documentation goes out of date -> _instrumentation_ reflects the reality of the system as it exists
    * it is possible to have too little info, or too much, or present it badly
- minimum doc: how to install, how to create and ship changes, roadmap, changelog, glossary, where to get help
http://keepachangelog.com -> best practices & advices
- wiki are great ! cf. "Lessons Learned" of AOSA chapter on SocialCalc: "I was able to catch up and start contributing in less than a week, simply due to the fact that **everything is in the wiki**"
    * store meeting notes, tasks list, team & members pages, build processes, design docs, software architecture diagrams...
    * + use it to share useful links, and try to encourage using this instead of individual bookmarks
    * ++ Ops Docs !
    * +++ DASHBOARD !! But dont create [ShittyDashboards]
    * include the wiki as part of task processes : sprints, ops, deployments...
    * get a leader whose goal is to motivate & educate others
    * templaaaaates are awesome. Alt: script page generation (e.g. for dashboards depending on parameters: IP, hostnames...)
- cf. [TeachDontTell], [BeautifulDocs], [AuthoringStyleGuide], [WriteTheDocs], [WhatToWrite]
- https://github.com/Kibibit/command-lime : build you web-based CLI onboarding demo in a fake terminal
- simple dashboard for JSON APIs : [freeboard](https://github.com/Freeboard/freeboard)
- http://www.mkdocs.org : simple static doc website generation from Markdown, "à la" ReadTheDocs
[Lucas]: used at oui.sncf, combined with Gitlab Pages => very powerful and efficient, allow to real deal with:
- **Doc As Code**:
> one should embrace lightweight markup languages, use static site generators, and store content in version control repositories with engineering code
- Ideas to go further: embed a REST API shooter, include formated docstrings, include BDD features, include configuration from the Configuration Management Tool (and even to edit them ?)
- one tool for assessing your documentation accessibility is the [Hemingway App](http://www.hemingwayapp.com/help.html).
The Hemingway App analyzes text and scores it based on tiered reading levels.
The assessments can help you spot potentially difficult passages in your documentation.
It’s available as a text editor application, a web app, and even a linter, if command line applications are your thing.
 - Donald Knuth advocated [literate programming](https://en.wikipedia.org/wiki/Literate_programming), where doc is written at the same time and location as the source code and extracted by automatic means
- [Living Documentation](https://leanpub.com/livingdocumentation)
  * make it easily searchable
  * Core Principles of Living Documentation: Reliable, Low-Effort, Collaborative, Insightful
  * **Living Glossary** : glossary from code (e.g. can be implemented in Python with decorators)
> Extract the glossary of the Ubiquitous Language from the source code. Consider the source code as the Single Source of Truth,
> and take great care of the naming of each class, interface and public method whenever they represent domain concepts.
> Add the description of the domain concept directly into the source code, as structured comments that can be extracted by a tool
- [Using 6 Page and 2 Page Documents To Make Organizational Decisions]
- Lightweight Architecture Decision Records: cf. [Les ADR pour garder une trace de tous les choix d'architecture]

## Recruiting / recrutement
- [HowFuckedUpIsYourManagement?]
- prebrief, debrief, assigned competences, bar raiser
- codility.com & cie
- recruiting shared and detailed: what soft/tech competencies to assess, how to evaluate code, loop prebrief/debrief process... cf. [Five essential phone screen questions]
- [STAR method of behavioral interviewing] -> Probe -> Challenge
  In just one picture: http://chezsoi.org/lucas/wwcb/photos/STAR-methodology.png
- some soft skills: teamwork, conflict resolution, listening, coordination...
- sample questions:
    * describe me the organisational methods you used on past project to tackle work efficiently. E.g. todo-list, programming journal, task planning software, time & emails management...
    * cf. [FrontendJobInterviewQuestions] & [Front End Interview Handbook]
    * cf. [What happens when you type google.com into your browser and press enter?]
    * cf. [JoeStumpTechnicalInterviewQuestions]
- cf. [HowAProgrammerReadsYourResumeVsARecruiter] & [Interviewing is broken] & [We Hire the Best, Just Like Everyone Else] :
"Bring them in for a few days, see if they can set up the dev environment, assign them some bugs nobody else wants to fix, have them meet everyone. - Pay them. - Decide if you want to keep paying them."
- [Foursquare](http://engineering.foursquare.com/2016/04/04/improving-our-engineering-interview-process/) :
> "We forgo technical phone interviews whenever possible. They’re typically unpleasant for everyone involved and we felt like the environment of a phone screen wasn’t conducive to learning about a candidate’s abilities comprehensively. Instead we give out a take-home exercise that takes about three hours."
- [HiringEngineeringManagers]: clearly define your interview process:
    - screening for **potential** or **experience** ?
    - what methodology to use ? what answers are you looking for ?
- [IfCompaniesInterviewedTechRecruitersTheWayTheyInterviewProgrammers]
- [10WaysToBeABetterInterviewer] by Kate Matsudaira:
  * Review the candidate's resume
  * Review feedback from previous interviews
  * Use calibrated questions
  * Test new questions on yourself and your peers
  * Create a timeline for the interview
  * Head in with a positive attitude
  * Take notes
  * Bring a list of questions to the interview
  * Be collaborative
  * Try to make the problems feel as real-world as possible
- [Test technique Xebia](https://github.com/snilyes/mowitnow)
- [Technical interview exercises] :
  > It’s an engineers market: You’re in competition with a lot of other companies and so you have to try and make this process as rewarding as possible for the candidate to ensure that they stay interested in your company.
  * Why we interview:
    + Understanding if the role/company/candidate are a fit for each other? It’s a two-way thing
    + Selling the company/role to the candidate
    + Attempting to minimise the number of mis-hires and number of missed opportunities.
    + Learning and having fun
  > Pick a few skills that matter (3 or 4) and interview for those in as realistic a way as possible
  > the top four skills I focus on are: architectural design, testing, coding and debugging
  > Throughout the interview I am looking for people that can learn quickly.
  > It’s important that all of the scoring and decision making is done independently to avoid anyone influencing anyone else.
  > Once a decision is made, feedback is given as quickly as possible : [this] will give the candidate a really good impression of you - even if the answer is a no.
- [CRACKING the CODING INTERVIEW]: prep sheets for soft skills, coding skills, PM skills
- [Rethinking how we interview in Microsoft’s Developer Division] for Project Managers:
  * Share the interview in advance
  * Use a real problem
  * Give access to data
  * Make it interactive
  * Follow a single scenario
  * Pair interviewers
  * Hold feedback until the end
  * Give feedback on the process too
- [Have interviewers practice]:
> Some teams calibrate new interviewers by having them shadow more experienced interviewers. After interviewers have shadowed a few interviews, the hiring team may ask them to “reverse shadow” where the new interviewer runs the interview and the experienced interviewer observes to provide feedback.
- Articles [L1221-6 à L1221-9 du Code du travail (Section 2: Recrutement)] :

> Le candidat à un emploi est expressément informé, préalablement à leur mise en oeuvre, des méthodes et techniques d'aide au recrutement utilisées à son égard.
> Les résultats obtenus sont confidentiels.
> Les méthodes et techniques d'aide au recrutement ou d'évaluation des candidats à un emploi doivent être pertinentes au regard de la finalité poursuivie.

> Aucune information concernant personnellement un candidat à un emploi ne peut être collectée par un dispositif qui n'a pas été porté préalablement à sa connaissance.
- [Why Don’t Tech Companies Pay Their Engineers to Stay?]:
> The hard truth that many companies struggle to wrap their heads around is that they should be paying their long-tenured engineers above market rate. This is because an engineer that’s been working at a company for a long time will be more impactful specifically at that company than at any other company.

### Matrice de compétences
- [ProgrammerCompetencyMatrix]
- draw a technical/functional skills matrix of your team, Avengers-style:
    * determine your "Dilts" role among: doer, conceptor, coordinator, systemic vision
    * cross matrix: Team / Products / Systemic & Vision VS Roles / Skills / Aspirations
- **objectifs** :
    * identifier de potentiels risques de truck factors dans l'équipe, afin de planifier du partage de compétence sur ces sujets
    * exprimer nos souhaits de progression dans des domaines techniques, et les attraits pour des rôles que nous pouvons avoir
- **note** : cette modélisation est fondamentalement limitée : il est bien sûr impossible de capturer sous ce format l'intégralité des domaines de compétence de chacun.
  Il est simplement accepté que cet exercice peut être utile à faire émarger des actions de partage de connaissances utiles.
- **processus** :
    1. Les membres de l'équipe complètent les tableaux ci-dessous pour ajouter des compétences qui leur semble manquer
    2. Les membres de l'équipe complètent leur colonne
    3. La personne en charge de l'exercice analyse les résultats pour identifier les _single-man-army_,
       ainsi que les opportunités de transmission de connaissance (lorsque les appétences apprendre/transmettre se rejoignent)
    4. Un court point de restitution à l'équipe est organisé pour proposer du _pairing_ sur les domaines "à risque"
- **critères** pour définir s'il est pertinent d'indiquer une compétence dans la matrice :
    * est-ce qu'en l'absence de cette compétence, l'équipe serait incapable d'effectuer correctement le RUN d'un asset ?
    * est-ce qu'en l'absence de cette compétence, une partie du "périmètre fonctionnel" (domaine) de l'équipe ne serait pas maîtrisé ?
- **légende** : il encouragé d'indiquer les compétences que vous souhaitez développer, ainsi que celles que vous maîtrisez pour lesquelles vous pourriez accompagner d'autres membres de l'équipe
    * 🟡 : pas de connaissances ou connaissances très basiques sur le sujet
    * 🟢 : capable de contribuer, seul ou en binôme, de traiter des issues, de répondre au support
    * ⭐ : capable de régler des bugs complexes ou des incidents, de concevoir des solutions de bout en bout, d'aider les autres.
    * 😊 : le sujet vous intéresse et vous aimeriez en apprendre plus si l'occasion se présente
    * 👨‍🏫 : vous pouvez aider vos camarades à en apprendre plus sur le sujet
- calcul du **Truck Factor** (susceptibilité à la perte d'un membre de l'équipe) :
    * ✔️ : OK, au moins 2 personnes maîtrisent
    * ⚠️ : Attention, une seule personne maîtrise, ou aucune ne maitrise et trop peu de membres de l'équipe sont autonomes sur le sujet
    * 🚨 : Uh oh, même sans « perturbation », l'équipe n'est pas autonome

### Outils
- cf. https://chezsoi.org/shaarli/?searchterm=&searchtags=Recruting
- http://collabedit.com
- https://sharemycode.fr (éditable uniquement par le 1er visiteur)

### Language-based question
- Python:
  * [Reddit: What are the top 10 key features/"advanced" topics of Python you would expect a senior python developer to know?](https://www.reddit.com/r/Python/comments/6wl0qk/what_are_the_top_10_key_featuresadvanced_topics/)
  * [Python interview questions for Junior / Middle / Senior devs](https://luminousmen.com/post/6)
