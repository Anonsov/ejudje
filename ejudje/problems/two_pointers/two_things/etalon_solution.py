# Etalon solution

# n = int(input())
# a = list(map(int, input().split()))
# q = int(input())
# pref = []
# s = 0
# for i in range(n):
#     s += a[i]
#     pref.append(s)
# for _ in range(q):
#     l, r  = map(int, input().split())
#     print(pref[r - 1] - pref[l - 2] if l > 1 else pref[r - 1])
    
# n = int(input())
# a = input()

# print(a[::-1])

n, m = map(int, input().split())
g = [[] for _ in range(n + 1)]
for i in range(m):
    u, v = map(int, input().split())
    g[u].append(v)
    g[v].append(u)
print("someotnhdef")