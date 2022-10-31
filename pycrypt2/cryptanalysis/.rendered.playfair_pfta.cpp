/*cppimport

*/
#include <pybind11/pybind11.h>

#include "playfair_pfta.h"

#include <iostream>
#include <cstdlib>
#include <string>
#include <vector>
#include <algorithm>
#include <random>
#include <fstream>
#include <cmath>
#include <utility>
#include <ppl.h>


const std::array<std::array<int, 25>, 3> trans = {
		0, 5, 10, 15, 20, 1, 6, 11, 16, 21, 2, 7, 12, 17, 22, 3, 8, 13, 18, 23, 4, 9, 14, 19, 24,
		20, 21, 22, 23, 24, 15, 16, 17, 18, 19, 10, 11, 12, 13, 14, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4,
		4, 3, 2, 1, 0, 9, 8, 7, 6, 5, 14, 13, 12, 11, 10, 19, 18, 17, 16, 15, 24, 23, 22, 21, 20
};

std::string playfair_pfta(const std::string& text, const std::string& quad_filename) {
	short quad_table[26][26][26][26];
	load_quadgrams(quad_table, quad_filename);

	std::vector<int> text_arr;
	text_arr.reserve(text.length());
	for (const char& c : text) {
		text_arr.push_back(c - 65);
	}
	//std::vector<int> current_decrypt(text_arr);

	double temperature = 2.692 + 0.087 * text_arr.size();
	int best_score = 0;
	std::array<int, 25> best = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
								  25 };
	
	concurrency::critical_section cs;
	concurrency::parallel_for(int(0), 50, [&](int trial) {
		srand(time(0));
		std::default_random_engine rng;
		std::uniform_real_distribution<> distribution(0.0, 1.0);

		std::array<int, 25> best_local;
		std::array<int, 25> child = best;
		std::array<int, 25> parent = best;
		std::shuffle(parent.begin(), parent.end(), rng);

		std::vector<int> current_decrypt(text_arr);
		decrypt(text_arr, parent, current_decrypt);

		int parent_score = get_score(current_decrypt, quad_table);
		int child_score, ds, counter = 0, best_local_score = 0;
		while (counter < 100000) {
			make_child(child, parent);
			decrypt(text_arr, child, current_decrypt);
			child_score = get_score(current_decrypt, quad_table);
			if (child_score > best_local_score) {
				best_local_score = child_score;
				best_local = child;
			}

			ds = child_score - parent_score;
			if (ds > 0 || exp(ds / temperature) > distribution(rng)) {
				parent = child;
				parent_score = child_score;
			}
			else {
				counter++;
			}
		}
		
		cs.lock();
		if (best_local_score > best_score) {
			best_score = best_local_score;
			best = best_local;
		}
		cs.unlock();
	});
	
	std::string res_key;
	for (int& c : best) {
		res_key += char(c + 65);
	}
	return res_key;
}

void load_quadgrams(short(&quad_table)[26][26][26][26], const std::string& quad_filename) {
	FILE* quad_file = fopen(quad_filename.c_str(), "rb");
	fread(quad_table, 2, 456976, quad_file);
	fclose(quad_file);
}

void decrypt(std::vector<int>& text_arr, std::array<int, 25> & key, std::vector<int>& decrypted) {
	std::vector<int> row, col;
	row.reserve(25);
	col.reserve(25);
	for (int i = 0; i < 25; i++) {
		row[key[i]] = i / 5;
		col[key[i]] = i % 5;
	}

	int c0, c1, p0, p1;
	size_t len = text_arr.size();
	for (size_t i = 0; i < len; i += 2) {
		c0 = text_arr[i];
		c1 = text_arr[i + 1];
		if (row[c0] == row[c1]) {
			p0 = col[c0] ? key[5 * row[c0] + col[c0] - 1]
				: key[5 * row[c0] + 4];
			p1 = col[c1] ? key[5 * row[c1] + col[c1] - 1]
				: key[5 * row[c1] + 4];
		}
		else if (col[c0] == col[c1]) {
			p0 = row[c0] ? key[5 * (row[c0] - 1) + col[c0]]
				: key[20 + col[c0]];
			p1 = row[c1] ? key[5 * (row[c1] - 1) + col[c1]]
				: key[20 + col[c1]];
		}
		else {
			p0 = key[5 * row[c0] + col[c1]];
			p1 = key[5 * row[c1] + col[c0]];
		}
		decrypted[i] = p0;
		decrypted[i + 1] = p1;
	}
}

int get_score(std::vector<int>& decrypted, short(&quad_table)[26][26][26][26]) {
	int score = 0;
	size_t len = decrypted.size() - 3;
	for (size_t j = 0; j < len; j++) {
		score = score + quad_table[decrypted[j]][decrypted[j + 1]][decrypted[j + 2]][decrypted[j + 3]];
	}
	return score;
}

