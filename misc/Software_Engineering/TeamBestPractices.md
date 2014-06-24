## Joining a new team
- talk to a colleague each day (but not for too long, and schedule it) and question him on what he does
- take notes in a file, complete/fix the existing docs & draw diagrams
- quickly get a short-term goal to focus on & follow the 'minimal info' loop:
    * Acquire as little information as possible
    * Acquire information as efficiently as possible
    * Use the information you acquire as effectively as possible
- ask people to have lunch with them (force yourself !)
- ask people for coffee breaks (force yourself !)

## Team culture building
- build a team brand: catching name, logo, slogan... [PP]
- small is good: 2-pizzas team
- whiteboard sessions
- team tenets as guidelines for priorities
- clear team goals with deadlines
- make decisions based on data
- coding style reference, tools to enforce it, code reviews
- allocate some hack time
- regular emails with tips. Or put a one-pager in the toilets, as Google is doing

## StandUp
It mush be SHORT:
- What did you do yesterday?
- What are you doing today?
- What is blocking your progress?
- What are your commitments for the week / progression / changes due to blockers or higher priorities

## Design
- start from a POC / MVP
- + Diagrams !

## Define team metrics
- customer satisfaction
- performance, output data quality
- availability : measured from the client side
- latency

## Ops
- monitor everything ! CPU, openFD, procCount... For services: throughput + delay + completness (% of potential src data processed). And store historical data !
- zero config: hard to document, hard to update, hard to set up, its persistent state can overlaps with other data
- emails are evil: no guarantee it will be actioned + no guarantee anyone is subscribed + sense of false security as it works from time to time
- when an alarm is raised, alerting tools should give a maximum of *context* on the system state and what triggered it
- prioritize identifying the root cause of an issue and resolving it
- hold weekly/monthly ops review meetings, including:
    * highlights from previous on-call shift: high severity events, metrics...
    * this week's priorities: deployments, hand-over of burning tickets or tickets failing over SLA
- frequently determine operational excellence goals: eliminate the top root cause of tickets, create a runbook/dashboard for a service...

## Documentation:
- Tenets:
    * the key challenge to sustaining a complex system is maintaining our *understanding* of it
    * documentation reduce accidents
    * trouble is, documentation goes out of date -> _instrumentation_ reflects the reality of the system as it exists
    * it is possible to have too little info, or too much, or present it badly
- Teach don't tell : http://stevelosh.com/blog/2013/09/teach-dont-tell/
- many more advices: https://github.com/PharkMillups/beautiful-docs
- wiki are great !
    * store meeting notes, tasks list, team & members pages, build processes, design docs, software architecture diagrams...
    * + use it to share useful links, and try to encourage using this instead of individual bookmarks
    * ++ Ops Docs !
    * +++ DASHBOARD !!
    * include the wiki as part of task processes : sprints, ops, deployments...
    * get a leader whose goal is to motivate & educate others
- use Doxygen / Docurium for code documentation

## Recruiting & coaching new hires
- recruiting shared and detailed: what soft/tech competencies to assess, how to evaluate code, loop prebrief/debrief process
- STAR -> Probe -> Chalenge
