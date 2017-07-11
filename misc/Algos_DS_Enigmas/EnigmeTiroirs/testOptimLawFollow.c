/*!
    @file testOptimLawFollow.c
    @brief Test du pourcentage de réussite de la stratégie "Suiveur"
    dans "l'enigme des tiroirs"
    @author CIMON Lucas
    @date printemps 2011
*/
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

//~ #define PRINT_VALID
#define PRINT_INVALID
#define SUCCESS_RATE

/* ALGO PERMUTATIONS FROM: http://www.daniweb.com/software-development/c/code/216767 */

int fact(int n)
{
    return (n == 1 || n == 0) ? 1 : fact(n - 1) * n;
}

static inline void swap(int *a, int *b)
{
    int temp = *a;
    *a = *b;
    *b = temp;
}

void printPerm(int *perm, int size)
{
    for (int i = 0; i < size; i++)
        printf(" %d", perm[i]);
}

int main(int argc, char *argv[])
{
    int size;
    if (argc <= 1 || (size = atoi(argv[1])) % 2) {
        printf("USAGE: %s SIZE\n", argv[0]);
        return 1;
    }

    printf("\nSIZE %d\n", size);
#ifdef PRINT_VALID
    puts("\tprinting valid series");
#endif
#ifdef PRINT_INVALID
    puts("\tprinting invalid series");
#ifdef SUCCESS_RATE
    puts("\t\tand success rate");
#endif
#endif

    int nbr_perm = fact(size);
    int *perm = (int *)malloc((size_t) size * sizeof(int));
    for (int i = 0; i < (int)size; i++)
        perm[i] = i;

    int *ctrl_tab = (int *)malloc((size_t) size * sizeof(int));
    for (int k = 0; k < size; ++k)
        ctrl_tab[k] = k;

    int serie_succes_count = 0, perm_index = 1;
    while (true) {
        int id_fail_count = 0;
        for (int numero = 0; numero < size; numero++) {
            int index = numero;
            bool found = false;
            for (int attempt = 0; attempt < size / 2; attempt++) {
                if (numero == perm[index]) {
                    found = true;
                    break;
                }
                index = perm[index];
            }
            if (!found) {
                id_fail_count++;
#ifndef SUCCESS_RATE
                break;
#endif
            }
        }
        if (!id_fail_count) {
            serie_succes_count++;
#ifdef PRINT_VALID
            printPerm(perm, size);
            puts("");
#endif
        }
#ifdef PRINT_INVALID
        else {
            printPerm(perm, size);
#ifdef SUCCESS_RATE
            printf("\t%d KO, ie %0.f%%\n", id_fail_count, 100 * id_fail_count / (double)size);
#else
            puts("");
#endif
        }
#endif

        /* Exit test */
        if (perm_index == size)
            break;

        /* Going through permutations */
        ctrl_tab[perm_index]--;
        int j = perm_index % 2 * ctrl_tab[perm_index];
        swap(&perm[perm_index], &perm[j]);

        perm_index = 1;
        while (perm_index != size && !ctrl_tab[perm_index]) {
            ctrl_tab[perm_index] = perm_index;
            perm_index++;
        }
    }
    puts("");

    free(ctrl_tab);
    free(perm);

    printf("serie_succes_count: %d\n", serie_succes_count);
    printf("proba: %f\n", (100 * (double)serie_succes_count / nbr_perm));

    return 0;
}

/* OUTPUT

SIZE 12

serie_succes_count: 234541440
proba: 48.964646

*/
