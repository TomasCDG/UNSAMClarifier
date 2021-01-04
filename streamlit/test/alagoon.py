import pandas as pd
import streamlit as st
#import plotly.express as px

class ALagoon():

########################################################################## INITIALIZER ############################################
	
	def __init__(self,starting_dbo,Q):
		self.name = "Anaerobic Lagoon"
		self._dbo0 = starting_dbo
		self._flow = Q
		self._initBiblio()
		############## NOT INITIALIZED VARIABLES

		#self._t
		#self._h

		############# BIBLIOGRAPHY
	def _initBiblio(self):
		self._lista= {'tr' : [20,50,'not available', 'days'],
		'h' : [2.5,5,'not available', 'm'],
		't' : [6,50,'20-25', '°C'],
		'cov' : [160,800,'not available', 'gDBO5/m3d']
		}
		self._commonvals = pd.DataFrame(self._lista,)
		self._commonvals = self._commonvals.transpose()
		self._commonvals.columns = ['lower limit','higher limit','typical','unit']

	
	############################################################ METHODS #######################################################################

	############### EFFICIENCY

	#def eff(self):
		#return ((self.dbo0-self.dbof)/self.dbo0)

	############## TEMPERATURE

	def _tvars(self,biblio):
		t= st.number_input('Enter please your temperature', min_value=6.1,value = 6.1,key=1)
		#if biblio == 'yes':
			#st.write(self.temps.loc['Y',:])
		st.write(f"{t} °C")
		self._t = t

	############## VOLUME

	def _hvars(self,biblio):
		h= st.number_input('Enter please your depth', min_value=2.5, max_value=5.0,value = 2.5,key=2)
		if biblio == 'yes':
			st.write(self._commonvals.loc['h',:])
		st.write(f"{h} meters")
		self._h = h

	def _vol(self):
		if self._dbo0 < 1000:
			return 100
		else:
			return 16.5*self._t-100

	def _ol(self):
		return self._flow*self._dbo0

	def volume(self):
		return self._ol()/self._vol()

	def _tr(self):
		return self.volume()/self._flow

	def sol(self):
		return (10*self._ol())/(self.volume()/self._h)

	############## VALIDATIONS

	def _tr_val(self):
		if self._tr() < 20 or self._tr() > 50:
			st.warning(f"**HYDRAULIC RESIDENCE TIME: {round(self._tr(),2)}.** *Should be between 20 and 50 days*")
		else:
			st.success(f"**HYDRAULIC RESIDENCE TIME: {round(self._tr(),2)}.** *Should be between 20 and 50 days*")

	############################################################ CORE ############################################################

	########################################## WARNINGS

	def warnings(self):
		st.markdown("### Warnings")
		self._wcov()
		self._wt()

	def _wcov(self):
		if self._dbo0 < 1000:
			st.warning("Due to the low initial BOD5 (<1000 mg/l), volumetric organic load (vol) is considered as 100 gBOD5/m3.d")

	def _wt(self):
		if self._t < 11 or self._t > 30:
			st.warning("All the trails where made within 10 and 30 °C, and the application of the model is not recommended for temperatures outside that range.")

	############## CALCULATE

	def calculate(self, biblio):
		self._tvars(biblio)
		self._hvars(biblio)

	######################################### VALIDATION

	def validate(self):
		st.markdown("### Validations")

		self._tr_val()

		st.markdown("### ----------------------------------------------------------------")

	#################################### SHOW RESULTS

	def results(self):
		st.markdown("### Results")

		#st.success(f'**EFFICIENCY: {round(self.eff(),2)*100}%**')
		st.success(f'**VOLUME: {round(self.volume(),2)} m3**')
		st.success(f'**SUPERFICIAL ORGANIC LOAD: {round(self.sol(),2)} kgBOD5/ha.d**')
		#st.success(f'**FINAL BOD5: {round(self.(),2)} gBOD5/m3.d**')
		

		st.markdown("### ----------------------------------------------------------------")

	############## EXECUTE

	def execute(self,biblio):
		self.calculate(biblio)
		self.validate()
		self.results()
		self.warnings()

