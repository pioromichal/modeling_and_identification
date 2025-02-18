#%%
import numpy as np
import matplotlib.pyplot as plt
from Projekt_2 import nmk_lin_mod_dyn, model_dyn_error, lin_mod_dyn_func, lin_mod_dyn_rek_func, lin_mod_dyn_y, \
    lin_mod_dyn_rek_y, nmk_nlin_mod_dyn, nlin_mod_dyn_y, nlin_mod_dyn_rek_y, model_error, model_dyn_error_rek

#%% md
# # Import danych
#%%
dane_ucz = np.loadtxt('dane/danedynucz13.txt')
dane_wer = np.loadtxt('dane/danedynwer13.txt')
#%% md
# ## Rysowanie wykresów
#%%
plt.figure(figsize=(6, 4))
plt.plot(dane_ucz[:,1], label='y')
plt.plot(dane_ucz[:,0], label='u')
plt.title('Wykres danych uczących')
plt.xlabel('k')
plt.ylabel('y,u')
plt.legend()
plt.grid(True)
path='wykresy_dyn/dane_uczace.png'
plt.savefig(path,dpi=200)
plt.show()
#%%
plt.figure(figsize=(6, 4))
plt.plot(dane_wer[:,1], label='y')
plt.plot(dane_wer[:,0], label='u')
plt.title('Wykres danych weryfikujących')
plt.xlabel('u')
plt.ylabel('y')
plt.legend()
plt.grid(True)
path='wykresy_dyn/dane_weryfikujace.png'
plt.savefig(path,dpi=200)
plt.show()
#%% md
# # Dynamiczny model liniowy metodą najmniejszych kwadratów
# 
#%%
N=3
#%% md
# ## Wyznaczanie parametrów
#%%
a=np.zeros((N,N))
b=np.zeros((N,N))

for n in range(1,N+1):
    a_temp, b_temp = nmk_lin_mod_dyn(dane_ucz[:,0],dane_ucz[:,1],n)
    b[0:n,n-1]=b_temp
    a[0:n,n-1]=a_temp
print(b)
print(a)

#%% md
# # Wykresy
#%% md
# ### Dane uczące bez rekurencji
#%%
for n in range(1, N+1):  
    plt.figure(figsize=(6, 4))
    plt.plot(dane_ucz[:,1], label='obiekt: y')
    plt.plot(dane_ucz[:,0], label='u')
    k_vals=np.array(range(N,dane_ucz.shape[0]))
    plt.plot(k_vals, lin_mod_dyn_y(dane_ucz[:,0],dane_ucz[:,1],a[:n,n-1],b[:n,n-1],k_vals,N), label='model: y')
    
    plt.title('Wykres modelu bez rekurencji dla zbioru uczącego dla n_A=n_B='+str(n))
    plt.xlabel('k')
    plt.ylabel('y,u')
    plt.legend()
    plt.grid(True)
    path='wykresy_dyn/dane_uczace_bez_rek_r_dyn_'+str(n)+'.png'
    plt.savefig(path,dpi=200)
    plt.show()
#%% md
# ### Dane uczące z rekurencją
#%%
for n in range(1, N+1):
    plt.figure(figsize=(6, 4))
    plt.plot(dane_ucz[:,1], label='obiekt: y')
    plt.plot(dane_ucz[:,0], label='u')
    k_vals=np.array(range(N,dane_ucz.shape[0]))
    y_mod=lin_mod_dyn_rek_y(dane_ucz[:,0],dane_ucz[:,1],a[:n,n-1],b[:n,n-1],k_vals, N)
    plt.plot(k_vals, y_mod[N:,0], label='model: y')
    plt.title('Wykres modelu z rekurencją dla zbioru uczącego dla n_A=n_B='+str(n))
    plt.xlabel('k')
    plt.ylabel('y,u')
    plt.legend()
    plt.grid(True)
    path='wykresy_dyn/dane_uczace_z_rek_r_dyn_'+str(n)+'.png'
    plt.savefig(path,dpi=200)
    plt.show()
#%% md
# ### Dane weryfikujące bez rekurencji
#%%
for n in range(1, N+1):
    plt.figure(figsize=(6, 4))
    plt.plot(dane_wer[:,1], label='obiekt: y')
    plt.plot(dane_wer[:,0], label='u')
    k_vals=np.array(range(N,dane_wer.shape[0]))
    plt.plot(k_vals, lin_mod_dyn_y(dane_wer[:,0],dane_wer[:,1],a[:n,n-1],b[:n,n-1],k_vals,N), label='model: y')
    plt.title('Wykres modelu bez rekurencji dla zbioru uczącego dla n_A=n_B='+str(n))
    plt.xlabel('k')
    plt.ylabel('y,u')
    plt.legend()
    plt.grid(True)
    path='wykresy_dyn/dane_weryf_bez_rek_r_dyn_'+str(n)+'.png'
    plt.savefig(path,dpi=200)
    
