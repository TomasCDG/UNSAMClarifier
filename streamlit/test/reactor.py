import pandas as pd
import streamlit as st
#import plotly.express as px

#st.set_page_config(
           # page_title="Reactor", # => Quick reference - Streamlit
            #page_icon=":droplet:",
            ##layout="centered", # wide
            #initial_sidebar_state="auto") # collapsed

####### MAIN CLASS

class Reactor():

###### INITIALIZER

	def __init__(self,starting_dbo,final_dbo,Q):
		self.dbo0 = starting_dbo
		self.dbof = final_dbo
		self.flow = Q
		self.eff = ((starting_dbo-final_dbo)/starting_dbo)

		##### not initialized variables

		#self.watertype
		#self.y
		#self.ks
		#self.umax
		#self.x
		#self.kd
		#self.xp
		#self.k
		#self.sssvsstratio

		##### bibliografia

		self.lista= {'Y' : [0.4,0.8,0.6,'mgSSV/mgDBO5'],
		'ks' : [25,100,60,'mgDBO5/L'],
		'umax' : ['not available', 'not available', 0.5, '1/d'],
		'X' : ['not available', 'not available', 3000, 'mgSSV/L'],
		'kd' : [0.04,0.075,0.06,'1/d'],
		'xp' : ['not available yet','not available yet',8000,'mgSSV/L'],
		'k' : [2,10,5,'1/d']
		}
		self.commonvals = pd.DataFrame(self.lista,)
		self.commonvals = self.commonvals.transpose()
		self.commonvals.columns = ['lower limit','higher limit','typical','unit']

###### GETTERS

	def get_dbo0(self):
		return self._dbo0

	def get_dbof(self):
		return self._dbof

	def get_flow(self):
		return self._flow

	def get_eff(self):
		return self._eff

	def get_watertype(self):
		return self._watertype

	def get_y(self):
		return self._y

	def get_ks(self):
		return self._ks

	def get_umax(self):
		return self._umax

	def get_x(self):
		return self._x

	def get_kd(self):
		return self._kd

	def get_xp(self):
		return self._xp

	def get_k(self):
		return self._k

	def get_sssvsstratio(self):
		return self._sssvsstratio

