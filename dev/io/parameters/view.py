
try:
    from funwavetvdtools.plotting.tools.svg_icons import SVGIcon
except Exception:
    # Temporary fix until main toolbox is fixed 
    import os
    import sys 
    fpath = os.path.dirname(os.path.abspath(__file__))
    fpath = os.path.join(fpath, '..', '..', '..', 'src')
    fpath = os.path.abspath(fpath)
    sys.path.append(os.path.abspath(fpath))
    from funwavetvdtools.plotting.tools.svg_icons import SVGIcon

import core
import numpy as np
import pandas as pd
from bokeh.events import ButtonClick
from bokeh.layouts import column, row
from bokeh.models import (Button, ColumnDataSource, DataCube, DataTable, Div,
                          GroupingInfo, HelpButton, MultiChoice, NumericInput,
                          ScrollBox, Select, StringFormatter, Switch,
                          TableColumn, TabPanel, Tabs, TextAreaInput,
                          TextInput, Toggle, Tooltip)
from bokeh.models.dom import HTML
from bokeh.plotting import curdoc
from core import Parameters, Type

#from enum import Enum
#from types import SimpleNamespace

#from random import random

#from bokeh.models import Button, TextInput, CustomJS
#from bokeh.palettes import RdYlBu3






PKEY = 'FORTRAN Name'

def frame2table(df):
    data = df.to_dict('list')
    source = ColumnDataSource(data)
    list(data.keys())
    columns = [TableColumn(field=c, title=c) for c in data]
    return DataTable(source=source, columns=columns, min_width=3000, height=280)


def get_cube_example():

    source = ColumnDataSource(data=dict(
        d0=['A', 'E', 'E', 'E', 'J', 'L', 'M'],
        d1=[None, 'D', 'D', 'H', 'K', 'L', 'N'],
        d2=['C', 'F', 'G', 'H', 'K', 'L', 'O'],
        px=[10, 20, 30, 40, 50, 60, 70],
    ))


    target = ColumnDataSource(data=dict(row_indices=[], labels=[]))

    formatter = StringFormatter(font_style='bold')

    columns = [
        TableColumn(field='d2', title='Name', width=80, sortable=False, formatter=formatter),
        TableColumn(field='px', title='Price', width=40, sortable=False),
    ]

    grouping = [
        GroupingInfo(getter='d0'),#, aggregators=[SumAggregator(field_='px')]),
        GroupingInfo(getter='d1')#, aggregators=[SumAggregator(field_='px')]),
    ]

    return DataCube(source=source, columns=columns, grouping=grouping, target=target)


def set_js_link(obj1, attr1, obj2, attr2):
    obj1.js_link(attr1, obj2, attr2)
    setattr(obj2, attr2, getattr(obj1, attr1))




def create_toggle(**kwargs):
    if 'label' in kwargs: raise Exception()

    toggle = Toggle(**kwargs)

    maps = {True : {'label': 'Yes', 'button_type': 'danger' },
            False: {'label': 'No' , 'button_type': 'success'}}

    toggle.update(**maps[toggle.active])

    def callback(self):
        m = self.model
        m.update(**maps[m.active])

    toggle.on_event('button_click', callback)

    return toggle

def _get_widget(key, col, enums, **ckwargs):


    #ckwargs = dict(max_width = width, width=width)
    if col.type in [Type.STRING, Type.OBJECT]:
        text_input = TextInput(value="", **ckwargs)
        return text_input 

    if col.type == Type.BOOL:
        toggle = create_toggle()
        return toggle

    if col.type == Type.KEY:
        select = Select(**ckwargs)
        #enums[key].link_widget_options(select)
        return select

    if col.type == Type.ENUM:
        select = Select(**ckwargs)
        enums[key].link_widget_options(select)
        return select

    if col.type == Type.DENUM:
        select = Select(**ckwargs)
        enums[key].link_widget_options(select)
        return select

    if col.type == Type.LIST:
        mchoice = MultiChoice(value=[], **ckwargs)
        enums[key].link_widget_options(mchoice)
        return mchoice

    if col.type == Type.FLOAT:
        input = NumericInput(mode='float', **ckwargs)
        return input 

    if col.type == Type.INTEGER:
        input = NumericInput(mode='int', **ckwargs)
        return input

    if col.type == Type.TEXT:
        return TextAreaInput(value="", rows=4, **ckwargs)

    raise Exception(col)


