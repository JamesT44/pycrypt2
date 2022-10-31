from ciphers.columnar_transposition import ColumnarTransposition
from statistics_data import bigram_discrepancy_data


def columnar_transposition_period(text, max_period=15, cipher=ColumnarTransposition()):
    text_length = len(text)
    text_indices = [cipher.alphabet_index[c] for c in text]

    used_columns = [False] * max_period
    column_array = [0] * max_period
    best_score, best_period = 0, 0
    next_shift, next_column = None, None
    for period in range(2, max_period + 1):
        num_full_rows = text_length // period
        num_long_columns = text_length % period
        num_short_columns = period - num_long_columns

        max_shifts = [min(i, num_long_columns) - max(0, i - num_short_columns) for i in range(period)]
        column_positions = [num_full_rows * i + max(0, i - num_short_columns) for i in range(period)]
        for start in range(period):
            column_array[0] = start
            used_columns[start] = True
            for curr_shift in range(max_shifts[start] - int(num_long_columns and start >= num_long_columns) + 1):
                shift_a = curr_shift
                index = 1
                for i in range(period):
                    if not used_columns[i]:
                        column_array[index] = i
                        index += 1
                score = 0
                for column in range(1, period):
                    maximum = 0
                    for i in range(column, period):
                        long_corr, short_corr = 0, 0
                        if column >= num_long_columns and column_array[i] >= num_short_columns:
                            short_corr = 1
                        elif column < num_long_columns <= column_array[i]:
                            long_corr = 1
                        next_shift = 0
                        for shift in range(short_corr, max_shifts[column_array[i]] - long_corr + 1):
                            total = 0
                            for j in range(num_full_rows):
                                total += bigram_discrepancy_data[text_indices[column_positions[column_array[column - 1]]
                                                                              + j + shift_a]][
                                    text_indices[column_positions[column_array[i]]
                                                 + j + shift]]
                            if total > maximum:
                                maximum = total
                                next_column = i
                                next_shift = shift
                    score += maximum
                    column_array[next_column], column_array[column] = column_array[column], column_array[next_column]
                    shift_a = next_shift
                score = score / (num_full_rows * (period - 1))
                if score > best_score:
                    best_score = score
                    best_period = period
            used_columns[start] = False
    return best_period