####### SETTERS
	
	def set_dbo0(self, var):
		self._dbo0 = var

	def set_dbof(self, var):
		self._dbof = var

	def set_flow(self, var):
		self._flow = var

	def set_eff(self, var):
		self._eff = var

	def set_watertype(self, var):
		self._watertype = var

	def set_y(self, var):
		self._y = var

	def set_ks(self, var):
		self._ks = var

	def set_umax(self, var):
		self._umax = var

	def set_x(self, var):
		self._x = var

	def set_kd(self, var):
		self._kd = var

	def set_xp(self, var):
		self._xp = var

	def set_k(self, var):
		self._k = var

	def set_sssvsstratio(self, var):
		self._sssvsstratio = var

	##### PROPERTIES

	dbo0 = property(get_dbo0, set_dbo0)
	dbof = property(get_dbof, set_dbof)
	flow = property(get_flow, set_flow)
	eff = property(get_eff, set_eff)
	watertype = property(get_watertype, set_watertype)
	y = property(get_y, set_y)
	ks = property(get_ks, set_ks)
	umax = property(get_umax, set_umax)
	x = property(get_x, set_x)
	kd = property(get_kd, set_kd)
	xp = property(get_xp, set_xp)
	k = property(get_k, set_k)
	sssvsstratio = property(get_sssvsstratio, set_sssvsstratio)

	##### METHODS

	############# VOLUME

	def setvolvars(self, biblio):
		self.yvars(biblio)
		self.ksvars(biblio)
		self.umaxvars(biblio)
		self.xvars(biblio)

	def yvars(self, biblio):
		y= st.number_input('Enter please your Y (relación masa celular formada/sustrato consumido)', value= 0.6)
		if biblio == 'yes':
			st.write(self.commonvals.loc['Y',:])     
		st.write(f"{y} mgSSV/mgDBO5")   
		self.set_y(y)

	def ksvars(self, biblio):
		ks= st.number_input('Enter please your ks (constante de sustrato)', value= 60.0)
		if biblio == 'yes':
			st.write(self.commonvals.loc['ks',:])     
		st.write(f"{ks} mgDBO5/L")   
		self.set_ks(ks)

	def umaxvars(self, biblio):
		umax= st.number_input('Enter please your umax (tasa de crecimiento específico máximo)', value= 0.5)
		if biblio == 'yes':
			st.write(self.commonvals.loc['umax',:])     
		st.write(f"{umax} 1/d")   
		self.set_umax(umax)

	def xvars(self, biblio):
		x= st.number_input('Enter please your X (biomasa en el reactor)', value = 3000.0)
		if biblio == 'yes':
			st.write(self.commonvals.loc['X',:])     
		st.write(f"{x} mgSSV/L")   
		self.set_x(x)

	def volume(self):
		upper = self.get_y() * (self.get_dbo0()-self.get_dbof()) * self.get_flow() * (self.get_ks() + self.get_dbof())
		lower = self.get_umax() * self.get_dbof() * self.get_x()
		vol = upper/lower
		if vol <= 100:
			st.warning('You may have to consider a radial shape for your reactor, since your volume is smaller than 100 cubic meters')
		return vol

	########### FLOW METHODS

	def kdvars(self, biblio):
		kd= st.number_input('Enter please your kd (constante de decaimiento)', value = 0.06)
		if biblio == 'yes':
			st.write(self.commonvals.loc['kd',:])     
		st.write(f"{kd} 1/d")   
		self.set_kd(kd)

	def xpvars(self, biblio):
		xp= st.number_input('Enter please your Xp (concentración de purga)', value = 8000)
		if biblio == 'yes':
			st.write(self.commonvals.loc['xp',:])     
		st.write(f"{xp} mgSSV/L")   
		self.set_xp(xp)

	def kvars(self, biblio):
		k= st.number_input('Enter please your k (tasa máxima de utilización de sustrato por unidad de masa de microorganismos)', value = 5)
		if biblio == 'yes':
			st.write(self.commonvals.loc['k',:])     
		st.write(f"{k} 1/d")   
		self.set_k(k)

	def qp(self):
		return (((self.get_umax()*self.get_x()*self.get_dbof())/(self.get_dbof()+self.get_ks()))-(self.get_x()*self.get_kd()))*(self.volume()/self.get_xp())

	def qr(self):
		return ((self.get_flow()*self.get_x()-self.qp()*self.get_xp())/(self.get_xp()-self.get_x()))

	###### VALIDATIONS

	def tr(self):
		return self.volume()/self.get_flow()

	def fm(self):
		return (self.get_flow()*self.get_dbo0())/(self.volume()*self.get_x())

	def cv(self):
		return (self.get_flow()*self.get_dbof()*0.0013)/self.volume()

	def theta(self):
		return (self.volume()*self.get_x())/(self.qp()*self.get_xp())

	def u(self):
		return (self.get_dbof()*self.get_k())/(self.get_ks()+self.get_dbof())


	def validate(self):
		self.tr_val()
		self.fm_val()
		self.cv_val()
		self.theta_val()
		self.u_val()

	def tr_val(self):
		if self.tr() < 0.125 or self.tr() > 0.2083:
			st.warning(f"**HYDRAULIC RESIDENCE TIME: {round(self.tr(),2)}.** *Should be between 0.125 and 0.2083 days (3 and 5 hours)*")
		else:
			st.success(f"**HYDRAULIC RESIDENCE TIME: {round(self.tr(),2)}.** *Should be between 0.125 and 0.2083 days (3 and 5 hours)*")

	def fm_val(self):
		if self.fm() < 0.2 or self.fm() > 0.6:
			st.warning(f"**MICROORGANISM - FOOD RELATION: {round(self.fm(),2)}.** *Should be between 0.2 and 0.6 1/d*")
		else:
			st.success(f"**MICROORGANISM - FOOD RELATION: {round(self.fm(),2)}.** *Should be between 0.2 and 0.6 1/d*")

	def cv_val(self):
		if self.cv() < 0.8 or self.cv() > 1.92:
			st.warning(f"**VOLUMETRIC LOAD: {round(self.cv(),2)}.** *Should be between 0.8 and 1.92 kgDBO5/m3*")
		else:
			st.success(f"**VOLUMETRIC LOAD: {round(self.cv(),2)}.** *Should be between 0.8 and 1.92 kgDBO5/m3*")
		return self.cv()

	def theta_val(self):
		if self.theta() < 5 or self.theta() > 15:
			st.warning(f"**CELULAR RESIDENCE TIME: {round(self.theta(),2)}.** *Should be between 5 and 15 days*")
		else:
			st.success(f"**CELULAR RESIDENCE TIME: {round(self.theta(),2)}.** *Should be between 5 and 15 days*")

	def u_val(self):
		if self.u() < 0.2 or self.u() > 0.6:
			st.warning(f"**RATE OF SUBSTRATE UTILIZATION: {round(self.u(),2)}.** *Should be between 0.2 and 0.6 kgDBO5/kgSSVLMd*")
		else:
			st.success(f"**RATE OF SUBSTRATE UTILIZATIONv: {round(self.u(),2)}.** *Should be between 0.2 and 0.6 kgDBO5/kgSSVLMd*")

