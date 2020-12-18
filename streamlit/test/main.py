import pandas as pd
import streamlit as st
import reactor as r

st.set_page_config(
            page_title="Reactor", # => Quick reference - Streamlit
            page_icon=":droplet:",
            #layout="centered", # wide
            initial_sidebar_state="auto") # collapsed



def biblio():
	if unit.get_watertype() == 'Sewage':
		bibliography = st.radio("Would you like to see the typical design values and ranges for typical sewage wastewater from now on?",
			('yes','no'), index = 1)   

	elif unit.get_watertype() == 'Industrial':
		bibliography = st.radio("Would you like to see some typical industrial values from bibliography?", ('yes','no'), index = 1)

	return bibliography

st.sidebar.markdown(f"""
    # INITIAL VARIABLES
    """)

########### INPUT VALUES
st.sidebar.markdown('### Flowrate:')
Qinput = st.sidebar.number_input('Insert your initial flowrate *(m3/d)*', value = 300.0*24, step = 10.0)
Q_max = Qinput * 2
Q = st.sidebar.slider('or fine-tune it:', 0.0, max_value = Q_max, value=  Qinput, key = '1')

st.sidebar.markdown('### initial DBO5:')
initial_dbo_input = st.sidebar.number_input('Insert your initial DBO5 *(mgDBO5/L)*', value = 300.0, step = 10.0)
dbo_max = initial_dbo_input * 2
initial_dbo = st.sidebar.slider('or fine-tune it:', 0.0, max_value = dbo_max, value = initial_dbo_input, key = '2')

st.sidebar.markdown('### final DBO5:')
final_dbo_input = st.sidebar.number_input('Insert your final DBO5 *(mgDBO5/L)*', min_value = 0.01, value = 30.0, step = 10.0)
final_dbo_max = final_dbo_input * 2 
final_dbo = st.sidebar.slider('or fine-tune it:', 0.01, max_value = final_dbo_max, value = final_dbo_input, key = '3')

st.markdown('# UNSAM Clarifier')
st.markdown('## *Waste water treatment software*')
st.markdown('### Please select your initial variables on the sidebar.')

########### EFFICIENCY
if final_dbo == 0:
    st.error("Error. You can't have an an efficiency of 100%")

unit = st.selectbox("Select unit to work with",('Reactor','Laguna'))

if (unit == 'Reactor'):
	unit = r.Reactor(initial_dbo,final_dbo,Q)
if unit.get_eff() < 1 and unit.get_eff() > 0 :
	if unit.get_eff() > 0.98:
		st.warning(f"""Your efficiency of {round(unit.get_eff(),2)*100} is maybe too optimist. \nPlease consider designing a train of reactors or improving the preceding treatment.""")
	st.success(f'Your efficiency is: **{round(unit.get_eff(),2)*100}%**')

########### WASTEWATER AND BIBLIOGRAPHY

st.markdown("### Let's calculate the Volume, but first:")
unit.set_watertype(st.selectbox("Which kind of waste water are you working with?",('Sewage','Industrial'))) 

st.markdown("### Please input your design variables:")
bibliography  = biblio()

######Volume variables init

unit.setvolvars(bibliography)

######Volume
st.success(f'**VOLUME: {round(unit.volume(),2)} m3**')
	
##### Flow variables init

st.markdown("### Let's calculate the Flow, but first:")
unit.kdvars(bibliography)
unit.xpvars(bibliography)
unit.kvars(bibliography)

#####Flow
st.success(f'**PURGE FLOW: {round(unit.qp(),2)} m3/d**')
st.success(f'**RECYCLE FLOW: {round(unit.qr(),2)} m3/d**')

######VALIDATIONS

st.markdown("### Validations")
unit.validate()

########SLUDGE

unit.sssvsstratio()
st.success(f'**TOTAL SLUDGE: {round(unit.pxss(),2)} kg/d **')