void make_child(std::array<int, 25> & child, std::array<int, 25> & parent) {
	int i, p, q;
	int start1, start2, store[5];

	int x = rand() % 50;
	switch (x) {
	case 0:
	case 1:
	case 2:
		for (i = 0; i < 25; i++) child[i] = parent[trans[x][i]];
		break;
	case 3:
		for (i = 0; i < 25; i++) child[i] = parent[i];
		start1 = (rand() % 5) * 5;
		start2 = (rand() % 5) * 5;
		for (i = 0; i < 5; i++) store[i] = child[start1 + i];
		for (i = 0; i < 5; i++) child[start1 + i] = child[start2 + i];
		for (i = 0; i < 5; i++) child[start2 + i] = store[i];
		break;
	case 4:
		for (i = 0; i < 25; i++) child[i] = parent[i];
		start1 = rand() % 5;
		start2 = rand() % 5;
		for (i = 0; i < 5; i++) store[i] = child[start1 + i * 5];
		for (i = 0; i < 5; i++) child[start1 + i * 5] = child[start2 + i * 5];
		for (i = 0; i < 5; i++) child[start2 + i * 5] = store[i];
		break;
	default:
		for (i = 0; i < 25; i++) child[i] = parent[i];
		p = rand() % 25;
		q = rand() % 25;
		child[p] = parent[q];
		child[q] = parent[p];
		break;
	}
}

//void display(int score, std::array<int, 25> & key, std::vector<int>& decrypted) {
//	std::cout << "score=" << score << std::endl;
//	for (int& i : key) {
//		std::cout << char(i + 65);
//	}
//	std::cout << std::endl;
//	for (int& i : decrypted) {
//		std::cout << char(i + 97);
//	}
//	std::cout << std::endl << std::endl;
//}

//int main() {
//    std::cout << playfair_pfta("RQMNCZDLFARQCFQPNBIOKABEVFKMXNTLCFGKATLQMRDLEBMSBKKNOSBPXCTLKSZLFAMYFSCFDZCFLBCFCLXNXSOWGMLKBKAYBHBOMTILVYIMLTPRMGCXQZBXARCLBRKPKMPMDKQPNBIOKAVYHVMNONLKKZCFXLFMKPCFBEVFKMPDKLLEYOGSMLGMDMHQLTSOKAPAEPKLLKATBKKNOSBPGATLIMHRIPGAEQLUKLLKATBXGAPDILEAQPILXCTLKSZLFAMYFSCFDZCFQPNBIOKASXXSQYKGEBRALPBYRMCKDZAHMKRIXSMYKLCFKOGLMLMYBNARQCXSLXLIHKNMXSOLULLXIXSKLZSKNABEVFKMTBMFQARPVNDTXGPDKSKOGLMLMYBNARQCXSLBRATLESSCLMRYKMSREFAYZLNAPDFLAPXSCSKCKIMRVFTARSCFDZBORQCFVHXASIULONANKNOSBPKOGLMLMYBNARQCXSTLCVTAGLXEMKLAMECONMLEFSCFDZIUSKANDKKMPRVNDTPHMRLZPRAKMSNADAIMEKYQQPNBIOKAXGPDBXEAMURSKCRAMGMSGAINQENMKSCOLILENDQLRAMSBQSXHPPDFLSMHGBSMDFSCFAKQZBXXLKCPHDZMBSKBMPQZMVHLIXIBDAKSKPBPHMDILGAPDILLENACDMFNZRMRABKYNNMTCXNAKRAHKNMPDILROFLZMVHLIDBPDIMXLZDMSSBAQCZAKYQVNMTYZRMSAPDSXXNXILEMXLIQPNBIOKASXMKBXNABIQCIOTLPRXLIMRYMKLWKAILANTQLESBULLWFSCLRQRSHQEBMSLBGMRMFAPHOTSMHGBSMZLIVNMUCDKLHVMNLKDLEAVHDZRASDZLANMYAKSKBMPTLEMKLTCZAKYQMBLZMSHMACRSDBPDKLEAKLCFGMLCBHNDQLRAMSBQLTHMMUCDMKRIPDLCILXBIFPDFKOGNMORSKNAXNLXLIULXAPRPDLCKONOIRYOTLCFHMCKDAIMEFATLFODOSTLCFONTLIOONXLBEVFKMHPGAOHPUKCPDFGZLZMFLMKXSCKRQHPPDLMXSGEGMMGCBKANAMXEWTLMXTLMRSERAHMBXQZRSHYKMSELMLKARRQRMPDZMMKIKARTCFURAPAKPCFMNBNSMXLZDMSSBAWOXMSOHUMRQIUAZILKMUFXBXNSFOQAFRQHPEPROFMRQCFBRDTXNLKATHPCSMBEFSZTLMRKSKONOBFXSWMEQKMKBIFNAFRPMACRAINMRSXSMRYNAFMKPCFPAPMONAQCFBKYRRPGRNVPDRSPDFKOSRAILKCILZDNHKMRONIKAFBRBMRAUKCRABTSEELBKOYMSIOARCLAKBMOQRSMNSCNRLQLZRYKMPDLENOORRYHPSELMLKARRQFAYOGEGMMGCBWMKSKCTLRSILARXOTMILKMUFFURATALEFKUFKZCFPHSUNVGAENILXBIFRSNAPDLCNMAGYQHPPDFMIOWEXLSZ", "..\\data\\ngram_counts\\playfair_quadgrams.dat");
//    return 0;
//}

namespace py = pybind11;

PYBIND11_MODULE(playfair_pfta, m) {
	m.def("playfair_pfta_cpp", &playfair_pfta, R"pbdoc(
        Playfair simulated annealing.
    )pbdoc");

#ifdef VERSION_INFO
	m.attr("__version__") = VERSION_INFO;
#else
	m.attr("__version__") = "dev";
#endif
}