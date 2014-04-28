// Prog moche pour tester le byte pair encoding

#include <iostream>
#include <fstream>
#include <sstream>
using namespace std;

#define CHAR_SIZE (1 << 8)
#define TAB_PAIR_SIZE (1 << 16)
#define T_P_INDEX(a,b) ((a) + ((b) << 8))
#define T_P_FIRST(x) ((x) % CHAR_SIZE)
#define T_P_SECOND(x) ((x) >> 8)
#define CHAR_MIN 33 // '!'
#define CHAR_MAX 126 // '!'

void print(unsigned int *tab, unsigned int i)
{
	cout << "nbr(" << (char)T_P_FIRST(i) << (char)T_P_SECOND(i) << ")[" << T_P_FIRST(i) << "," << T_P_SECOND(i) << "]=" << tab[i] << "\n";	
}

void print_tab_codes(char* tab)
{
	unsigned int i = 0;
	while (tab[i])
		cout<<tab[i++]<<" ";
	cout<<endl;
}

void init_tab_unused(ifstream& file, char* tab_codes)
{
	unsigned int tab_used[CHAR_SIZE] = {0};

	char cour;
	while (file) {
		file.get(cour);
		tab_used[cour] = 1;
	}
	
	unsigned int tab_codes_cour = 0;
	for (unsigned int i = CHAR_MIN; i <= CHAR_MAX; i++)
		if (!tab_used[i])
			tab_codes[tab_codes_cour++] = i;	
}

unsigned int byte_encode(stringstream& sstr, char tab[], unsigned int code_index, char tab_out[][2])
{
	unsigned int tab_pairs[TAB_PAIR_SIZE] = {0};
	char cour, last;

	sstr.get(last);
	while (sstr) {
		sstr.get(cour);
		tab_pairs[T_P_INDEX(last,cour)]++;
		last = cour;
	}
	
	unsigned int max = 0;
	for (unsigned int i = 0; i < TAB_PAIR_SIZE; i++)
		if (tab_pairs[i]) {
			if (tab_pairs[i] > tab_pairs[max])
				max = i;
		}
//~ 	print(tab_pairs, max);

	if (!tab[code_index] || tab_pairs[max] <= 1)
		return code_index - 1;

	char code = tab[code_index];
	tab_out[code_index][0] = T_P_FIRST(max);
	tab_out[code_index][1] = T_P_SECOND(max);
	
	sstr.clear(); // WTF?
	sstr.seekg(0, std::ios::beg);

	stringstream s_in;
	s_in << sstr.rdbuf();
	sstr.str("");
	
	s_in.get(last);
	while (s_in) {
		s_in.get(cour);
		if (T_P_INDEX(last,cour) == max) {
			sstr << code;
			s_in.get(last);
		} else {
			sstr << last;
			last = cour;
		}
	}
	
	cout<<sstr.str()<<endl;
	
	return byte_encode(sstr, tab, code_index + 1, tab_out);
}

void byte_decode(stringstream& sstr, char tab[], char tab_out[][2], unsigned int code_index, unsigned int code_index_min)
{
	char cour, code = tab[code_index];

	sstr.clear(); // WTF?
	sstr.seekg(0, std::ios::beg);

	stringstream s_in;
	s_in << sstr.rdbuf();
	sstr.str("");
	
	while (s_in) {
		if (s_in.peek() == -1) break;
		s_in.get(cour);
		if (cour == tab[code_index]) {
			sstr << tab_out[code_index][0];
			sstr << tab_out[code_index][1];
		} else {
			sstr << cour;
		}
	}
	
	cout<<sstr.str()<<endl;
	
	if (code_index != code_index_min)
		byte_decode(sstr, tab, tab_out, code_index - 1, code_index_min);
}

int main()
{
	char tab_unused[CHAR_SIZE] = {0};
	char tab_coded[CHAR_SIZE][2] = {0};
	
	ifstream file("text.in");	
	
	init_tab_unused(file, tab_unused);
	print_tab_codes(tab_unused);
	
	stringstream sstr;
	file.clear(); // WTF?
	file.seekg(0, std::ios::beg);
	file >> sstr.rdbuf();
	
	unsigned int code_min = 32;
	unsigned int code_max = byte_encode(sstr, tab_unused, code_min, tab_coded);

	for (unsigned int i = code_min; i <= code_max; i++)
		cout << tab_unused[i] << " ";
	cout << endl;
	
	byte_decode(sstr, tab_unused, tab_coded, code_max, code_min);
	
//~ 	ofstream out("text.out");
//~ 	out << sstr.str();
}
