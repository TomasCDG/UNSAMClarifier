import pandas as pd
import streamlit as st
#import plotly.express as px

class Unit_body():

########################################################################## INITIALIZER ############################################
	
	def __init__(self,starting_dbo,Q):
		self._dbo0 = starting_dbo
		self._flow = Q
		self._initBiblio()
		############## NOT INITIALIZED VARIABLES

		############# BIBLIOGRAPHY

	############################################################ METHODS #######################################################################

	######################################### EXECUTE

	def execute(self,biblio):
		self.calculate(biblio)
		self.validate()
		self.results()
		self.warnings()