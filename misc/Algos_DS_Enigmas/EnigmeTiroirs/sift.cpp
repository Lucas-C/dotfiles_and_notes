/*!
    @file sift.cpp
    @brief Advanced program to test different strategies to solve
    the "Drawers enigma"
    @author CIMON Lucas
    @date printemps 2011
*/
#include <iostream>
#include <algorithm>
#include <math.h>
#include <time.h>

using namespace std;

typedef bool genCoeff_callback(int, int, int);
typedef int law_callback(int, int, int, int, int);

const int cst_size = 8;

bool cst_sift[][cst_size] = {
    {1, 1, 1, 1, 0, 0, 0, 0},
    {1, 1, 1, 1, 0, 0, 0, 0},
    {1, 1, 1, 1, 0, 0, 0, 0},
    {1, 1, 1, 1, 0, 0, 0, 0},
    {0, 0, 0, 0, 1, 1, 1, 1},
    {0, 0, 0, 0, 1, 1, 1, 1},
    {0, 0, 0, 0, 1, 1, 1, 1},
    {0, 0, 0, 0, 1, 1, 1, 1}
};

bool genCoeff_cstSift(int i, int j, int size)
{
    (void)size;
    return cst_sift[i][j];
}

int fact(int n)
{
    return (n == 1 || n == 0) ? 1 : fact(n - 1) * n;
}

bool siftIsValid(bool ** sift, int size)
{
    for (int i = 0; i < size; i++) {
        int count = 0;
        for (int j = 0; j < size; j++)
            if (sift[i][j])
                count++;
        if (count != size / 2)
            return false;
    }
    return true;
}

bool siftIsFair(bool ** sift, int size)
{
    for (int j = 0; j < size; j++) {
        int count = 0;
        for (int i = 0; i < size; i++)
            if (sift[i][j])
                count++;
        if (count != size / 2)
            return false;
    }
    return true;
}

bool permPassSift(int *perm, bool ** sift, int size)
{
    for (int i = 0; i < size; i++) {
        if (!sift[i][perm[i]])
            return false;
    }
    return true;
}

void printPerm(int *perm, int size)
{
    for (int i = 0; i < size; i++)
        cout << " " << perm[i];
    cout << endl;
}

void printSift(bool ** sift, int size)
{
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++)
            cout << " " << sift[i][j];
        cout << endl;
    }
}

int enumValidPermStatic(bool ** sift, int size, bool print = false)
{
    int *perm = new int[size];
    for (int i = 0; i < size; i++)
        perm[i] = i;

    int count = 0;
    do {
        if (permPassSift(perm, sift, size)) {
            count++;
            if (print)
                printPerm(perm, size);
        }
    } while (next_permutation(perm, perm + size));

    return count;
}

bool **genSift(int size, bool(*genCoeff) (int, int, int))
{
    bool **sift = new bool *[size];

    for (int i = 0; i < size; i++) {
        sift[i] = new bool[size];
        for (int j = 0; j < size; j++)
            sift[i][j] = genCoeff(i, j, size);
    }

    return sift;
}

/*
    bool sift[][size] = {
        {1, 1, 1, 0, 0, 0},
        {0, 1, 1, 1, 0, 0},
        {0, 0, 1, 1, 1, 0},
        {0, 0, 0, 1, 1, 1},
        {1, 0, 0, 0, 1, 1},
        {1, 1, 0, 0, 0, 1}
    };
*/
bool genCoeff_diag(int i, int j, int size)
{
    return (((size + i - j - 1) % size) >= size / 2);
}

/*
    bool sift[][size] = {
        {1, 1, 1, 0, 0, 0},
        {1, 1, 1, 0, 0, 0},
        {1, 1, 1, 0, 0, 0},
        {0, 0, 0, 1, 1, 1},
        {0, 0, 0, 1, 1, 1},
        {0, 0, 0, 1, 1, 1}
    };
*/
bool genCoeff_dualWindow(int i, int j, int size)
{
    if (j < size / 2)
        return (i < size / 2);
    else
        return (i >= size / 2);
}

