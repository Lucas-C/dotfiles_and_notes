Open source challenges
=====================

::: toc
[[toc]]
:::

## References
- [ScalingOpenSourceCommunities](http://buytaert.net/scaling-open-source-communities)
- [4StepsToCreatingAThrivingOpenSourceProject](https://opensource.com/life/15/5/4-steps-creating-thriving-open-source-project)
- [HowToCreateASuccessfulOpenSourceProject](https://ipg.host.cs.st-andrews.ac.uk/monty/open-source-project-andrews.pdf)
- [TheProblemsWithOpenSourceAndHowToFixThem](http://blog.fogcreek.com/the-problems-with-open-source-and-how-to-fix-them-interview-with-justin-searls/)
- [MakingYourOpenSourceProjectNewcomerFriendly](https://manishearth.github.io/blog/2016/01/03/making-your-open-source-project-newcomer-friendly/)
- [LeLogicielLibreEtLEntrepriseParTanguiMorlier](http://www.april.org/le-logiciel-libre-et-lentreprise-par-tangui-morlier-lup-le-5-novembre-2010)
- [MotivationGovernanceAndTheViabilityOfHybridFormsInOpenSourceSoftwareDevelopment](http://climate-action.engin.umich.edu/figures/Rood_Library/Shah_open_source_governance_2006.pdf)
- [To gamify or not to gamify community](https://opensource.com/business/16/9/gamify-or-not-gamify-community)
- [Are we there yet: is open source gamification enterprise ready?](http://www.gameffective.com/is-open-source-gamification-enterprise-ready/)
- [freeCodeCamp guide to contribute to Open Source](https://github.com/freeCodeCamp/how-to-contribute-to-open-source) projects for newcomers
- [Six things to know about successful open-source software](https://knightlab.northwestern.edu/2013/07/24/six-lessons-on-success-and-failure-for-open-source-software/)
- [Open Source is awful](https://steemit.com/opensource/@crell/open-source-is-awful)
- [Comparison of 7 governance models for CPython by Victor Stinner](https://discuss.python.org/t/comparison-of-the-7-governance-peps/392)
- [The Meme Hustler - Tim O’Reilly’s crazy talk | Evgeny Morozov - The Baffler](https://thebaffler.com/salvos/the-meme-hustler)
- [The struggles of an open source maintainer - @antirez](http://antirez.com/news/129)
- [How to Create an Open Source Program](https://github.com/todogroup/guides/blob/master/creating-an-open-source-program.md)

## Resources for newcomers
- [freeCodeCamp guide to contribute to Open Source]
- Roshan Jossey repo so that newcomers can make their very first PR: https://github.com/Roshanjossey/first-contributions/blob/master/README.md

## Methodologies/advices
...to make both entreprise-internal & public OSS projects successful:

- Eric S. Raymon 1st lesson for creating good open source software:
> Every good work of software starts by scratching a developer's personal itch.

- basic repo documentation: README.md, LICENSE, CONTRIBUTORS.md, CONTRIBUTING.md, CHANGELOG.md, Architecture.md, .github/ISSUE_TEMPLATE, .github/PULL_REQUEST_TEMPLATE
cf. https://github.com/todogroup/repolinter
  * README templates: https://open-source-guide.18f.gov/making-readmes-readable/ https://gist.github.com/PurpleBooth/109311bb0361f32d87a2
  * CONTRIBUTING.md content: https://opensource.guide/starting-a-project/#writing-your-contributing-guidelines
  * [ARCHITECTURE.md](https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html): "specify only things which are unlikely to frequently change" - "Start with a bird’s eye overview of the problem being solved" - "Do name important files, modules, and types" - "Explicitly call-out architectural invariants" - "Point out boundaries between layers and systems as well"

- other tools:
  * pre-launch checklist: https://opensource.guide/starting-a-project/#your-pre-launch-checklist
  * [Licensee](https://github.com/benbalter/licensee): detect under what license a project is distributed (Ruby) - Alt: https://github.com/pivotal/LicenseFinder (Python / NodeJS / Go / Java) - https://github.com/davglass/license-checker (NodeJS)
  * curated lists:
    - https://opensource.guide/best-practices/#bring-in-the-robots : include `mention-bot`, `no-response` or `stale`, `dependabot-preview`...
    - https://github.com/todogroup/awesome-oss-mgmt
    - https://www.linuxfoundation.org/tools-managing-open-source-programs/ include project health, stats & dashboard tools

- [ScalingOpenSourceCommunities] -> free-rider problem: when to many people uses an Open Source software project without contributing to it
> the most promising solution for Open Source is known as "privileged groups". Privileged groups are those who receive "selective benefits".
ex: "prominently showcase devs contributions & bug fixes"

- [BogBody:CommittingToOpenSource] -> A key aspect: patronage in OSS -> "those receiving patronage want to practice their craft. Those giving patronage want to enhance their reputation amongst their industry peers"
Point out the need for Community Managers

- [4StepsToCreatingAThrivingOpenSourceProject] by Andrey Petrov, urllib3 author

> Having a great README is basically 80% of the work to success. You need to be able to answer three questions for your contributors: "Who else uses it?" "What do they use it for?" and "Where can I get more help?"

> In order to help build interest, Andrey reached out to people on Twitter and offered free Go programming lessons in exchange for opening pull requests.

> Accept pull requests very generously, and very graciously

Market and promote your project:

    * write blog posts on Medium
    * answer questions on Stack Overflow (set up alerts on Stack Overflow / Google Alerts for specific topics)
    * participate in discussions on Hacker News, reddit/r/programming, etc.
    * sell to other open source projects and establish partnerships with them. "The only reason urllib3 is the most popular third-party Python library today is because it's part of requests."
    * feed the non-trolls: Getting upvotes on your announcement post is only half the equation. More activity and discussion yields more people clicking on it and more updates, so if you respond to almost every comment, then that's 2x as many comments.

- [HowToCreateASuccessfulOpenSourceProject] by MySQL & MariaDB founder:
  * it's not just software
  * you need a good team and active community
  * transparency is critical for long time success
  * communicate with your community
  * be good open source citizens
  * you need to get the product out there and used!

- [TheProblemsWithOpenSourceAndHowToFixThem] by Justin Searls, excellent read

- [MakingYourOpenSourceProjectNewcomerFriendly]:
  * mention steps for getting involved in your CONTRIBUTING.md
  * create & maintain a list of easy bugs
  * have open channels for communication, and encourage people ask questions in it (ex: https://framateam.org)
  * celebrate new contributors
  * empathize
  * mentoring
  * discoverability of bugs
  * "programs like Google Summer of Code and Outreachy provide ways for new contributors to try out your project at a significant level of involvement"

- [MotivationGovernanceAndTheViabilityOfHybridFormsInOpenSourceSoftwareDevelopment]:

> The primary reasons cited by need-based participants for contributing code include reciprocity ("Others helped me, so I should help them"), future improvements (get feedback, improve their code), source code commits ("so that their functional needs will continue to be met as the software evolves"), and career concerns ("reputation, skill development...")

> Over half of long-term open source participants describe their open source work as a fun and challenging hobbylike activity

> Contribution is necessary to obtain feedback affirming that one’s activities are useful to others

> Time, too much have you
> Major geeks these people are
> Boss know you do this? :)

- project governance models: cf. https://opensource.guide/leadership-and-governance/
  * benevolent dictator: there is an identified project facilitator
  * meritocracy / liberal contribution: everyone (with merit) commits and is responsible for everything
  * Tech Lead + Core Committers: à la Google AMP
  * _cf._ [Comparison of 7 governance models for CPython by Victor Stinner]

- [Are we there yet: is open source gamification enterprise ready?] by Gal Rimon & [To gamify or not to gamify community] by Jono Bacon -> lesssons learned:
  * Gamification is not just about trophies
  * Reward is important, but so is discovery
  * Gamification is a helpful onboarding tool
  * gamification should go beyond simplistic PBL (Points. Badges, Leaderboards)
  * interesting discussion on Reddit, mostly arguing it's a bad idea: https://www.reddit.com/r/linux/comments/52mna6/to_gamify_or_not_to_gamify_community/
Also: https://openbadges.org

- personal advice: invest in mentoring & publishing a wish-list of sexy+well-defined features, like a real OSS project product owner !
  * the scope of this feature is...
  * by implementing this feature YOU, as a benevolent OSS developper, will help X people/improve the quality of Y/make this compatible with Z...
  * by working on this, YOU will learn from experimented user @toto the following skills: ...

- define some clear (S.M.A.R.T. ?) goals, cf. https://www.linuxfoundation.org/measuring-your-open-source-program-success/#3, e.g.:
  * have 1 in-house core contributor of a "big" FLOSS project used by the company
  (define a shortlist 1st, maybe as an internal vote ?)
  * organize a contribution sprint on a FLOSS project in the entreprise, but invite outsider developpers
  * have X contributions to external FLOSS projects by collaborators merged this year
  (a vote could also be cast to collect ideas for contributions / or a page maintained)

- [Six things to know about successful open-source software] from a 2012 study by Charles Schweik and Robert English:
  * Most open-source projects are not successful
  * Successful projects have some common characteristics:
    - A "relatively clearly defined vision and a mechanism to communicate the vision early in the project's life"
    - A clearly defined set of users who have a need that can be met by the software
    - Well-articulated and clear goals established by the project's leaders
    - Good project communication -- a quality website, good documentation, a bug-tracking system and a communication system such as an email list or forum.
    - Once a project has achieved its initial release, a software architecture that is modular
  * Open-source projects flourish when developers are also users of the software


### credentials / passwords / secrets detection in source code:
- [dxa4481/truffleHog](https://github.com/dxa4481/truffleHog)
- [landscapeio/dodgy](https://github.com/landscapeio/dodgy)
- [Yelp/detect-secrets](https://github.com/Yelp/detect-secrets)
- [awslabs/git-secrets](https://github.com/awslabs/git-secrets)
- [auth0/repo-supervisor](https://github.com/auth0/repo-supervisor)


### GitHub
- Github configuration as code: https://github.com/probot/settings
- [dump_github_org_perms.py](https://github.com/Lucas-C/dotfiles_and_notes/blob/master/languages/python/dump_github_org_perms.py) & [activedirectory_github_sync.py](https://github.com/Lucas-C/dotfiles_and_notes/blob/master/languages/python/activedirectory_github_sync.py)
- Contributor License Agreement Bots: https://github.com/cla-assistant/cla-assistant & https://github.com/salesforce/salesforce-cla
- use Github tags to welcome & attract newcomers: `first-timers-only` `trivial` `beginner` `easy pick` `good first issue` `good-first-bug` `starter` `easy fix` `new contributor` `up-for-grabs` `your-first-pr`
    * bonus: reference your project on http://up-for-grabs.net & https://www.codetriage.com & badge http://www.firsttimersonly.com
- [GitHub repo social media preview](https://docs.github.com/en/github-ae@latest/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview)
- [techgaun/active-forks](https://github.com/techgaun/active-forks): find the most active forks of a repository


### Gitlab
- [GitLab Ultimate & Gold free for open source](https://about.gitlab.com/2018/06/05/gitlab-ultimate-and-gold-free-for-education-and-open-source/)
- [Gitlab AutoDevops](https://docs.gitlab.com/ce/topics/autodevops/)


### Websites dedicated to the subject
- https://sustainoss.org reports
- https://opensource.guide
- https://opensource.com/resources:
  * [How to build an open source community](https://opensource.com/life/13/9/how-build-open-source-community)
  * [How to self-promote your open source project](https://opensource.com/business/13/2/self-promoting-open-source-projects)
    1. Ease into self promotion with shameless plugs
    2. Use the buddy system
    3. Market the project, not yourself
    4. Highlight your contributions
    5. Speak to be heard, social media is your megaphone
- https://www.linuxfoundation.org/resources/open-source-guides/
- http://todogroup.org/blog/
- https://codecuriosity.org/faq
  * "Automated scoring is done on commits, comments and opening an issue today."
  * "You will be able to see only those repositories that have more than 25 stars"
  * "Organization contributions are not counted (yet) and commits as collaborator to another repository is not counted." (from FAQ)
- https://www.codetriage.com
- http://linuxfr.org & https://cercll.wordpress.com/ (actualités FR)
- https://www.theopensourceway.org
  * [Organizing a community - checklist](https://www.theopensourceway.org/wiki/Organizing_a_community_-_checklist)
  * [Books you should read](https://www.theopensourceway.org/wiki/Books_you_should_read)
  * [Guidelines outline](https://github.com/theopensourceway/guidebook/blob/master/OUTLINE.adoc)


### Funding, financing
- https://opencollective.com/learn-more : "Open your finances to your community"
- demandes de subvention européenne : https://nlnet.nl/propose/


### Cons
[Open Source is awful]:
> I used to think Open Source was amazing. I've since come to realize just how awful it is.

> First, I need to draw a clear distinction between three often-confused concepts: Free Software, Open Source, and Volunteer Coding.

> We love to encourage developers to get involved; "give back" is the mantra.

> That is simply the polite way of saying "do work for free and we'll pay you in exposure". We all know that's called exploitation

> My code is free — my time is not.


### Copyleft licenses contamination from dependencies
Si votre projet a des dépendances, veillez à analyser leurs licenses.
Typiquement, si une de vos dépendances est sous une license copyleft (ex: GPL & AGPL), vous devez utilisez cette license (ou une license compatible) pour votre projet.

- [GNU licenses compatibility matrix](https://www.gnu.org/licenses/gpl-faq.en.html#AllCompatibility)
- [Reports of GPLv3 and AGPLv3 "virality" are greatly exaggerated](https://softwareengineering.stackexchange.com/a/314908/157979) :
  * If you use a library X that comes under GPLv3 or AGPLv3, modify its source code, but still use it as a library,
  you have to make available the modified source code of X (but not any other part of your overall application)
  if you distribute your own application and X has GPLv3 or AGPLv3.
  * Richard Stallman likes the idea that all software should be free, but he does not claim infectiousness of GPL code.
  He says "The GPL's domain does not spread by proximity or contact, only by deliberate inclusion of GPL-covered code in your program."

#### Automated analysis
Des outils existent pour automatiser cela si vous avez des dépendances en cascade (note: certains se basent sur le standard [SPDX](https://spdx.org)):

- https://reuse.software/comparison/
- https://github.com/nexB/scancode-toolkit : développé en Python mais "language-agnostic" quant au code source analysé
- https://www.npmjs.com/package/licensecheck : développé en NodeJS, pour des projets NodeJS
- https://github.com/fossology/fossology : conteneur Docker dispo, développé en PHP, mais "language-agnostic" quant au code source analysé
- https://docs.sonarqube.org/display/SCAN/Analyzing+with+SonarQube+Scanner+for+Maven : plugin maven pour SonarQube, pour analyser les dépendances de pom.xml
- https://wiki.debian.org/CopyrightReviewTools : Debian copyright review tools


### Lessons learned from "The Architecture of Open Source Applications"
This is a personal selection:
- [Berkeley DB by Margo Seltzer & Keith Bostic](http://aosabook.org/en/bdb.html)
  * choose upgrade battles carefully. Don't hide them to users, highlight them and make sure they break old code at compile time
- [SocialCalc by Audrey Tang](http://aosabook.org/en/socialcalc.html):
  * Chief Designer with a Clear Vision
  * Wikis for Project Continuity
  * Always Have a Roadmap
  * Distribute Knwoledge
- [VisTrails](http://aosabook.org/en/vistrails.html)
  * "The initial feedback and the encouragement we received from these users was instrumental in driving the project forward",
  * "most features in the system were designed as direct response to user feedback",
  * "being responsive to users does not necessarily mean doing exactly what they ask for"


### Le Logiciel Libre Et L'entreprise
_cf._ [LeLogicielLibreEtLEntrepriseParTanguiMorlier](http://www.april.org/le-logiciel-libre-et-lentreprise-par-tangui-morlier-lup-le-5-novembre-2010)

Par Tangui Morlier

4 libertés qui définissent le Logiciel Libre en entreprise [1]:
- la liberté d'utiliser, sans condition
- la liberté d'étudier le logiciel
- la liberté de modifier
- la liberté de diffuser

+ des obligations:
- respect du droit d'auteur: vous n'avez pas le droit de dire que c'est vous qui l'avez fait
- devoir contributif, facultatif ou non

Pourquoi une entreprise a des avantages à faire du logiciel libre ?
- améliore la sécurité (cf. anecdote)
- véhicule l'expertise (ex: Sensio avec Symphony)


### Open Source Monitor 2023
Rapport PDF accessible ici : [Open Source Monitor 2023](https://numeum.fr/actu-informatique/etude-lusage-de-lopen-source-en-france-open-source-monitor-2023)

Le modèle open-source est promu par les institutions françaises : <https://code.gouv.fr/fr/bluehats/>

[La stratégie open source de RTE](https://code.gouv.fr/fr/bluehats/rte/)



### Producing Open Source Software: How to Run a Successful Free Software Project
By Karl Fogel, 2005-2023 - https://producingoss.com
Traduit par Framasoft en français : https://framabook.org/produire-du-logiciel-libre-2/

#### Chapter 1 - Introduction

> An open license does not guarantee that hordes of active developers will suddenly devote their time to your project

> Opening up means arranging the code to be comprehensible to complete strangers, setting up a development web site and email lists, and often writing documentation for the first time. All this is a lot of work. And of course, if any interested developers do show up, there is the added burden of answering their questions for a while before seeing any benefit from their presence.

> software, unlike other creative forms like prose or the visual arts, must pass semi-objective tests in order to be considered successful: it must run, and be reasonably free of bugs. This gives all participants in a project a kind of automatic common ground, a reason and a framework for working together without worrying too much about qualifications or motivations beyond the technical.

> If someone writes good code, you don't ask them whether they do it for moral reasons, or because their employer paid them to, or because they're building up their résumé, or whatever. You evaluate the contribution on technical grounds, and respond on technical grounds.

#### Chapter 2 - Getting started

> the very first thing a visitor learns about a project is what its home page looks like. Most of us can tell in one glance whether a home page was thrown together quickly or was given serious thought. This is the first piece of information your project puts out, and the impression it creates will carry over to the rest of the project by
association.

> By giving off this aura of preparedness, the project sends out a message: "Your time will not be wasted if you get involved," which is exactly what people need to hear.

> You and the other founders must decide what the project is really about — that is, decide its limitations, what it won't do as well as what it will — and write up a mission statement.

> For large projects, it is a good idea to own the project's name in as many of the relevant namespaces on the Internet as you can

> State That the Project is Free

> Features and Requirements List

> Development Status : Visitors usually want to know how a project is doing. For new projects, they want to know the gap between the project's promise and current reality. For mature projects, they want to know how actively it is maintained, how often it puts out new releases, how responsive it is likely to be to bug reports, etc.


### The Dramatic Consequences of the Open Source revolution - Heather Miller
Our day-to-day, digital infrastructure is similar to our physical one

In case of physical infra issues:
1. some citizen report it
2. local government fixes it

Les solutions open-source sont utilisées par 78% des entreprises sondées,
et 66% envisagent d'abord les solutions open-source (Black Duck report 2015)

> I always assumed, (as had the rest of the world) that the OpenSSL team was large, active and well resourced
Steve Marquess

64% of top Github open-source projects have a 1-2 truck factor (1-2 developpers are critical to those projects)
-> http://peerj.com/preprints/1233.pdf

Collective Code Construction Contract: https://rfc.zeromq.org/spec:42/C4

Contributing hackathon/sprint:
ahead of time, library author curates ~10 todos accomplishable in 3hours by newcomers


### Managing Open-Source contributions in large organizations - James Ward - Devoxx 2017
Why do open-source ?
* build trust with customers / partners
* create an ecosystem around a library / tool / framework
* unmerged internal forks of FLOSS projects are a maintenance nightmare
* show leadership in the software industry
* recruiting

Solutions:
* do nothing
* use a foundation
* build some tools

Full-time dedicated to FLOSS at Salesforce (~25 000 employees in 2017)

Process, process, process:
* outgoing contribution VS new FLOSS project ?
* in-take form (on internal website, triggers various actions)
* instructions/help on License stuff
* legal review (patent & license)
* security review
* engineering marketing team review
* Corporate Contributor License AGreement ?

Demo: Github CLA bot asking contributors to sign it


### Open Source Archetypes: A framework For Purposeful Open Source - May 2018 - moz://a
- Benefits of Open Source:
  * Lead a standardization effort in a particular area
  * Improve product quality
  * Amplify or expand developer base
  * Increase the size or quality of your organization’s developer hiring pool
  * Improve internal developer morale and retention
  * Improve internal collaboration within one’s own organization
  * Establish a basis for product reputation
  * Establish a basis for organizational brand and credibility
  * Stop someone else from establishing early dominance in an particular area
  * Engage with users
  * Provide transparency to customers and partners
- Open Source Project Archetypes:
  * Business-to-Business (B2B) Open Source
  * Multi-Vendor Infrastructure
  * Rocket Ship To Mars
  * Controlled Ecosystem
  * Wide Open
  * Mass Market
  * Specialty Library
  * Trusted Vendor
  * Upstream Dependency
  * Bathwater
- Questions to Consider:
  * How many separable open source pieces are there?
  * Who is expected to participate in the project, and why?
  * How is the code expected to be deployed?
  * How is the project managed and governed?
  * What is the project’s business model or sustainability model?
  * Which open source license does it use?
  * Does technical architecture match social structure?


### Open Source vs Logiciel Libre (Free as in "free speech")
History:
- [The Meme Hustler - Tim O’Reilly’s crazy talk | Evgeny Morozov - The Baffler]

> Stallman’s may not have been the best software on offer, but some sacrifice of technological efficiency was a price worth paying for emancipation.

> Any move to subject the fruits of developers’ labor to public regulation, even if its goal was to promote a greater uptake of open source software, must be opposed, since it would taint the reputation of open source as technologically and economically superior to proprietary software.

> As O’Reilly put it in 2010, “the art of promoting openness is not to make it a moral crusade, but rather to highlight the competitive advantages of openness.”

Licenses & related websites of interest:
- [Climate Strike Software](https://github.com/climate-strike/license)
- [The Hippocratic License](https://firstdonoharm.dev)
- https://tldrlegal.com
- https://choosealicense.com


### The struggles of an open source maintainer - @antirez
http://antirez.com/news/129 FROM https://github.com/nayafia/awesome-maintainers

> This creates an obvious congestion. Most people try to address it in the wrong way: using pragmatism. Let’s close the issue after two weeks of no original poster replies, after we ask some question. Close all the issues that are not very well specified. And other “inbox zero” solutions. The reality is that to process community feedbacks very well you have to take the time needed
> So what happens? That you start to prioritize more and more what to look at and what not. And you feel you are a piece of shit at ignoring so many things and people, and also the contributor believes you don’t care about what others have to give you. It’s a complex situation.

> Sometimes I just stop looking at issues and PRs for weeks, because I’m coding or designing: that is the work I really love and enjoy. However this in turn creates ways more pressure on me, psychologically. To do what I love and I can do well I’ve to feel like shit.

> the sum of the productivity of me working just when I want is greater than the productivity I’ve when I’m forced to work every day in a steady way.
