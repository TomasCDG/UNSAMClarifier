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
	if watertype == 'Sewage':
		bibliography = st.radio("Would you like to see the typical design values and ranges for typical sewage wastewater from now on?",
			('yes','no'), index = 1)
        #if bibliography == "yes" :
         #   return bibliography
        #elif bibliography == "no":
           # return bibliography       
	elif watertype == 'Industrial':
		bibliography = st.radio("Would you like to see some typical industrial values from bibliography?", ('yes','no'), index = 1)
        #if bibliography == "yes":
          #  return bibliography
        #elif bibliography == "no":
          #  return bibliography
	return bibliography

def yvars():
    y= st.number_input('Enter please your Y (relación masa celular formada/sustrato consumido)', value= 0.6)
    #if bibliography == 'yes':
        #st.write(commonvals.loc['Y',:])     
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
        st.warning('You may hav to consider a radial shape for your reactor, since your volume is smaller than 100 cubic meters')
    return vol

<<<<<<< HEAD
def volumey(selected):
    return selected * (df['DBO0']-df['DBOf']) * df['Q'] * (ks + df['DBOf']) / (umax * df['DBOf'] * x)
def volumeumax(selected):
    return y * (df['DBO0']-df['DBOf']) * df['Q'] * (ks + df['DBOf']) /(selected * df['DBOf'] * x)
def volumeks(selected):
    return y * (df['DBO0']-df['DBOf']) * df['Q'] * (selected + df['DBOf']) /(umax * df['DBOf'] * x)
def volumex(selected):
    return y * (df['DBO0']-df['DBOf']) * df['Q'] * (ks + df['DBOf']) /(umax * df['DBOf'] * selected)
=======
####### FLOW FUNCTIONS

def kdvars():
    kd= st.number_input('Enter please your kd (constante de decaimiento)', value = 0.06)
    if bibliography == 'yes':
        st.write(commonvals.loc['kd',:])     
    st.write(f"{kd} 1/d")   
    return kd

def xpvars():
    xp= st.number_input('Enter please your Xp (concentración de purga)', value = 8000)
    if bibliography == 'yes':
        st.write(commonvals.loc['xp',:])     
    st.write(f"{xp} mgSSV/L")   
    return xp

def kvars():
    k= st.number_input('Enter please your k (tasa máxima de utilización de sustrato por unidad de masa de microorganismos)', value = 5)
    if bibliography == 'yes':
        st.write(commonvals.loc['k',:])     
    st.write(f"{k} 1/d")   
    return k

def pflow():
    qp= (((umax*x*final_dbo)/(final_dbo+ks))-(x*kd))*(vol/xp)
    return qp

def recflow():
    qr= ((Q*x-qp*xp)/(xp-x))
    return qr

###### VALIDATIONS

def tr():
	tr = vol/Q
	if tr < 0.125 or tr > 0.2083:
		st.warning(f"**HYDRAULIC RESIDENCE TIME: {round(tr,2)}.** *Should be between 0.125 and 0.2083 days (3 and 5 hours)*")
	else:
		st.success(f"**HYDRAULIC RESIDENCE TIME: {round(tr,2)}.** *Should be between 0.125 and 0.2083 days (3 and 5 hours)*")

def fm():
	fm = (Q*initial_dbo)/(vol*x)
	if fm < 0.2 or fm > 0.6:
		st.warning(f"**MICROORGANISM - FOOD RELATION: {round(fm,2)}.** *Should be between 0.2 and 0.6 1/d*")
	else:
		st.success(f"**MICROORGANISM - FOOD RELATION: {round(fm,2)}.** *Should be between 0.2 and 0.6 1/d*")

def cv():
	cv = (Q*final_dbo*0.0013)/vol
	if cv < 0.8 or cv > 1.92:
		st.warning(f"**VOLUMETRIC LOAD: {round(cv,2)}.** *Should be between 0.8 and 1.92 kgDBO5/m3*")
	else:
		st.success(f"**VOLUMETRIC LOAD: {round(cv,2)}.** *Should be between 0.8 and 1.92 kgDBO5/m3*")

def theta():
	theta = (vol*x)/(qp*xp)
	if theta < 5 or theta > 15:
		st.warning(f"**CELULAR RESIDENCE TIME: {round(theta,2)}.** *Should be between 5 and 15 days*")
	else:
		st.success(f"**CELULAR RESIDENCE TIME: {round(theta,2)}.** *Should be between 5 and 15 days*")
	return theta

