# -*- coding: utf-8 -*-

if __name__ == '__main__':
    k = 7
    # alist = [1, 99, 1, 99, 98, 2, 2, 98, 3]
    alist = [1, 99, 98, 2, 2]
    v_n = {}
    for v in alist:
        if v not in v_n:
            v_n[v] = 1
            v_n[100-v] = 0
        else:
            v_n[v] += 1
    N = 0
    for v in v_n:
        N += (v_n[v] * v_n[100-v]) / 2
        
        
        