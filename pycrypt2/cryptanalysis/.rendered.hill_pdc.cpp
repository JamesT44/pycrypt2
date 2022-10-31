/*cppimport

*/

#include <pybind11\pybind11.h>
#include <pybind11\stl.h>

#include "hill_pdc.h"

#include <iostream>
#include <cstdlib>
#include <string>
#include <limits>
#include <algorithm>
#include <vector>
#include <fstream>
#include <ppl.h>


std::vector<vi> hill_pdc(const std::string& text, size_t key_len, const std::string& data_file) {
	vd mono_table, half_mono_table, quad_table;
	mono_table.reserve(26);
	half_mono_table.reserve(13);
	quad_table.reserve(456976);
	load_data(data_file, mono_table, half_mono_table, quad_table);

	size_t text_len = std::min(text.size(), key_len * 150);
	text_len -= text_len % key_len;
	size_t chunk_num = text_len / key_len;

	vi text_arr;
	text_arr.reserve(text_len);
	for (const char& c : text.substr(0, text_len)) {
		text_arr.push_back(c - 65);
	}

	vi curr_row(key_len);
	concurrency::critical_section cs;
	scored_rows candidate_half_rows(2 * key_len, std::make_pair(-std::numeric_limits<double>::max(), curr_row));
	concurrency::parallel_for(int(0), 13, [&](int first) {
		scored_rows child_candidate_half_rows(2 * key_len, std::make_pair(-std::numeric_limits<double>::max(), curr_row));
		size_t i;

		vi child_row(key_len);
		child_row[0] = first;

		if (first) insort_row(child_candidate_half_rows, score_row(child_row, text_arr, half_mono_table, text_len, key_len, 13), child_row);

		while (true) {
			i = 1;
			child_row[i]++;
			while (child_row[i] == 13) {
				child_row[i] = 0;
				i++;
				if (i == key_len) break;
				child_row[i]++;
			}
			if (i == key_len) break;

			insort_row(child_candidate_half_rows, score_row(child_row, text_arr, half_mono_table, text_len, key_len, 13), child_row);
		}

		cs.lock();
		for (auto& child_half_row : child_candidate_half_rows) {
			insort_row(candidate_half_rows, child_half_row.first, child_half_row.second);
		}
		cs.unlock();
	});

	double score;
	size_t i, j;
	int curr_c;

	size_t mask_limit = (size_t)pow(2, key_len), mask;
	scored_rows candidate_rows(3 * key_len / 2, std::make_pair(-std::numeric_limits<double>::max(), curr_row));
	for (auto& half_row : candidate_half_rows) {
		for (mask = 0; mask < mask_limit; mask++) {
			for (i = 0; i < key_len; i++) {
				curr_row[i] = half_row.second[i] + ((mask & (1 << i)) ? 13 : 0);
			}

			insort_row(candidate_rows, score_row(curr_row, text_arr, mono_table, text_len, key_len, 26), curr_row);
		}
	}

	vi current_part(chunk_num);
	decrypted_rows candidate_parts;
	candidate_parts.reserve(3 * key_len / 2);
	for (auto& row : candidate_rows) {
		for (i = 0; i < chunk_num; i++) {
			curr_c = 0;
			for (j = 0; j < key_len; j++) {
				curr_c += text_arr[i * key_len + j] * row.second[j];
			}
			current_part[i] = curr_c % 26;
		}
		candidate_parts.emplace_back(std::make_pair(current_part, row.second));
	}
	std::sort(candidate_parts.begin(), candidate_parts.end());

	vi current_decrypt(text_len);
	std::vector<vi> best_key(key_len, std::vector<int>(key_len));
	double best_score = -std::numeric_limits<double>::max();
	do {
		for (i = 0; i < text_len; i++) {
			current_decrypt[i] = candidate_parts[i % key_len].first[i / key_len];
		}
		
		score = 0.0;
		for (i = 0; i < text_len - 3; i++) {
			score += quad_table[current_decrypt[i] * 17576 + current_decrypt[i + 1] * 676 + current_decrypt[i + 2] * 26 + current_decrypt[i + 3]];
		}
		if (score > best_score) {
			best_score = score;
			for (i = 0; i < key_len; i++) {
				best_key[i] = candidate_parts[i].second;
			}
		}

		std::reverse(candidate_parts.begin() + key_len, candidate_parts.end());
	} while (std::next_permutation(candidate_parts.begin(), candidate_parts.end()));

    return best_key;
}

void load_data(const std::string& data_file, vd& mono_table, vd& half_mono_table, vd& quad_table) {
	std::ifstream data_stream(data_file);
	std::istream_iterator<double> data_stream_it(data_stream);
	std::copy_n(data_stream_it, 26, std::back_inserter(mono_table));
	std::copy_n(++data_stream_it, 13, std::back_inserter(half_mono_table));
	std::copy_n(++data_stream_it, 456976, std::back_inserter(quad_table));
}

double score_row(vi& row, vi& text_arr, vd& score_table, size_t text_len, size_t key_len, int alphabet_len) {
	double score = 0.0;
	int curr_c;
	size_t i, j;
	for (i = 0; i < text_len; i += key_len) {
		curr_c = 0;
		for (j = 0; j < key_len; j++) {
			curr_c += text_arr[i + j] * row[j];
		}
		score += score_table[curr_c % alphabet_len];
	}
	return score;
}

void insort_row(scored_rows& a, double score, vi& row) {
	if (score < a.back().first) return;
	size_t lo = 0, hi = a.size(), mid;
	while (lo < hi) {
		mid = (lo + hi) / 2;
		if (score > a[mid].first) {
			hi = mid;
		}
		else {
			lo = mid + 1;
		}
	}

	a.insert(a.begin() + lo, std::make_pair(score, row));
	a.pop_back();
}

namespace py = pybind11;

PYBIND11_MODULE(hill_pdc, m) {
	m.def("hill_pdc_cpp", &hill_pdc, R"pbdoc(
        Hill divide and conquer.
    )pbdoc");

#ifdef VERSION_INFO
	m.attr("__version__") = VERSION_INFO;
#else
	m.attr("__version__") = "dev";
#endif
}