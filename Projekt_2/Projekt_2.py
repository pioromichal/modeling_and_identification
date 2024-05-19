import numpy as np


def nmk_lin_mod_stat(u, y):
    M = np.column_stack((np.ones(u.shape[0]), u[:, 0]))
    a = np.dot(np.dot(np.linalg.inv(np.dot(M.T, M)), M.T), y)
    return a


def nmk_nlin_mod_stat(u, y, n):
    M = np.ones(u.shape[0])
    for i in range(1, n + 1):
        M = np.column_stack((M, np.power(u[:, 0], i)))
    a = np.dot(np.dot(np.linalg.inv(np.dot(M.T, M)), M.T), y)
    return a


def nmk_nlin_mod_dyn(u_k, y_k, n):
    M_b = np.zeros((u_k.shape[0] - n, n))
    M_a = np.zeros((u_k.shape[0] - n, n))
    for i in range(1, n + 1):
        M_b[:, i - 1] = u_k[n - i:-i]
        M_a[:, i - 1] = y_k[n - i:-i]
    M = np.column_stack((M_b, M_a))
    w_temp = np.dot(np.dot(np.linalg.inv(np.dot(M.T, M)), M.T), y_k[n:])
    b = w_temp[:n]
    a = w_temp[n:]
    return a, b


def model_error(y, y_mod):
    return np.sum((y - y_mod) ** 2)


def model_stat_error(u, y, mod_func, a):
    y_mod = np.array([mod_func(x, a) for x in u]).T
    return model_error(y, y_mod)


def model_dyn_error(u, y, a, b, k_start, func):
    k_vals = np.array(range(k_start, u.shape[0]))
    y_mod = func(u, y, a, b, k_vals, k_start)
    return model_error(y[k_start:], y_mod)


def lin_mod_stat_func(u, a):
    return a[0] + a[1] * u


def nlin_mod_stat_func(u, a):
    val = a[0]
    N=a.shape[0]-1
    for i in range(1, N+1):
        val += a[i] * pow(u, i)
    return val


def nlin_mod_dyn_func(u, y, a, b, k):
    val = 0
    n = a.shape[0]
    for j in range(1, n + 1):
        val += b[j - 1] * u[k - j] + a[j - 1] * y[k - j]
    return val


def nlin_mod_dyn_rek_func(u, y_mod, a, b, k):
    val = 0
    n=a.shape[0]
    for j in range(1, n+1):
        val += b[j-1] * u[k-j] + a[j-1] * y_mod[k-j]
    return val


def nlin_mod_dyn_y(u, y, a, b, k_vals, k_start):
    return np.array([nlin_mod_dyn_func(u, y, a, b, k) for k in k_vals]).T


def nlin_mod_dyn_rek_y(u, y, a, b, k_vals, k_start):
    y_mod = np.zeros((y.shape[0], 1))
    y_mod[0:k_start] = y[0:k_start][:, np.newaxis]
    for k in k_vals:
        y_mod[k] = nlin_mod_dyn_rek_func(u, y_mod, a, b, k)
    return y_mod

