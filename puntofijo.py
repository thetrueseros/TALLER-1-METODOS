import numpy as np 
import os
import sympy as sp 
from sympy.parsing.sympy_parser import parse_expr as pexpr, standard_transformations as strans, implicit_multiplication_application as ima
from tabulate import tabulate as t

def EjecutarPuntoFijo():
    x = sp.Symbol('x')
    
    LimpiarConsola()
    funcion = input("Ingrese la función g(x). \n\n"
                    "OPERADORES: \n"
                    "suma: +                     resta: -\n"
                    "multipl.: *                 división: /\n"
                    "potencia: **                raiz cuad.: sqrt()\n"
                    "trig: sin(), cos(), tan()   log. nat.: log()\n"
                    "exponencial: exp()\n"
                    "Ejemplo de función: 2x**3+5x+8. Notese cómo no hay necesidad de poner asterisco al multiplicar 2x y 5x.\n\n"
                    "Consideraciones: No olvide usar paréntesis.\n"
                    "Si necesita modificar algo, debe borrar.\n"
                    "g(x) = ")
    try:
        # traductor de multiplicaciones implícitas
        transformaciones=strans + (ima,)
        # convertir (parse)
        expresion = pexpr(funcion, transformations=transformaciones)
        # Convertir a función evaluable
        g=sp.lambdify(x, expresion, 'numpy')
    except Exception as e:
        print("Error: la expresión ingresada no es válida. ", e)
        input("Presione enter para volver.")
        return
    
    # pedir intervalo
    a = PedirNumero("Ingrese el límite inferior (a): ")
    b = PedirNumero("Ingrese el límite superior (b): ")
    p0 = PedirNumero("Ingrese el valor inicial (P0): ")
    tol = input("Ingrese la tolerancia (por defecto 0.00000001; enter para asignarla. Escriba otra si no desea esta.): ")
    tol = ValidacionVariable(tol.strip())

    #máximo de |g'x| en intervalo probando varios puntos
    #(aprox numerica del máximo en consola)

    puntos=[a +(b-a)*i/100 for i in range(101)]

    #criterio de automapeo
    valores_g = [g(p) for p in puntos]
    g_min, g_max = min(valores_g), max(valores_g)
    if not (a<=g_min<=b) or not (a<=g_max<=b):
        print(f"Alerta: g(x) NO se automapea en [{a}, {b}]. Rango de g(x): [{g_min:.4f}, {g_max:.4f}")
    
    #hallar constante de contracción K usando g'(x)

    g_derivada_simb = sp.diff(expresion, x)
    g_derivada = sp.lambdify(x, g_derivada_simb, 'numpy')

    try:
        valores_derivada = [abs(g_derivada(p)) for p in puntos]
        k = max(valores_derivada)
    except Exception:
        print(f"Error al evaluar la derivada en el intervalo.")
        return
    
    print(f"\n Constante de contracción estimada k = {k:.6f}")

    if k>=1:
        print("El criterio |g'x| < k < 1 NO se cumple. El método puede divergir")
        return
    else: 
        print("Se cumple |g'x| < 1. El punto fijo es ÚNICO y el método converge.")

    #calc 'n' teorico (iteraciones necesarias)
    # n>=log(((1-k)*tol)/|P0-g(P0)|)/log(k)

    gp0 = g(p0)
    diferencia = abs(p0 - gp0)

    # Evitar división por cero si P0 ya es el punto fijo
    if diferencia < tol:
        print("El valor inicial P0 ya es el punto fijo o cumple la tolerancia.")
        n_teorico = 1
    else:
        # Argumento exacto de la fórmula matemática: (tol * (1 - k)) / |P0 - g(P0)|
        arg_log = (tol * (1 - k)) / diferencia
        
        # Validar indeterminación de logaritmo
        if arg_log <= 0:
            n_teorico = 1
        else:
            val_n = np.log(arg_log) / np.log(k)
            # Manejar infinito o NaN por errores flotantes
            if np.isinf(val_n) or np.isnan(val_n):
                n_teorico = 50
            else:
                n_teorico = int(np.ceil(val_n))

        print(f" ---> Según el criterio de tolerancia, se necesitan mínimo {n_teorico} iteraciones.")
    #ejecutar el método hasta cumplir la tolerancia o alcanzar n teorico de seguridad
    max_iter = max(n_teorico, 50)

    # iterar y guardar en lista
    tablaDatos=[]
    error= 100
    i=1


    while error>=tol and i<=max_iter:
        p1 = g(p0)
        error= abs(p1-p0)

        tablaDatos.append([i, p0, p1, error])

        p0 = p1
        i+=1

    encabezados=["Iter (n)", "P_n-1", "P_n = g(P_n-1)", "Error Absoluto"]
    print("TABLA DE ITERACIONES")
    print(t(tablaDatos,headers=encabezados, tablefmt="fancy_grid", floatfmt=".8f"))
    input("Presione enter para volver al menú principal.")

def LimpiarConsola():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

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

def ValidacionVariable(variable):
    # si variable está vacío
    if not variable:
        print("Se asignó la tolerancia en 0.00000001")
        return 0.00000001

    # si variable no es un número
    try:
        return float(variable)
    except ValueError:
        print("Valor inválido. Se asignó la tolerancia por defecto 0.00000001")
        return 0.00000001