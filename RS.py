import numpy as np
import threading as thr
import time
import name
def f(x, y, t):
    return name.C1*t*np.exp(-((x-7*name.a/12)**2 + (y-5*name.b/12)**2)*name.alpha)
def g1(x, t):
    return 0
def g2(y, t):
    return 0
def g3(x, t):
    return 0
def g4(y, t):
    return 0

def initRS():
    name.n1 = int(name.a / name.h1) + 1
    name.n2 = int(name.b / name.h2) + 1
    name.x = np.linspace(0, name.a, name.n1)
    name.y = np.linspace(0, name.b, name.n2)
    name.u = np.array([[name.C2 for _ in range(name.n1)] for _ in range(name.n2)])

def progonka_x(u, u_temp, j):
    k1 = -name.tau*name.h2**2
    k2 = 2*name.tau*name.h2**2 + 2*name.h1**2*name.h2**2
    A = np.empty(name.n1-2)
    b = np.empty(name.n1-2)
    for i in range(1, name.n1-2+1):
        A[i-1] = k2
        b[i-1] = name.tau*name.h1**2*u[j-1][i] + (-2*name.tau*name.h1**2 + 2*name.h1**2*name.h2**2)*u[j][i] + name.tau*name.h1**2*u[j+1][i] + name.tau*name.h1**2*name.h2**2*f(name.x[i], name.y[j], name.t+name.tau/2)
    b[0] = b[0] - k1 * u_temp[j][0]
    b[name.n1 - 2 - 1] = b[name.n1 - 2 - 1] - k1 * u_temp[j][name.n1 - 1]
    k_temp = 0
    for i in range(name.n1-2-1):
        k_temp = k1 / A[i]
        A[i + 1] -= k_temp * k1
        b[i + 1] -= k_temp * b[i]
    b[name.n1 - 2 - 1] /= A[name.n1 - 2 - 1]
    for i in range(name.n1-2-2, -1, -1):
        b[i] = (b[i] - b[i + 1] * k1) / A[i]
    return b

def progonka_y(u, u_temp, i):
    k1 = -name.tau *name.h1**2
    k2 = 2*name.tau * name.h1**2 + 2*name.h1**2*name.h2**2
    A = np.empty(name.n2-2)
    b = np.empty(name.n2-2)
    for j in range(1, name.n2-1):
        A[j-1] = k2
        b[j-1] = name.tau*name.h2**2*u_temp[j][i-1] + (-2*name.tau *name.h2**2 + 2*name.h1**2*name.h2**2) *u_temp[j][i] + name.tau*name.h2**2*u_temp[j][i+1] + name.tau * name.h1**2*name.h2**2*f(name.x[i], name.y[j], name.t+name.tau/2)
    b[0] = b[0] - k1*u[0][i]
    b[name.n2-2-1] = b[name.n2 - 2- 1] - k1*u[name.n2-1][i]
    k_temp = 0
    for i in range(name.n2-2-1):
        k_temp = k1/A[i]
        A[i+1] -= k_temp*k1
        b[i+1] -= k_temp*b[i]
    b[name.n2-2-1] /= A[name.n2 - 2 - 1]
    for i in range(name.n2 - 2 - 2, -1, -1):
        b[i] = (b[i] - b[i+1]*k1) /A[i]
    return b

def second_thread():
    L1 = thr.Lock()
    u_cur = np.empty((name.n2, name.n1), dtype=float)
    while True:
        L1.acquire()
        for i in range(name.n1):
            for j in range(name.n2):
                u_cur[j][i] = name.u[j][i]
        L1.release()
        u_temp = np.empty((name.n2, name.n1), dtype=float)
        for i in range(name.n1):
            u_temp[0][i] = g1(name.x[i], name.t+name.tau/2)
            u_temp[name.n2-1][i] = g3(name.x[i], name.t+name.tau/2)
        for j in range(name.n2):
            u_temp[j][0] = g2(name.y[j], name.t+name.tau/2)
            u_temp[j][name.n1-1] = g4(name.y[j], name.t+name.tau/2)
        for j in range(1, name.n2-1):
            bx = progonka_x(u_cur, u_temp, j)
            for i in range(name.n1-2):
                u_temp[j][i+1] = bx[i]
        for i in range(1, name.n1-1):
            bx = progonka_y(u_cur, u_temp, i)
            for j in range(name.n2-2):
                u_cur[j+1][i] = bx[j]
        name.t += name.tau
        L1.acquire()
        for i in range(name.n1):
            for j in range(name.n2):
                name.u[j][i] = u_cur[j][i]
        L1.release()
        time.sleep(0.250)