def u():
	u = (final_dbo*k)/(ks+final_dbo)
	if u < 0.2 or u > 0.6:
		st.warning(f"**RATE OF SUBSTRATE UTILIZATION: {round(u,2)}.** *Should be between 0.2 and 0.6 kgDBO5/kgSSVLMd*")
	else:
		st.success(f"**RATE OF SUBSTRATE UTILIZATIONv: {round(u,2)}.** *Should be between 0.2 and 0.6 kgDBO5/kgSSVLMd*")

######### SLUDGE PURGE

###### RATIO BETWEEN SSSV AND SST

def sssvsstratio():
    sssvsstratio = st.number_input('Enter please your sssv/sst ratio (relación entre sssv y sst)', value= 0.8)
    #if bibliography == 'yes':
        #st.write(commonvals.loc['umax',:])     
    st.write(f"{sssvsstratio}")   
    return sssvsstratio

###### CALCULATE OBSERVED "Y"

def yobs():
	yobs = y/(1+kd+theta())
	return yobs

###### CALCULATE VOLATILE ACTIVATED SLUDGE MASS

def px():
	px = yobs()*Q*(initial_dbo-final_dbo)/1000
	return px

###### CALCULATE TOTAL SLUDGE MASS, BASED ON TOTAL SUSPENDED SOLIDS

def pxss():
	pxss = px()/sssvsstratio()
	return pxss
>>>>>>> 9edd4048c1a2c8433eaa0ecca2ea1f6ed2aaf9ce

############################################################################################################################
############################################################################################################################
############################################PANDAS PRE-LOADING


lista= {'Y' : [0.4,0.8,0.6,'mgSSV/mgDBO5'],
        'ks' : [25,100,60,'mgDBO5/L'],
        'umax' : ['not available', 'not available', 0.5, '1/d'],
        'X' : ['not available', 'not available', 3000, 'mgSSV/L'],
        'kd' : [0.04,0.075,0.06,'1/d'],
        'xp' : ['not available yet','not available yet',8000,'mgSSV/L'],
        'k' : [2,10,5,'1/d']
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
st.markdown('## *Waste water treatment software*')
st.markdown('### Please select your initial variables on the sidebar.')


########### EFFICIENCY
eff = efficiency(initial_dbo,final_dbo)

if final_dbo == 0:
    st.error("Error. You can't have an an efficiency of 100%")
elif eff < 1 and eff > 0 :
    if eff > 0.98:
        st.warning(f"""Your efficiency of {eff} is maybe too optimist. \nPlease consider designing a train of reactors or improving the preceding treatment.""")
    st.success(f'Your efficiency is: **{eff*100}%**')


########### WASTEWATER AND BIBLIOGRAPHY

if eff > 0 and eff < 100:
    st.markdown("### Let's calculate the Volume, but first:")
    #possibletypes = ['sewage','industrial']
    #watertype = st.text_input("Which kind of waste water are you working with?\nSelect either 'sewage' or 'industrial'",value = None, key = 'a')
    watertype = st.selectbox("Which kind of waste water are you working with?",('Sewage','Industrial'))

#if watertype == 'None':
#    st.stop()
#elif watertype != None:
#    if watertype not in possibletypes:
 #       st.error("please enter either 'sewage' or 'industrial'" )
 #       st.stop()


#if watertype in possibletypes:
    st.markdown("### Please input your design variables:")
    bibliography  = biblio()


    y = yvars()
    if bibliography == 'yes':
        st.write(commonvals.loc['Y',:])
    ks = ksvars()
    umax = umaxvars()
    x = xvars()


#if st.button('Calculate volume!'):
vol = volume()
st.success(f'**VOLUME: {round(vol,2)} m3**')
	
	##### FLOW

st.markdown("### Let's calculate the Flow, but first:")
kd = kdvars()
xp = xpvars()
k = kvars()

	#if st.button('Calculate flow!'):
qp = pflow()
qr = recflow()
st.success(f'**PURGE FLOW: {round(qp,2)} m3/d**')
st.success(f'**RECYCLE FLOW: {round(qr,2)} m3/d**')

	#VALIDATIONS

st.markdown("### Validations")
tr()
fm()
cv()
theta()
u()

	#SLUDGE

<<<<<<< HEAD
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

=======
st.success(f'**TOTAL SLUDGE: {round(pxss(),2)} kg/d **')
>>>>>>> 9edd4048c1a2c8433eaa0ecca2ea1f6ed2aaf9ce
