function wykresy_char_stat_nlin(data,y)
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


figure;
u_vals=linspace(u_min,u_max,100);
y_fun = matlabFunction(y);
y_vals=y_fun(u_vals);
plot(u_vals, y_vals);
legend('Charakterystyka nieliniowa','Location','northeast');
setPlotParams('$y$', '$u$', [-1, 3], [12 10]);
exportgraphics(gcf,'./wykresy/nieliniowa_charakterystyka_statyczna.png','Resolution',400);


end