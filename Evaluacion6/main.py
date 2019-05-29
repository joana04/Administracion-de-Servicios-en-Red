import rrdtool
from e6 import *
from MonitorGeneral import *


def main():
	entra=1
	mg= MonitorGeneral()
	print("\t\t EVALUACION 6 \n")
	while entra==1:
		print("\nSeleccione la opcion deseada \n\t 1.- Agregar dispositivo \n\t 2.- Examinar dispositivos \n\t 3.- Examinar dispositivo  \n\t 4.- Enviar archivos a un dispositivo\n")
		opc=int(input())
		if opc==1:
			mg.agregarDisp()
		elif opc==2:
			mg.verDisp()
		elif opc==3:
			mg.verUnDisp()
		elif opc==4:
			mg.enviarArchivo()


		#elif opc==5:
		#	mg.minimosCuadrados()
			
		print ("desea regresar?\n 1.-Si \n 2.-No")
		entra=int(input())
	print ("\n\t ADIOS\n")

main()