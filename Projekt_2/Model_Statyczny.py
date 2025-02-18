#%%
import numpy as np
import matplotlib.pyplot as plt
from Projekt_2 import nmk_lin_mod_stat, nmk_nlin_mod_stat, model_stat_error, lin_mod_stat_func,nlin_mod_stat_func
#%% md
# # Wczytanie i podział danych statycznych na zbiór uczący i weryfikujący.
#%%
dane_stat = np.loadtxt('dane/danestat13.txt')
dane_ucz = dane_stat[::2]
dane_wer = dane_stat[1::2]
print(dane_wer.shape)
#%% md
# # Rysowanie wykresów zbirów uczącego i weryfikującego
#%%
plt.figure(figsize=(6, 4))
plt.plot(dane_ucz[:,0],dane_ucz[:,1], 'o')
plt.title('Wykres zbioru uczącego')
plt.xlabel('u')
plt.ylabel('y')
plt.grid(True)
path='wykresy/dane_stat_ucz.png'
plt.savefig(path,dpi=300)
plt.show()
#%%
plt.figure(figsize=(6, 4))
plt.plot(dane_wer[:,0],dane_wer[:,1],'o')
plt.title('Wykres zbioru weryfikującego')
plt.xlabel('u')
plt.ylabel('y')
plt.grid(True)
path='wykresy/dane_stat_wer.png'
plt.savefig(path,dpi=300)
plt.show()
#%% md
# # Statyczny model liniowy metodą najmiejszych kwadratów
# ## Wyznaczanie parametrów
#%%
M=np.column_stack((np.ones(dane_ucz.shape[0]), dane_ucz[:,0]))
Y=dane_ucz[:,1][:, np.newaxis]
#%%
# a=np.dot(np.dot(np.linalg.inv(np.dot(M.T, M)), M.T), Y)
a=nmk_lin_mod_stat(dane_ucz[:,0][:, np.newaxis],dane_ucz[:,1][:, np.newaxis])
print(a)
#%%
u_vals = np.linspace(-1,1,100)
def func(x):
    return a[0]+a[1]*x

plt.figure(figsize=(6, 4))
plt.plot(u_vals,np.vectorize(func)(u_vals))

plt.title('Charakterystyka statyczna y(u)')
plt.xlabel('u')
plt.ylabel('y')
plt.grid(True)
plt.show()
#%% md
# ## Sprawdzenie poprawności rozwiązania
#%%
def func(x):
    return a[0]+a[1]*x

plt.figure(figsize=(6, 4))
plt.plot(dane_ucz[:,0],dane_ucz[:,1], 'o', label='obiekt')
plt.plot(dane_ucz[:,0],np.vectorize(func)(dane_ucz[:,0]), 'o', label='model')
plt.title('Wykres modelu i obiektu zbioru uczącego')
plt.xlabel('u')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.show()
#%%
def func(x):
    return a[0]+a[1]*x

plt.figure(figsize=(6, 4))
plt.plot(dane_wer[:,0],dane_wer[:,1], 'o', label='obiekt')
plt.plot(dane_wer[:,0],np.vectorize(func)(dane_wer[:,0]), 'o', label='model')
print(dane_wer.shape)
print(np.array([func(x) for x in dane_wer[:,0]]).T.shape)
plt.title('Wykres modelu i obiektu zbioru weryfikującego')
plt.xlabel('u')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.show()
#%% md
# ##  Wyznaczenie błędów
#%%
error_ucz_sum = model_stat_error(dane_ucz[:,0], dane_ucz[:,1], lin_mod_stat_func, a)
error_wer_sum = model_stat_error(dane_wer[:,0], dane_wer[:,1], lin_mod_stat_func, a)