def get_widget(key, col,enum, title_width=90, is_switch=False, **kwargs):


    if not 'width' in kwargs: kwargs['width'] = 250

    kwargs['width'] -= title_width

    if is_switch: 
        switch = Switch(active=False)
        kwargs['width'] -= switch.width


    div = Div(text=col.name, width=title_width)
    filt = _get_widget(key, col, enum, **kwargs)

    #tooltip = HelpButton(tooltip=Tooltip(content=HTML(col.desc), position="right"))
    panels = [div, filt]

    if is_switch: 
        panels.append(switch)
        def callback(attr, old, new): filt.disabled = not new
        switch.on_change('active', callback)
        filt.disabled = not switch.active

    if is_switch:
        return filt, row(panels, max_width=kwargs['width']), switch
    else:
        return filt, row(panels, max_width=kwargs['width'])
    

class FilterWidget:

    def __init__(self, k, col, enums, width=250):
        pass

        #col = cols[k]
        self._type = col.type 
        self._name = col.name

        kwargs=dict(is_switch=True, width=width)
        self._filt, self._panel, self._switch = get_widget(k, col, enums, **kwargs)
        #self._switch = switch = Switch(active=False)
        #self._title = Div(text=col.name, width=DIV_WIDTH)


        
       # self._filt = self._get_filt(k, col, denums, width-DIV_WIDTH)

        #def callback(attr, old, new): self._filt.disabled = not new
        #self._switch.on_change('active', callback)
        #self._filt.disabled = not self._switch.active

      #  self._panel = row(self._title, self._filt, self._switch, max_width=width)

    def filter(self, df):

        if self._type in [Type.ENUM, Type.BOOL, Type.DENUM]:
            return df[df[self._name] == self.value] 

        if self._type == Type.LIST:

            selects = self.value
            values= df[self._name].values

            idxs = [np.all([s in v for s in selects]) for v in values]

            return df[idxs]


        tmp = dict(type=self._type, df=df)
        raise Exception(tmp)

    @property
    def is_active(self):
        return self._switch.active

    @property 
    def panel(self): return self._panel

    @property
    def value(self): return getattr(self._filt, self._filt_attr)

    @value.setter
    def value(self, value): setattr(self._filt, self._filt_attr, value)

    @property
    def _filt_attr(self):

        attrs =  {Type.ENUM : 'value' ,
                  Type.BOOL : 'active',
                  Type.LIST : 'value' ,
                  Type.DENUM: 'value' }

        return attrs[self._type]


class TablePanel:

    @property
    def panel(self): return self._panel

    @property
    def key(self): return self._key

    @property
    def name(self): return self._name

    @property
    def select_widget(self): return self._select_widget

    def __getitem__(self, items): 
        return self._dt.source.data[items]

    def __init__(self, key, name, df, cols, select_key='Name', select_widget=None, row_to_string=None, width=600, height=280):

        self._key = key
        self._name = name 
        self._df = df
        self._cols = cols
        self._skey = select_key
        #data = df.to_dict('list')
        self._src = src = ColumnDataSource(df.to_dict('list'))

        def qtable(d): 
            return TableColumn(field = d.name ,
                               title = d.name ,
                               width = d.width)

        rtn_vals = [(d.width ,qtable(d)) for k, d in cols.items()]
        widths, tcols = list(zip(*rtn_vals))
        max_width = np.sum(widths)

        kwargs = dict(source    = src        , 
                      columns   = list(tcols), 
                      min_width = max_width  , 
                      height    = height   )

        self._dt = dt = DataTable(**kwargs)

 
        #self._panel = ScrollBox(child=dt, horizontal_scrollbar='visible', max_width=width)
        self._panel = ScrollBox(child=dt, max_width=width)

        if not select_widget is None:
            self._select_widget = select_widget
        else:
            self._select_widget = self.create_select_widget()

        self._widgets = []
        self._dt.source.on_change('data', self._update_widgets)
        self._row_to_string = self.__row_to_string if row_to_string is None else row_to_string

    def _get_options(self):
        return[self._row_to_string(row) for i, row in self._df.iterrows()]

    def link_widget_options(self, widget):
        widget.update(options=self._get_options())
        self._widgets.append(widget)

    def _update_widgets(self, attr, old, new):
        options = self._get_options()
        for w in self._widgets: w.update(options=options)

    def __row_to_string(self, row):
        return row[self._skey]

    def create_select_widget(self):
        src, key = self._dt.source, self._skey
        values = [str(v) for v in src.data[key]] if key in src.data else []
        select = Select(title=self.name, options=sorted(values))

        def callback(attr, old, new):
            select.options = sorted(new[key])

        src.on_change("data", callback)
        return select


