# Etalon solution

n = int(input())
a = list(map(int, input().split()))
q = int(input())
pref = []
s = 0
for i in range(n):
    s += a[i]
    pref.append(s)
for _ in range(q):
    l, r  = map(int, input().split())
    print(pref[r - 1] - pref[l - 2] if l > 1 else pref[r - 1])
    