print(error_ucz_sum)
print(error_wer_sum)
errors=np.array([error_ucz_sum])
errors=np.column_stack((errors,error_wer_sum))
header = "Dane uczące,Dane weryfikujące"
np.savetxt("wyniki_csv/bledy_mod_lin.csv", errors, delimiter=",", header=header, comments='', fmt='%.2f')
#%% md
# # Statyczny model nieliniowy metodą najmieszych kwadratów
# ## Wyznaczanie parametrów
#%%
N=6
print(N)
#%%
a=np.zeros((N+1,N))

for n in range(1,N+1):
    a_temp=nmk_nlin_mod_stat(dane_ucz[:,0][:, np.newaxis],dane_ucz[:,1][:, np.newaxis],n)
    a[0:n+1,n-1]=a_temp.ravel()
print(a)
#%% md
# ## Wyznaczanie błędów
#%%
error_ucz_sum = np.zeros((N,1))
error_wer_sum = np.zeros((N,1))
for n in range(1, N+1):
    error_ucz_sum[n-1, 0] = model_stat_error(dane_ucz[:,0], dane_ucz[:,1], nlin_mod_stat_func, a[:n+1,n-1])
    error_wer_sum[n-1, 0] = model_stat_error(dane_wer[:,0], dane_wer[:,1], nlin_mod_stat_func, a[:n+1,n-1])

print(error_ucz_sum)
print(error_wer_sum)

errors=np.array([range(1,N+1)]).T
errors=np.column_stack((errors,error_ucz_sum))
errors=np.column_stack((errors,error_wer_sum))

header = "Stopień wielomianu,Dane uczące,Dane weryfikujące"
np.savetxt("wyniki_csv/bledy_mod_nlin.csv", errors, delimiter=",", header=header, comments='', fmt='%d, %.5f, %.5f')
#%% md
# ## Wykresy
# 
#%% md
# #### Generowanie charakterystyk
#%%
u_vals=np.linspace(-1,1,100)
for n in range(0, N):
    def func(x):
        val=a[0,n]
        for i in range(1,N+1):
            val = val+a[i,n]*x**i
        return val
    
    plt.figure(figsize=(6, 4))
    plt.plot(u_vals,np.vectorize(func)(u_vals))
    
    plt.title('Charakterystyka statyczna y(u) dla potęgi'+str(n+1))
    plt.xlabel('u')
    plt.ylabel('y')
    plt.grid(True)
    path='wykresy/char_stat_nlin'+str(n+1)+'.png'
    plt.savefig(path,dpi=300)
    plt.show()
#%% md
# #### Generowanie wykresów dla zbioru uczącego
#%%
for n in range(0, N):
    def func(x):
        val=a[0,n]
        for i in range(1,N+1):
            val = val+a[i,n]*x**i
        return val

    plt.figure(figsize=(6, 4))
    plt.plot(dane_ucz[:,0],dane_ucz[:,1], 'o', label='obiekt')
    plt.plot(dane_ucz[:,0],np.array([func(x) for x in dane_ucz[:,0]]).T, 'o', label='model')
    plt.title('Wykres modelu i obiektu zbioru uczącego dla potęgi '+str(n+1))
    plt.xlabel('u')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)
    path='wykresy/model_stat_nlin_dane_ucz_pow_'+str(n+1)+'.png'
    plt.savefig(path,dpi=300)
    plt.show()
#%% md
# #### Generowanie wykresów dal zbioru weryfikującego
#%%
for n in range(0, N):
    def func(x):
        val=a[0,n]
        for i in range(1,N+1):
            val = val+a[i,n]*x**i
        return val

    plt.figure(figsize=(6, 4))
    plt.plot(dane_wer[:,0],dane_wer[:,1], 'o', label='obiekt')
    plt.plot(dane_wer[:,0],np.array([func(x) for x in dane_wer[:,0]]).T, 'o', label='model')
    plt.title('Wykres modelu i obiektu zbioru weryfikującego dla potęgi '+str(n+1))
    plt.xlabel('u')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)
    path='wykresy/model_stat_nlin_dane_wer_pow_'+str(n+1)+'.png'
    plt.savefig(path,dpi=300)
    plt.show()
#%%
