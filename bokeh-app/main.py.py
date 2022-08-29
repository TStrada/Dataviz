#!/usr/bin/env python
# coding: utf-8

# # Time series

# In[1]:


import numpy as np
import pandas_bokeh

# import pkg_resources
# pkg_resources.require("panel==0.13.1")
import panel as pn

pn.extension('tabulator', sizing_mode="stretch_width")
import hvplot.pandas
import holoviews as hv

hv.extension('bokeh')
pn.extension('tabulator')
pn.extension('bokeh')


import pandas as pd
from bokeh.io import show, output_notebook
from bokeh.plotting import figure, output_file, show
import bokeh.io


from bokeh.models.tools import Toolbar, HoverTool
from holoviews import dim, opts


# In[2]:



# # Define function to determine environment
# def environment():
#     try:
#         get_ipython()
#         return "notebook"
#     except:
#         return "server"
# environment()


# In[3]:


db = pd.read_excel('fusione5.xlsx', index_col='Unnamed: 0', dtype={'Year': int})
db


# In[4]:


# Choose country
country = pn.widgets.Select(
#     name = 'Select Country',
    width = 200, height = 50,
    margin = [5,10],
    options = ['Singapore', 'Occupied Palestinian Territory', 'Malaysia', 'Kazakhstan',
               'Turkey', 'Chile', 'Latvia', 'New Zealand', 'Switzerland', 'Serbia',
               'Argentina', 'Japan', 'Belarus', 'Hungary',  'Australia','Denmark',
               'Norway', 'Iceland', 'Poland', 'Bulgaria', 'France',
               'Belgium', 'Netherlands',  'Slovenia', 'Greece',  'Italy',
               'Ireland', 'United Kingdom', 'Spain', 'Romania', 'Germany',
               'Finland', 'Lithuania', 'Portugal', 'Croatia', 'Sweden',  'Luxembourg', 'Austria']
)

# Choose country
country1 = pn.widgets.Select(
#     name = 'Select Country',
    width = 200, height = 50,
    margin = [5,10],
    options = ['Singapore', 'Occupied Palestinian Territory', 'Malaysia', 'Kazakhstan',
               'Turkey', 'Chile', 'Latvia', 'New Zealand', 'Switzerland', 'Serbia',
               'Argentina', 'Japan', 'Belarus', 'Hungary',  'Australia','Denmark',
               'Norway', 'Iceland', 'Poland', 'Bulgaria', 'France',
               'Belgium', 'Netherlands',  'Slovenia', 'Greece',  'Italy',
               'Ireland', 'United Kingdom', 'Spain', 'Romania', 'Germany',
               'Finland', 'Lithuania', 'Portugal', 'Croatia', 'Sweden',  'Luxembourg', 'Austria'],
    visible = False
)
not_euts = ['Singapore', 'Occupied Palestinian Territory', 'Malaysia', 'Kazakhstan',
        'Turkey', 'Chile', 'Latvia', 'New Zealand', 'Switzerland', 'Serbia',
        'Argentina', 'Japan', 'Belarus', 'Hungary',  'Australia']
euts = ['Denmark', 'Norway', 'Iceland', 'Poland', 'Bulgaria', 'France', 
        'Belgium', 'Netherlands',  'Slovenia', 'Greece',  'Italy',
        'Ireland', 'United Kingdom', 'Spain', 'Romania', 'Germany',
        'Finland', 'Lithuania', 'Portugal', 'Croatia', 'Sweden',  'Luxembourg', 'Austria']

country.jslink(country1, value='value', bidirectional=True)
pn.Row(country, country1)


# In[5]:


# Define Palette
PALETTE = ["#d57883", "#04d9ff", "#003953", "#800000", "#8B0000", "#A52A2A"]
# PALETTE = ['#228B22', '#00FFFF', '#7DF9FF', '#800000', '#8B0000', '#A52A2A']
PALETTE_COLOR_BLINDNESS = ['#44749D', '#ff0000', '#EBE7E0', '#F5793A', '#382119', '0F2080']    


# In[6]:


## Color widget for color blindness
select_mode_main = pn.widgets.RadioBoxGroup(name='Select Vision', 
                                            options={'Standard': PALETTE[0], 'Daltonism':  PALETTE_COLOR_BLINDNESS[0]}, 
                                            width = 200, height = 50,
                                            margin = [20,50],
                                            inline = True
                                            )

select_mode_kyotoI = pn.widgets.RadioBoxGroup(name='Select Vision', 
                                              options={'Standard': PALETTE[1], 'Daltonism':  PALETTE_COLOR_BLINDNESS[1]}, 
                                              width = 200, height = 50,
                                              visible = False,
                                              margin = [5,10]
                                              )

