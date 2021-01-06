import pandas as pd
import streamlit as st
import numpy as np
import plotly.graph_objects as go


st.set_page_config(
            page_title="Reactor", # => Quick reference - Streamlit
            page_icon=":droplet:",
            #layout="centered", # wide
            initial_sidebar_state="auto") # collapsed


############################################################################################################################
############################################################################################################################
###########################                          FUNCTIONS                                      ########################

def efficiency(starting_dbo,final_dbo):
    e =((starting_dbo-final_dbo)/starting_dbo)
    return e   
           
def biblio():
    if watertype == 'sewage':
        bibliography = st.radio("Would you like to see the typical design values and ranges for typical sewage wastewater from now on?",
            ('yes','no'), index = 1)
        if bibliography == "yes" :
            return bibliography
        elif bibliography == "no":
            return bibliography       
    elif watertype == 'industrial':
        bibliography = st.radio("Would you like to see some typical industrial values from bibliography?", ('yes','no'), index = 1)
        if bibliography == "yes":
            return bibliography
        elif bibliography == "no":
            return bibliography

def yvars():
    y= st.number_input('Enter please your Y (relacón masa celular formada/sustrato consumido)', value= 0.65)
    if bibliography == 'yes':
        st.write(commonvals.loc['Y',:])     
    st.write(f"{y} mgSSV/mgDBO5")   
    return y

def ksvars():
    ks= st.number_input('Enter please your ks (constante de sustrato)', value= 60.0)
    if bibliography == 'yes':
        st.write(commonvals.loc['ks',:])     
    st.write(f"{ks} mgDBO5/L")   
    return ks

        
def umaxvars():
    umax= st.number_input('Enter please your umax (tasa de crecimiento específico máximo)', value= 0.5)
    if bibliography == 'yes':
        st.write(commonvals.loc['umax',:])     
    st.write(f"{umax} 1/d")   
    return umax

def xvars():
    x= st.number_input('Enter please your X (biomasa en el reactor)', value = 3000.0)
    if bibliography == 'yes':
        st.write(commonvals.loc['X',:])     
    st.write(f"{x} mgSSV/L")   
    return x

def volume():
    upper = y * (initial_dbo-final_dbo) * Q * (ks + final_dbo)
    lower = umax * final_dbo * x
    vol = upper/lower
    if vol <= 100:
        st.warning('you may hav to consider a radial shape for your reactor, since your volume is smaller than 100 cubic meters')
    
    return vol

def volumey(selected):
    return selected * (df['DBO0']-df['DBOf']) * df['Q'] * (ks + df['DBOf']) / (umax * df['DBOf'] * x)
def volumeumax(selected):
    return y * (df['DBO0']-df['DBOf']) * df['Q'] * (ks + df['DBOf']) /(selected * df['DBOf'] * x)
def volumeks(selected):
    return y * (df['DBO0']-df['DBOf']) * df['Q'] * (selected + df['DBOf']) /(umax * df['DBOf'] * x)
def volumex(selected):
    return y * (df['DBO0']-df['DBOf']) * df['Q'] * (ks + df['DBOf']) /(umax * df['DBOf'] * selected)

############################################################################################################################
############################################################################################################################
############################################PANDAS PRE-LOADING


lista= {'Y' : [0.4,0.8,0.65,'mgSSV/mgDBO5'],
        'ks' : [25,60,60,'mgDBO5/L'],
        'umax' : ['not available', 'not available', 0.5, '1/d'],
        'X' : ['not available', 'not available', 3000, 'mgSSV/L']
       }
commonvals = pd.DataFrame(lista,)
commonvals = commonvals.transpose()
commonvals.columns = ['lower limit','higher limit','typical','unit']


############################################################################################################################
############################################################################################################################
###########################                          SIDEBAR                                        ########################
    

st.sidebar.markdown(f"""
    # INITIAL VARIABLES
    """)

########### INPUT VALUES
st.sidebar.markdown('### Flowrate:')
Qinput = st.sidebar.number_input('Insert your initial flowrate *(m3/d)*', value = 300.0*24, step = 10.0)
Q_max = Qinput * 1.5
Q = st.sidebar.slider('or fine-tune it:', 0.0, max_value = Q_max, value=  Qinput, key = '1')

st.sidebar.markdown('### initial DBO5:')
initial_dbo_input = st.sidebar.number_input('Insert your initial DBO5 *(mgDBO5/L)*', value = 300.0, step = 10.0)
dbo_max = initial_dbo_input *1.5
initial_dbo = st.sidebar.slider('or fine-tune it:', 0.0, max_value = dbo_max, value = initial_dbo_input, key = '2')

st.sidebar.markdown('### final DBO5:')
final_dbo_input = st.sidebar.number_input('Insert your final DBO5 *(mgDBO5/L)*', value = 30.0, step = 10.0)
final_dbo_max = final_dbo_input *1.5 
final_dbo = st.sidebar.slider('or fine-tune it:', 0.0, max_value = final_dbo_max, value = final_dbo_input, key = '3')

############################################################################################################################
############################################################################################################################
###########################                          BODY OF PAGE                                   ########################

st.markdown('# UNSAM Clarifier')
st.markdown('## *waste water treatment software*')

st.markdown('### Please select your initial variables on the sidebar.')


########### EFFICIENCY
eff = efficiency(initial_dbo,final_dbo)

if final_dbo == 0:
    st.error("Error. you can't have an an efficiency of 100%")
