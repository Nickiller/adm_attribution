function [MSE,accuracy,accuracy_loose] = calculate_dianping_me(parameters, training_data, testing_data, U, I, E, K, S, rmax, options, testing_num, count_times, predict_name)
    old_parameters = parameters;
    difference = 1;
    rounds = 1;
    last_training_data = training_data;
    while difference~=0
        tic;[new_parameters,f] = minFunc(@fg_calculation, old_parameters, options, last_training_data, U, I, E, K, S, rmax);toc;
        tic;next_training_data = route_calculation(new_parameters, last_training_data, U, I, E, K, S, rmax);toc;
        old_level = last_training_data(:,4);
        new_level = next_training_data(:,4);
        difference = sum(abs(new_level - old_level));
        last_training_data = next_training_data;
        fprintf('Calculation finished %g round(s), route difference is %g, parameter difference is %g, f value is %g.\n',rounds, difference, sum(abs(new_parameters - old_parameters)), f);
        rounds = rounds + 1;
        old_parameters = new_parameters;
    end
    
    parameters_output = strcat('..\dianping\Final_Results_Me\final_parameters_dianping_chaoyang_total_me_testing_',num2str(testing_num),'_count_',num2str(count_times),'.txt');
    fid = fopen(parameters_output,'wt');
    [m n] = size(new_parameters);
    for i = 1:1:m
        for j = 1:1:n
            if j == n
                fprintf(fid,'%g\n',new_parameters(i,j));
            else
                fprintf(fid,'%g\t',new_parameters(i,j));
            end
        end
    end
    fclose(fid);
    data_output = strcat('..\dianping\Final_Results_Me\final_data_dianping_chaoyang_total_me_testing_',num2str(testing_num),'_count_',num2str(count_times),'.txt');
    fid2 = fopen(data_output,'wt');
    [m n] = size(next_training_data);
    for i = 1:1:m
        for j = 1:1:n
            if j == n
                fprintf(fid2,'%g\n',next_training_data(i,j));
            else
                fprintf(fid2,'%g\t',next_training_data(i,j));
            end
        end
    end
    fclose(fid2);
    
    [MSE,accuracy,accuracy_loose] = predict_calculation(new_parameters, testing_data, next_training_data, U, I, E, K, rmax, testing_num, predict_name, count_times);
end


function [f,g] = fg_calculation(parameters, data, U, I, E, K, S, rmax)
f = 0;

lu = reshape(parameters(1:U), U, 1);
li = reshape(parameters(U+1 : U+E*(E-1)*I/2), I, E*(E-1)/2);
al = reshape(parameters(U+E*(E-1)*I/2+1 : U+E*(E-1)*I/2+E), E, 1);
bu = reshape(parameters(U+E*(E-1)*I/2+E+1 : U+E*(E-1)*I/2+E+U*E), U, E);
bi = reshape(parameters(U+E*(E-1)*I/2+E+U*E+1 : U+E*(E-1)*I/2+E+U*E+I*E), I, E);
gu = reshape(parameters(U+E*(E-1)*I/2+E+U*E+I*E+1 : U+E*(E-1)*I/2+E+U*E+I*E+U*K*E), U, E*K);
gi = reshape(parameters(U+E*(E-1)*I/2+E+U*E+I*E+U*K*E+1 : U+E*(E-1)*I/2+E+U*E+I*E+U*K*E+I*K*E), I, E*K);
xs = reshape(parameters(U+E*(E-1)*I/2+E+U*E+I*E+U*K*E+I*K*E+1 : U+E*(E-1)*I/2+E+U*E+I*E+U*K*E+I*K*E+U*E), U, E);
ys = reshape(parameters(U+E*(E-1)*I/2+E+U*E+I*E+U*K*E+I*K*E+U*E+1 : U+E*(E-1)*I/2+E+U*E+I*E+U*K*E+I*K*E+U*E+U*S*E), U, E*S);