select_mode_kyotoII = pn.widgets.RadioBoxGroup(name='Select Vision', 
                                               options={'Standard': PALETTE[2], 'Daltonism':  PALETTE_COLOR_BLINDNESS[2]}, 
                                               width = 200, height = 50,
                                               visible = False,
                                               margin = [5,10]
                                              )

select_mode_mean = pn.widgets.RadioBoxGroup(name='Select Vision', 
                                              options={'Standard': PALETTE[3], 'Daltonism':  PALETTE_COLOR_BLINDNESS[3]}, 
                                              width = 200, height = 50,
                                              visible = False,
                                              margin = [5,10]
                                              )
## Combine color widget
select_mode_main.jslink(select_mode_kyotoI, value='value', bidirectional=True)
select_mode_main.jslink(select_mode_kyotoII, value='value', bidirectional=True)
select_mode_main.jslink(select_mode_mean, value='value', bidirectional=True)


# ## Pipeline and interactive DataFrame

# In[7]:


## Make DataFrame Pipeline Interactive
idc = db[['Entity', 'Code', 'Year', 'PercentageChangeProduction',
          'PercentageChange', 'Renewable electricity productions (TWh)',
          'Eco-friendly Production/Total Production Share(%)', 'Renewable electricity productions (TWh) Kyoto',
          'Eco-friendly Production/Total Production Share(%) Kyoto', 'Kyoto I', 'Kyoto II' 
         ]]

idf = idc.interactive()



# Define pipeline
ipipeline1 = (
      idf[
        (idf.Entity == country)
    ].round(4))
ipipeline1.head(1)


itable = ipipeline1.rename(columns={'PercentageChange': 
                                    'Relative Change Share (%)', 
                                    'PercentageChangeProduction':
                                    'Relative Change Production (%)',
                                    'Eco-friendly Production/Total Production Share(%)': 
                                    'Renewable Production/Total Production (%)'})[['Entity', 
                                                                                   'Code', 
                                                                                   'Year', 
                                                                                   'Relative Change Share (%)',
                                                                                   'Relative Change Production (%)',
                                                                                   'Renewable electricity productions (TWh)',
                                                                                   'Renewable Production/Total Production (%)']].pipe(pn.widgets.Tabulator, pagination='remote', 
                         page_size=10, sizing_mode = 'stretch_width', theme = 'bulma')
itable


# ## Share Time serie

# ### Combine mean plot and main plot

# In[8]:


## Combine Plot and Pipeline
hover = HoverTool(tooltips=[("Year", "@{Year}"), 
                            ("Share", "@{Eco-friendly Production/Total Production Share(%)}%"),
                            ("Relative Change", "@{PercentageChange}%")
                           ],
                  mode = 'vline')

main_plot = ipipeline1.hvplot(x = 'Year',
                              y = 'Eco-friendly Production/Total Production Share(%)',
                              size = 'PercentageChange',
                              width=200, height=400,
                              alpha = 0.7, line_color= select_mode_main,
                              label = 'Annual Share'
                             ).opts(tools=['vline', 'box_zoom', 'reset'], toolbar='above')


kyotoI_plot = ipipeline1.hvplot(x = 'Kyoto I', 
                                y = 'Eco-friendly Production/Total Production Share(%) Kyoto',
                                width=200, height=400,
                                alpha = 0.7, line_color= select_mode_kyotoI,
                                label = 'Kyoto Protocol first part'
                                ).opts(tools=[""], toolbar=None)


kyotoII_plot = ipipeline1.hvplot(x = 'Kyoto II', 
                                 y = 'Eco-friendly Production/Total Production Share(%) Kyoto', 
                                 width=200, height=400, 
                                 label = 'Kyoto Protocol second part',
                                 alpha = 0.7, line_color= select_mode_kyotoII, 
                                 ).opts(tools=[""], 
                                        toolbar=None
                                       )
## Share mean band
mean_share = idc.groupby('Year').mean()[['Renewable electricity productions (TWh)', 'Eco-friendly Production/Total Production Share(%)']]
mean_share['Upper Share'] = mean_share['Eco-friendly Production/Total Production Share(%)'] + idc.groupby('Year').std()['Eco-friendly Production/Total Production Share(%)']
mean_share['Lower Share'] = mean_share['Eco-friendly Production/Total Production Share(%)'] - idc.groupby('Year').std()['Eco-friendly Production/Total Production Share(%)']

