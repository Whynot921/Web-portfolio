# for N in range(0,100000):
#     N = bin(N)[2:]
#     if len(str(N)) % 2 == 0:
#         R = str(N) + "11"
#     else:
#         R = str(N) + "01"
#     if int(R,2) > 61:
#         print(int(R, 2))
#         break

n=1000000
def f(a1, a2,x):
    return (17 <=x <= 58) <= ((not(29 <=x<=80) and not(a1<=x<=a2)) <= (not(17<=x<=58)))
for a1 in range(1,100):
    for a2 in range(1,100):
        if all(f(a1,a2,x) for x in range(17,81)):
            n=min(n, a2-a1)
print(n)