/**
 * @file main.cpp
 * @brief Codeur/décodeur
 *
 * @author CIMON Lucas & MOREL Benoit
 * @date IMAG 2009-2010
 */

#include <iostream>
#include <string>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#define SYMBG '('
#define SYMBD ')'
#define SYMBDG ")("
#define SYMBGD "()"

#define LONG_MAX_AMORCE 20

using namespace std ;

unsigned int tabPrems[100] = {2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199} ;

/*    Insère des symboles inutiles en début de texte crypté */
string CryptagePrologue()
{
    return "" ;
}


/*    Progresse dans un début de texte crypté juqu'à la fin du Prologue et retourne l'indice de cette position */
int DecryptagePrologue(const char *chaine)
{
    return chaine - chaine ;
}


/*    Insère des symboles inutiles en fin de texte crypté */
string CryptageDigression()
{
    return "" ;
}


/*    Indique la fin de la partie pertinente d'un texte crypté */
bool DecryptageDigression()
{
    return true ;
}


/*    Fonction recursive de Cryptage d'un entier positif en chaine de SYMBG & SYMBGD */
string CryptageRecursif(unsigned int N)
{
    int i = 0;
    int exposantDecompo = 0 ;
    string retour("") ;

    if (N==0){
        return "" ;
    }
    //decomposition
    while (N != 1){
        if ((N % tabPrems[i]) == 0){
            exposantDecompo ++ ;
            N = N / tabPrems[i] ;
        }
        else{
            retour = SYMBG + CryptageRecursif(exposantDecompo) + SYMBD + retour ;
            i++ ;
            exposantDecompo = 0 ;
        }
    }

    retour = SYMBG + CryptageRecursif(exposantDecompo) + SYMBD + retour ;

    return retour ;
}

/*    Fonction recursive de décryptage d'une chaine de SYMBG & SYMBGD en entier positif */
int DecryptageRecursif(const char* chaineParentheses, int tailleChaine)
{
    int compteurParentheses=1;

    int indiceNombrePremier=0;
    int resultat=1;
    int debutChaine=tailleChaine-2, finChaine=tailleChaine-2;

    if(tailleChaine==0){
        return 0;
    }
    else{
        for(int indice=tailleChaine-2; indice>=0; indice--){
            if(chaineParentheses[indice]==SYMBD){
                compteurParentheses++;
            }
            else{
                compteurParentheses--;
            }
            if(compteurParentheses==0){
                debutChaine=indice+1;
                resultat=resultat*pow(tabPrems[indiceNombrePremier],DecryptageRecursif(chaineParentheses+debutChaine, finChaine-debutChaine+1));
                indiceNombrePremier++;
                finChaine=indice-2;
                indice--;
                compteurParentheses=1;
            }
        }
        return resultat;
    }
}


/*    Insère des symboles inutiles en début de mot, automatiquement ignorés au décryptage (propriété du code) */
string CryptageAmorce()
{
    srand((unsigned)time(NULL));
    int tailleMax = rand() % LONG_MAX_AMORCE ;
    string amorce ;

    for(int i = 0 ; i<tailleMax ; i++)
        amorce += SYMBGD ;

    return amorce ;
}


/*    Crypte une chaine de caracteres en suite de SYMBG & SYMBGD */
string Cryptage(const char *chaine)
{
    if (*chaine == '\0'){
        return "" ;
    }
    string chaineCryptee = CryptageAmorce() + CryptageRecursif((int)*chaine) ;

    for (int i = 1 ; chaine[i] != '\0'; i++){
        chaineCryptee += SYMBDG + CryptageAmorce() + CryptageRecursif((int)chaine[i]) ;
    }

    return CryptageAmorce() + chaineCryptee ;
}


/*    Décrypte une suite de SYMBG & SYMBGD en une chaine de caracteres*/
string Decryptage(const char *chaine)
{
    string chaineDecryptee ;
    int    indiceDebutMot = DecryptagePrologue(chaine),
        tailleMot,
        nombreSymbG ;
    bool lecture = true;

    while(lecture){
        tailleMot = 0 ;
        nombreSymbG = 0 ;
        while(lecture && (nombreSymbG != -1)){ // Boucle servant à déterminer tailleMot
            switch(*(chaine+indiceDebutMot+tailleMot)){
                case SYMBG :
                    nombreSymbG++ ;
                    break ;
                case SYMBD :
                    nombreSymbG-- ;
                    break ;
                default :
                    lecture = false ;
                    break ;
            }
            tailleMot++ ;
        }
        chaineDecryptee += (char)DecryptageRecursif(chaine+indiceDebutMot, tailleMot-1) ; // On a lu un SYMBD de trop
        indiceDebutMot += tailleMot + 1 ; // on dépasse le SYMBG suivant
    }

    return chaineDecryptee ;
}


/*    Produit une table ASCII des caractères entre les indices deb et fin */
string CreerASCII(int deb , int fin)
{
    string retour ;

    for (int i=deb;i<=fin;i++){
        retour += (char)i ;
    }

    return retour ;
}


int main(int argc, char** argv)
{
    if (argc < 2){
        cout << "Premier argument : c, p, e ou d" << endl;
        return 0 ;
    }
    switch (argv[1][0]){ // Choix du mode selon la première lettre du premier argument
        case 'c' : // Cryptage d'un texte
            for (int i=2;i<argc;i++)
                cout << Cryptage(argv[i]) << endl;
            break ;
        case 'p' : // décryptage d'un texte
            for (int i=2;i<argc;i++)
                cout << Decryptage(argv[i]) << endl;
            break ;
        case 'e' : // Cryptage d'un entier
            for (int i=2;i<argc;i++)
                cout << CryptageRecursif(atoi(argv[i])) << endl;
            break ;
        case 'd' : // décryptage d'un nombre
            for (int i=2;i<argc;i++)
                cout << DecryptageRecursif(argv[i], strlen(argv[i])) << endl;
            break ;
        default : // intervalle minimum de caractères devant être supporté : 32-126 + 9-10 | Tabulation-LineFeed
            cout << CreerASCII(32,126) + CreerASCII(9,10) << endl;
        break ;
    }

    return 0 ;
}
