

from funwavetvdtools.plotting.tools.svg_icons import SVGIconStr
from funwavetvdtools.plotting.tools.customjs import load as load_customjs
from bokeh.models import Button, NumericInput, SVGIcon, CustomJS
from bokeh.layouts import column, row, gridplot

class AdvanceBoxEditTool:
    
    def __init_buttons__(self, source):

        def get_button(svg_icon_str, name="test", aspect_ratio=1, fit_direction=None):
            icon = SVGIcon(svg=svg_icon_str.value, size = '1.2em')
            m = 2; margin = (m, m, m, m)
            btn = Button(icon=icon, label="", button_type="default", margin=margin, aspect_ratio=aspect_ratio, width_policy = 'fit', name=name)  
            self._buttons.append(btn)
            return btn
        
        self._buttons = []
        
        self._btn_nnorth = get_button(SVGIconStr.UPARROWBAR, name="NNORTH", aspect_ratio=2)
        self._btn_north  = get_button(SVGIconStr.UPARROW   , name="NORTH")
        self._btn_snorth = get_button(SVGIconStr.DOWNARROW , name="SNORTH")
        #self._buttons.extend([self._btn_nnorth, self._btn_north, self._btn_snorth]) 
        lay_north = column(self._btn_nnorth, row(self._btn_north, self._btn_snorth))
        
        self._btn_eeast = get_button(SVGIconStr.RIGHTARROWBAR, name="EEAST")
        self._btn_east  = get_button(SVGIconStr.RIGHTARROW   , name="EAST")
        self._btn_weast = get_button(SVGIconStr.LEFTARROW    , name="WEAST")
        #self._buttons.extend([self._btn_eeast, self._btn_east, self._btn_weast]) 
        lay_east = row(column(self._btn_weast, self._btn_east), self._btn_eeast)
        
        self._btn_ssouth = get_button(SVGIconStr.DOWNARROWBAR, name="SSOUTH", aspect_ratio=2)
        self._btn_south  = get_button(SVGIconStr.DOWNARROW   , name="SOUTH")
        self._btn_nsouth = get_button(SVGIconStr.UPARROW     , name="NSOUTH")
        #self._buttons.extend([self._btn_ssouth, self._btn_south, self._btn_nsouth]) 
        lay_south = column(row(self._btn_nsouth, self._btn_south), self._btn_ssouth)
        
        self._btn_wwest = get_button(SVGIconStr.LEFTARROWBAR, name="WWEST")
        self._btn_west  = get_button(SVGIconStr.LEFTARROW   , name="WEST")
        self._btn_ewest = get_button(SVGIconStr.RIGHTARROW  , name="EWEST")
        #self._buttons.extend([self._btn_wwest, self._btn_west, self._btn_ewest]) 
        lay_west = row(self._btn_wwest, column(self._btn_west, self._btn_ewest))    

        self._nip_amount = NumericInput(value=0, title="Shift Amount:", mode='float', width=80)
        
        grid = [None    , lay_north       , None    , 
                lay_west, self._nip_amount, lay_east, 
                None    , lay_south       , None    ]
        
        self._grid = gridplot(grid, ncols=3)   
        
        arg_dict = dict(source=source, amount_obj=self._nip_amount)
        
        
        self._callback_buttons = load_customjs('advance_box_edit_tool_buttons.js', arg_dict)
        for button in self._buttons: button.js_on_click(self._callback_buttons)
        
    def __init_info__(self, source, plot):

        self._nip_x = NumericInput(value=0, title="Center x:", mode='float')
        self._nip_y = NumericInput(value=0, title="Center y:", mode='float')
        self._nip_w = NumericInput(value=0, title="Width:", mode='float')
        self._nip_h = NumericInput(value=0, title="Height:", mode='float')           
        self._nip_xe = NumericInput(value=0, title="East x", mode='float')
        self._nip_xw = NumericInput(value=0, title="West x:", mode='float')
        self._nip_yn = NumericInput(value=0, title="North y", mode='float')
        self._nip_ys = NumericInput(value=0, title="South y:", mode='float')
        
        self._info = column([self._nip_x, self._nip_y, 
                             self._nip_w, self._nip_h, 
                             self._nip_xw, self._nip_xe,
                             self._nip_ys, self._nip_yn])
        
        arg_dict = dict(
            source=source, 
            x=self._nip_x  , y=self._nip_y  , 
            w=self._nip_w  , h=self._nip_h  ,
            xw=self._nip_xw, xe=self._nip_xe,
            ys=self._nip_ys, yn=self._nip_yn)
        
        self._callback_select = load_customjs('advance_box_edit_tool_select.js', arg_dict)
        
        plot.js_on_event('tap', self._callback_select)
        
    def __init__(self, source, plot):
        self.__init_buttons__(source)
        self.__init_info__(source, plot)
        self._panel = row(self._grid, self._info)
    
    @property
    def panel(self): return self._panel
