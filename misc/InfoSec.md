shc : Bash Shell Script Compiler, converts shell scripts directly into binaries http://www.datsi.fi.upm.es/~frosal/
-> uncompile with yanncam/UnSHc

iKAT : gain access to the underlying OS in Kiosk (browser) restricted environment http://ikat.ha.cked.net/Windows/index.html
-> also: https://blog.netspi.com/breaking-out-of-applications-deployed-via-terminal-services-citrix-and-kiosks/

http://pwnwiki.io/#!presence/windows/blind.md # read common Windows files to discover vulnerabilities

PowerShellMafia/PowerSploit # Post-Exploitation Framework


https://github.com/3gstudent/Javascript-Backdoor
https://github.com/PowerShellMafia/PowerSploit/


# Formation @VSCT by Antonio Fortes

maven check deps: https://blog.lanyonm.org/articles/2015/12/22/continuous-security-owasp-java-vulnerability-check.html

SSL3 est mort depuis 2015/12/22/continuous-security-owasp-java-vulnerability-check

sqlmap.py -r burp_raw_exemple_request.txt

Principe de Kerkchoff

General Data Protection Regulation
Organismes d'Importance Vitale

Slowloris denial-of-service attack: "The server says "well, I can't start too many threads, or I will run out of memory. I will therefore set a limit, say, 200, and refuse to start more threads if I have 200 currently serving a request." The attacker says "Ok, fine...I'll just submit 200 requests that talk to the server in a deliberately slow way, taking up all the lines you made available.""

CSRF

Web Security Dojo: https://www.mavensecurity.com/resources/web-security-dojo/
https://sourceforge.net/projects/websecuritydojo/
OWASP Broken Apps
OWASP Shepherd

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


Sniffage de mdp wifi avec Cain: http://www.oxid.it/cain.html

Strongloop NodeJS framework has same injection vulnerabilities as a typical PHP+SQL framework

PBKDF2

https://www.owasp.org/index.php/OWASP_Cheat_Sheet_Series
OWASP Zap Proxy (Zed Attack Proxy) concurrent OSS de Burp

Follow:
http://www.theregister.co.uk/security/
http://arstechnica.com/security/

En cas de faille de sécu non encore patchée dans une lib: utiliser le "virtual patching" du WAF pour résoudre la faille temporairement.
