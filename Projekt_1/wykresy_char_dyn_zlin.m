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
        plot(yt_lin_sim.time,yt_lin_sim.Data, ':');
        legend('Sygnał sterujący u', 'Model nieliniowy', sprintf('Model zlinearyzowany w pkt. %.1f', ud),'Location','southeast');
        setPlotParams('$y,u$','$t$',[u_step_sim*(-0.1), u_step_sim*1.1], [15 10]);
        exportgraphics(gcf,paths_zlin(i,j),'Resolution',400);
    end
end