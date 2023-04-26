function figWin(figtag)      

      if isempty(findobj('tag',figtag)), 
            h=sfigure; set(h,'tag',figtag,'doublebuf','on','menu','figure'); 
      else, 
            sfigure(findobj('tag',figtag)); clf;     
      end
      
      

