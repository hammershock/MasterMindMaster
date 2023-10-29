#include <string>
#include <vector>
#include <unordered_map>
#include <cmath>
#include <limits>
#include <algorithm>

#include <cstring>
#include <cassert>

#include<iostream>

extern "C" {
    void compare2(const char *answer, const char *guess, int *num_a, int *num_b) {
        int len_answer = std::strlen(answer);
        int len_guess = std::strlen(guess);

        // 确保答案和猜测的长度相同
        assert(len_answer == len_guess);

        *num_a = 0;
        *num_b = 0;
        int foo[10] = {0};

        for (int i = 0; i < len_answer; ++i) {
            if (answer[i] == guess[i]) {
                (*num_a)++;
            } else {
                foo[answer[i] - '0']++;
            }
        }

        for (int i = 0; i < len_guess; ++i) {
            int digit = guess[i] - '0';
            if (answer[i] != guess[i] && foo[digit] > 0) {
                (*num_b)++;
                foo[digit]--;
            }
        }
    }

    // 注意：返回 char* 而不是 std::string
    void calculate(const char* action, const char** memory, size_t memory_size, double* entropy, const int number_of_digit) {
        // std::unordered_map<int, double> prob_observation;
        double prob_observation[number_of_digit * number_of_digit + 1] = {0};
        double prob = 1.0 / memory_size;
        *entropy = 0.0;  // 初始化 entropy
        bool inplace = false;
        for (size_t i = 0; i < memory_size; ++i) {
            int num_a = 0, num_b = 0;
            compare2(memory[i], action, &num_a, &num_b);
            int observation = num_a * number_of_digit + num_b;
            if (memory[i] == action) inplace = true;
            prob_observation[observation] += prob;
        }

        for(double x : prob_observation) {
        if (x > 0)*entropy -= x * std::log2(x);
        }
        if (inplace) *entropy += 0.0001;
//        for (const auto& kv : prob_observation) {
//            *entropy -= kv.second * std::log2(kv.second);
//        }

        // 注意：这里我们仅返回指向原始 action 字符串的指针
        return;
    }
}

// int main() {
//     const char* memory[] = {"1234", "2345", "3456", "4567"};
//     const char* action = "1234";
//     double entropy = 0;  // 分配内存给 entropy
//     auto result = calculate(action, memory, 4, &entropy);
//     std::cout << "Entropy: " << entropy << ", Action: " << result << std::endl;
//     return 0;
// }