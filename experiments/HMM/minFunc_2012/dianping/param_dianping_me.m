function parameters = param_dianping_me(U, I, E, K, S)
param1 = 2 * rand(U + E*(E-1)*I/2, 1) - 1;
param2 = 0.5 + 0.5 * rand(E + U*E + I*E + U*E*K + I*E*K, 1);
param3 = 0.05 * rand(U*E + U*S*E, 1);
parameters = [param1;param2;param3];
end