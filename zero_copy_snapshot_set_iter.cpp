#include <climits>
#include <cstddef>
#include <string>
#include <unordered_map>
#include <vector>

struct Record {
    int value;
    int addedAt;
    int removedAt;
};

struct IteratorState {
    int snapshot;
    int cursor;
    std::size_t limit;
};

class Solution {
  public:
    std::vector<int> solution(const std::vector<std::string> &operations,
                              const std::vector<std::vector<int>> &args) {
        std::unordered_map<int, std::size_t> active{};
        std::vector<Record> records{};
        std::vector<int> result;
        std::vector<IteratorState> iterators;
        auto clock = 0;
        auto INF = INT_MAX;

        auto advancetoVisible = [&](IteratorState &iter) {
            while (iter.cursor < iter.limit) {
                const Record &record = records[iter.cursor];
                const bool visible =
                    record.addedAt <= iter.snapshot && iter.snapshot < record.removedAt;
                if (visible)
                    break;
                ++iter.cursor;
            }
        };

        for (int i = 0; i <= operations.size(); i++) {
            auto op = operations[i];
            int arg = args[i][0];
            if (op == "add") {
                if (active.contains(arg)) {
                    result.push_back(0);
                } else {
                    clock += 1;
                    records.push_back({
                        arg,
                        clock,
                        INF,
                    });
                    active[arg] = records.size() - 1;
                }
            } else if (op == "remove") {
                if (!active.contains(arg)) {
                    result.push_back(0);
                } else {
                    clock += 1;
                    auto idx = active[arg];
                    records[idx].removedAt = clock;
                    active.erase(idx);
                    result.push_back(1);
                }
            } else if (op == "contains") {
                const int value = args[i][0];
                result.push_back(active.contains(value) ? 1 : 0);
            } else if (op == "iterator") {
                const int handle = static_cast<int>(iterators.size());
                iterators.push_back(IteratorState{clock, 0, records.size()});
                result.push_back(handle);
            } else if (op == "next") {
                const std::size_t handle = static_cast<std::size_t>(args[i][0]);
                auto &iter = iterators[handle];
                advancetoVisible(iter);
                result.push_back(records[iter.cursor].value);
                ++iter.cursor;
            } else if (op == "has_next") {
                const std::size_t handle = static_cast<std::size_t>(args[i][0]);
                auto &iter = iterators[handle];
                advancetoVisible(iter);
                result.push_back(iter.cursor < iter.limit ? 1 : 0);
            }
        }
        return {};
    }
};
