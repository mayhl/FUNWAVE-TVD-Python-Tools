%%
clear all

%plot spectrogram

% fdir='/media/carola.forlini/Elements/HPC/wl/0_3_SP_4/output/';
fdir='/home/UFAD/carola.forlini/Desktop/HPC/Sedimentation_models/mesh_convergence_study/wl/LANIKAI_0_3/U_6_speed1000N/output/';
sta_01 = load([fdir 'sta_0001']);
eta = sta_01(:,2)*100;
h = 2.2;
k_pi = pi/h;
Omega_pi = sqrt(9.81*k_pi*(tanh(k_pi*h)));    %rad/s
fOmega_pi = Omega_pi/(2*pi);               %1/s=Hz

k_2 = 2/h;
Omega_2 = sqrt(9.81*k_2*(tanh(k_2*h)));    %rad/s
fOmega_2 = Omega_2/(2*pi);               %1/s=Hz

k_1 = 1/h;
Omega_1 = sqrt(9.81*k_1*(tanh(k_1*h)));    %rad/s
fOmega_1 = Omega_1/(2*pi);               %1/s=Hz
%% Spectrogram

cmap='MPL_StepSeq.rgb';                       %very nice colormap (used in the paper)
map=getNCLColmap(cmap,100);

% max frequency to show
fLim=[0.005,1];

% define analysis parameters
fs=8;                               %sampling frequency (Hz)
wk.p = eta;
wk.Nft=256;                         %number of FFT points
wk.hop=24;                          %hop size (here it's equal to the hamming window size)

% perform STFT
[sp,fsp,tsp,nts]=stft(wk.p, wk.Nft, wk.hop, wk.Nft, fs);

% cutoff corrections at fMax and sigmoid
nf=length(fsp);
fMax=0.7;

% define sigmoid (1-tanh((f-f0)*ffact))/2 for frequency correction:
f0=0.5; 
wdth=1/5;
sgm=0.5*(1-tanh((fsp-f0)/wdth));

sp=abs(sp).^2;                     %power     

% "rescaling" to fit sp into the colormap
kf=find((fsp-fLim(1)).*(fsp-fLim(2))<=0);
fsp=fsp(kf); 
sp=sp(kf,:);
sma=max(sp(:));
s2=log10(sp/sma);

%plot the spectrogram
% figure
% pcolor(tsp,fsp,s2);
% shading interp;
% hold on;
% colormap(map);
% set(gca,'tag','sptgMap');
% uistack(gca,'bottom');
% set(gca,'layer','top','clim',[-3,1]);  box on;
% xlabel('Time (s)','fontsi',12)
% ylabel('Frequency (Hz)','fontsi',12)

%%

% open figure and plot spectrograms and time series
ftag='wake Sp'; figWin(ftag);
set(findobj('tag',ftag),'paperpos',[0.2,0.2,4.5,4.5]);
hax=sameAxSubM(2,1,ftag);
tLim=[0,max(sta_01(:,1))];

hx=hax(1,1); axes(hx);
hpc=pcolor(tsp,fsp,s2);
shading interp;
colorbar('northoutside') 
colormap(map);
hold on 
yline(fOmega_pi,'m--')%,'kh=\pi','LineWidth',1,'LabelHorizontalAlignment','left')
a = yline(fOmega_2,'--')%,'kh=2','LineWidth',1,'LabelHorizontalAlignment','left')
a.Color = [0.65 0.65 0.65];
b = yline(fOmega_1,'--')%,'kh=1','LineWidth',1,'LabelHorizontalAlignment','left')
b.Color = [0.65 0.65 0.65];
set(hpc,'tag','sptgMap');
uistack(hpc,'bottom');
vx=[tLim,fLim]; axis(vx);
box on;
set(hx,'clim',[-3,0],'Layer','top');
set(hax(1,1),'xticklabel',[]);

hx=hax(2,1); axes(hx)
plot(sta_01(:,1),eta);
pLim=[min(eta),max(eta)]; pLim=pLim+0.1*(pLim(2)-pLim(1))*[-1,1];
tLim_1=[0,max(sta_01(:,1))];
vx=[tLim_1,pLim]; axis(vx);
xtk=get(gca,'xtick');

linkaxes(hax,'x')
set(hax,'fontsize',11,'layer','top');
axes(hax(1,1)); ylabel('Frequency (Hz)');
axes(hax(2,1)); ylabel('Surface (cm)');
axes(hax(2,1)); xlabel('Time (s)');
set(hax(1,1),'YAxisLocation','right')
set(hax(2,1),'YAxisLocation','right')

% fig=open('spectroU_5.fig');
% eprt(fig)