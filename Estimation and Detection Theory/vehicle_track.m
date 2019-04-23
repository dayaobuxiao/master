clear all;
clc;

delta = 1;
su_square = 0.0001;
A = [1 0 delta 0;0 1 0 delta;0 0 1 0;0 0 0 1];
miu = [0;0;0;0];
Q = [0 0 0 0;0 0 0 0;0 0 su_square 0;0 0 0 su_square];
s_init = [10;-5;-0.2;0.2];
x_ideal = [];
y_ideal = [];
x_true = [];
y_true = [];
sigmaR_square = 0.1;
sigmabeta_square = 0.01;
x_observation = [];
y_observation = [];
s_hat_init = [5;5;0;0];
M_init= [100 0 0 0;0 100 0 0;0 0 100 0;0 0 0 100];
C = [sigmaR_square 0;0 sigmabeta_square];
x_KFestimate = [];
y_KFestimate = [];

for n = 0:100
    %True Track
    u = mvnrnd(miu,Q,1).';
    if n == 0
        s = s_init;
    end
    s = A * s + u;
    x_true(1,n+1) = s(1,1);
    y_true(1,n+1) = s(2,1);
    
    %Ideal Track
    rx = 10 - 0.2 * n;
    ry = -5 + 0.2 * n;
    x_ideal(1,n+1) = rx;
    y_ideal(1,n+1) = ry;
    
    %Observed/Measured
    R = sqrt(s(1,1)^2 + s(2,1)^2);
    beta = atan(s(2,1)/s(1,1));
    wR = normrnd(0,sigmaR_square);
    wbeta = normrnd(0,sigmabeta_square);
    R_hat = R + wR;
    beta_hat = beta + wbeta;
    X = [R_hat;beta_hat];
    x_observation(1,n+1) = R_hat * cos(beta_hat);
    y_observation(1,n+1) = R_hat * sin(beta_hat);
    
    %Kalman Filter Estimate
    if n == 0
        s1 = s_hat_init;
        M1 = M_init;
    end
    s2 = A * s1;
    M2 = A * M1 * A' + Q;
    R1 = sqrt(s2(1,1)^2 + s2(2,1)^2);
    H = [s2(1,1)/R1 s2(2,1)/R1 0 0;-s2(2,1)/(R1^2) s2(1,1)/(R1^2) 0 0];
    K = M2 * H' * (C + H * M2 * H')^(-1);
    h = [sqrt(s2(1,1)^2 + s2(2,1)^2);atan(s2(2,1)/s2(1,1))];
    s1 = s2 + K * (X - h);
    M1 = (eye(4) - K * H) * M2;
    x_KFestimate(1,n+1) = s1(1,1);
    y_KFestimate(1,n+1) = s1(2,1);
end

figure(1);  %plot figure 13.22
a = plot(x_ideal,y_ideal,'--b');
hold on;
b = plot(x_true,y_true,'-r');
xlabel('True and straight line rx[n]');
ylabel('True and straight line ry[n]');
legend([a,b],'Ideal Track','True Track');
title('Realization of vehicle track');
 
figure(2);  %plot figure 13.24
c = plot(x_true,y_true,'--b');
hold on;
d = plot(x_observation,y_observation,'-r');
xlabel('Noise corrupted and true rx[n]');
ylabel('Noise corrupted and true ry[n]');
legend([c,d],'True Track','Observed Track');
title('True and observed vehicle tracks');

figure(3);  %plot figure 13.25
e = plot(x_true,y_true,'--b');
hold on;
f = plot(x_KFestimate,y_KFestimate,'-r');
xlabel('Kalman estimate and true rx[n]');
ylabel('Kalman estimate and true ry[n]');
legend([e,f],'True Track','Kalman estimate');
title('True and extended Kalman filter estimate');

figure(4);  %plot Kalman Filter Estimate vs. Observed Track vs. True Track
g = plot(x_true,y_true,'--');
hold on;
i = plot(x_observation,y_observation);
hold on;
j = plot(x_KFestimate,y_KFestimate);
xlabel('rx[n]');
ylabel('ry[n]');
legend([g,i,j],'True Track','Observed Track','Kalman estimate');
title('Kalman Filter Estimate vs. Observed Track vs. True Track');