#%% md
# ### Dane weyfikujące z rekurencją
#%%
for n in range(1, N+1):
    plt.figure(figsize=(6, 4))
    plt.plot(dane_wer[:,1], label='obiekt: y')
    plt.plot(dane_wer[:,0], label='u')
    k_vals=np.array(range(N,dane_wer.shape[0]))
    y_mod=lin_mod_dyn_rek_y(dane_wer[:,0],dane_wer[:,1],a[:n,n-1],b[:n,n-1],k_vals, N)
    plt.plot(k_vals, y_mod[N:,0], label='model: y')
    plt.title('Wykres modelu z rekurencją dla zbioru uczącego dla n_A=n_B='+str(n))
    plt.xlabel('k')
    plt.ylabel('y,u')
    plt.legend()
    plt.grid(True)
    path='wykresy_dyn/dane_weryf_z_rek_r_dyn_'+str(n)+'.png'
    plt.savefig(path,dpi=200)
    plt.show()
#%% md
# ## Obliczanie błędów
#%%

error_ucz = np.zeros((N,1))
error_wer = np.zeros((N,1))
error_ucz_rek = np.zeros((N,1))
error_wer_rek = np.zeros((N,1))
for n in range(N):
    error_ucz[n, 0] = model_dyn_error(dane_ucz[:,0],dane_ucz[:,1],a[:n+1,n],b[:n+1,n],N,lin_mod_dyn_y)
    error_wer[n, 0] = model_dyn_error(dane_wer[:,0],dane_wer[:,1],a[:n+1,n],b[:n+1,n],N,lin_mod_dyn_y)
    error_ucz_rek[n, 0] = model_dyn_error_rek(dane_ucz[:,0],dane_ucz[:,1],a[:n+1,n],b[:n+1,n],N)
    error_wer_rek[n, 0] = model_dyn_error_rek(dane_wer[:,0],dane_wer[:,1],a[:n+1,n],b[:n+1,n],N)

errors=np.array([range(1,N+1)]).T
errors=np.column_stack((errors,error_ucz))
errors=np.column_stack((errors,error_ucz_rek))
errors=np.column_stack((errors,error_wer))
errors=np.column_stack((errors,error_wer_rek))

header = "Stopień wielomianu,Dane uczące,Dane weryfikujące"
np.savetxt("wyniki_csv/bledy_mod_dyn_lin.csv", errors, delimiter=",", header=header, comments='', fmt='%d, %.5f, %.5f, %.5f, %.5f')
print(errors)
#%% md
# # Dynamiczny model nieliniowy metodą najmniejszych kwadratów
# 
#%% md
# ## Wyznaczanie parametrów nmk
#%%
p_max=4
r_dyn_max=3

w_vals=np.zeros((p_max*r_dyn_max*2,(p_max-1)*r_dyn_max))
tmp=0
for r_dyn in range(1, r_dyn_max + 1):
    for p in range(2, p_max + 1):
        w = nmk_nlin_mod_dyn(dane_ucz[:,0],dane_ucz[:,1],r_dyn, p)
        w_vals[0:r_dyn*p*2,tmp] = w
        tmp+=1
print(w_vals)
#%% md
# ## Wykresy
#%%
errors={'wer': np.zeros((r_dyn_max,p_max-1)),
        'ucz': np.zeros((r_dyn_max,p_max-1)),
        'wer_rek': np.zeros((r_dyn_max,p_max-1)),
        'ucz_rek': np.zeros((r_dyn_max,p_max-1))
        }
#%% md
# ### Dane uczące bez rekurencji
#%%
for r_dyn in range(1, r_dyn_max + 1):
    for p in range(2, p_max + 1):
        w = nmk_nlin_mod_dyn(dane_ucz[:,0],dane_ucz[:,1],r_dyn, p)
        y_mod = nlin_mod_dyn_y(dane_ucz[:,0],dane_ucz[:,1],w,r_dyn,p,r_dyn_max)
        errors['ucz'][r_dyn-1,p-2] = model_error(dane_ucz[r_dyn_max:,1], y_mod)
        k_vals=np.array(range(r_dyn_max,dane_ucz.shape[0]))

        plt.figure(figsize=(6, 4))
        plt.plot(dane_ucz[:,1], label='obiekt: y')
        plt.plot(dane_ucz[:,0], label='u')
        plt.plot(k_vals,y_mod, label='model: y')
        
        plt.title('Wykres modelu bez rekurencji dla zbioru uczącego rzedu '+str(r_dyn)+' stopnia '+str(p))
        plt.xlabel('k')
        plt.ylabel('y,u')
        plt.legend()
        plt.grid(True)
        path='wykresy_dyn_nlin/dane_uczace_bez_rek_r_dyn_'+str(r_dyn)+'_st_'+str(p)+'.png'
        plt.savefig(path,dpi=200)
        plt.show()