elif eff < 1 and eff > 0 :
    if eff > 0.98:
        st.warning(f"""your efficiency of {eff} is maybe too optimist. \nPlease consider designing a train of reactors or improving the preceding treatment.""")
    st.success(f'Your efficiency is: **{eff*100}%**')


########### WASTEWATER AND BIBLIOGRAPHY

if eff > 0 and eff < 100:
    st.markdown("### Let's calculate the Volume, but first:")
    possibletypes = ['sewage','industrial']
    watertype = st.text_input("Which kind of waste water are you working with?\nSelect either 'sewage' or 'industrial'",value = None, key = 'a')

if watertype == 'None':
    st.stop()
elif watertype != None:
    if watertype not in possibletypes:
        st.error("please enter either 'sewage' or 'industrial'" )
        st.stop()


if watertype in possibletypes:
    st.markdown("### Please input your design variables:")
    bibliography  = biblio()


    y = yvars()
    ks = ksvars()
    umax = umaxvars()
    x = xvars()


if st.button('calculate volume!'):
    vol = volume()
    st.success(f'{round(vol,2)} m3')

for i in range(0,6):
    st.write('\n')

############################################################################################################################
############################################################################################################################
###########################                          Plots!                                         ########################

st.markdown("""\n\n\n # select variables  to plot and check volume!""")



third = st.radio('Please select your variable.',
                    ('Y', 'umax', 'ks', 'X'))
variables = { 'flowrate': Q , 'DBO': initial_dbo, 'DBOfinal': final_dbo, 'Y': y,  
            'umax': umax, 'ks': ks, 'X' : x  }


Qrange= np.linspace(Q*0.5,Q*1.5,20) 
dborange= np.linspace(initial_dbo*0.5,initial_dbo*1.5,20)
dbofrange = np.linspace(final_dbo*0.5,final_dbo*1.5,20)

selected = variables[third]
selected = np.linspace(selected*0.5,selected*1.5,5)  


df= pd.DataFrame(data = [Qrange,dborange,dbofrange])
df = df.transpose()
df.columns = ['Q','DBO0','DBOf']

st.write(f'X is the ***flowrate***, y is the ***initial DBO***\n and z is the resulting ***volume***')

if third == 'Y':
    for i in range(len(selected)):
        df['vol' + f'({third}' + f'={round(selected[i],3)})'] = volumey(selected[i])
    x=df['Q']
    y=df['DBO0']

    fig=go.Figure()
    for i in range(len(selected)):
        fig.add_trace(go.Scatter3d(x=x,y=y,z=df['vol' + f'({third}' + f'={round(selected[i],3)})'],
                        mode='lines+markers',
                        name='vol' + f'({third}' + f'={round(selected[i],3)})'), )

    camera = dict(up=dict(x=0, y=0, z=1), center=dict(x=0, y=0, z=0), eye=dict(x=2.25, y=1.25, z=0.5))

    st.plotly_chart(fig.update_layout(scene_camera=camera, 
        #width=800, height=700, 
        autosize = True, title = 'hover over me!'),)
    st.write(df.head())

if third == 'umax':
    for i in range(len(selected)):
        df['vol' + f'({third}' + f'={round(selected[i],3)})'] = volumeumax(selected[i])
    x=df['Q']
    y=df['DBO0']
    fig=go.Figure()
    for i in range(len(selected)):
        fig.add_trace(go.Scatter3d(x=x,y=y,z=df['vol' + f'({third}' + f'={round(selected[i],3)})'],
                        mode='lines+markers',
                        name='vol' + f'({third}' + f'={round(selected[i],3)})'))
    
    camera = dict(up=dict(x=0, y=0, z=1), center=dict(x=0, y=0, z=0), eye=dict(x=2.25, y=1.25, z=0.5))
    st.plotly_chart(fig.update_layout(scene_camera=camera, 
        #width=800, height=700, 
        autosize = True, title = 'hover over me!'))
    st.write(df.head())

if third == 'ks':
    for i in range(len(selected)):
        df['vol' + f'({third}' + f'={round(selected[i],3)})'] = volumeks(selected[i])
    x=df['Q']
    y=df['DBO0']
    fig=go.Figure()
    for i in range(len(selected)):
        fig.add_trace(go.Scatter3d(x=x,y=y,z=df['vol' + f'({third}' + f'={round(selected[i],3)})'],
                        mode='lines+markers',
                        name='vol' + f'({third}' + f'={round(selected[i],3)})'))
    
    camera = dict(up=dict(x=0, y=0, z=1), center=dict(x=0, y=0, z=0), eye=dict(x=2.25, y=1.25, z=0.5))
    st.plotly_chart(fig.update_layout(scene_camera=camera, 
        #width=800, height=700, 
        autosize = True, title = 'hover over me!'))
    st.write(df.head())

if third == 'X':

    for i in range(len(selected)):
        df['vol' + f'({third}' + f'={round(selected[i],3)})'] = volumex(selected[i])

    x=df['Q']
    y=df['DBO0']
    fig=go.Figure()
    for i in range(len(selected)):
        fig.add_trace(go.Scatter3d(x=x,y=y,z=df['vol' + f'({third}' + f'={round(selected[i],3)})'],
                        mode='lines+markers',
                        name='vol' + f'({third}' + f'={round(selected[i],3)})'))
    
    
    camera = dict(up=dict(x=0, y=0, z=1), center=dict(x=0, y=0, z=0), eye=dict(x=2.25, y=1.25, z=0.5))
    st.plotly_chart(fig.update_layout(scene_camera=camera, 
        #width=800, height=700, 
        autosize = True, title = 'hover over me!'))
    st.write(df.head())

