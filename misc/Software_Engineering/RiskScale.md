| Gravité | Description                 | Exemples
|---------|-----------------------------|-
| 1       | **Irritant**                | Ralentit la vélocité de l'équipe. Source de bugs. Manque de temps pour se concentrer sur une tâche. Manque de visibilité de l'équipe sur certains sujets.
| 2       | **Obstacle**                | MEP repoussée. Évolution du code coûteuse dû à l'architecture logicielle. Interface utilisateur peu séduisante. Manque de connaissances de l'équipe dans un domaine. Choix technologique se révêlant coûteux en temps.
| 3       | **Impact business mineur**  | Incident de prod rendant le widget HS plusieurs heures. Dizaines de JH perdus sur une fonctionnalité inutilisée. Opportunité de chiffre d'affaire manquée pour raisons liées au projet. Forte fatigue de l'équipe dû à des conflits / une grande démotivation.
| 4       | **Impact business majeur**  | Site `oui.sncf` fortement dégradé à cause du widget. Lien vers un partenaire invalide pendant plusieurs mois. Faille de sécurité exploitée pour obtenir des données clientes. Poursuite en justice. Bad buzz.

| Probabilité | Description                                     | Exemples
|-------------|-------------------------------------------------|-
| 1           | **Peu probable**                                | Faille de sécurité non réferencée. Widget causant une panne de `oui.sncf`.
| 2           | **Assez probable**                              | Cas non testé survenant en prod. Revue d'accessibilité et/ou sécurité. Départ d'un membre de l'équipe.
| 3           | **Très probable et/ou surviendra dans l'année** | Oubli d'opération manuelle mineure en MEP ou release. Versions patchées de nos dépendances _releasées_.
| 4           | **Se produira dans le mois**                    | Le cycle de sprint/release/MEP. Une _deadline_ (ex: bascule OUI). L'expiration de _credentials_. Une réduction d'effectif de l'équipe.
