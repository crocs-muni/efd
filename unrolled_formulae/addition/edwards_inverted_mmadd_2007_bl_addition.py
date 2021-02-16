from sage.all import PolynomialRing, ZZ

pr = PolynomialRing(ZZ, ('c', 'd', 'X1', 'X2', 'Y1', 'Y2'), 6)
c, d, X1, X2, Y1, Y2 = pr.gens()
ccd = c * c * d
ccd2 = 2 * c * c * d
c2 = 2 * c
cc4 = 4 * c * c
k = 1 / c
Z1, Z2 = 1, 1
formula = {}
C = X1 * X2
formula['C'] = C
D = Y1 * Y2
formula['D'] = D
E = C * D
formula['E'] = E
H = C - D
formula['H'] = H
t0 = X1 + Y1
formula['t0'] = t0
t1 = X2 + Y2
formula['t1'] = t1
t2 = t0 * t1
formula['t2'] = t2
t3 = t2 - C
formula['t3'] = t3
I = t3 - D
formula['I'] = I
t4 = E + d
formula['t4'] = t4
t5 = t4 * H
formula['t5'] = t5
X3 = c * t5
formula['X3'] = X3
t6 = E - d
formula['t6'] = t6
t7 = t6 * I
formula['t7'] = t7
Y3 = c * t7
formula['Y3'] = Y3
Z3 = H * I
formula['Z3'] = Z3
