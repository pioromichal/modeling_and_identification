function [G, K_stat] = transmitancja_dyskretna(data, dX_lin)
a0=data.a0;
a1=data.a1;
a2=data.a2;
b0=data.b0;
alpha1=data.alpha1;
alpha2=data.alpha2;
alpha3=data.alpha3;
alpha4=data.alpha4;
syms ut ud s

% Zadanie dodatkowe
A=[-a2 1 0; -a1 0 1; -a0 0 0];
u_coeffs=coeffs(dX_lin(3),ut);
u_coeff=u_coeffs(2);
B=[0; 0; u_coeff];
C=[0 0 1];
G=C*(s*eye(3,3)-A)^(-1)*B;
expand(G);
collect(G);
K_stat=subs(G,s,0);

end