class FilterTablePanel(TablePanel):

    def __init__(self, key, name, df, tables, cols, filt_cols, select_key, row_to_string=None, table_width=600, height=280, filter_width=300):

        super().__init__(key, name, df, cols, select_key, None, row_to_string, table_width, height)

        self._filts = [FilterWidget(c, cols[c], tables, filter_width)  for c in filt_cols]

        for f in self._filts:
            f._switch.on_change('active', self._on_change)
            f._filt.on_change(f._filt_attr, self._on_change)

        panels = [Div(text='Filters')] 
        panels.extend([f.panel for f in self._filts])
        self._filter_panel = column(panels)

    def _on_change(self, attr, old, new):
        filts = [f for f in self._filts if f.is_active]
        df, dt = self._df, self._dt
        for f in filts: df = f.filter(df)
        dt.source.data = df.to_dict('list')

    @property 
    def filter_panel(self): return self._filter_panel

    @property
    def key(self): return self._key

    def key_values(self):
        return self._df[self.key].values

    def add_foreign_table(self, foreign_table, foreign_key):

        def callback(attr, old, new):
            df = foreign_table._df
            df = df[df[foreign_key].isin(new)]
            foreign_table._dt.source.data = df.to_dict('list')

        self._select_widget.on_change('options', callback)


class DisplayWidget:

    def __init__(self, key, col, tables, help_switch, on_change_cb, width = 600):

        self._type = col.type

        kwargs=dict(width=width)
        self._widget, self._panel = get_widget(key, col, tables, **kwargs)

        self._widget.disabled = col.is_locked

        def callback(attr, old, new):
            on_change_cb()
        self._widget.on_change(self._value_attr, callback)


    @property
    def _value_attr(self):
        if self._type == Type.BOOL: return 'active'
        return 'value' 

    @property
    def value(self): return getattr(self._widget, self._value_attr)

    @value.setter
    def value(self, value):
        #self._widget.syncable = False 
        #if value is None: value = ""
        if np.all(pd.isnull(value)) or value is None: 
            if not self._type in [Type.INTEGER, Type.FLOAT]: 
                    value = ""
        setattr(self._widget, self._value_attr, value)
        if self._type is Type.BOOL:
            w = self._widget
            w._trigger_event(ButtonClick(w))

    @property
    def panel(self): return self._panel


class EditPanel():

    def __init__(self, dt):

        self._df = dt._df
        self._key = dt._skey
        self._are_updates = False 

        self._button = Button(label="Update Record", button_type='warning')
        dt._select_widget.on_change('value', self.__select_key)

        self._header = row(dt._select_widget, self._button)
        self.__is_update_lock = False 

    def __select_key(self, attr, old, new):
        not self._are_updates
        self._button.button_type = 'warning'
        self._are_updates = False 
        #  warning if not is clear
        # Fake Button CustomJS + __select_key => ButtonClick => _select_key 
        self.__is_update_lock = True
        self._select_key(attr, old, new)
        self.__is_update_lock = False 

    def _queue_update(self):
        if self.__is_update_lock: return 
        if self._are_updates: return 
        self._are_updates = True
        self._button.button_type = 'primary'

    @property
    def panel(self): return self._panel

class RecordsPanel(EditPanel):

    def __init__(self, fdt, tables, help_switch, link_select_opts=None):

        super().__init__(fdt)

        cargs = (tables, help_switch, self._queue_update)


        self._dwidgets = {c.name: DisplayWidget(k, c, *cargs) for k, c in fdt._cols.items()}

        panels = [self._header]
        panels.extend([dw.panel for k, dw in self._dwidgets.items()])
        self._panel = column(panels)


    def _select_key(self, attr, old, new):
        data = {k: w.value for k, w in self._dwidgets.items()}
        self._df
        row = self._df.loc[self._df[self._key]==new].iloc[0]

        for k, w in self._dwidgets.items(): 
            w.value = row[k]

class GroupsPanel(EditPanel):

    def __init__(self, dt, tables, help_switch, link_select_opts=None):

        super().__init__(dt)

        ckwargs = {} 
        
        self._parents = MultiChoice(value=[], **ckwargs)
        tables['parent'].link_widget_options(self._parents)

        self._pselect = Select(options=[], **ckwargs)

        set_js_link(self._parents, 'value', self._pselect, 'options')

        self._panel = column(self._header, self._parents, self._pselect)

    def _set_key(self, key):
        df = self._df
        df = df[df['Dependent'] == key]
        self._parents.value = list(df['Parent'].values)


    def _select_key(self, attr, old, new):
        self._set_key(new)