#%% md
# ### Dane uczące z rekurencją
# 
#%%
for r_dyn in range(1, r_dyn_max + 1):
    for p in range(2, p_max + 1):
        w = nmk_nlin_mod_dyn(dane_ucz[:,0],dane_ucz[:,1],r_dyn, p)
        y_mod=nlin_mod_dyn_rek_y(dane_ucz[:,0],dane_ucz[:,1],w,r_dyn,p,r_dyn_max)
        errors['ucz_rek'][r_dyn-1,p-2] = model_error(dane_ucz[r_dyn_max:,1][:, np.newaxis], y_mod)
        
        plt.figure(figsize=(6, 4))
        plt.plot(dane_ucz[:,1], label='obiekt: y')
        plt.plot(dane_ucz[:,0], label='u')
        
        plt.plot(nlin_mod_dyn_rek_y(dane_ucz[:,0],dane_ucz[:,1],w,r_dyn,p,r_dyn_max), label='model: y')
        
        plt.title('Wykres modelu z rekurencją dla zbioru uczącego rzedu '+str(r_dyn)+' stopnia '+str(p))
        plt.xlabel('k')
        plt.ylabel('y,u')
        plt.legend()
        plt.grid(True)
        path='wykresy_dyn_nlin/dane_uczace_z_rek_r_dyn_'+str(r_dyn)+'_st_'+str(p)+'.png'
        plt.savefig(path,dpi=200)
        plt.show()
#%% md
# ### Dane weryfikujące bez rekurencji
#%%
for r_dyn in range(1, r_dyn_max + 1):
    for p in range(2, p_max + 1):
        w = nmk_nlin_mod_dyn(dane_ucz[:,0],dane_ucz[:,1],r_dyn, p)
        y_mod=nlin_mod_dyn_y(dane_wer[:,0],dane_wer[:,1],w,r_dyn,p,r_dyn_max)
        y=dane_wer[:,1]
        errors['wer'][r_dyn-1,p-2] = model_error(dane_wer[r_dyn_max:,1], y_mod)
        
        plt.figure(figsize=(6, 4))
        plt.plot(dane_wer[:,1], label='obiekt: y')
        plt.plot(dane_wer[:,0], label='u')
        plt.plot(y_mod, label='model: y')
        
        plt.title('Wykres modelu bez rekurencji dla zbioru weryfikującego rzedu '+str(r_dyn)+' stopnia '+str(p))
        plt.xlabel('k')
        plt.ylabel('y,u')
        plt.legend()
        plt.grid(True)
        path='wykresy_dyn_nlin/dane_wer_bez_rek_r_dyn_'+str(r_dyn)+'_st_'+str(p)+'.png'
        plt.savefig(path,dpi=200)
        plt.show()
#%% md
# ### Dane weryfikujące z rekurencją
#%%
for r_dyn in range(1, r_dyn_max + 1):
    for p in range(2, p_max + 1):
        w = nmk_nlin_mod_dyn(dane_ucz[:,0],dane_ucz[:,1],r_dyn, p)
        y_mod=nlin_mod_dyn_rek_y(dane_wer[:,0],dane_wer[:,1],w,r_dyn,p,r_dyn_max)
        error = model_error(dane_wer[r_dyn_max:,1][:, np.newaxis], y_mod)
        errors['wer_rek'][r_dyn-1,p-2] = error
        
        plt.figure(figsize=(6, 4))
        plt.plot(dane_wer[:,1], label='obiekt: y')
        plt.plot(dane_wer[:,0], label='u')
        plt.plot(y_mod, label='model: y')

        plt.title('Wykres modelu z rekurencją dla zbioru weryfikującego rzędu '+str(r_dyn)+' stopnia '+str(p))
        plt.xlabel('k')
        plt.ylabel('y,u')
        plt.legend()
        plt.grid(True)
        path='wykresy_dyn_nlin/dane_wer_z_rek_r_dyn_'+str(r_dyn)+'_st_'+str(p)+'.png'
        plt.savefig(path,dpi=200)
        plt.show()
#%%
print(errors['ucz'])
#%%
print(errors['ucz_rek'])
#%%
print(errors['wer'])
#%%
print(errors['wer_rek'])
#%%
errors_csv=np.array([range(1, N + 1)]).T
errors_csv=np.column_stack((errors_csv, errors['ucz']))
errors_csv=np.column_stack((errors_csv, errors['ucz_rek']))
errors_csv=np.column_stack((errors_csv, errors['wer']))
errors_csv=np.column_stack((errors_csv, errors['wer_rek']))

header = "Rząd dynamiki,Dane uczące,Dane weryfikujące"
np.savetxt("wyniki_csv/bledy_mod_dyn_nlin.csv", errors_csv, delimiter=",", header=header, comments='',fmt = ['%d'] + ['%.4f'] * (errors_csv.shape[1] - 1))
#%%

#%%

#%%
