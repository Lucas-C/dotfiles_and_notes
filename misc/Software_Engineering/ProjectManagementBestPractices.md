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
