#include <vector>
#include <string>

typedef std::vector<int> vi;
typedef std::vector<double> vd;
typedef std::vector<std::pair<double, vi>> scored_rows;
typedef std::vector<std::pair<vi, vi>> decrypted_rows;


std::vector<vi> hill_dc(const std::string& text, size_t key_len, const std::string& data_file);

void load_data(const std::string& data_file, vd& mono_table, vd& half_mono_table, vd& quad_table);

double score_row(vi& row, vi& text_arr, vd& score_table, size_t text_len, size_t key_len, int alphabet_len);

void insort_row(scored_rows& a, double score, vi& row);
