class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        L1, L2 = len(word1), len(word2)
        dp = [[0] * (L2 + 1) for _ in range(L1 + 1)]
        for i in range(L1):
            for j in range(L2):
                dp[i + 1][j + 1] = max(dp[i][j + 1], dp[i + 1][j], dp[i][j] + (word1[i] == word2[j]))
        return L1 + L2 - 2* dp[L1][L2]


# TESTS
for word1, word2, expected in [
    ("sea", "eat", 2),
    ("sea", "aet", 4),
    ("leetcode", "etco", 4),
]:
    sol = Solution()
    actual = sol.minDistance(word1, word2)
    print("Minimal # of deletion to make", word1, "==", word2, "->", actual)
    assert actual == expected
