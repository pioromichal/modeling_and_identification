set(0, 'defaulttextinterpreter','latex');
set(0, 'DefaultLineLineWidth',1);
set(0, 'DefaultStairLineWidth',1);




symbolicznie = false;
if symbolicznie == true
    syms a0 a1 a2 b0 alpha1 alpha2 alpha3 alpha4
else
    a0=0.00185185;
    a1=0.0462963;
    a2=0.377778;
    b0=0.00333333;
    alpha1=0.4;
    alpha2=0.55;
    alpha3=-0.92;
    alpha4=0.53;
end


u_min=-1;
u_max=1;
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
Xs = solve(dXdt==zeros(3,1), Xt);
y=collect(Xs.x1);

% figure;
% fplot(y,[u_min u_max]);

% setPlotParams('$u$', '$y$', [-1, 3]));
% exportgraphics(gcf,'./wykresy/nieliniowa_charakterystyka_statyczna.png','Resolution',400);



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




%  Zadanie 3
paths_stat=["./wykresy/zlinearyzowane_charakterystyki_statyczne_1.png";"./wykresy/zlinearyzowane_charakterystyki_statyczne_2.png";"./wykresy/zlinearyzowane_charakterystyki_statyczne_3.png"];

u_sim=[-0.5 0 0.5];
% for i=1:3
%     figure;
%     fplot(y,[u_min u_max]);
%     hold on;
%     fplot(subs(y_lin, ud, u_sim(i)), [u_min u_max]);

%     setPlotParams('$u$','$y$',[-1, 3]);
%     exportgraphics(gcf,paths_stat(i),'Resolution',400);
% end




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
ud = 0;
yt_lin = yt;





% Zadanie 6
% Wykresy, wykresy, wykresy
u_step=[0.1, 0.5, 1];
uds=[0 0.5 1];
t_u_step_sim=1;

model_nlin = 'ciagly_nieliniowy_model_dynamiczny';
model_lin = 'ciagly_zlinearyzowany_model_dynamiczny';
open_system(model_nlin,'loadonly');

open_system(model_lin,'loadonly');
paths_zlin=["./wykresy/odpowiedzi_skokowe_1_plin_1.png","./wykresy/odpowiedzi_skokowe_2_plin_1.png","./wykresy/odpowiedzi_skokowe_3_plin_1.png";
    "./wykresy/odpowiedzi_skokowe_1_plin_2.png","./wykresy/odpowiedzi_skokowe_2_plin_2.png","./wykresy/odpowiedzi_skokowe_3_plin_2.png";
    "./wykresy/odpowiedzi_skokowe_1_plin_3.png","./wykresy/odpowiedzi_skokowe_2_plin_3.png","./wykresy/odpowiedzi_skokowe_3_plin_3.png";
    ];
for j=1:3
    u_step_sim=u_step(j);
    simout_nlin = sim(model_nlin,'Solver','ode45','StartTime','0','StopTime','100');
    yt_nlin_sim = simout_nlin.get("yt");
    ut_nlin_sim = simout_nlin.get("ut");
    
    for i=1:3
        ud=uds(i);
        simout_lin = sim(model_lin,'Solver','ode45','StartTime','0','StopTime','100');
        yt_lin_sim = simout_lin.get("yt");
        ut_lin_sim = simout_lin.get("ut");
 
        figure;
        plot(ut_nlin_sim.time,ut_nlin_sim.Data);
        hold on;
        plot(yt_nlin_sim.time,yt_nlin_sim.Data);
        plot(yt_lin_sim.time,yt_lin_sim.Data, '--');
        legend('Sygnał sterujący u', 'Model nieliniowy', sprintf('Model zlinearyzowany w pkt. %.1f', ud),'Location','southeast');
        setPlotParams('$y,u$','$t$',[u_step_sim*(-0.1), u_step_sim*1.1]);
        exportgraphics(gcf,paths_zlin(i,j),'Resolution',400);
    end
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





% Zadanie 8
% Wykresy, wykresy, wykresy
u_step_sim=1;
T_sim=[0.2,1,5];
t_u_step_sim=1;
model_nlin = 'ciagly_nieliniowy_model_dynamiczny';
model_dys = 'dyskretny_nieliniowy_model_dynamiczny';
open_system(model_nlin,'loadonly');
open_system(model_dys,'loadonly');

simout_nlin = sim(model_nlin,'Solver','ode45','StartTime','0','StopTime','100');
yt_nlin_sim = simout_nlin.get("yt");
ut_nlin_sim = simout_nlin.get("ut");

paths_dys=["./wykresy/odpowiedzi_skokowe_dyskretny_1.png";"./wykresy/odpowiedzi_skokowe_dyskretny_2.png";"./wykresy/odpowiedzi_skokowe_dyskretny_3.png"];

for i=1:3
    T=T_sim(i);
    simout_dys = sim(model_dys,'Solver','ode45','StartTime','0','StopTime','100');
    yt_dys_sim = simout_dys.get("yt");
    figure;
    plot(ut_nlin_sim.time,ut_nlin_sim.Data);
    hold on;
    plot(yt_nlin_sim.time,yt_nlin_sim.Data);
    stairs(yt_dys_sim.time,yt_dys_sim.Data);
    ylabel('$y$');
    xlabel('$t$');
    setPlotParams();
    exportgraphics(gcf,paths_dys(i),'Resolution',400);
end


