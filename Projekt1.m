a0=0.00185185;
a1=0.0462963;
a2=0.377778;
b0=0.00333333;
alpha1=0.4;
alpha2=0.55;
alpha3=-0.92;
alpha4=0.53;
u_min=-1;
u_max=1;
% syms a0 a1 a2 b0 alpha1 alpha2 alpha3 alpha4

X_0=[0;0;0];

syms x1 x2 x3 u y

dx1=-a2*x1+x2;
dx2=-a1*x1+x3;
dx3=-a0*x1+b0*(alpha1*u+alpha2*u^2+alpha3*u^3+alpha4*u^4);
yt=x1;

% Zadanie 1
Xs = solve([dx1 == 0, dx2 == 0, dx3 == 0], [x1, x2, x3]);
y=collect(Xs.x1);

%fplot(y,[u_min u_max]);

% Zadanie 2
syms ud

% Linearyzacja f_i(u)
up = [u u^2 u^3 u^4];
up_lin=u;
for i=2:4
    up_lin(i) = subs(up(i),u,ud) + subs(diff(up(i), u),u,ud)*(u-ud); 
end

% Linearyzacja ciągłego modelu statycznego
y_lin=y;
for i=4:-1:2
    y_lin=subs(y_lin,up(i),up_lin(i)); 
end
y_lin = collect(y_lin);

%  Zadanie 3

% fplot(y,[u_min u_max]);
% hold on;
% y_lin_p = subs(y_lin, ud, 0);
% fplot(y_lin_p, [u_min u_max])
% y_lin_p = subs(y_lin, ud, -0.5);
% fplot(y_lin_p, [u_min u_max])
% y_lin_p = subs(y_lin, ud, 0.5);
% fplot(y_lin_p, [u_min u_max])

% Zadanie 4
% Simulink

% Zadanie 5
% Linearyzacja ciągłego modelu dynamicznego

dx3_lin = dx3;
for i=4:-1:2
    dx3_lin=subs(dx3_lin,up(i),up_lin(i)); 
end
expand(dx3_lin);
dx3_lin = collect(dx3_lin);
dX_lin = [dx1;dx2;dx3_lin];
ud = 0;
yt_lin = yt;


