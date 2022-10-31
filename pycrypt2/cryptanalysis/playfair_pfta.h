#ifndef PLAYFAIR_PFTA_H
#define PLAYFAIR_PFTA_H

#include <vector>
#include <array>
#include <string>

std::string playfair_pfta(const std::string& text, const std::string& quad_filename);

void load_quadgrams(short (&quad_table)[26][26][26][26], const std::string& quad_filename);

void decrypt(std::vector<int> &text, std::array<int, 25> &key, std::vector<int> &decrypted);

int get_score(std::vector<int> &decrypt, short (&quad_table)[26][26][26][26]);

void make_child(std::array<int, 25> &child, std::array<int, 25> &parent);

#endif