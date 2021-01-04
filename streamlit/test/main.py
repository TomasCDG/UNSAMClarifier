import pandas as pd
import streamlit as st

#################### UNITS IMPORT

import reactor as r
import alagoon as al
import alagoon_tr as al_tr

#################################

st.set_page_config(
			page_title="Reactor", # => Quick reference - Streamlit
			page_icon=":droplet:",
			initial_sidebar_state="auto") # collapsed

################################

def biblio():
	bibliography = st.radio("Would you like to see some typical values from bibliography?", ('yes','no'), index = 1)

	return bibliography

def unit_selector(unit_list):
	option = st.selectbox("Select unit to work with",('Reactor','Anaerobic Lagoon','Anaerobic Lagoon_tr'),key="1")
	for i in unit_list:
		if i.name == option:
			unit = i
	return unit

def return_name(unit):
	return unit.name

st.sidebar.markdown(f"""
    # INITIAL VARIABLES
    """)

###################################################### SIDE BAR IMPUT VALUES
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


##################################################### CENTRAL BLOCK

st.markdown('# UNSAM Clarifier')
st.markdown('## *Waste water treatment software*')
st.markdown('### Please select your initial variables on the sidebar.')

##################PROGRAM START

def main():

	used_units_list = []

	reactor = r.Reactor(initial_dbo,final_dbo,Q)
	alagoon = al.ALagoon(initial_dbo,Q)
	alagoon_tr = al_tr.ALagoon_tr(initial_dbo,Q)

	unit_list = [reactor,alagoon,alagoon_tr]

	while (not(st.button("salir",key=2))):
		st.sidebar.markdown('### Units: ')
		unit = unit_selector(unit_list)
		unit.execute(biblio())
		if st.button("Save unit",key=1):
			used_units_list.append(unit)

if __name__ == "__main__":
	main()