mean_s = mean_share.hvplot(x = 'Year',
                          y = 'Eco-friendly Production/Total Production Share(%)',
                          kind = 'line',
                          label = 'Mean Share',
                          alpha = 0.5, 
                          line_color= select_mode_mean.value,
                          ylim = (0,110),
                          xlim= (1990,2020),
                          )

band_s = mean_share.hvplot(x='Year', y='Upper Share', y2='Lower Share',
                          kind = 'area',
                           color = select_mode_mean.value,
                          alpha = 0.075
                         )

share_band = (mean_s * band_s.opts(tools = [], toolbar = None))


## Define interactive title
column_prod = pn.Column('## Renweable Energy Share: Singapore (Not in EUTS)') 
def set_title_1(event):
    if event.new in euts:
        column_prod[0]=f'## Renweable Energy Share: {event.new} (In EUTS)'
    else:
        column_prod[0]=f'## Renweable Energy Share: {event.new} (Not in EUTS)'

country.param.watch(set_title_1, 'value')

# Set y ticks format
def formatter(value):
    return str(value) + ' %'

# Add context Official Start Kyoto Protocol and Doha Agreement
context = hv.Text('2005', 70, 'Kyoto Protocol official start', 8).opts(text_font_style = 'italic')
context2 = hv.Text('2012', 90, 'Doha Agreement official start', 8).opts(text_font_style = 'italic')

vline = hv.VLine(2005).opts(alpha = 0.1, color = PALETTE[4])
vline2 = hv.VLine(2012).opts(alpha = 0.1, color = PALETTE[5])

share_plot = (main_plot.opts(tools=[hover], 
                            toolbar = 'above', 
                            ) * 
              kyotoI_plot *
              kyotoII_plot *
              context * 
              vline *
              vline2 * 
              context2 *
              share_band)

time_series_figure_share = pn.Column(column_prod, #country,
                                     share_plot.opts(legend_position='right', padding = (0.4, 0.4),
                                                     xlim=(1990, 2021), ylim = (0,110), 
                                                     ylabel = 'Renewable Production/Total Production',
                                                     xticks=5, yticks=5,
                                                     yformatter = formatter,
                                                     text_font_style = 'bold italic'
                                                     ).panel(width=800, height = 400))

# time_series_figure_share.show()
# # time_series_figure_share.servable()


# ## Time serie Production

# ### Combine mean plot and main plot

# In[9]:


## Combine Plot and Pipeline
hover = HoverTool(tooltips=[("Year", "@{Year}"), 
                            ("Value", "@{Renewable electricity productions (TWh)} Twh"),
                            ("Relative Change Production", "@{PercentageChangeProduction}%")
                           ],
                  mode = 'vline')

main_plot = ipipeline1.hvplot(x = 'Year',
                              y = 'Renewable electricity productions (TWh)', 
                              size = 'PercentageChangeProduction',
                              width=200, height=400,
                              alpha = 0.7, line_color= select_mode_main, 
                              label = 'Renewable Production (Twh)', 
                              )


kyotoI_plot = ipipeline1.hvplot(x = 'Kyoto I', 
                                y = 'Renewable electricity productions (TWh) Kyoto',
                                width=200, height=400,
                                alpha = 0.7, line_color= select_mode_kyotoI,
                                label = 'Kyoto Protocol first part'
                                ).opts(tools=[""], toolbar=None)


kyotoII_plot = ipipeline1.hvplot(x = 'Kyoto II', 
                                 y = 'Renewable electricity productions (TWh) Kyoto', 
                                 width=200, height=400, 
                                 label = 'Kyoto Protocol second part',
                                 alpha = 0.7, line_color= select_mode_kyotoII, 
                                 ).opts(tools=[""], toolbar=None
                                       )

## Production mean band
mean_prod = idc.groupby('Year').mean()[['Renewable electricity productions (TWh)', 'Eco-friendly Production/Total Production Share(%)']]
mean_prod['Upper'] = mean_prod['Renewable electricity productions (TWh)'] + idc.groupby('Year').std()['Renewable electricity productions (TWh)']
mean_prod['Lower'] = mean_prod['Renewable electricity productions (TWh)'] - idc.groupby('Year').std()['Renewable electricity productions (TWh)']


mean_p = mean_prod.hvplot(x = 'Year',
                          y = 'Renewable electricity productions (TWh)',
                          kind = 'line',
                          label = 'Mean Production',
                          alpha = 0.5, 
                          line_color= select_mode_mean.value,
                          ylim = (0,110),
                          xlim= (1990,2020),
                          )

band_p = mean_prod.hvplot(x='Year', y='Upper', y2='Lower',
                          kind = 'area',
                          color = select_mode_mean.value,
                          alpha = 0.075
                         )
