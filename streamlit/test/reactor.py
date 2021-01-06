import pandas as pd
import streamlit as st
from unit_body import Unit_body
#import plotly.express as px

####### MAIN CLASS

class Reactor(Unit_body):

############################################################# INITIALIZER ########################################
	
	def __init__(self,starting_dbo,Q):
		super().__init__(starting_dbo,Q)
		self.name = 'Reactor'
		############## NOT INITIALIZED VARIABLES

		#self._watertype
		#self._y
		#self._ks
		#self._umax
		#self._x
		#self._kd
		#self._xp
		#self._k
		#self._sssvsstratio
		#self._dbof

		############### BIBLIOGRAPHY
	def _initBiblio(self):
		self._lista= {'Y' : [0.4,0.8,0.6,'mgSSV/mgDBO5'],
		'ks' : [25,100,60,'mgDBO5/L'],
		'umax' : ['not available', 'not available', 0.5, '1/d'],
		'X' : ['not available', 'not available', 3000, 'mgSSV/L'],
		'kd' : [0.04,0.075,0.06,'1/d'],
		'xp' : ['not available yet','not available yet',8000,'mgSSV/L'],
		'k' : [2,10,5,'1/d']
		}
		self._commonvals = pd.DataFrame(self._lista,)
		self._commonvals = self._commonvals.transpose()
		self._commonvals.columns = ['lower limit','higher limit','typical','unit']

	################################################################### METHODS ##################################

	################################## EFFICIENCY

	def eff(self):
		return ((self._dbo0 -self._dbof)/self._dbo0)

	def _dbofvars(self):
		dbof = st.number_input('Enter please your final DBO',value=30)
		st.write(f"{dbof} mgDBO5/l")
		self._dbof = dbof

	################################ WATERTYPE

	def _wvars(self):
		var = st.selectbox("Enter please your watertype", ('Sewage','Industrial'))
		self._watertype = var
		
	############################### VOLUME

	def _yvars(self, biblio):
		y= st.number_input('Enter please your Y (relación masa celular formada/sustrato consumido)', value= 0.6)
		if biblio == 'yes':
			st.write(self._commonvals.loc['Y',:])     
		st.write(f"{y} mgSSV/mgDBO5")   
		self._y = y

	def _ksvars(self, biblio):
		ks= st.number_input('Enter please your ks (constante de sustrato)', value= 60.0)
		if biblio == 'yes':
			st.write(self._commonvals.loc['ks',:])     
		st.write(f"{ks} mgDBO5/L")   
		self._ks = ks

	def _umaxvars(self, biblio):
		umax= st.number_input('Enter please your umax (tasa de crecimiento específico máximo)', value= 0.5)
		if biblio == 'yes':
			st.write(self._commonvals.loc['umax',:])     
		st.write(f"{umax} 1/d")   
		self._umax = umax

	def _xvars(self, biblio):
		x= st.number_input('Enter please your X (biomasa en el reactor)', value = 3000.0)
		if biblio == 'yes':
			st.write(self._commonvals.loc['X',:])     
		st.write(f"{x} mgSSV/L")   
		self._x = x

	def volume(self):
		upper = self._y * (self._dbo0-self._dbof) * self._flow * (self._ks + self._dbof)
		lower = self._umax * self._dbof * self._x
		vol = upper/lower
		return vol

	#################################### FLOW

	def _kdvars(self, biblio):
		kd= st.number_input('Enter please your kd (constante de decaimiento)', value = 0.06)
		if biblio == 'yes':
			st.write(self._commonvals.loc['kd',:])     
		st.write(f"{kd} 1/d")   
		self._kd = kd

	def _xpvars(self, biblio):
		xp= st.number_input('Enter please your Xp (concentración de purga)', value = 8000)
		if biblio == 'yes':
			st.write(self._commonvals.loc['xp',:])     
		st.write(f"{xp} mgSSV/L")   
		self._xp = xp

	def _kvars(self, biblio):
		k= st.number_input('Enter please your k (tasa máxima de utilización de sustrato por unidad de masa de microorganismos)', value = 5)
		if biblio == 'yes':
			st.write(self._commonvals.loc['k',:])     
		st.write(f"{k} 1/d")   
		self._k = k

	def qp(self):
		return (((self._umax*self._x*self._dbof)/(self._dbof+self._ks))-(self._x*self._kd))*(self.volume()/self._xp)

	def qr(self):
		return ((self._flow*self._x-self.qp()*self._xp)/(self._xp-self._x))

	######################################### SLUDGE PURGE

	############### RATIO BETWEEN SSSV AND SST

	def _sssvsstratio(self):
	    sssvsstratio = st.number_input('Enter please your sssv/sst ratio (relación entre sssv y sst)', value= 0.8) 
	    st.write(f"{sssvsstratio}")   
	    self._sssvsstratio = sssvsstratio

	########### CALCULATE OBSERVED "Y"

	def _yobs(self):
		yobs = self._y/(1+self._kd+self._theta())
		return yobs

	########## CALCULATE VOLATILE ACTIVATED SLUDGE MASS

	def _px(self):
		px = self._yobs()*self._flow*(self._dbo0-self._dbof)/1000
		return px

	########## CALCULATE TOTAL SLUDGE MASS, BASED ON TOTAL SUSPENDED SOLIDS

	def pxss(self):
		pxss = self._px()/self._sssvsstratio
		return pxss


	############################################# VALIDATIONS

	def _tr(self):
		return self.volume()/self._flow

	def _fm(self):
		return (self._flow*self._dbo0)/(self.volume()*self._x)

	def _cv(self):
		return (self._flow*self._dbof*0.0013)/self.volume()

	def _theta(self):
		return (self.volume()*self._x)/(self.qp()*self._xp)

	def _u(self):
		return (self._dbof*self._k)/(self._ks+self._dbof)

	def _tr_val(self):
		if self._tr() < 0.125 or self._tr() > 0.2083:
			st.warning(f"**HYDRAULIC RESIDENCE TIME: {round(self._tr(),2)}.** *Should be between 0.125 and 0.2083 days (3 and 5 hours)*")
		else:
			st.success(f"**HYDRAULIC RESIDENCE TIME: {round(self._tr(),2)}.** *Should be between 0.125 and 0.2083 days (3 and 5 hours)*")

	def _fm_val(self):
		if self._fm() < 0.2 or self._fm() > 0.6:
			st.warning(f"**MICROORGANISM - FOOD RELATION: {round(self._fm(),2)}.** *Should be between 0.2 and 0.6 1/d*")
		else:
			st.success(f"**MICROORGANISM - FOOD RELATION: {round(self._fm(),2)}.** *Should be between 0.2 and 0.6 1/d*")

	def _cv_val(self):
		if self._cv() < 0.8 or self._cv() > 1.92:
			st.warning(f"**VOLUMETRIC LOAD: {round(self._cv(),2)}.** *Should be between 0.8 and 1.92 kgDBO5/m3*")
		else:
			st.success(f"**VOLUMETRIC LOAD: {round(self._cv(),2)}.** *Should be between 0.8 and 1.92 kgDBO5/m3*")

	def _theta_val(self):
		if self._theta() < 5 or self._theta() > 15:
			st.warning(f"**CELULAR RESIDENCE TIME: {round(self._theta(),2)}.** *Should be between 5 and 15 days*")
		else:
			st.success(f"**CELULAR RESIDENCE TIME: {round(self._theta(),2)}.** *Should be between 5 and 15 days*")

	def _u_val(self):
		if self._u() < 0.2 or self._u() > 0.6:
			st.warning(f"**RATE OF SUBSTRATE UTILIZATION: {round(self._u(),2)}.** *Should be between 0.2 and 0.6 kgDBO5/kgSSVLMd*")
		else:
			st.success(f"**RATE OF SUBSTRATE UTILIZATION: {round(self._u(),2)}.** *Should be between 0.2 and 0.6 kgDBO5/kgSSVLMd*")

