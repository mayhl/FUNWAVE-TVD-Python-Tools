clear all

fdir='/home/UFAD/carola.forlini/Desktop/HPC/Sedimentation_models/mesh_convergence_study/wl/LANIKAI_0_3/U_5_speed1000/output/';

% Time series files to plot
nfile=[235 350];
nF = length(nfile);

% Time values for series in minutes
times={'200' '300'};


% Determining domain dimensions
eta=load([fdir 'eta_00001']);
[n,m]=size(eta);

% Setting up partition
dx=0.3;
dy=0.3;
x=[0:m-1]*dx;
y=[0:n-1]*dy;

% Dimensions of plot window 

% wid=3;
% len=5;
% set(gcf,'units','inches','paperunits','inches','papersize', [wid len],'position',[1 1 wid len],'paperposition',[0 0 wid len]);
% clf
ftag=['Surface'];
figWin(ftag);
set(findobj('tag',ftag),'paperpos',[0.2 ,0.2 ,5.2 ,4.5]);

hax=sameAxSubM (1,nF,ftag);
x1 = 66.78;
y1 = 1015.9;

x2 = 70.68;
y2 = 1015.9;

x3 = 75.69;
y3 = 1015.9;

x4 = 70.68;
y4 = 992.7;

for num=1:nF

fnum=sprintf('%.5d',nfile(num));

% Loading wave displacement from file
eta=load([fdir 'eta_' fnum]);

% Plotting wave displacement
NCL_colorMap_4 = importNCLColorMap('MPL_YlGnBu.rgb');

hx=hax(num); axes(hx);
pcolor(x,y,eta)
colormap(flipud(NCL_colorMap_4))
shading flat;

% Colorbar range
caxis([-0.1 0.1])
% colorbar('northoutside')
% title([' Time = ' times{num} ' sec '])
hold on
plot(x2,y2,'Marker','o','LineStyle','none','Color',[0 0 0],'MarkerFaceColor',[1.0 0 0],'MarkerSize',6);
% plot(x2,y2,'Marker','o','LineStyle','none','Color',[0.72 0.27 1],'MarkerFaceColor',[0.72 0.27 1],'MarkerSize',3);
% plot(x3,y3,'Marker','o','LineStyle','none','Color',[0.72 0.27 1],'MarkerFaceColor',[0.72 0.27 1],'MarkerSize',3);
% plot(x4,y4,'Marker','o','LineStyle','none','Color',[0.72 0.27 1],'MarkerFaceColor',[0.72 0.27 1],'MarkerSize',3);
rectangle('Position', [0 0 50 1991], 'EdgeColor','b','LineStyle', '--','EdgeColor',[0.0 0.45 0.74])
rectangle('Position',[290 0 50 1991],'EdgeColor','b','LineStyle', '--','EdgeColor',[0.0 0.45 0.74])
rectangle('Position', [0 0 340 1991])
text(312.53014354067,637.74249201278,'Sponge layer','Color',[0.0 0.45 0.74],'FontSize',12,'Rotation',90)
text(20.6488038277512,633.094888178914,'Sponge layer','Color',[0.0 0.45 0.74],'FontSize',12,'Rotation',90)
ylabel('Y (m)')
xlabel('X (m)')
fontsize(12)
set(gcf,'Renderer','zbuffer')


linkaxes(hax ,'x');
set(hax(1,2),'YAxisLocation','right')
end

% fig1 = open('surfaceU_5.fig');
% eprt(fig1);
%%
clear all

%Parameters

fdir='/home/UFAD/carola.forlini/Desktop/HPC/Sedimentation_models/mesh_convergence_study/wl/LANIKAI_0_3/U_5_speed800/output/';
sta_01 = load([fdir 'sta_0001']);
eta = sta_01(:,2);
x = eta;


wid=5;
len=5;
set(gcf,'units','inches','paperunits','inches','papersize', [wid len],'position',[1 1 wid len],'paperposition',[0 0 wid len]);
clf

plot(sta_01(:,1),x*100)
xlim([0 max(sta_01(:,1))])
set(gca,'YAxisLocation','right')
set(gca, 'FontName', 'Times New Roman', 'FontSize', 11)
set(gcf,'Renderer','zbuffer')
xlabel('Time (s)', 'FontSize', 11)
ylabel('Surface (cm)')

%%
% h=1.7;
% % T=2.02;
% 
% 
% [Lr,kr,sigma]=disper(h,T)
% 
wavepar();