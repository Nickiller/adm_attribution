clear all;clc;

STARTING_POINT = 1;
END_POINT = 1;

info = importdata('..\dianping\info_dianping_chaoyang_50_0.txt');
U = info(1);
I = info(2);

testing_num = 5;
training_name = strcat('..\dianping\data_dianping_chaoyang_total_training_set_testing_',num2str(testing_num),'.txt');
testing_name = strcat('..\dianping\data_dianping_chaoyang_total_testing_set_testing_',num2str(testing_num),'.txt');
predict_name = strcat('..\dianping\predict_value_dianping_chaoyang_total_me_testing_',num2str(testing_num),'.txt');
predict_min_name = strcat('..\dianping\predict_value_dianping_chaoyang_total_me_min_testing_',num2str(testing_num),'.txt');
training_data = importdata(training_name);
testing_data = importdata(testing_name);

E = 5;
K = 1;
S = 5;
rmax = 5;

maxFunEvals = 5000;
maxIter = 1000;
LS_interp = 0;
LS_type = 0;
options = [];
%options.display = 'none';
options.maxFunEvals = maxFunEvals;
options.maxIter = maxIter;
options.LS_interp = LS_interp;
options.LS_type = LS_type;
options.Method = 'lbfgs';

fprintf('Number of testing data per user is %g.\n\n',testing_num);

%matlabpool open local 6;

for count_times = STARTING_POINT:1:END_POINT
    parameters = param_dianping_me(U, I, E, K, S);
    [MSE, accuracy, accuracy_loose] = calculate_dianping_me(parameters, training_data, testing_data, U, I, E, K, S, rmax, options, testing_num, count_times, predict_name);
    fprintf('MSE, accuracy and loose accuracy value of my prediction (full version, starting points sets %g)\nis %g, %g and %g.\n', count_times, MSE, accuracy, accuracy_loose);
    fprintf('\nAlready finished prediction of %gth sets of starting points.\n\n',count_times);
end

%matlabpool close;

pause(2);

prediction = importdata(predict_name);
MSE = prediction(:,1);
accuracy = prediction(:,2);
accuracy_loose = prediction(:,3);
average_MSE = mean(MSE);
var_MSE = std(MSE);
average_accuracy = mean(accuracy);
var_accuracy = std(accuracy);
average_accuracy_loose = mean(accuracy_loose);
var_accuracy_loose = std(accuracy_loose);
fprintf('Average MSE value and variance of prediction on dianping datasets \nusing my method (full version) is %g (%g).\n',average_MSE, var_MSE);
fprintf('Average accuracy and variance of prediction on dianping datasets \nusing my method (full version) is %g (%g).\n',average_accuracy, var_accuracy);
fprintf('Average loose accuracy and variance of prediction on dianping datasets \nusing my method (full version) is %g (%g).\n',average_accuracy_loose, var_accuracy_loose);