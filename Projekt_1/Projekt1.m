set(0, 'defaulttextinterpreter','latex');
set(0, 'DefaultLineLineWidth',1);
set(0, 'DefaultStairLineWidth',1);
clear all;
close all;

wykresy = true;
symbolicznie = true;    

if wykresy
    data = dane(false);
else
    data = dane(symbolicznie);
end


a0=data.a0;
a1=data.a1;
a2=data.a2;
b0=data.b0;
alpha1=data.alpha1;
alpha2=data.alpha2;
alpha3=data.alpha3;
alpha4=data.alpha4;
u_min=data.u_min;
u_max=data.u_max;  

X_0=[0;0;0];


syms x1 x2 x3 ut
Xt=[x1;x2;x3];
dx1=-a2*x1+x2;
dx2=-a1*x1+x3;
dx3=-a0*x1+b0*(alpha1*ut+alpha2*ut^2+alpha3*ut^3+alpha4*ut^4);
yt=x1;
dXdt=[dx1;dx2;dx3];


% Zadanie 1
% Model nieliniowy statyczny
X = solve(dXdt==zeros(3,1), Xt);
y=collect(X.x1);

if wykresy
    wykresy_char_stat_nlin(data, y);
end


% Zadanie 2
syms ud

% Linearyzacja f(u(t))
up = [ut ut^2 ut^3 ut^4];
up_lin=ut;
for i=2:4
    up_lin(i) = subs(up(i),ut,ud) + subs(diff(up(i), ut),ut,ud)*(ut-ud); 
end

% Linearyzacja ciągłego modelu statycznego
y_lin=y;
for i=4:-1:2
    y_lin=subs(y_lin,up(i),up_lin(i)); 
end
y_lin = collect(expand(y_lin),ut);




% %  Zadanie 3
if wykresy
    wykresy_char_stat_zlin(data,y,y_lin);
end

% Zadanie 4
% Simulink


% Zadanie 5
% Simulink
% Linearyzacja ciągłego modelu dynamicznego

dx3_lin = dx3;
for i=4:-1:2
    dx3_lin=subs(dx3_lin,up(i),up_lin(i)); 
end

dx3_lin = collect(expand(dx3_lin),[ut b0]);
dx3_lin_lat = latex(dx3_lin);
dX_lin = [dx1;dx2;dx3_lin];
yt_lin = yt;


% Zadanie 6
% Wykresy, wykresy, wykresy

if wykresy
    wykresy_char_dyn_zlin;
end


% Zadanie 7
% Dyskretyzacja modelu nieliniowego
syms xk1 xk2 xk3 xkp11 xkp12 xkp13 uk
syms T
Xk=[xk1;xk2;xk3];
Xkp1=[xkp11; xkp12; xkp13];
for i=1:3
    Xkp1(i)=solve(dXdt(i)==(Xkp1(i)-Xk(i))/T,Xkp1(i));
    for j=1:3
        Xkp1(i)=subs(Xkp1(i),Xt(j),Xk(j));
    end
    Xkp1(i)=subs(Xkp1(i),ut,uk);
    Xkp1(i)=collect(Xkp1(i));
end
yk = xk1;
Xkp1_lat=latex(Xkp1);
yk_lat=latex(yk);

% Zadanie 8
% Wykresy, wykresy, wykresy
if wykresy
    wykresy_char_dyn_dys;
end


%Zadanie dodatkowe

[G, K_stat]=transmitancja_dyskretna(data, dX_lin);
syms ud
if wykresy==true || symbolicznie==false
    uds=[0.0 0.5 1.0];
    for i=1:3
        K_stat_vals(i)=double(subs(K_stat, ud, uds(i)));
    end
end