prod_band = (mean_p * band_p.opts(tools = [], toolbar = None))

## Define interactive title
column_prod_share = pn.Column('## Renweable Energy Production: Singapore (Not in EUTS)') 
def set_title_2(event):
    if event.new in euts:
        column_prod_share[0]=f'## Renweable Energy Production: {event.new} (In EUTS)'
    else:
        column_prod_share[0]=f'## Renweable Energy Production: {event.new} (Not in EUTS)'

country1.param.watch(set_title_2, 'value')

## Define axis y style 
def formatter(value):
    return str(value) + ' TWh'

## Write context lines (Kyoto Protocol starts, Doha starts)
context = hv.Text('2005', 220, 'Kyoto Protocol official start', 8).opts(text_font_style = 'italic')
context2 = hv.Text('2012', 240, 'Doha Agreement official start', 8).opts(text_font_style = 'italic')

vline = hv.VLine(2005).opts(alpha = 0.1, color = PALETTE[4])
vline2 = hv.VLine(2012).opts(alpha = 0.1, color = PALETTE[5])


## Combine plots
plot = (main_plot.opts(tools = [hover], 
                      toolbar = 'above') *
        kyotoI_plot * kyotoII_plot *
        context *
        vline *
        vline2 *
        context2 * 
        prod_band
        )

## Define a column for plot, widgets and titles
time_series_figure = pn.Column(column_prod_share,# country1,
                               select_mode_mean,
                               select_mode_kyotoI, select_mode_kyotoII,
                               plot.opts(legend_position='right',
                                         padding = (0.4, 0.4),
                                         xlim=(1990, 2021), ylim = (0,300), 
                                         ylabel = 'Renewable Production',
                                         xticks=5, yticks=5,
                                         yformatter = formatter,
                                         text_font_style = 'bold italic'
                                         ).panel(width=800, height = 400, margin = (0,0))
                                )
# time_series_figure.show()
# time_series_figure.servable()


# ## Dashboard

# In[10]:


## Import Lollipop
fname = "Lollipop_html.html"
html_file = open(fname, 'r', encoding='utf-8')
source_code = html_file.read() 
lollipop = pn.pane.HTML(source_code)
lollipop


# In[36]:



# Add all plot together into an interactive dashboard
template = pn.template.MaterialTemplate(
            title = 'Did Kyoto Protocol have effects on renewable production over the years?',
            sidebar=[pn.pane.PNG('KyotoProtocol.png',
                                 width = 300, height = 300, align = 'center'
                                ),
                     pn.pane.Markdown('The Kyoto Protocol is an international treaty signed and ratified by 192 country all over the world. It’s considered the first and most important agreement to reduce greenhouse gas emissions that are linked to global warming. The Kyoto Protocol was adopted on 11 December 1997 but officially entered into force on 16 February 2005 when 55 Nations, representing at least 55% of gas emissions, ratified the treaty. It’s first part finished at 2012 but was extended to 2020, thanks to Doha Agreement. The aim was to drop the percentage of gas emissions compared with 1990’s gas emissions for each country and the results had to be achieved at any level (energetic industry, transportation, manufacturing industry, etc…). So the Kyoto Protocol represents the first way to change world habits to a more sustainable life where energy is produced thanks to low-carbon emissions materials. For the energy level the EU-ET^1 play an import role for decrease and monitor gas emissions.  Here we consider the 38 Country with most high HDI^2 () which signed the Kyoto Protocol.'
                                     ,width=100),
                     pn.pane.Markdown("1 EU- ETS (European Union Emissions Trading System) = is a ‘cap and trade’ scheme where a limit is placed to the right to emit specified pollutants. It covers around 45% of EU’s greenhouse gas emissions."
                                     ),
                     pn.pane.Markdown("2 HDI (Human Development Index) = is a summary measure of average achievement in key dimensions of human development: a long and healthy life, being knowledgeable and have a decent standard of living. The HDI is the geometric mean of normalized indices for each of the three dimensions."
                                     )
                    ],
            main=[pn.Row(lollipop),
                  pn.Spacer(height = 50),
                  pn.Row('## Select Country', country, country1, '## Choose Color', select_mode_main,
                                                                          select_mode_mean,
                                                                          select_mode_kyotoI, select_mode_kyotoII
                        ),
                  pn.Row(time_series_figure_share, 
                         time_series_figure),
                  pn.Row(itable.panel(width = 500)
                       )
                  ]
)
# template.show()
template.servable()
pn.serve(template, threaded=True, title='Interactive dashboard')

