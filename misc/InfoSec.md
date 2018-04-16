[![](https://imgs.xkcd.com/comics/2018_cve_list.png)](https://xkcd.com/1957/)

cf. also "Hacking & Forensic" section in notes.py

How to Start Your Career in Cyber Security by Mikko Hypponen : https://safeandsavvy.f-secure.com/2017/02/03/a-hacker-hunters-advice-for-getting-into-infosec/

# Phases of Penetration Testing
From http://www.pentest-standard.org


## Intelligence Gathering
DNSMAP
Patator : Multi-threaded Service & URL Brute Forcing Tool, in Python
https://github.com/eldraco/domain_analyzer Python script that automatically discovers and reports information about the given domain
https://github.com/SharadKumar97/OSINT-SPY : Python, call Clearbit / Shodan / Fullcontact / Virus_Total / EmailHunter APIs
[Wappalyzer](https://www.wappalyzer.com): Chrome plugin to detect libs used on a website

[wafw00f](https://github.com/EnableSecurity/wafw00f) : allows one to identify and fingerprint Web Application Firewall (WAF) products protecting a website


### Sniffing
OWASP Zap Proxy (Zed Attack Proxy) concurrent OSS de Burp


## Threat Modeling
Méthodologie d'attaque:
(diagramme/mindmap généré via http://asciiflow.com, convertissable en image avec ditaa)

                                     +-----------------+
 +--------------------------+        |                 |
 |                          |        |  Devenir riche  |             +-----------------+
 |  Injection               <--------+ au Hacme Casino +------------->                 +--------> gagner honnêtement
 |  => accès total à la DB  |        |                 |             |  Gagner au jeu  |
 |                          |        ++---------------++             |                 +--------> tricher +-------> bot
 +--------------------------+         |               |              +-----------------+
                                      |               |
                                      |               |
                   +------------------v+            +-v-------------------+
                   |                   |            |                     +----> injection de référence
                   | Voler de l'argent |            |  Transfert d'argent |
                   |    à quelqu'un    |            |                     +----> CSRF
      +------------+                   +----+       +---------------------+
      |            ++-------+---------++    |
      |             |       |         |     v
      |             |       |         |    XSS
      v             v       v         |
phishing        sniffer  redirections +---->orce brute



## Vulnerability Analysis

### Reverse engineering
radare2 : unix-like reverse engineering framework and commandline tools


## Exploitation
iKAT : gain access to the underlying OS in Kiosk (browser) restricted environment http://ikat.ha.cked.net/Windows/index.html
-> also: https://blog.netspi.com/breaking-out-of-applications-deployed-via-terminal-services-citrix-and-kiosks/

https://github.com/3gstudent/Javascript-Backdoor : JSRAT is a Python script that can be used to get a remote shell on a target PC simply by making hime visit an URL with a browser
http://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet : with Bash, Perl, Python, PHP, Ruby, Java...

Content-Security-Policy HTTP response header : reduce XSS risks by declaring what dynamic resources are allowed to load

[browser autofill phishing](https://github.com/anttiviljami/browser-autofill-phishing)
[Target="_blank" - the most underestimated vulnerability ever](https://www.jitbit.com/alexblog/256-targetblank---the-most-underestimated-vulnerability-ever/)

https://github.com/x0rz/EQGRP - NSA hacking tools - Decrypted content of eqgrp-auction-file.tar.xz released by "The Shadow Brokers" : supposedly a free sample of the files exfiltrated from the Equation Group

### DB attacks
sqlmap.py -r burp_raw_exemple_request.txt
Strongloop NodeJS framework has same injection vulnerabilities as a typical PHP+SQL framework
stampery/mongoaudit : MongoDB auditing and pentesting in Python


## Post Exploitation
- https://github.com/PowerShellMafia/PowerSploit/ # Post-Exploitation Framework
- john the ripper multicoeurs: http://www.planet-libre.org/?post_id=20989
- https://github.com/hashcat/hashcat : world's fastest password cracking/recovery utility, for over 200 highly-optimized hashing algorithms:

    hashcat -a 0 -m 3200 hashes.txt ~/Downloads/10_million_password_list_top_10000.txt --force # from a cloudfare blog post

### Windows
mimikatz : extract plaintexts Windows passwords, hash, PIN code and kerberos tickets from memory; can also perform pass-the-hash, pass-the-ticket or build Golden tickets
mimipenguin: same as Mimikatz for Linux - must be root
http://pwnwiki.io/#!presence/windows/blind.md # read common Windows files to discover vulnerabilities



## Reporting



# Other

## Frameworks
Metasploit
w3af
FuzzBunch -> used by the NSA : https://github.com/fuzzbunch/fuzzbunch
wapiti -> modular & in Python, website "fuzzer", performs "black-box" scans of a web application by crawling the webpages of the deployed webapp, looking for scripts and forms where it can inject data
https://n0where.net/popular-pentesting-scanner-v3n0m Python pentesting scanner

## Dependency checking
maven check deps: https://blog.lanyonm.org/articles/2015/12/22/continuous-security-owasp-java-vulnerability-check.html


## Cryptography
SSL3 est mort depuis 2015/12/22/continuous-security-owasp-java-vulnerability-check
PBKDF2 : new Public-Key Cryptography Standard


## Obfuscation
shc : Bash Shell Script Compiler, converts shell scripts directly into binaries http://www.datsi.fi.upm.es/~frosal/
-> uncompile with yanncam/UnSHc

## Reference orgs
OWASP: https://www.owasp.org/index.php/OWASP_Cheat_Sheet_Series
General Data Protection Regulation
Organismes d'Importance Vitale

## Information sources
http://www.theregister.co.uk/security/
http://arstechnica.com/security/
http://pentestit.com
http://www.miscmag.com
https://labsblog.f-secure.com

## Training
Web Security Dojo: https://www.mavensecurity.com/resources/web-security-dojo/
https://sourceforge.net/projects/websecuritydojo/
OWASP Broken Apps
OWASP Shepherd

## Secret sharing
https://github.com/benschw/springboard : cli utility to help get your secrets into https://www.vaultproject.io
-> Vault secures, stores, and tightly controls access to tokens, passwords, certificates, API keys, and other secrets in modern computing. Vault handles leasing, key revocation, key rolling, and auditing

https://github.com/square/keywhiz : A system for distributing and managing secrets

## AWS
http://flaws.cloud
https://github.com/andresriancho/nimbostratus : Tools for fingerprinting and exploiting Amazon cloud infrastructures
https://github.com/RhinoSecurityLabs/Security-Research/tree/master/tools/aws-pentest-tools : buckethead.py searches across every AWS region for a variety of bucket names based on a domain name, subdomains, affixes given and more

## Wifi
- Wireless hacking 101: http://www.kalitutorials.net/2016/08/things-you-should-know-wireless-hacking.html
- sniffage wifi passwords with Cain: http://www.oxid.it/cain.html
- https://github.com/derv82/wifite2 (Python)
- https://github.com/wi-fi-analyzer/fluxion : MITM attacks (Python)

# Formation @VSCT by Antonio Fortes

Techniques Opératoires d'Intrusion:
- Observation: Network sniffing, physical access, viewing client artifacts, etc.
- Injection: packets or commands, modifying client artifacts, etc.
- Analyse: Reverse engineering protocols, disassembling binaries, etc.
- Force Brute: brute forcing, fuzzing, dictionary enumerating, etc.
- Influence: social engineering, eavesdropping, shoulder surfing, phishing, etc.
- Saturation: network flooding, CPU flooding, memory flooding, etc.

9 compétences pour le développement sécurisé:
1. Maintenir la sécurité en cas d'erreur ou d'exception
2. Contrôler/valider une donnée client
3. Renvoyer une donnée client avec l'encodage adéquat
4. Identifier et manipuler des jetons d'accès
5. Requête AAA: Authentifiée, Autorisée, Auditée
6. Interagir avec des ressources externes
7. Stocker et/ou transporter des données sensibles
8. Connaître les forces et faiblesses des technologies utilisées
9. Savoir qui contacter pour de l'aide et quand

CHEAT SHEET : DEVELOPPEMENT SECURISE
1. Des données sont-elles collectées?
– Où/Quelles sont les règles de validation?
– Avec quelle API valide-t-on?
2. Des données sont-elles envoyées au client?
– Quel conteneurs les affichent?
– Quelle API fournit-elle l’encodage?
3. Une requête est-elle envoyée à un interpréteur?
– Comment l’appel est-il paramétrisé?
– …ou échappé??
4. Est-ce un jeton d’accès?
– Résiste-t-il aux menaces « jetons »?
– Les transactions sont-elles protégées contre les CSRFs?
5. Données sensibles/personnelles?
– Qui configure TLS pour transmettre?
– Comment le stockage est-il protégé?
6. Triple A:
– Toute requête est-elle authentifiée?
– Toute requête est-elle autorisée?
– Toute requête est-elle journalisée?
7. Composants externes / librairies
– Sont-ils à jour?
8. Cas spéciaux nécessitant une revue par un tiers:
– Algorithmique numérique
– Multithreading / synchronisation
– Réflexion / Récursivité
– Appels aux primitives cryptographiques

Principe de Kerckhoffs : la sécurité d'un cryptosystème ne doit reposer que sur le secret de la clef; autrement dit, tous les autres paramètres doivent être supposés publiquement connus

Slowloris denial-of-service attack: The server says "well, I can't start too many threads, or I will run out of memory. -> https://pypi.python.org/pypi/PySlowLoris
I will therefore set a limit, say, 200, and refuse to start more threads if I have 200 currently serving a request."
The attacker says "Ok, fine...I'll just submit 200 requests that talk to the server in a deliberately slow way,
taking up all the lines you made available."

En cas de faille de sécu non encore patchée dans une lib: utiliser le "virtual patching" du WAF pour résoudre la faille temporairement.
