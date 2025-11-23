"""
Given two strings s and t, return true if the two strings are anagrams of each other, otherwise
return false.

An anagram is a string that contains the exact same characters as another string, but the order of
the characters can be different.
"""
=== MEMO START ===
def isAnagram(s, t):
    if len(s) != len(t):
        return False

    countS, countT = {}, {}

    for i in range(len(s)):
        countS[s[i]] = 1 + countS.get(s[i], 0)
        countT[t[i]] = 1 + countT.get(t[i], 0)
    return countS == countT