######### SLUDGE PURGE

###### RATIO BETWEEN SSSV AND SST

	def sssvsstratio(self):
	    sssvsstratio = st.number_input('Enter please your sssv/sst ratio (relación entre sssv y sst)', value= 0.8)
	    #if bibliography == 'yes':
	        #st.write(commonvals.loc['umax',:])     
	    st.write(f"{sssvsstratio}")   
	    self.set_sssvsstratio(sssvsstratio)

	###### CALCULATE OBSERVED "Y"

	def yobs(self):
		yobs = self.get_y()/(1+self.get_kd()+self.theta())
		return yobs

	###### CALCULATE VOLATILE ACTIVATED SLUDGE MASS

	def px(self):
		px = self.yobs()*self.get_flow()*(self.get_dbo0()-self.get_dbof())/1000
		return px

	###### CALCULATE TOTAL SLUDGE MASS, BASED ON TOTAL SUSPENDED SOLIDS

	def pxss(self):
		pxss = self.px()/self.get_sssvsstratio()
		return pxss

############################################################################################################################
############################################################################################################################
###########################                          FUNCTIONS                                      ########################

#def biblio():
	#if reactor.get_watertype() == 'Sewage':
		#bibliography = st.radio("Would you like to see the typical design values and ranges for typical sewage wastewater from now on?",
			#('yes','no'), index = 1)   

	#elif reactor.get_watertype() == 'Industrial':
		#bibliography = st.radio("Would you like to see some typical industrial values from bibliography?", ('yes','no'), index = 1)

	#return bibliography

############################################################################################################################
############################################################################################################################
############################################PANDAS PRE-LOADING

#lista= {'Y' : [0.4,0.8,0.6,'mgSSV/mgDBO5'],
       # 'ks' : [25,100,60,'mgDBO5/L'],
        #'umax' : ['not available', 'not available', 0.5, '1/d'],
       # 'X' : ['not available', 'not available', 3000, 'mgSSV/L'],
       # 'kd' : [0.04,0.075,0.06,'1/d'],
       # 'xp' : ['not available yet','not available yet',8000,'mgSSV/L'],
       # 'k' : [2,10,5,'1/d']
       #}
#commonvals = pd.DataFrame(lista,)
#commonvals = commonvals.transpose()
#commonvals.columns = ['lower limit','higher limit','typical','unit']

############################################################################################################################
############################################################################################################################
###########################                          SIDEBAR                                        ########################
    

#st.sidebar.markdown(f"""
   # # INITIAL VARIABLES
    #""")

########### INPUT VALUES
#st.sidebar.markdown('### Flowrate:')
#Qinput = st.sidebar.number_input('Insert your initial flowrate *(m3/d)*', value = 300.0*24, step = 10.0)
#Q_max = Qinput * 2
#Q = st.sidebar.slider('or fine-tune it:', 0.0, max_value = Q_max, value=  Qinput, key = '1')

#st.sidebar.markdown('### initial DBO5:')
#initial_dbo_input = st.sidebar.number_input('Insert your initial DBO5 *(mgDBO5/L)*', value = 300.0, step = 10.0)
#dbo_max = initial_dbo_input * 2
#initial_dbo = st.sidebar.slider('or fine-tune it:', 0.0, max_value = dbo_max, value = initial_dbo_input, key = '2')

#st.sidebar.markdown('### final DBO5:')
#final_dbo_input = st.sidebar.number_input('Insert your final DBO5 *(mgDBO5/L)*', min_value = 0.01, value = 30.0, step = 10.0)
#final_dbo_max = final_dbo_input * 2 
#final_dbo = st.sidebar.slider('or fine-tune it:', 0.01, max_value = final_dbo_max, value = final_dbo_input, key = '3')

############################################################################################################################
############################################################################################################################
###########################                          BODY OF PAGE                                   ########################