class ViewPanel:


    def __init__(self, fdt, dt, tables, help_switch):

        self._are_updates = False 

        #select_widget = fdt._select_widget


        cargs = (help_switch      , #, select_widget     ,
                 self.queue_update, self.clear_updates)

        info = InfoPanel(fdt, tables, *cargs)
        depe = DependenciesPanel(dt, fdt, *cargs)

        tab_info = TabPanel(child=info.panel , title = "Info")
        tab_deps = TabPanel(child=depe.panel, title = "Dependencies")

        tabs = Tabs(tabs=[tab_info, tab_deps])
        self._panel = tabs #column(header, tabs)


    @property
    def panel(self): return self._panel

    def queue_update(self):
        if self._are_updates: return 
        self._are_updates = True
        self._button.button_type = 'primary'

    def clear_updates(self):
        is_clear = not self._are_updates
        if is_clear: self._button.button_type = 'warning'
        self._are_updates = False
        return is_clear




class HeaderPanel:

    def __init__(self, params, title, width = 1000):

        HELP_WIDTH=50
        SWITCH_WIDTH=25

        div_width = width - HELP_WIDTH - SWITCH_WIDTH - 200

        div = Div(text="<H3>%s</H3>" % title, width=div_width) 
        self._panel = div
    
        html = HTML("FUNWAVE Bokeh app for managing FORTRAN input parameters <br>"     \
                    "and their dependencies. Stores info with additional metadata <br>"\
                    "in CSV files stored at the <a href='https://github.com/mayhl/"\
                    "FUNWAVE-TVD-Python-Tools'>FUNWAVE Python Toolbox repo</a>."   )
        self._help = HelpButton(tooltip=Tooltip(content=html, position="left"), width=HELP_WIDTH)

        ######################################################################
        #self._file_input = FileInput(name='FileInputElement')
        #self._saveas_button = Button(icon=SVGIcon.SAVEASICON.value, button_type='warning')
        #for c in dir(FileInput()): print(c)
        #print(self._file_input.id)
        #from bokeh.events import ValueSubmit as Test
        #def callback(event):
        #    print("HERE")

        #self._save_button.on_event('button_click', callback)
        #def callback(event):
        #    mdl = self._file_input
        #    mdl._trigger_event(Test(mdl))

        #js_code = "document.getElementById('FileInputElement').querySelector('input[type=file]').dispatchEvent(new MouseEvent('click'));"
        
        #js_code = "console.log(document.getElementsByTagName('FileInputElement'));"
        #self._saveas_button.js_on_event('button_click', CustomJS(code=js_code))
        #self._save_button._trigger_event(ButtonClick)
        ######################################################################

        self._save_button = save_button = Button(icon=SVGIcon.SAVEICON.value, button_type='warning', label="")
        self._are_updates = False 

        def qswitch(label, active):
            div = Div(text=label)
            switch = Switch(active=active, width=SWITCH_WIDTH)
            return switch, row(div, switch)

        self._filt_switch, filt_panel = qswitch('Show Filter', True )
        self._help_switch, help_panel = qswitch('Show Help'  , False)
        set_js_link(self._help_switch, 'active', self._help, 'visible')

        menu = column([help_panel, filt_panel])
        #menu = row(self._save_button, self._saveas_button, self._file_input, menu)
        menu = row(self._save_button, menu)
        self._panel = row(div, menu, self._help, max_width=width,width=width)




    @property
    def panel(self): return self._panel 

    @property
    def help_switch(self): return self._help_switch

    @property
    def filter_switch(self): return self._filt_switch

    def mark_pending_update(self):
        if self._are_updates: return 
        self._are_updates = True
        self._save_button.button_type = 'primary'

    def mark_clear_updates(self):
        self._save_button.button_type = 'warning'
        is_clear = not self._are_updates
        self._are_updates = True
        return is_clear


