function varargout=wavepar(varargin);
% for running as a function: 
%     input arguments are depth, period(s), amplitude
%     output parameters are lambda, c, cg 

      if isempty(varargin),
            prompt={'Depth(m):','Period(s):','Amplitude(m):'};
            def={'5','5','1'};
            ti='Wave parameters';
            lineNo=1;
            answer=inputDlg(prompt,ti,lineNo,def);
            H=str2num(answer{1}); Tp=str2num(answer{2}); a=str2num(answer{3});

	     disp('WAVE CHARACTERISTICS (full dispersion):');%----------------------------
% calculation of the wave length:
            o = 2*pi/Tp;
            ak1=o/sqrt(9.81*H);
            for it=1:100
            	    ak2=.7*o*o/(9.81*tanh(ak1*H))+.3*ak1;
            	    if abs(ak2-ak1)/ak1<=1.e-5, break; else ak1=ak2; end;
            end;
            fprintf('number of iterations=%d\n',it);
            cg=0.5*o/ak2*(1+2*ak2*H/sinh(2*ak2*H));
            lambda=2*pi/ak2;
            nrdisp=(ak2*H)^2;
            nrshal=a/H;
            U=nrshal/nrdisp;

     	     disp(['	Wave length:  ',num2str(lambda),'m']);
     	     disp(['	Phase velocity:  ',num2str(o/ak2),'m/s']);
     	     disp(['	Group velocity:  ',num2str(cg),'m/s']);
% calculation of the factors of steepness, dispersion, nonlinearity
            disp(['	Dispersion parameter (k*H)^2:  ',num2str(nrdisp)]);
            disp(['	Nonlinearity parameter(a/H):  ',num2str(nrshal)]);
            disp(['	Nonlinearity parameter(a*k):  ',num2str(a*ak2)]);
            disp(['	Ursell number:  ',num2str(U)]);  

	     disp('WAVE CHARACTERISTICS (weak dispersion):');%----------------------------
            sigma=o/sqrt(9.81d0);
            ak2=sigma/sqrt(H)*(1.0d0+sigma^2*H/6.0d0);
            cg=0.5*o/ak2*(1+2*ak2*H/sinh(2*ak2*H));
            lambda=2*pi/ak2;
            nrdisp=(ak2*H)^2;
            nrshal=a/H;
            U=nrshal/nrdisp;
     	     
	     disp(['	Wave length:  ',num2str(lambda),'m']);
     	     disp(['	Phase velocity:  ',num2str(o/ak2),'m/s']);
     	     disp(['	Group velocity:  ',num2str(cg),'m/s']);
% calculation of the factors of steepness, dispersion, nonlinearity
            disp(['	Dispersion parameter (k*H)^2:  ',num2str(nrdisp)]);
            disp(['	Nonlinearity parameter(a/H):  ',num2str(nrshal)]);
            disp(['	Nonlinearity parameter(a*k):  ',num2str(a*ak2)]);
            disp(['	Ursell number:  ',num2str(U)]);  

	     disp('WAVE CHARACTERISTICS (no dispersion):');%----------------------------
            sigma=o/sqrt(9.81d0);
            ak2=sigma/sqrt(H);
            cg=sqrt(9.81*H);
            lambda=2*pi/ak2;
            nrdisp=(ak2*H)^2;
            nrshal=a/H;
            U=nrshal/nrdisp;
     	     disp(['	Wave length:  ',num2str(lambda),'m']);
     	     disp(['	Phase velocity:  ',num2str(o/ak2),'m/s']);
     	     disp(['	Group velocity:  ',num2str(cg),'m/s']);
% calculation of the factors of steepness, dispersion, nonlinearity
            disp(['	Dispersion parameter (k*H)^2:  ',num2str(nrdisp)]);
            disp(['	Nonlinearity parameter(a/H):  ',num2str(nrshal)]);
            disp(['	Nonlinearity parameter(a*k):  ',num2str(a*ak2)]);
            disp(['	Ursell number:  ',num2str(U)]);  
      else 
% running as a function - calculation of the wave length:
            H=varargin{1}; Tp=varargin{2}; a=varargin{3};
            o = 2*pi/Tp; ak1=o/sqrt(9.81*H);
            for it=1:100
            	    ak2=.7*o*o/(9.81*tanh(ak1*H))+.3*ak1;
            	    if abs(ak2-ak1)/ak1<=1.e-5, break; else ak1=ak2; end;
            end;
            fprintf('number of iterations=%d\n',it);
            cg=0.5*o/ak2*(1+2*ak2*H/sinh(2*ak2*H));
            lambda=2*pi/ak2;
	     c=o/ak2;

     	     disp(['	Wave length:  ',num2str(lambda),'m']);
     	     disp(['	Phase velocity:  ',num2str(c),'m/s']);
     	     disp(['	Group velocity:  ',num2str(cg),'m/s']);
	     nargout=3;
            varargout={lambda,c,cg};
      end
