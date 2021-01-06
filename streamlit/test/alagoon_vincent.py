import pandas as pd
import streamlit as st
#import plotly.express as px
from alagoon import ALagoon

class ALagoon_vincent(ALagoon):

########################################################################## INITIALIZER ############################################
	
	def __init__(self,starting_dbo,Q):
		super().__init__(starting_dbo,Q)
		self.name = "Anaerobic Lagoon - Vincent"
		
		############## NOT INITIALIZED VARIABLES

		#self._t
		#self._h
		#self._tr

	############################################################ METHODS #######################################################################

	############### EFFICIENCY

	def vol(self):
		return self._ol()/self.volume()

	############## VOLUME

	def _trvars(self):
		tr= st.number_input('Enter please your residence time', min_value=20, max_value=50, value = 35)
		st.write(f"{tr} days")
		self._tr=tr

	def volume(self):
		return self._flow*self._tr

	############################################################ CORE ############################################################

	########################################## WARNINGS

	def warnings(self):
		st.markdown("### Warnings")
		self._wt()

	def _wt(self):
		if self._t < 11 or self._t > 30:
			st.warning("All the trails where made within 10 and 30 °C, and the application of the model is not recommended for temperatures outside that range.")

	######################################### CALCULATE

	def calculate(self, biblio):
		self._tvars(biblio)
		self._hvars(biblio)
		self._trvars()

	######################################### VALIDATION

	def validate(self):
		pass