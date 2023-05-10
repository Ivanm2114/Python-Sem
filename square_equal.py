"""Выдаем корни квадратного уравнения с заданными коэф-ми"""
# -*- coding: utf-8 -*-

def solve_quad(a, b, c):    
    """Выдаем корни квадратного уравнения с заданными коэф-ми"""
    
    if(a!=0):
        D=b ** 2 - 4 * a * c
        if D<0:
            return "Big sad"
        x1=(-b + D ** 0.5) / (2 * a)
        x2=(-b - D ** 0.5) / (2 * a)
        if x1==x2:
            return x1
        return (x1, x2)
    return -c / b
            

l = int(input("Input A\n"))
m = int(input("Input B\n"))
k = int(input("Input C\n"))
print(solve_quad(l, m, k))
