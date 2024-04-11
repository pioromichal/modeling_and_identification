function wykresy_char_stat_zlin(data, y, y_lin)
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
syms u ud 
 
paths_stat=["./wykresy/zlinearyzowane_charakterystyki_statyczne_1.png";"./wykresy/zlinearyzowane_charakterystyki_statyczne_2.png";"./wykresy/zlinearyzowane_charakterystyki_statyczne_3.png"];
u_vals=linspace(u_min,u_max,100);
y_fun = matlabFunction(y);
y_vals=y_fun(u_vals);
u_sim=[-0.5 0 0.5];
for i=1:3
    figure;  
    plot(u_vals, y_vals);
    hold on;
    y_lin_fun = matlabFunction(subs(y_lin, ud, u_sim(i)));
    y_lin_vals=y_lin_fun(u_vals);
    plot(u_vals, y_lin_vals, ':');
    legend('Charakterystyka nieliniowa', sprintf('Charakterystyka zlinearyzowana w pkt. %.1f', u_sim(i)),'Location','northeast');
    setPlotParams('$u$','$y$',[-1, 3], [13 10]);
    exportgraphics(gcf,paths_stat(i),'Resolution',400);
end
end