##################################################################### CORE #################################################

########################################## WARNINGS

	def warnings(self):
		st.markdown("### Warnings")
		self._wvolumen()
		self._weff()

	def _wvolumen(self):
		if self.volume() <= 100:
			st.warning('You may have to consider a radial shape for your reactor, since your volume is smaller than 100 cubic meters')

	def _weff(self):
		if self.eff() < 1 and self.eff() > 0 :
			if self.eff() > 0.98:
				st.warning(f"""Your efficiency of {round(self.eff(),2)*100} is maybe too optimist. \nPlease consider designing a train of reactors or improving the preceding treatment.""")

	###################################### CALCULATE

	def calculate(self, biblio):
		st.markdown("### Please input your design variables:")
		
		self._wvars()
		self._dbofvars()
		self._yvars(biblio)
		self._ksvars(biblio)
		self._umaxvars(biblio)
		self._xvars(biblio)
		self._kdvars(biblio)
		self._xpvars(biblio)
		self._kvars(biblio)
		self._sssvsstratio()

	#################################### VALIDATION

	def validate(self):
		st.markdown("### Validations")

		self._tr_val()
		self._fm_val()
		self._cv_val()
		self._theta_val()
		self._u_val()

		st.markdown("### ----------------------------------------------------------------")

	#################################### SHOW RESULTS

	def results(self):
		st.markdown("### Results")

		st.success(f'**EFFICIENCY: {round(self.eff(),2)*100}%**')
		st.success(f'**VOLUME: {round(self.volume(),2)} m3**')
		st.success(f'**PURGE FLOW: {round(self.qp(),2)} m3/d**')
		st.success(f'**RECYCLE FLOW: {round(self.qr(),2)} m3/d**')
		st.success(f'**TOTAL SLUDGE: {round(self.pxss(),2)} kg/d **')

		st.markdown("### ----------------------------------------------------------------")

