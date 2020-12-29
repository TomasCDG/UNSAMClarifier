import pandas as pd
import streamlit as st
#import plotly.express as px

#st.set_page_config(
           # page_title="Reactor", # => Quick reference - Streamlit
            #page_icon=":droplet:",
            ##layout="centered", # wide
            #initial_sidebar_state="auto") # collapsed

class ALagoon():

########################################################################## INITIALIZER ############################################
	
	def __init__(self,starting_dbo,final_dbo,Q):
		self.__name = "Anaerobic Lagoon"
		self.__dbo0 = starting_dbo
		self.__dbof = final_dbo
		self.__flow = Q
		
		############## NOT INITIALIZED VARIABLES

		#self.t

		############# BIBLIOGRAPHY

		self.lista= {'tr' : [20,50,'not available', 'days'],
		'h' : [2.5,5,'not available', 'm'],
		't' : [6,50,'20-25', '°C'],
		'cov' : [160,800,'not available', 'gDBO5/m3d']
		}
		self.commonvals = pd.DataFrame(self.lista,)
		self.commonvals = self.commonvals.transpose()
		self.commonvals.columns = ['lower limit','higher limit','typical','unit']

	################# GETTERS
	
	@property
	def name(self):
		return self.__name

	@property
	def dbo0(self):
		return self.__dbo0

	@property
	def dbof(self):
		return self.__dbof

	@property
	def flow(self):
		return self.__flow

	@property
	def t(self):
		return self._t

#################### SETTERS
	
	@name.setter
	def name(self, var):
		self.__name = var

	@dbo0.setter
	def dbo0(self, var):
		self.__dbo0 = var

	@dbof.setter
	def dbof(self, var):
		self.__dbof = var

	@flow.setter
	def flow(self, var):
		self.__flow = var

	@t.setter
	def t(self, var):
		self.__t = var

	############################################################ METHODS #######################################################################

	############### EFFICIENCY

	def eff(self):
		return ((self.dbo0-self.dbof)/self.dbo0)

	############## TEMPERATURE

	def tvars(self):
		t= st.number_input('Enter please your temperature')
		st.write(f"{t} °C")
		self.t = t

	
	############## CALCULATE

	def calculate(self, biblio):
		self.tvars()

	############## EXECUTE

	def execute(self,biblio):
		self.calculate(biblio)
		#self.validate()
		#self.results()
		#self.warnings()