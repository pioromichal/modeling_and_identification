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


def nmk_lin_mod_dyn(u_k, y_k, n):
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


def nmk_nlin_mod_dyn(u_k, y_k, r_dyn, p):
    M = np.zeros((u_k.shape[0] - r_dyn, r_dyn * p * 2))
    for i in range(r_dyn * p * 2):
        if i < r_dyn * p:
            r = int(i / p + 1)
            M[:, i] = u_k[r_dyn - r:-r] ** (i % p + 1)
        else:
            r = int((i - r_dyn * p) / p + 1)
            M[:, i] = y_k[r_dyn - r:-r] ** (i % p + 1)

    return np.dot(np.dot(np.linalg.inv(np.dot(M.T, M)), M.T), y_k[r_dyn:])


def model_error(y, y_mod):
    return np.sum((y[:, np.newaxis] - y_mod[:, np.newaxis]) ** 2) / y_mod.shape[0]


def model_stat_error(u, y, mod_func, a):
    y_mod = np.array([mod_func(x, a) for x in u]).T
    return model_error(y, y_mod)


def model_dyn_error(u, y, a, b, k_start, func):
    k_vals = np.array(range(k_start, u.shape[0]))
    y_mod = func(u, y, a, b, k_vals, k_start)
    return model_error(y[k_start:], y_mod)


def model_dyn_error_rek(u, y, a, b, k_start):
    k_vals = np.array(range(k_start, u.shape[0]))
    y_mod = lin_mod_dyn_rek_y(u, y, a, b, k_vals, k_start)
    return model_error(y[k_start:][:, np.newaxis], y_mod[k_start:])


def lin_mod_stat_func(u, a):
    return a[0] + a[1] * u


def nlin_mod_stat_func(u, a):
    val = a[0]
    N = a.shape[0] - 1
    for i in range(1, N + 1):
        val += a[i] * pow(u, i)
    return val


def lin_mod_dyn_func(u, y, a, b, k):
    val = 0
    n = a.shape[0]
    for j in range(1, n + 1):
        val += b[j - 1] * u[k - j] + a[j - 1] * y[k - j]
    return val


def nlin_mod_dyn_func(u, y, w, k, r_dyn, p):
    val = 0
    # n = a.shape[0]
    for i in range(1, r_dyn + 1):
        d = (i - 1) * p
        for n in range(1, p + 1):
            u_ind = d + n - 1
            y_ind = u_ind + r_dyn * p
            val += w[u_ind] * (u[k - i] ** n) + w[y_ind] * (y[k - i] ** n)
    return val


def lin_mod_dyn_rek_func(u, y_mod, a, b, k):
    val = 0
    n = a.shape[0]
    for j in range(1, n + 1):
        val += b[j - 1] * u[k - j] + a[j - 1] * y_mod[k - j]
    return val


def lin_mod_dyn_y(u, y, a, b, k_vals, k_start):
    return np.array([lin_mod_dyn_func(u, y, a, b, k) for k in k_vals]).T


def nlin_mod_dyn_y(u, y, w, r_dyn, p, k_start):
    k_vals = np.array(range(k_start, u.shape[0]))
    return np.array([nlin_mod_dyn_func(u, y, w, k, r_dyn, p) for k in k_vals]).T


def nlin_mod_dyn_rek_y(u, y, w, r_dyn, p, k_start):
    k_vals = np.array(range(k_start, u.shape[0]))
    y_mod = np.zeros((y.shape[0], 1))
    y_mod[0:k_start] = y[0:k_start][:, np.newaxis]
    for k in k_vals:
        y_mod[k] = nlin_mod_dyn_func(u, y_mod, w, k, r_dyn, p)
    return y_mod[k_start:]


def lin_mod_dyn_rek_y(u, y, a, b, k_vals, k_start):
    y_mod = np.zeros((y.shape[0], 1))
    y_mod[0:k_start] = y[0:k_start][:, np.newaxis]
    for k in k_vals:
        y_mod[k] = lin_mod_dyn_rek_func(u, y_mod, a, b, k)
    return y_mod