class MainDisplay:

    def __init__(self):
        depend_cube = get_cube_example()

        params = Parameters()

        total_width = 1100
        sidemenu_width = 400
        table_width = total_width - sidemenu_width

        header = HeaderPanel(params, "FUNWAVE Input Parameters", width = total_width)
        # Method for constucting tables in order of depedences, but
        # sorting for display purposes 
        tables={}
        table_idxs={}
        def add_tbl(i, tbl):
            tables[tbl.key] = tbl
            if i in table_idxs: raise Exception()
            table_idxs[i] = tbl.key
            return tbl


        dt_units  = add_tbl(4, TablePanel('units'      , 'Units'       , params._units_df, core.UNIT_COLUMNS    , width=table_width))
        dt_cat    = add_tbl(3, TablePanel('category'   , 'Categories'  , params._cat_df  , core.CATEGORY_COLUMNS, width=table_width))
        dt_data   = add_tbl(5, TablePanel('datatype'   , 'Datatypes'   , params._data_df , core.DATATYPE_COLUMNS, width=table_width))
        dt_skill  = add_tbl(6, TablePanel('skill_floor', 'Skill Levels', params._skill_df, core.SKILLLVL_COLUMNS, width=table_width))
        dt_mask   = add_tbl(7, TablePanel('mask_type'  , 'Mask Types'  , params._mask_df , core.MASKTYPE_COLUMNS, width=table_width))


        kwargs=dict(table_width   = table_width,
                    filter_width  = sidemenu_width)
        dt_par = add_tbl(0, FilterTablePanel('parent', 'Parameters', params._par_df, tables, 
                                             core.INPUT_COLUMNS, core.FILTER_COLUMNS, 'Name', **kwargs))

        kwargs=dict(select_key    = 'Parent',
                    width   = table_width,
                    select_widget = dt_par.create_select_widget())
        dt_dep = add_tbl(1, TablePanel('dependencies', 'Dependencies', params._dep_df, core.DEPENDENT_COLUMNS, **kwargs))
        dt_par.add_foreign_table(dt_dep, 'Dependent')


        kwargs=dict(table_width   = table_width,
                    filter_width  = sidemenu_width)
        dt_fenums = add_tbl(2, FilterTablePanel('Name', 'FUNWAVE Enums', params._fenums_df, tables, 
                                                core.FUN_ENUM_COLUMNS, core.FFILTER_COLUMNS, 'Name', **kwargs))

        #dt_par_sel = dt_par.select_panel

    
        # Sortting tabs 
        dts = [tables[table_idxs[k]] for k in sorted(table_idxs.keys())]
        ptypes = [GroupsPanel if dt.key=='dependencies' else RecordsPanel for dt in dts] 

        edit_tabs = [PType(dt, tables, header.help_switch) for dt, PType in zip(dts, ptypes)]
        edit_tabs = Tabs(tabs=[TabPanel(child=et.panel, title=dt.name) for et, dt in zip(edit_tabs,dts)])
        tab_edit = ScrollBox(child=edit_tabs, max_width=table_width)
        tab_edit = TabPanel(child=tab_edit, title='Edit')

        tab_depend = TabPanel(child=depend_cube, title="Dependencies")

        raw_tabs = Tabs(tabs=[TabPanel(child=dt.panel, title=dt.name) for dt in dts])
        tab_raw = ScrollBox(child=raw_tabs, max_width=table_width)
        tab_raw = TabPanel(child=tab_raw, title="Raw Data")

        main_display = Tabs(tabs=[tab_edit, tab_depend, tab_raw], max_width=table_width)


        filt_panels = {dt.name: dt.filter_panel for dt in dts if isinstance(dt, FilterTablePanel)}
        for k, p in filt_panels.items(): p.visible = False 
        filt_panel = column([p for _, p in filt_panels.items()], max_width=sidemenu_width)
        # Hack to 'mirror' filter display for secondary table
        filt_panels[dt_dep.name]=filt_panels[dt_par.name]
        filt_panels = {i: filt_panels[dt.name] for i, dt in enumerate(dts) if dt.name in filt_panels}
        
        side_menu = filt_panel

        def callback(attr, old, new):

            if old in filt_panels:
                filt_panels[old].visible=False

            if new in filt_panels:
                filt_panels[new].visible=True

        raw_tabs.on_change('active', callback)
        edit_tabs.on_change('active', callback)

        filter_panel = dt_par.filter_panel
        set_js_link(header.filter_switch, 'active', filter_panel, 'visible')

        body = row(main_display, side_menu)

        self._panel = column(header.panel, body)

    @property
    def panel(self): return self._panel




main_display = MainDisplay()

#raise Exception()
curdoc().add_root(main_display.panel)



