Open source challenges
=====================

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

## Methodologies/advices
...to make both entreprise-internal & public OSS projects successful:

- basic repo documentation: README.md, LICENSE, CONTRIBUTORS.md, CONTRIBUTING.md, CHANGELOG.md, Architecture.md, .github/ISSUE_TEMPLATE, .github/PULL_REQUEST_TEMPLATE
cf. https://github.com/todogroup/repolinter
  * README templates: https://open-source-guide.18f.gov/making-readmes-readable/ https://gist.github.com/PurpleBooth/109311bb0361f32d87a2
  * CONTRIBUTING.md content: https://opensource.guide/starting-a-project/#writing-your-contributing-guidelines

- other tools:
  * pre-launch checklist: https://opensource.guide/starting-a-project/#your-pre-launch-checklist
  * Licensee: detect under what license a project is distributed (Ruby) -> https://github.com/benbalter/licensee
  * https://github.com/facebook/mention-bot : Automatically mention potential reviewers on pull requests.
  * a curated list: https://github.com/todogroup/awesome-oss-mgmt

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
  * maintain a list of easy bugs
  * have open channels for communication, and encourage people ask questions in it (ex: https://framateam.org)
  * celebrate new contributors
  * empathize
  * mentoring
  * create easy bugs
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

- define some clear (S.M.A.R.T. ?) goals, e.g.:
  * have 1 in-house core contributor of a "big" FLOSS project used by the company
  (define a shortlist 1st, maybe as an internal vote ?)
  * organize a contribution sprint on a FLOSS project in the entreprise, but invite outsider developpers
  * have X contributions to external FLOSS projects by collaborators merged this year
  (a vote could also be cast to collect ideas for contributions / or a page maintained)

### Websites dedicated to the subject
- https://opensource.guide/
- https://opensource.com/resources:
  * [How to build an open source community](https://opensource.com/life/13/9/how-build-open-source-community)
  * [How to self-promote your open source project](https://opensource.com/business/13/2/self-promoting-open-source-projects)
    1. Ease into self promotion with shameless plugs
    2. Use the buddy system
    3. Market the project, not yourself
    4. Highlight your contributions
    5. Speak to be heard, social media is your megaphone
- http://todogroup.org/blog/
- https://codecuriosity.org/faq
  * "Automated scoring is done on commits, comments and opening an issue today."
  * "You will be able to see only those repositories that have more than 25 stars"
  * "Organization contributions are not counted (yet) and commits as collaborator to another repository is not counted." (from FAQ)
- https://www.codetriage.com
- http://blog.smile.fr (actualité FR)

### Copyleft licenses contamination from dependencies

Si votre projet a des dépendances, veillez à analyser leurs licenses.
Des outils existent pour automatiser cela si vous avez des dépendances en cascade (note: certains se basent sur le standard [SPDX](https://spdx.org)):

- https://github.com/nexB/scancode-toolkit : développé en Python mais "language-agnostic" quant au code source analysé
- https://www.npmjs.com/package/licensecheck : développé en NodeJS, pour des projets NodeJS
- https://github.com/fossology/fossology : conteneur Docker dispo, développé en PHP, mais "language-agnostic" quant au code source analysé
- https://docs.sonarqube.org/display/SCAN/Analyzing+with+SonarQube+Scanner+for+Maven : plugin maven pour SonarQube, pour analyser les dépendances de pom.xml

Typiquement, si une de vos dépendances est sous une license copyleft (ex: GPL & AGPL), vous devez utilisez cette license (ou une license compatible) pour votre projet.

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
Par Tangui Morlier

4 libertés qui définissent le Logiciel Libre en entreprise [1]:
- la liberté d'utiliser, sans condition
- la liberté d'étudier le logiciel
- la liberté de modifier
- la liberté de diffuser

+ des obligations:
- respect du droit d'auteur: vous n'avez pas le droit de dire que c'est vous qui l'avez fait
- devoir contributif, facultatif ou non:

Pourquoi une entreprise a des avantages à faire du logiciel libre ?
- améliore la sécurité (cf. anecdote)
- véhicule l'expertise (ex: Sensio avec Symphony)

### Producing Open Source Software: How to Run a Successful Free Software Project
By Karl Fogel

> Opening up means arranging the code to be comprehensible to complete strangers, setting up a development web site and email lists, and often writing documentation for the first time. All this is a lot of work. And of course, if any interested developers do show up, there is the added burden of answering their questions for a while before seeing any benefit from their presence.

### The Dramatic Consequences of the Open Source revolution - Heather Miller

Our day-to-day, digital infrastructure is similar to our physical one

In case of physical infra issues:
1. some citizen report it
2. local government fixes it

Les solutions open-source sont utilisées par 78% des entreprises sondées,
et 66% envisagent d'abord les solutions open-source (Black Duck report 2015)

> I always assumed, (as had the rest of the world) that the OpenSSL team was large, active and well rsourced
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