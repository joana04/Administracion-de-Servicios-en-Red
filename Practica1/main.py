import rrdtool
from pysnmp.hlapi import *
from MonitorGeneral import *


def main():
	mg= MonitorGeneral()
	entra=1
	print("\t\t BIENVENIDOS\n")
	mg.verDisp(0)

	while entra==1:
		print("\nSeleccione la opcion deseada \n\t 1.- Ver dispositivos \n\t 2.- Agregar un agente \n\t 3.- Eliminar un agente \n\t 4.- Estado de dispositivo\n\t 3.- Eliminar un agente ")
		opc=int(input())
		if opc==1:
			mg.verDisp(1)
		elif opc==2:
			mg.agregarDisp()
		elif opc==3:
			mg.eliminarDisp()
		elif opc==4:
			mg.consulta()
		#elif opc==5:
		#	mg.minimosCuadrados()
			
		print ("desea regresar?\n 1.-Si \n 2.-No")
		entra=int(input())
	print ("\n\t ADIOS\n")

main()