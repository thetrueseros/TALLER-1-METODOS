import numpy as np 
import os
import sympy as sp 
from tabulate import tabulate as t

def EjecutarBiseccion():


    x = sp.Symbol('x')
    
    LimpiarConsola()
    funcion = input("Ingrese la función f(x) a la que desea encontrar su punto P. \n\n"
                    "OPERADORES: \n"
                    "suma: +                     resta: -\n"
                    "multipl.: *                 división: /\n"
                    "potencia: **                raiz cuad.: sqrt()\n"
                    "trig: sin(), cos(), tan()   log. nat.: log()\n"
                    "exponencial: exp()\n\n"
                    "Consideraciones: No olvide usar paréntesis y, en especial, utilice " 
                    "el símbolo de multiplicación para escribir cosas como 3x, 2x⁵, etc. (ejemplo: 3*x, 2*x**5). "
                    "Si necesita modificar algo, debe borrar.\n"
                    "f(x) = ")
    
    try:
        # convertir texto a expresión de sympy
        expresion = sp.sympify(funcion)
        # Convertir a función evaluable
        f=sp.lambdify(x, expresion, 'numpy')
    except Exception as e:
        print("Error: la expresión ingresada no es válida. ", e)
        return

    # datos del usuario

    a = PedirNumero("Ingrese el límite inferior (a): ")
    b = PedirNumero("Ingrese el límite superior (b): ")

    tol = input("Ingrese la tolerancia (por defecto 0.00000001; enter para asignarla. Escriba otra si no desea esta.): ")
    tol = ValidacionVariable(tol.strip(), "tol", float)

    max_iter = input("Ingrese el número de iteraciones máximas a ejecutar (por defecto 100; enter para asignarla. Escriba otra cantidad si no desea esta.): ")
    max_iter = ValidacionVariable(max_iter.strip(), "max_iter", int)

    # validación teorema del bolzano
    if f(a)*f(b)>=0:
        print(f"\nERROR: La función no cambia de signo en el intervalo  [{a},{b}].")
        print(f"f(a) = {f(a):.4f} | f(b) = {f(b):.4f}")
        print(f"El método de la bisección no puede garantizar una raíz.")
        return
    tablaDatos = []
    i = 1
    error = b - a

    while error>tol and i<=max_iter:
        p=(a+b)/2
        fp=f(p)

        #guardar fila en lista
        tablaDatos.append([i,a,b,p,fp,error])

        if f(a)*f(p)<0:
            b=p
        else:
            a=p
        
        error = (b-a)/2
        i+=1

    encabezados=["Iter.", "a", "b", "p (Raíz)", "f(p)", "Error"]

    print("\n\nTABLA DE ITERACIONES GENERADA:")
    print(t(tablaDatos, headers=encabezados, tablefmt="fancy_grid", floatfmt=".8f"))
    input(f"Proceso terminado. Raíz aproximada encontrada en x = {p:.8f}\n\n"
    "Presione enter para volver al menú")
    return

def LimpiarConsola():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def ValidacionVariable(variable, nombre, tipo):
    # si variable está vacío
    if variable is None or variable == "":
        if nombre=="max_iter":
            variable=100
            print("Se asignó las iteraciones máximas = 100")
        if nombre=="tol":
            variable = 0.00000001
            print("Se asignó la tolerancia 0.00000001")

    # si variable no es un número
    while not isinstance(variable, tipo):
        if nombre=="max_iter":
            variable = input("Ingresó algo diferente a un número entero. Intente nuevamente o deje el campo vacío para asignarle 100.: ")
            variable = int(variable.strip())
            if variable is None or variable == "":
                variable = 100
                print("Se asignó las iteraciones máximas = 100")

        if nombre=="tol":
            variable = input("Ingresó algo diferente a un número decimal. Intente nuevamente o deje el campo vacío para asignarle 0.00000001.: ")
            variable = float(variable.strip())
            if variable is None or variable == "":
                variable = 0.00000001
                print("Se asignó la tolerancia 0.00000001")
    return variable

def PedirNumero(mensaje):
    while True:
        entrada = input(mensaje).strip()
        if not entrada:
            print("No ingresó ningún caracter. Intente nuevamente.") 
            continue
        try:
            return float(entrada)
        except ValueError:
            print("Ingresó un caracter inválido. Ingrese solo caracteres de tipo entero o decimal.")
            