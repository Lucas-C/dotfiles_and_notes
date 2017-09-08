Project management best practices
=================================

## References
- [PP] : The Pragmatic Programmer : Chapter 7 "Before the project" - Andrew Hunt & David Thomas
- [VisualSpec](http://www.targetprocess.com/articles/visual-specifications.html)
- [ProductOwnership](https://blog.codecentric.de/en/2014/07/devops-product-ownership/)
- [NorrisNumbers](http://www.teamten.com/lawrence/writings/norris-numbers.html)
- [EvidenceBasedScheduling](http://www.joelonsoftware.com/items/2007/10/26.html)
- [NoHourlyTimeTrackingInSoftware](http://bocoup.com/weblog/developer-weeks/)
- [DieScrum] : [Why Scrum Should Basically Just Die In A Fire](http://gilesbowkett.blogspot.com.au/2014/09/why-scrum-should-basically-just-die-in.html)
- [Log-driven programming](http://antirez.com/news/51)
- [TechnologyRadar](http://nealford.com/memeagora/2013/05/28/build_your_own_technology_radar.html) + [visualization](https://github.com/bdargan/techradar)
- [ThoughbotPlaybook](http://playbook.thoughtbot.com)
- [OnUseCasesAndUserStories](http://www.batimes.com/articles/user-stories-and-use-cases-dont-use-both.html)
- [ChooseBoringTechnology](http://mcfunley.com/choose-boring-technology)
- [RetrospectiveWiki](http://retrospectivewiki.org/index.php?title=Main_Page)
- [10 reasons not to adopt this new toy techno in production](https://translate.google.fr/translate?sl=auto&tl=en&js=y&prev=_t&hl=fr&ie=UTF-8&u=http%3A%2F%2Feax.me%2Favoid-new-toys%2F&edit-text=)
- [TheFailureOfAgileAndGROWS](http://blog.toolshed.com/2015/05/the-failure-of-agile.html)
- [Les développeurs Heisenberg](http://blog.ticabri.com/blog/2015/04/21/les-developpeurs-heisenberg/) - TL;DR Vous ne pouvez pas observer un développeur sans en altérer son comportement.
- "flow-breaking interruptions & effectiveness of an org / number of engineers devoted to an Engineering Effectiveness team" : http://www.gigamonkeys.com/flowers/
- [No bullshit : What is Scrum ?](https://www.youtube.com/watch?v=jNhRX-RBs_4)
- [AYoungLadysPrimerToTechnicalDecisionMaking](https://speakerdeck.com/charity/a-young-ladys-primer-to-technical-decision-making)
- [LawOfTriviality_aka_bikeshedding](https://en.wikipedia.org/wiki/Law_of_triviality)
- [HypeDrivenDevelopment](https://blog.daftcode.pl/hype-driven-development-3469fc2e9b22)
- [QuelquesConseilsPourAméliorerVotreProcessDeChoixDOutil](http://blog.octo.com/quelques-conseils-pour-ameliorer-votre-process-de-choix-doutil/)
- [ScalingOpenSourceCommunities](http://buytaert.net/scaling-open-source-communities)
- [BogBody:CommittingToOpenSource](https://oisinh.wordpress.com/2011/08/26/bog-body-committing-to-open-source/?)
- [YouAreNotGoogle](https://blog.bradfieldcs.com/you-are-not-google-84912cf44afb)
- [4StepsToCreatingAThrivingOpenSourceProject](https://opensource.com/life/15/5/4-steps-creating-thriving-open-source-project)
- [HowToCreateASuccessfulOpenSourceProject](https://ipg.host.cs.st-andrews.ac.uk/monty/open-source-project-andrews.pdf)
- [TheProblemsWithOpenSourceAndHowToFixThem](http://blog.fogcreek.com/the-problems-with-open-source-and-how-to-fix-them-interview-with-justin-searls/)
- [MakingYourOpenSourceProjectNewcomerFriendly](https://manishearth.github.io/blog/2016/01/03/making-your-open-source-project-newcomer-friendly/)
- [LeLogicielLibreEtLEntrepriseParTanguiMorlier](http://www.april.org/le-logiciel-libre-et-lentreprise-par-tangui-morlier-lup-le-5-novembre-2010)
- [MotivationGovernanceAndTheViabilityOfHybridFormsInOpenSourceSoftwareDevelopment](http://climate-action.engin.umich.edu/figures/Rood_Library/Shah_open_source_governance_2006.pdf)
- [To gamify or not to gamify community](https://opensource.com/business/16/9/gamify-or-not-gamify-community)
- [Are we there yet: is open source gamification enterprise ready?](http://www.gameffective.com/is-open-source-gamification-enterprise-ready/)

### "Comment manager des Geeks" Agilité, Méthodologie & Tests - Luc Legardeur - Devoxx Paris 2015
- Bien définir les valeurs de l'entreprise (ex: Xebia : des logiciels de haute qualité)
- Regrouper les gens par centre d'intérêt plutôt que par hiérarchie, créer des communautés
- Un/des dej par semaine open avec les collaborateurs en one-to-one
- Evolution de projet/carrière/etc. fréquente.
- 1 journée par mois en mode "quicky/échange/etc."
- Fêter les petites victoires comme les grandes !
- Processus de recrutement exigent : coding, 2h de review, etc.

## Choosing the right techno
- [AYoungLadysPrimerToTechnicalDecisionMaking]
- [QuelquesConseilsPourAméliorerVotreProcessDeChoixDOutil]
- cf. [TechnologyRadar] & its innovation adoption lifecycle
- [ChooseBoringTechnology] :
    - "let's say every company gets about three innovation tokens"
    - "Your job is keeping the company in business, god damn it. And the "best" tool is the one that occupies the "least worst" position for as many of your problems as possible. It is basically always the case that the long-term costs of keeping a system working reliably vastly exceed any inconveniences you encounter while building it. Mature and productive developers understand this."
    - "Technology for its own sake is snake oil"
- compare projects on their maturity / current activity & liveliness / community :
    commits count
    creation date
    last commit date
    issues count
    contributors count
- cf. [10 reasons not to adopt this new toy techno in production]
- OSS projects comparator: https://www.openhub.net/p/_compare?project_0=cURL&project_1=Wget
- [HypeDrivenDevelopment]
- [YouAreNotGoogle]: "This is not how rational people make decisions, but it is how software engineers decide to use MapReduce." - "you got there through a ritualistic belief that imitating the giants would bring the same riches." - "As of 2016, Stack Exchange served 200 million requests per day, backed by just four SQL servers"
UNPHAT:
- Understand the problem
- eNumerate multiple candidate solutions, don’t just start prodding at your favorite!
- consider a candidate solution, then read the Paper if there is one
- determine the Historical context in which the candidate solution was designed or developed
- weigh Advantages against disadvantages
- Think: how well this solution fits your problem ?

## Design
- interface design + decoupling >>more critical>> component design [MVB]
- start from a POC / MVP. [MVB]: "come with code" -> proof of concept + momentum + build motivation
- + Diagrams !
- Team design : Google Ventures' Product Design Sprints, cf. [ThoughbotPlaybook]

## Requirements
- write a one-pager summing up:
    - the stakes, the problem, the success criteria
    - the high level requirements, user stories
    - the high level design & architecture
    - the dependencies and required preconditions / assumptions
    - high level project planning
- don't gather requirements, **dig** for them [PP]
- whenever possible, **become** a user, else work with one to think like him [PP]
- separate policy concerns from requirements [PP]
- don't **overspecify**. Good requirements remain _abstract_. They are not archictecture, design nor UI. They are **needs** [PP]
- keep track of requirements growth to spot features creep/bloat [PP]
- don't fall into the specifications spiral [PP]. A tech lead primary contribution is to say NO to features that are not needed [NN]
- formal methods (CASE, waterfall, spiral model, UML...) have some serious shortcomings [PP]
- [VisualSpec]
    * do: sketches, flows, storyboard, paper prototype, short narratives, wireframe (e.g. Axure RP, tsx/shireframe, or Keynote as Thib did)
    * don't: behavior-Driven Development, pseudo-narrative
    * do if enough time: live prototype, animation
- maintain a project glossary [PP]. Document the vocabulary used in the domain and shared with clients, to avoid ambiguity (from [ThoughbotPlaybook])
- Agile recommend using user stories over UML use cases (that can be drawn with e.g. PlantUML). Use cases are NOT a form a requirements, just an illustration of them. They are NOT Agile, user stories are. Cf. [OnUseCasesAndUserStories]

## Agile
[TheFailureOfAgileAndGROWS]

### Stories
Stories should be clearly defined so there aren’t any misunderstandings between the Development Team and Product Owner about what is being delivered.

A story usually includes:
- Text Description:
The description is often phrased as: “As an X I would like Y because of Z…”. It should explain what is being done for whom and why it is being done.
- Acceptance Criteria:
The acceptance criteria are a list items which are unambiguously either done or not done. The Story is considered to be done at the end of the Sprint if and only if all of the acceptance criteria have been met.

A story may also include:
- Assumptions
Any assumptions without which the story would be difficult or impossible to implement. For example, a Story may assume another related Story has been completed.
- Not Included
If there is any possibility of misunderstanding what is included, it is sometimes helpful to explicitly enumerate what is not included in the Story.

#### Sub-story
The smallest unit of work that has value for our customers

## Personal tasks management
- Etherpad is great: it gives flexibility, a copy/paste scratchpad, hyperlinks, a persistent history of changes, multi-users access and plenty of plugins
- For tips on priotizating issues of a service: _cf._ [ProductOwnership]
- [Log-driven programming] > nested-thinking: never interrupt the flow, take notes of subtasks you'll achieve later on
- Pomodoro Technique: use a timer to break down work into ~25min intervals separated by short breaks

## Team tasks management
- [EvidenceBasedScheduling]
- [DieScrum]
- [NoHourlyTimeTrackingInSoftware]
- la [Roue de Deming](https://fr.wikipedia.org/wiki/Roue_de_Deming) : Plan-Do-Check-Act
- To evaluate a project progress : SEMAT Essence (Software Engineering Method and Theory)
cf. the [game cards](http://www.ivarjacobson.com/alphastatecards/)
![](http://semat.org/wp-content/uploads/2013/03/spiral.png)
- la règles des 3 emails: au délà, téléphonez ou déplacer vous pour discuter en personne
- attention à [LawOfTriviality_aka_bikeshedding]

### Methodologies
- CMMI = Capability Maturity Model Integration
- RUP = Rational Unified Process, and its lightweight Agile version: OpenUP
- 2TUP = 2 Tracks Unified Process, aka cycle en Y

## User-testing
- User Interviews & Usability Testing: cf. [ThoughbotPlaybook]

## Open-Source projects
Methodologies/advices to make both entreprise-internal & public OSS projects successful:

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
"the most promising solution for Open Source is known as "privileged groups". Privileged groups are those who receive "selective benefits"."
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
