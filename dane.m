function data = dane(symb)
data = struct();
if symb
    syms a0 a1 a2 b0 alpha1 alpha2 alpha3 alpha4 u_min u_max
    data.a0=a0;
    data.a1=a1;
    data.a2=a2;
    data.b0=b0;
    data.alpha1=alpha1;
    data.alpha2=alpha2;
    data.alpha3=alpha3;
    data.alpha4=alpha4;
    data.u_min=u_min;
    data.u_max=u_max;
else
    data.a0=0.00185185;
    data.a1=0.0462963;
    data.a2=0.377778;
    data.b0=0.00333333;
    data.alpha1=0.4;
    data.alpha2=0.55;
    data.alpha3=-0.92;
    data.alpha4=0.53;
    data.u_min=-1;
    data.u_max=1;
end
end