void testPermStatic(int size, genCoeff_callback genCoeff, bool print = false)
{
    cout << "\nSIZE " << size << endl;

    bool **sift = genSift(size, genCoeff);

    printSift(sift, size);

    cout << siftIsValid(sift, size) << endl;
    cout << siftIsFair(sift, size) << endl;

    int count = enumValidPermStatic(sift, size, print);
    cout << "count: " << count << endl;
    cout << "proba: " << (100 * (double)count / fact(size)) << "%\n";
}

int enumValidPermDynamic(law_callback law, int size, bool print = false)
{
    int *perm = new int[size];
    for (int i = 0; i < size; i++)
        perm[i] = i;

    int count = 0;
    bool last_perm = false;
    while (true) {
        bool valid = true;
        for (int numero = 0; numero < size; numero++) {
            int index = 0;
            bool found = false;
            for (int attempt = 0; attempt < size / 2; attempt++) {
                index = law(index, perm[index], attempt, numero, size);
                if (numero == perm[index]) {
                    found = true;
                    break;
                }
            }
            if (!found) {
                valid = false;
                break;
            }
        }
        if (valid)
            count++;
        else if (print)
            printPerm(perm, size);
        // Fin des permutations ?
        if (last_perm)
            break;
        // Permutation suivante
        last_perm = !next_permutation(perm, perm + size);
    }

    return count;
}

void testPermDynamic(int size, law_callback law, bool print = false)
{
    cout << "\nSIZE " << size << endl;

    int count = enumValidPermDynamic(law, size, print);
    cout << "count: " << count << endl;
    cout << "proba: " << (100 * (double)count / fact(size)) << "%\n";
}



/*********************************/
/********* SOLUTION ?? ***********/
/*********************************/
int law_follow(int index_prec, int perm_index_prec, int attempt, int numero,
               int size)
{
    (void)index_prec;
    (void)size;
    if (attempt == 0)
        return numero;
    else
        return perm_index_prec;
}
/*********************************/



void randomStrategy(int nb_tirages, double proba, int size)
{
    int nb_possibilites = fact(size);

    int *perm = new int[size];
    for (int i = 0; i < size; i++)
        perm[i] = i;

    bool** sift = new bool*[size];
    for (int i = 0; i < size; i++)
        sift[i] = new bool[size];

    srand(static_cast<unsigned int>(time(NULL)));
    int count = 0;
    for (int b = 0; b < nb_tirages; b++) {
        for(int i = 0; i < size; i++) {
            int nb_alea = rand()%nb_possibilites;
            int k = 0;
            while(k++ < nb_alea && next_permutation(perm, perm + size));
            for (int j = 0; j < size; j++)
                sift[i][j] = perm[j] % 2;
        }
        count += enumValidPermStatic(sift, size);
    }

    double p = count / (double)(nb_tirages * nb_possibilites);
    cout << "En moyenne (" << nb_tirages << " tirages) on a une proba de " << p << " de trouver la permutation.\n";

    double q = 1.0 - p;
    int nb = 0;
    double qk = 1.0;
    while ((1.0 - qk) < proba) {
        qk = (fabs(qk - 1.0) < 0.001 ? q : qk * q);
        nb++;
    }
    cout << "On a une proba supérieur à " << proba << " de partir en vacances avant le jour " << nb << ".\n";

    for (int i = 0; i < size; i++)
        delete[] sift[i];
    delete[] sift;
    delete[] perm;
}

int main()
{
    int max_size = 4;

//~     for (int half_size = 1; half_size <= max_size / 2; half_size++)
//~         testPermStatic(half_size * 2, genCoeff_diag);
//~         testPermStatic(half_size * 2, genCoeff_dualWindow);

    testPermStatic(cst_size, genCoeff_cstSift);

    for (int half_size = 1; half_size <= max_size / 2; half_size++)
        testPermDynamic(half_size * 2, law_follow, true);

//~     randomStrategy(10000, 9.f / 10, 8);

    return 0;
}
