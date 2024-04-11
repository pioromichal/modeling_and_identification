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
    stairs(yt_dys_sim.time,yt_dys_sim.Data, ':');

    legend('Sygnał sterujący u', 'Model nieliniowy', sprintf('Model dyskrtetny: T=%.1f', T),'Location','southeast');    
    setPlotParams('$y,u$','$t$',[u_step_sim*(-0.1), u_step_sim*1.1], [15 10]);
    exportgraphics(gcf,paths_dys(i),'Resolution',400);
end