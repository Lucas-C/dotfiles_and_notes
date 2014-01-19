// Prog affichant des statistiques sur un fichier texte et retournant un fichier composé d'une suite numérique équivalente
// Idées tri croissant codé par permutation ? (log2(n!))
#include <iostream>
#include <fstream>
using namespace std;

#define CHAR_SIZE (1 << 8)

int main()
{
	unsigned int char_tab[CHAR_SIZE] = {0};
	
	ifstream file("text.in");	
	ofstream out("text.x");	// Suite
	
	char cour;
	while (file) {
		cour = file.peek();
		if (cour == 10) {
			out << 0 << " ";
		} else if (cour == ' ') {
			out << 1 << " ";
		} else if (cour >= 'a' && cour <= 'z') {
			char_tab[cour]++;
			out << cour - 'a' + 2 << " ";
		}
		file.seekg(1, ios_base::cur);
	}

	for (unsigned int i = 0; i < CHAR_SIZE; i++)
		if (char_tab[i])
			cout << (char)i << " : " << char_tab[i] << "\n";
}
