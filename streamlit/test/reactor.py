import pandas as pd
import streamlit as st
#import plotly.express as px

####### MAIN CLASS

class Reactor():

############################################################# INITIALIZER ########################################
	
	def __init__(self,starting_dbo,final_dbo,Q):
		self.__name = 'Reactor'
		self.__dbo0 = starting_dbo
		self.__dbof = final_dbo
		self.__flow = Q

		############## NOT INITIALIZED VARIABLES

		#self.watertype
		#self.y
		#self.ks
		#self.umax
		#self.x
		#self.kd
		#self.xp
		#self.k
		#self.sssvsstratio

		############### BIBLIOGRAPHY

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

####################### GETTERS
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
	def watertype(self):
		return self.__watertype

	@property
	def y(self):
		return self.__y

	@property
	def ks(self):
		return self.__ks

	@property
	def umax(self):
		return self.__umax

	@property
	def x(self):
		return self.__x

	@property
	def kd(self):
		return self.__kd

	@property
	def xp(self):
		return self.__xp

	@property
	def k(self):
		return self.__k

	@property
	def sssvsstratio(self):
		return self.__sssvsstratio

############################### SETTERS
	
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

	@watertype.setter
	def watertype(self, var):
		self.__watertype = var

	@y.setter
	def y(self, var):
		self.__y = var

	@ks.setter
	def ks(self, var):
		self.__ks = var

	@umax.setter
	def umax(self, var):
		self.__umax = var

	@x.setter
	def x(self, var):
		self.__x = var

	@kd.setter
	def kd(self, var):
		self.__kd = var

	@xp.setter
	def xp(self, var):
		self.__xp = var

	@k.setter
	def k(self, var):
		self.__k = var

	@sssvsstratio.setter
	def sssvsstratio(self, var):
		self.__sssvsstratio = var

	################################################################### METHODS ##################################

	################################## EFFICIENCY

	def eff(self):
		return ((self.dbo0 -self.dbof)/self.dbo0)

	################################ WATERTYPE

	def wvars(self):
		var = st.selectbox("Enter please your watertype", ('Sewage','Industrial'),key = "2")
		self.watertype = var
		
	############################### VOLUME

	def yvars(self, biblio):
		y= st.number_input('Enter please your Y (relación masa celular formada/sustrato consumido)', value= 0.6)
		if biblio == 'yes':
			st.write(self.commonvals.loc['Y',:])     
		st.write(f"{y} mgSSV/mgDBO5")   
		self.y = y

	def ksvars(self, biblio):
		ks= st.number_input('Enter please your ks (constante de sustrato)', value= 60.0)
		if biblio == 'yes':
			st.write(self.commonvals.loc['ks',:])     
		st.write(f"{ks} mgDBO5/L")   
		self.ks = ks

	def umaxvars(self, biblio):
		umax= st.number_input('Enter please your umax (tasa de crecimiento específico máximo)', value= 0.5)
		if biblio == 'yes':
			st.write(self.commonvals.loc['umax',:])     
		st.write(f"{umax} 1/d")   
		self.umax = umax

	def xvars(self, biblio):
		x= st.number_input('Enter please your X (biomasa en el reactor)', value = 3000.0)
		if biblio == 'yes':
			st.write(self.commonvals.loc['X',:])     
		st.write(f"{x} mgSSV/L")   
		self.x = x

	def volume(self):
		upper = self.y * (self.dbo0-self.dbof) * self.flow * (self.ks + self.dbof)
		lower = self.umax * self.dbof * self.x
		vol = upper/lower
		return vol

	#################################### FLOW

	def kdvars(self, biblio):
		kd= st.number_input('Enter please your kd (constante de decaimiento)', value = 0.06)
		if biblio == 'yes':
			st.write(self.commonvals.loc['kd',:])     
		st.write(f"{kd} 1/d")   
		self.kd = kd

	def xpvars(self, biblio):
		xp= st.number_input('Enter please your Xp (concentración de purga)', value = 8000)
		if biblio == 'yes':
			st.write(self.commonvals.loc['xp',:])     
		st.write(f"{xp} mgSSV/L")   
		self.xp = xp

	def kvars(self, biblio):
		k= st.number_input('Enter please your k (tasa máxima de utilización de sustrato por unidad de masa de microorganismos)', value = 5)
		if biblio == 'yes':
			st.write(self.commonvals.loc['k',:])     
		st.write(f"{k} 1/d")   
		self.k = k

	def qp(self):
		return (((self.umax*self.x*self.dbof)/(self.dbof+self.ks))-(self.x*self.kd))*(self.volume()/self.xp)

	def qr(self):
		return ((self.flow*self.x-self.qp()*self.xp)/(self.xp-self.x))

	######################################### SLUDGE PURGE

	############### RATIO BETWEEN SSSV AND SST

	def sssvsstratio(self):
	    sssvsstratio = st.number_input('Enter please your sssv/sst ratio (relación entre sssv y sst)', value= 0.8) 
	    st.write(f"{sssvsstratio}")   
	    self.sssvsstratio = sssvsstratio

	########### CALCULATE OBSERVED "Y"

	def yobs(self):
		yobs = self.y/(1+self.kd+self.theta())
		return yobs

	########## CALCULATE VOLATILE ACTIVATED SLUDGE MASS

	def px(self):
		px = self.yobs()*self.flow*(self.dbo0-self.dbof)/1000
		return px

	########## CALCULATE TOTAL SLUDGE MASS, BASED ON TOTAL SUSPENDED SOLIDS

	def pxss(self):
		pxss = self.px()/self.sssvsstratio
		return pxss


	############################################# VALIDATIONS

	def tr(self):
		return self.volume()/self.flow

	def fm(self):
		return (self.flow*self.dbo0)/(self.volume()*self.x)

	def cv(self):
		return (self.flow*self.dbof*0.0013)/self.volume()

	def theta(self):
		return (self.volume()*self.x)/(self.qp()*self.xp)

	def u(self):
		return (self.dbof*self.k)/(self.ks+self.dbof)

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

##################################################################### CORE #################################################

########################################## WARNINGS

	def warnings(self):
		st.markdown("### Warnings")
		self.wvolumen()
		self.weff()

	def wvolumen(self):
		if self.volume() <= 100:
			st.warning('You may have to consider a radial shape for your reactor, since your volume is smaller than 100 cubic meters')

	def weff(self):
		if self.eff() < 1 and self.eff() > 0 :
			if self.eff() > 0.98:
				st.warning(f"""Your efficiency of {round(self.eff(),2)*100} is maybe too optimist. \nPlease consider designing a train of reactors or improving the preceding treatment.""")

	###################################### CALCULATE

	def calculate(self, biblio):
		self.wvars()
		self.yvars(biblio)
		self.ksvars(biblio)
		self.umaxvars(biblio)
		self.xvars(biblio)
		self.kdvars(biblio)
		self.xpvars(biblio)
		self.kvars(biblio)
		self.sssvsstratio()

	#################################### VALIDATION

	def validate(self):
		st.markdown("### Validations")

		self.tr_val()
		self.fm_val()
		self.cv_val()
		self.theta_val()
		self.u_val()

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

	#################################### EXECUTE UNIT

	def execute(self,biblio):
		self.calculate(biblio)
		self.validate()
		self.results()
		self.warnings()

