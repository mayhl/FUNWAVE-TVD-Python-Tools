function hax=sameAxSubM(N,M,figtag)
% function hax=sameAxSubplt(N,M,figtag) makes a N by M table of axes in 
% the figure having the tag figtag and returns a MATRIX hax of handles 
% the same way the subplot command does. figtag is the tag of the figure where
% the plots are drawn.  

      figh=findobj('tag',figtag);
      if isempty(figh), msgbox(['no figure with tag ',figtag,'. returning...']); return; end
      figure(figh)
% This sets the subplot axes
      Y0=0.92;  Dy=0.8/N; dy=0.93*Dy;
      X0=0.12; Dx=0.8/M; dx=0.93*Dx; 
      hax=[];
      for iN=1:N
            for iM=1:M
            	pos=[X0+(iM-1)*Dx,Y0-iN*Dy,dx,dy];		     
 	     	    	hax(iN,iM)=axes('pos',pos);
	     end 
      end