glu = zeros(U,1);
gli = zeros(I,E*(E-1)/2);
gal = zeros(E,1);
gbu = zeros(U,E);
gbi = zeros(I,E);
ggu = zeros(U,E*K);
ggi = zeros(I,E*K);
gxs = zeros(U,E);
gys = zeros(U,E*S);

for nu = 1:1:U
    udata = data(data(:,1) == nu,:);
    T = size(udata, 1);
    
    for ni = 1:1:T
        idu = udata(ni,1);
        idi = udata(ni,2);
        r = udata(ni,3);
        level = udata(ni,4);
        if ni == 1
            level_last = 1;
        else
            level_last = udata(ni-1,4);
        end
        ravg = udata(ni,5);
        rpre = udata(ni,6:10);
        
        QQ = zeros(1,E);
        QQ(level_last) = 1;
        for k = level_last+1:1:E
            QQ(k) = exp(lu(idu) + li(idi, (4-k/2)*(k-1)-1+level));
        end
        Q = QQ ./ sum(QQ);
        
        if level ~= level_last
            glu(idu) = glu(idu) + Q(level_last);
            for slash = level_last+1:1:E
                if slash == level
                    gli(idi, (4-level_last/2)*(level_last-1)-1+slash) = gli(idi, (4-level_last/2)*(level_last-1)-1+slash) + 1 -  QQ(slash) / sum(QQ);
                else
                    gli(idi, (4-level_last/2)*(level_last-1)-1+slash) = gli(idi, (4-level_last/2)*(level_last-1)-1+slash) -  QQ(slash) / sum(QQ);
                end
            end
        else
            glu(idu) = glu(idu) + Q(level_last) - 1;
            for slash = level_last+1:1:E
                gli(idi, (4-level_last/2)*(level_last-1)-1+slash) = gli(idi, (4-level_last/2)*(level_last-1)-1+slash) -  QQ(slash) / sum(QQ);
            end
        end
        
        p = (al(level,1) + bu(idu,level) + bi(idi,level) + gu(idu,level*K-K+1:level*K) * gi(idi,level*K-K+1:level*K) + xs(idu,level) * (ravg-r) + ys(idu,level*S-S+1:level*S) * (rpre - r)') / rmax;
        fai = nchoosek(rmax-1, r-1) * p^(r-1) * (1-p)^(rmax-r);
        
        diff = ((r-1)/p + (rmax - r)/(p-1))/rmax;
        gal(level) = gal(level) + diff;
        gbu(idu,level) = gbu(idu,level) + diff;
        gbi(idi,level) = gbi(idi,level) + diff;
        ggu(idu,level*K-K+1:level*K) = ggu(idu,level*K-K+1:level*K) + diff * ggi(idi,level*K-K+1:level*K);
        ggi(idi,level*K-K+1:level*K) = ggi(idi,level*K-K+1:level*K) + diff * ggu(idu,level*K-K+1:level*K);
        gxs(idu,level) = gxs(idu,level) + diff * (ravg-r);
        for s = 1:1:S
            temp_r = rpre - r;
            gys(idu,(level-1)*S+s) = gys(idu,(level-1)*S+s) + diff * temp_r(s);
        end
        
        f = f - log(Q(level)) - log(fai);
    end
end

ngli = reshape(gli,I*E*(E-1)/2,1);
ngbu = reshape(gbu,U*E,1);
ngbi = reshape(gbi,I*E,1);
nggu = reshape(ggu,U*E*K,1);
nggi = reshape(ggi,I*E*K,1);
ngxs = reshape(gxs,U*E,1);
ngys = reshape(gys,U*E*S,1);
g = [glu;ngli;gal;ngbu;ngbi;nggu;nggi;ngxs;ngys];
g = -g;
end


function output = route_calculation(parameters, data, U, I, E, K, S, rmax)
output = [];
pai = [1,0,0,0,0];
lu = reshape(parameters(1:U), U, 1);
li = reshape(parameters(U+1 : U+E*(E-1)*I/2), I, E*(E-1)/2);
al = reshape(parameters(U+E*(E-1)*I/2+1 : U+E*(E-1)*I/2+E), E, 1);
bu = reshape(parameters(U+E*(E-1)*I/2+E+1 : U+E*(E-1)*I/2+E+U*E), U, E);
bi = reshape(parameters(U+E*(E-1)*I/2+E+U*E+1 : U+E*(E-1)*I/2+E+U*E+I*E), I, E);
gu = reshape(parameters(U+E*(E-1)*I/2+E+U*E+I*E+1 : U+E*(E-1)*I/2+E+U*E+I*E+U*K*E), U, E*K);
gi = reshape(parameters(U+E*(E-1)*I/2+E+U*E+I*E+U*K*E+1 : U+E*(E-1)*I/2+E+U*E+I*E+U*K*E+I*K*E), I, E*K);
xs = reshape(parameters(U+E*(E-1)*I/2+E+U*E+I*E+U*K*E+I*K*E+1 : U+E*(E-1)*I/2+E+U*E+I*E+U*K*E+I*K*E+U*E), U, E);
ys = reshape(parameters(U+E*(E-1)*I/2+E+U*E+I*E+U*K*E+I*K*E+U*E+1 : U+E*(E-1)*I/2+E+U*E+I*E+U*K*E+I*K*E+U*E+U*S*E), U, E*S);

for user = 1:1:U
    umatrix = data(data(:,1)==user,:);
    nit = size(umatrix,1);
    ksi = zeros(E,nit);
    fai = zeros(E,nit);
    for a = 1:1:nit
        uid = umatrix(a,1);
        iid = umatrix(a,2);
        r = umatrix(a,3);
        ravg = umatrix(a,5);
        rpre = umatrix(a,6:10);
        if a == 1
            for b = 1:1:E
                p = (al(b,1)+bu(uid,b)+bi(iid,b)+gu(uid,E*K-K+1:E*K)*gi(iid,E*K-K+1:E*K)+xs(uid,b)*(ravg-r)+ys(uid, E*S-S+1:E*S)*(rpre - r)')/rmax;
                ksi(b,a) = pai(b) * nchoosek(rmax-1, r-1) * p^(r-1) * (1-p)^(rmax-r);
            end
        else
            for b = 1:1:E
                p = (al(b,1)+bu(uid,b)+bi(iid,b)+gu(uid,E*K-K+1:E*K)*gi(iid,E*K-K+1:E*K)+xs(uid,b)*(ravg-r)+ys(uid, E*S-S+1:E*S)*(rpre - r)')/rmax;
                bo = nchoosek(rmax-1, r-1) * p^(r-1) * (1-p)^(rmax-r);
                temp_ksi = zeros(1,E);
                temp_fai = zeros(1,E);
                pcb = ones(1,b);
                if b > 1
                    for c = 1:1:b-1
                        pcb(c) = exp(lu(uid) + li(iid, (4-c/2)*(c-1)-1+b));
                    end
                end
                pcb = pcb / sum(pcb);
                for c = 1:1:b
                    temp_ksi(c) = ksi(c,a-1) * pcb(c) * bo;
                    temp_fai(c) = ksi(c,a-1) * pcb(c);
                end
                ksi(b,a) = max(temp_ksi);
                temp = find(temp_fai == max(temp_fai));
                fai(b,a) = temp(1);
            end
        end
    end
    temp_last = find(ksi(:,nit)==max(ksi(:,nit)));
    q = temp_last(1);
    for d = nit:-1:1
        umatrix(d,4) = q;
        q_last = fai(q,d);
        q = q_last;
    end
    output = [output;umatrix];
end
end


function [MSE,accuracy,accuracy_loose] = predict_calculation(parameters, testing_data, training_data, U, I, E, K, rmax, testing_num, predict_name, count_times)
rat = reshape(testing_data(:,3),testing_num,U);
rec = zeros(testing_num,U);

lu = reshape(parameters(1:U), U, 1);
li = reshape(parameters(U+1 : U+E*(E-1)*I/2), I, E*(E-1)/2);
al = reshape(parameters(U+E*(E-1)*I/2+1 : U+E*(E-1)*I/2+E), E, 1);
bu = reshape(parameters(U+E*(E-1)*I/2+E+1 : U+E*(E-1)*I/2+E+U*E), U, E);
bi = reshape(parameters(U+E*(E-1)*I/2+E+U*E+1 : U+E*(E-1)*I/2+E+U*E+I*E), I, E);
gu = reshape(parameters(U+E*(E-1)*I/2+E+U*E+I*E+1 : U+E*(E-1)*I/2+E+U*E+I*E+U*K*E), U, E*K);
gi = reshape(parameters(U+E*(E-1)*I/2+E+U*E+I*E+U*K*E+1 : U+E*(E-1)*I/2+E+U*E+I*E+U*K*E+I*K*E), I, E*K);

predict_output = strcat('..\dianping\Final_Results_Me\predict_result_dianping_chaoyang_total_me_testing_',num2str(testing_num),'_count_',num2str(count_times),'.txt');
pfid = fopen(predict_output,'wt');
for u = 1:1:U  
    user_test = testing_data(testing_data(:,1)==u,:);
    user_train = training_data(training_data(:,1)==u,:);
    last = size(user_train,1);
    last_level = user_train(last,4);
    for i = 1:1:size(user_test,1)
        user = user_test(i,1);
        item = user_test(i,2);
        temp_level = zeros(1,E);
        temp_level(last_level) = 1;
        if last_level ~= E
            for j = last_level+1:1:E
                temp_level(j) = exp(lu(user) + li(item, (4-last_level/2)*(last_level-1)-1+j));
            end
        end
        temp_level_num = find(temp_level == max(temp_level));
        level = temp_level_num(1);
    
        score = zeros(1,rmax);
        for r = 1:1:rmax
            p = (al(level,1) + bu(user,level) + bi(item,level) + gu(user,level*K-K+1:level*K) * gi(item,level*K-K+1:level*K))/rmax;
            score(r) = nchoosek(rmax-1, r-1) * p^(r-1) * (1-p)^(rmax-r);
        end
        max_score_pos = find(score == max(score));
        rec(i,u) = max_score_pos(1);
        fprintf(pfid,'%g\t%g\t%g\t%g\t%g\n',user,item,level,rat(i,u),rec(i,u));
    end
end
fclose(pfid);

MSE =  sum(sum((rec - rat).^2)) / (testing_num*U);
accuracy = sum(sum(rec==rat)) / (testing_num*U);
accuracy_loose = sum(sum(abs(rec-rat)<=1)) / (testing_num*U);
MSE_set = zeros(1,testing_num);
accuracy_set = zeros(1,testing_num);
accuracy_loose_set = zeros(1,testing_num);
for pos = 1:1:testing_num
    MSE_set(pos) = sum(sum((rec(pos,:) - rat(pos,:)).^2)) / U;
    accuracy_set(pos) = sum(sum(rec(pos,:)==rat(pos,:))) / U;
    accuracy_loose_set(pos) = sum(sum(abs(rec(pos,:)-rat(pos,:))<=1)) / U;
end

fid = fopen(predict_name,'at');
fprintf(fid,'%g\t',MSE);
fprintf(fid,'%g\t',accuracy);
fprintf(fid,'%g\t',accuracy_loose);
for pos = 1:1:testing_num
    fprintf(fid,'%g\t',MSE_set(pos));
end
for pos = 1:1:testing_num
    fprintf(fid,'%g\t',accuracy_set(pos));
end
for pos = 1:1:testing_num
    if pos < testing_num
        fprintf(fid,'%g\t',accuracy_loose_set(pos));
    else
        fprintf(fid,'%g\n',accuracy_loose_set(pos));
    end
end
fclose(fid);
end