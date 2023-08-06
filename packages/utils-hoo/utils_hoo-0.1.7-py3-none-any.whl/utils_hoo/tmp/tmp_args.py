# -*- coding: utf-8 -*-


def a(b, c, d):
    print(b, c, d)
    return b + c * d


def a_(b):
    return b**2


def e(b, **kwargs):
    print(kwargs)
    kwargs_new = kwargs.copy()
    kwargs_new.update({'a': 'a'})
    print(kwargs_new)
    return a(b, **kwargs)


def e_(b, **kwargs):
    return a_(b, **kwargs)


def f(a, b, **kwargs):
    if 'c' in kwargs.keys():
        print('c:', kwargs['c'])
    print(a+b)
    

def g(a, b, kwargs_f):
    f(a, b, **kwargs_f)
    
    
if __name__ == '__main__':
    params = {'b': 2, 'kargs': {'c': 4, 'd': 3}}    
    result = e(params['b'], **params['kargs'])    
    print(f'result: {result}')
    
    params_ = {'b': 2, 'kargs': {}}
    result_ = e_(params_['b'], **params_['kargs'])
    print(f'result_: {result_}')
    
    
    print('\n')
    f(1, 2, c=5, d=3)
    
    print('\n')
    g(a=1, b=2, kwargs_f={'a0': 8, 'c': 3})
    