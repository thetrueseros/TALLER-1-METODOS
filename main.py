import biseccion as b 
import puntofijo as pf 
import newton as n
def Ejecutar():
    print("------ --- -- -- - MENÚ DE OPCIONES - -- -- --- ------")
    print("Bienvenido. Por favor, seleccione una de las opciones a continuación.")
    entrada = input("1. Método de la bisección\n"
                    "2. Método del punto fijo\n"
                    "3. Método de Newton\n"
                    "4. Salir.\n")
    entrada.strip()

    # Si el input no es un número del 1 al 3
    if not entrada.isdigit() or int(entrada) < 1 or int(entrada) > 4:
        input("Entrada inválida. Presione enter para regresar.")
        Ejecutar()
        return
    
    # Ejecutar bisección
    if int(entrada) == 1:
        b.EjecutarBiseccion()
    
    # Ejecutar punto fijo
    if int(entrada) == 2:
        pf.EjecutarPuntoFijo()
    
    # Ejecutar Newton
    if int(entrada) == 3:
        n.EjecutarNewton()
    
    # Ejecutar salir
    if int(entrada) == 4:
        entradacerrar = input("¿Está seguro que desea salir? [si/no]")
        entradacerrar = entradacerrar.lower
        if entradacerrar == "si":
            input("Presione enter para cerrar.")
            exit
        if entradacerrar== "no":
            input("Presione enter para regresar.")
            Ejecutar()
            return


if __name__ == "__main__":
    Ejecutar()