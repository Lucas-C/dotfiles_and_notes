Project management best practices
=================================

<!-- To update this Table Of Contents:
    markdown-toc --indent "    " --maxdepth 3 -i ProjectManagementBestPractices.md
-->

<!-- toc -->

- [References](#references)
    * ["Comment manager des Geeks" Agilité, Méthodologie & Tests - Luc Legardeur - Devoxx Paris 2015](#comment-manager-des-geeks-agilite-methodologie--tests---luc-legardeur---devoxx-paris-2015)
- [Choosing the right techno](#choosing-the-right-techno)
- [Technical debt](#technical-debt)
- [Design](#design)
- [Software migration from legacy](#software-migration-from-legacy)
- [Requirements](#requirements)
- [Agile](#agile)
    * [Stories](#stories)
    * [Studies](#studies)
- [Personal tasks management](#personal-tasks-management)
- [Team tasks management](#team-tasks-management)
    * [Methodologies](#methodologies)
- [User-testing](#user-testing)

<!-- tocstop -->

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
- [10 reasons not to adopt this new toy techno in production](https://translate.google.fr/translate?sl=auto&tl=en&js=y&prev=_t&hl=fr&ie=UTF-8&u=http%3A%2F%2Feax.me%2Favoid-new-toys%2F&edit-text=)
- [Les développeurs Heisenberg](http://blog.ticabri.com/blog/2015/04/21/les-developpeurs-heisenberg/) - TL;DR Vous ne pouvez pas observer un développeur sans en altérer son comportement.
- "flow-breaking interruptions & effectiveness of an org / number of engineers devoted to an Engineering Effectiveness team" : http://www.gigamonkeys.com/flowers/
- [No bullshit : What is Scrum ?](https://www.youtube.com/watch?v=jNhRX-RBs_4)
- [AYoungLadysPrimerToTechnicalDecisionMaking](https://speakerdeck.com/charity/a-young-ladys-primer-to-technical-decision-making)
- [LawOfTriviality_aka_bikeshedding](https://en.wikipedia.org/wiki/Law_of_triviality)
- [HypeDrivenDevelopment](https://blog.daftcode.pl/hype-driven-development-3469fc2e9b22)
- [QuelquesConseilsPourAméliorerVotreProcessDeChoixDOutil](http://blog.octo.com/quelques-conseils-pour-ameliorer-votre-process-de-choix-doutil/)
- [BogBody:CommittingToOpenSource](https://oisinh.wordpress.com/2011/08/26/bog-body-committing-to-open-source/?)
- [YouAreNotGoogle](https://blog.bradfieldcs.com/you-are-not-google-84912cf44afb)
- [Growing Your Tech Stack: When to Say No](https://blog.codeship.com/growing-tech-stack-say-no/)
- [EvolutionaryArchitecture](https://codeburst.io/evolutionary-architecture-27dae14b323d)
- [KnowledgeDebt](http://amir.rachum.com/blog/2016/09/15/knowledge-debt/)
- [A Taxonomy of Tech Debt](https://engineering.riotgames.com/news/taxonomy-tech-debt)
- [TechnicalDebtQuadrant by Martin Fowler](https://martinfowler.com/bliki/TechnicalDebtQuadrant.html)
- [Why "Agile" and especially Scrum are terrible](https://michaelochurch.wordpress.com/2015/06/06/why-agile-and-especially-scrum-are-terrible/)
- [How to Ensure You’re Working on the Most Important Items Each Iteration](https://www.mountaingoatsoftware.com/blog/how-to-ensure-youre-working-on-the-most-important-items-each-iteration)
- [In Pursuit of Production Minimalism](https://brandur.org/minimalism)
- [Run less software](https://www.intercom.com/blog/run-less-software/)
- [We already have nice things](https://opensource.com/article/18/10/nice-things)
- [La dette technique : une supercherie mythologique pour galériens de l’IT](https://medium.com/@waxzce/la-dette-technique-une-supercherie-mythologique-pour-gal%C3%A9riens-de-lit-7ed0dfbf39c7)
- [The Gartner Hype Cycle is … hype. Don’t use it as an excuse](https://davidgerard.co.uk/blockchain/2019/10/03/the-gartner-hype-cycle-is-hype-dont-use-it-as-an-excuse/)
- [5 arguments to make managers care about technical debt](https://understandlegacycode.com/blog/5-arguments-to-make-managers-care-about-technical-debt/)
- [Is tasking developers with creating detailed estimates a waste of company money?](https://iism.org/article/is-tasking-developers-with-creating-detailed-estimates-a-waste-of-company-money-42)
- [Agilité à grande échelle @ Spotify avec les Tribus, Brigades, Chapitres & Guildes](http://www.les-traducteurs-agiles.org/assets/fabrice_aimetti/SpotifyScaling_fr.pdf) mais [Spotify Doesn't Use the Spotify Model](https://www.agility11.com/blog/2020/6/22/spotify-doesnt-use-the-spotify-model)

### "Comment manager des Geeks" Agilité, Méthodologie & Tests - Luc Legardeur - Devoxx Paris 2015
- Bien définir les valeurs de l'entreprise (ex: Xebia : des logiciels de haute qualité)
- Regrouper les gens par centre d'intérêt plutôt que par hiérarchie, créer des communautés
- Un/des dej par semaine open avec les collaborateurs en one-to-one
- Evolution de projet/carrière/etc. fréquente.
- 1 journée par mois en mode "quicky/échange/etc."
- Fêter les petites victoires comme les grandes !
- Processus de recrutement exigeant : coding, 2h de review, etc.

## Choosing the right techno
- [AYoungLadysPrimerToTechnicalDecisionMaking] - Manifesto on slide 26:
    1. Technology serves the mission
    2. Reuse solutions
    3. Create friction for adding new components
    4. Choose boring technology, when you can
    5. Spend your risk tokens on key differentiators
    6. The longer you survive, the more operational impact trumps all
- [QuelquesConseilsPourAméliorerVotreProcessDeChoixDOutil]
- cf. [TechnologyRadar] & its innovation adoption lifecycle
- [ChooseBoringTechnology] :
> let's say every company gets about three innovation tokens

> Your job is keeping the company in business, god damn it. And the "best" tool is the one that occupies the "least worst" position for as many of your problems as possible. It is basically always the case that the long-term costs of keeping a system working reliably vastly exceed any inconveniences you encounter while building it. Mature and productive developers understand this.

> Technology for its own sake is snake oil

> Etsy in its early years suffered from this pretty badly.
> We hired a bunch of Python programmers and decided that we needed to find something for them to do in Python,
> and the only thing that came to mind was creating a pointless middle layer that required years of effort to amputate.
> Meanwhile, the 90th percentile search latency was about two minutes.
> Etsy didn't fail, but it went several years without shipping anything at all.

- [Run less software] :
> The art of choosing a standard technology is that when you encounter a new problem,
> you need to break it down into a series of subproblems that can be solved using your standard patterns and tools.

- compare projects on their maturity / current activity & liveliness / community :
  + commits count
  + creation date
  + last commit date
  + issues count
  + contributors count

- cf. [10 reasons not to adopt this new toy techno in production]
- OSS projects comparator: https://www.openhub.net/p/_compare?project_0=cURL&project_1=Wget & https://libraries.io
- [HypeDrivenDevelopment]
- [YouAreNotGoogle]: "This is not how rational people make decisions, but it is how software engineers decide to use MapReduce." - "you got there through a ritualistic belief that imitating the giants would bring the same riches." - "As of 2016, Stack Exchange served 200 million requests per day, backed by just four SQL servers"
UNPHAT:
  + Understand the problem
  + eNumerate multiple candidate solutions, don’t just start prodding at your favorite!
  + consider a candidate solution, then read the Paper if there is one
  + determine the Historical context in which the candidate solution was designed or developed
  + weigh Advantages against disadvantages
  + Think: how well this solution fits your problem ?
- [Growing Your Tech Stack: When to Say No] : Nice walk-through of consequences & risks estimation
> The right technology today will be the wrong technology at some point.
- [EvolutionaryArchitecture]:
  1. Build for the “now”: "Build to meet the needs for your near-term time horizon"
  2. Prefer evolution: "prefer the technological approach which gives you the maximum ability to modify / replace / evolve the architecture."

- [In Pursuit of Production Minimalism]
  * Over time, technologies are added, but are rarely removed. This effect is dangerous
  * Do more and more with less and less until eventually you can do everything with nothing.
  * To recognize the effort that went into tearing down or replacing old technology, we created a ritual where we symbolically fed dead components to a flame called a burn party
  * Mitigations
    + Retire old technology
    + Build common service conventions
    + Favor simplicity and reduce moving parts
    + Don’t use new technology the year that it’s initially released
    + Avoid custom technology
    + Use public services

- [We already have nice things], and other reasons not to write in-house ops tools
  + the "not invented here" (NIH) syndrome
  + Do you need to roll it yourself ?
    * Have we polled the greater ops community for solutions?
    * Have we compared the costs of proprietary tools to the estimated engineering time needed to maintain an in-house solution?
    * Have we identified open source solutions, even those that lack desired features, and attempted to contribute to them?
    * Can we fork any open source tools that are well-written but unmaintained?

- [The Gartner Hype Cycle is … hype. Don’t use it as an excuse]
> The problem is that the Hype Cycle isn’t science. Gartner present the Hype Cycle as if it’s a well-established natural law — and it just isn’t.

## Technical debt
- [A Taxonomy of Tech Debt]: "I define tech debt as code or data that future developers will pay a cost for." - Metrics:
  * impact : user-facing & developer-facing issues
  * (corollary, personnal) fix benefits : what improvments would a fix bring ?
  * fix cost : the measure must take into consideration risks
  * contagion : if this tech debt is allowed to continue to exist, how much will it spread?
=> IMHO: classifying between local debt / MacGyver debt (aka homogenization) / foundational debt / data debt does not bring much help in organizing the reduction of tech debt.
However, grouping elements of tech debts thematically may help to organize & prioritize tactical strikes on them
E.g. fix all the doc pain points, homogenize & securize all our DB requests, improve resiliency, etc.
- [TechnicalDebtQuadrant by Martin Fowler]:
> To my mind, the question of whether a design flaw is or isn't debt is the wrong question. [...] A particular benefit of the debt metaphor is that it's very handy for communicating to non-technical people.
- [asottile/git-code-debt](https://github.com/asottile/git-code-debt)
- [La dette technique : une supercherie mythologique pour galériens de l’IT] -> en terme de vocbulaire, mieux vaut parler de d'**investissement**
- [5 arguments to make managers care about technical debt]
> “Refactoring will reduce the volatility in the marginal cost of features”
> “In the last 3 months, we spent X% of development budget in fixing quality issues”
> “We took technical loans to ship faster, we need to pay back some debt to keep a low time-to-market”
> “We can reduce our turnover by investing 10% of our time in our code quality”
> “Investing 20% of budget in refactoring will cut FRT in half with a positive ROI on devs productivity”

## Design
- interface design + decoupling >>more critical>> component design [MVB]
- start from a POC / MVP. [MVB]: "come with code" -> proof of concept + momentum + build motivation
- + Diagrams !
- Team design : Google Ventures' Product Design Sprints, cf. [ThoughbotPlaybook]
- Event Storming

## Software migration from legacy
- one strategy: use a [teeproxy](https://github.com/chrislusf/teeproxy)
> You may have production servers running, but you need to upgrade to a new system. You want to run A/B test on both old and new systems
> to confirm the new system can handle the production load, and want to see whether the new system can run in shadow mode continuously without any issue.

> teeproxy is a reverse HTTP proxy. For each incoming request, it clones the request into 2 requests, forwards them to 2 servers.
> The results from server A are returned as usual, but the results from server B are ignored.

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
    * https://github.com/LisaDziuba/Awesome-Design-Tools
- maintain a project glossary [PP]. Document the vocabulary used in the domain and shared with clients, to avoid ambiguity (from [ThoughbotPlaybook])
Same recommendation from Domain Driven Design / Event Storming : **ubiquitous language**
- Agile recommend using user stories over UML use cases (that can be drawn with e.g. PlantUML).
  Use cases are NOT a form a requirements, just an illustration of them. They are NOT Agile, user stories are. Cf. [OnUseCasesAndUserStories]
- van Genuchten, 1991
> The two biggest causes of project failure are poor estimation an unstable requirements.

## Agile
[Why "Agile" and especially Scrum are terrible]:
- "the work gets atomized into “user stories” and “iterations” that often strip a sense of accomplishment from the work, as well as any hope of setting a long-term vision for where things are going."
Instead of working on actual, long-term projects that a person could get excited about, they’re relegated to working on atomized, feature-level “user stories” and often disallowed to work on improvements that can’t be related to short-term, immediate business needs
- these "Agile" systems, so often misapplied, demand that they provide humiliating visibility into their time and work, despite a lack of reciprocity
- Scrum is the worst, with its silliness around two-week “iterations”. It induces needless anxiety about microfluctuations in one’s own productivity
- Ultimately, Agile (as practiced) and Waterfall both are forms of business-driven engineering, and that’s why neither is any good at producing quality software or happy employees.

[Agilité à grande échelle @ Spotify avec les Tribus, Brigades, Chapitres & Guildes](http://www.les-traducteurs-agiles.org/assets/fabrice_aimetti/SpotifyScaling_fr.pdf) mais [Spotify Doesn't Use the Spotify Model](https://www.agility11.com/blog/2020/6/22/spotify-doesnt-use-the-spotify-model)

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

Sub-story: The smallest unit of work that has value for our customers

![](http://formations.imt-atlantique.fr/bi/images/bi/invest.png)
_**INVEST**_: A good user story should be:
* **“I” ndependent** (of all others)
* **“N” egotiable** (not a specific contract for features)
* **“V” aluable** (or vertical)
* **“E” stimable** (to a good approximation)
* **“S” mall** (so as to fit within an iteration)
* **“T” estable** (in principle, even if there isn’t a test for it yet)

#### Template
- Objectifs de l'étude
  * Contexte: Dans le cadre de la mise en place de ...
  * Entrants: Liens vers expression de besoin, use cases, configuration d'exemple, contraintes techniques des partenaires ou de l'environnement...
=> Indiquer si certains points techniques sont particulièrement pressentis pour nécessiter un examen approfondi
  * Attendus : En sortie de l'étude, nous souhaitons:
    + qu'un REX à l'équipe + un chiffrage aient été organisés
    + connaitre la solution technique retenue, accompagnée d'au moins un document explicatif (diagramme de séquence, schéma des interactions entre services, swagger d'API, arbre des tâches ETL, maquettes...)
    + avoir le découpage en US : tâches technique ainsi qu'une estimation de complexité pour chacune
- Contenu de l'étude
Penser entre autres:
  * à la complexité introduite par la solution, et son impact en termes de risques et maintenance
  * à la retro-compatibilité
  * au process de MEP
  * à la supervision et à la gestion des erreurs (fail-fast ?)
  * à l'impact sur les performances (ex: appels HTTP séquentiels ou parallèles, temps de réponse du partenaire...)
- Solutions envisagées
  * Solution A : Avantages / Inconvénients / Risques
  * Solution B : Avantages / Inconvénients / Risques
  * Commentaires de l'équipe
- Résultat de l'étude
Points soulevés lors du REX avec l'équipe
  * point soulevé
    + solution apportée
  * point soulevé
    + solution apportée
- Solution finale retenue:
Solution A pour les raisons principales suivantes ...
- Liste des US
  * créer les JIRAs
  * indiquer l'estimation en points décidée en équipe
  * mettre un lien vers l'étude
  * indiquer si ces US nécessitent des BDDs et notifier le PO


## Personal tasks management
- Etherpad is great: it gives flexibility, a copy/paste scratchpad, hyperlinks, a persistent history of changes, multi-users access and plenty of plugins
- For tips on priotizating issues of a service: _cf._ [ProductOwnership]
- [Log-driven programming] > nested-thinking: never interrupt the flow, take notes of subtasks you'll achieve later on
- Pomodoro Technique: use a timer to break down work into ~25min intervals separated by short breaks
- [Knowledge Debt]:
> You should, intentionally and tactically, decide which piece of information you can do without, for now.
> But you should also, intentionally and strategically, decide when to pay back that debt.
> Being a programmer is about being in a continuous state of learning
> Great programmers don’t settle on not knowing; but they are also not obesessed about learning right now

## Team tasks management
- [EvidenceBasedScheduling]
- [DieScrum]
- [NoHourlyTimeTrackingInSoftware]
- la [Roue de Deming](https://fr.wikipedia.org/wiki/Roue_de_Deming) : Plan-Do-Check-Act
- To evaluate a project progress : SEMAT Essence (Software Engineering Method and Theory)
cf. the [game cards](http://www.ivarjacobson.com/alphastatecards/)
![](http://semat.org/wp-content/uploads/2013/03/spiral.png)
- la règles des 3 emails: au délà, téléphonez ou déplacez-vous pour discuter en personne
- attention à [LawOfTriviality_aka_bikeshedding]
- [How to Ensure You’re Working on the Most Important Items Each Iteration]:
> For the agile product owner, the equivalent of the topographic map is having a larger, multi-iteration goal.
> Without a multi-iteration goal, the product owner is merely climbing from false peak to false peak.
> That product owner and team may eventually arrive at their ultimate destination, but often only after descending and climbing out of the equivalent of the 10,000-foot valley.
> “What is important is seldom urgent, and what is urgent is seldom important.”
> Product Owners Should Identify a Significant Objective Quarterly
- [Is tasking developers with creating detailed estimates a waste of company money?]:
> use historicals to set good expectations and let engineers focus on creating amazing software that your customers really want!

### Methodologies
- CMMI = Capability Maturity Model Integration
- RUP = Rational Unified Process, and its lightweight Agile version: OpenUP
- 2TUP = 2 Tracks Unified Process, aka cycle en Y

## User-testing
- User Interviews & Usability Testing: cf. [ThoughbotPlaybook]
