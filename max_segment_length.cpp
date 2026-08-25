#include <algorithm>
#include <vector>

class Solution {
    private:

    bool makesAtLeastK(long long k, const std::vector<long long>& woods, long long segment) {
        long long acc = 0;
        for (auto wood: woods) {
            acc += (wood / segment);
            if (acc >= k) {
                break;
            }
        }
        return acc >= k;
    }

    public:

    long long maxSegmentLength(std::vector<long long> woods, long long k) {
        long long l = 1, r = *std::max_element(woods.begin(), woods.end());
        while (l <= r) {
            auto m = l + (r - l) / 2;
            if (makesAtLeastK(k, woods, m)) {
                l = m + 1;
            } else {
                r = m - 1;
            }
        }
        return l - 1;
    }
};
