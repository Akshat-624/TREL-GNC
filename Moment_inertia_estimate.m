clc;
clear;
R = 15;%in
R = R/39.37; % in meters 
M = 1200; %lb (assuming mass)
M = M/2.205 ; 
l =23*12/39.37 ; % length of cylinder in meters
Ixx = 1/2 * M * R^2; 
Iyy = 1/4 * M * R^2 + 1/12 * M * l^2; 