RiskManagement
==============

## Resources

- bonne intro PDF: [Guide de gestion des risques des projets de développement de système](http://collections.banq.qc.ca/ark:/52327/bs53966) - Quebec 2005
- gestion du risque dans un projet Agile: [slideshare](https://fr.slideshare.net/bduplessis/risk-in-agilemanagement)
- [diagramme](http://nkerzazi.adilou.com/Ressources/cmmi/contents_fr_1_2/RSKM_Diagram.html) des critères du modèle CMMI, domaine RSKM


## Définition ?

> Un évênement incertain qui peut impacter le chemin choisi

C'est un phénomène **normal** de la vie d'un projet.

Caractéristiques:
- impact potentiel / gravité des conséquences
- probabilité d'occurence
- fenêtre de temps où le risque peut subvenir / des actions peuvent être mises en oeuvre


## Quelques types de risques

cf. "Taxonomy of Software Development Risks" page 38 of [Taxonomy-Based Risk Identification](https://resources.sei.cmu.edu/library/asset-view.cfm?assetid=11847) - 1993

- risques financiers
- risques juridiques
- risques organisationnels: pratiques agiles, spécifications, manque d'étude...
  * risques de non-agilité: ne pas de fier à l'équipe, commande à l'équipe, faire le travail de l'équipe, ne pas laisser l'équipe évaluer elle-même les risques
  * alignement / besoin : opportunitées manquées, inadéquation des features développées, faible ROI...
- risques humains : manque de compétences/formations, humeur, fatigue de l'équipe, satisfaction du travail réalisé, conflits...
- risques InfoSec
- risques d'UX
- risques de QA: bugs
- risques techniques :
  * explosion de complexité
  * limitations dues aux technos
  * maintenabilité de la solution

Beaucoup de ces risques interviennent lors du choix des solutions techniques - cf. :
- [Growing Your Tech Stack: When to Say No](https://blog.codeship.com/growing-tech-stack-say-no/)
- [AYoungLadysPrimerToTechnicalDecisionMaking](https://speakerdeck.com/charity/a-young-ladys-primer-to-technical-decision-making), especially the Manifesto on slide 26


## Comment les adresser ?

- Accept / Research / Eliminate / Reduce (its impact or probability) / Transfer
- Continuous Process: Identify -> Analyze -> Plan -> Track -> Control -> loop


## Mise en application concrète

- _risk board_ de collection des risques, où n'impporte qui peut rajouter un post-it lorsqu'il en identifie un
cf. "Risk Form / Risk Identification Summary" -> [An Introduction to Team Risk Management - 1994](https://resources.sei.cmu.edu/library/asset-view.cfm?assetID=12063) - 1994

- atelier en équipe d'identification puis classement des risques

- une phase d'**étude** avant le chiffrage d'une US par l'équipe permet d'identifier/comprendre les risques, et ainsi de grandement réduire l'incertitude de l'estimation
