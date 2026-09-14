# SOFTWARE DE CÁLCULO POR MÉTODOS NUMÉRICOS


### Método de Bisección
Ingresa:
- FA: Función f(x). Ejemplo: x**2-x-2
- tol: Tolerancia. Por defecto, 0.0000001
- max_iter: Número máximo de iteraciones para evitar que el programa se congele. Por defecto 100
- a: límite inferior
- b: límiete superior

Sale: 
- Tabla de información
- Raíz

### Método de Punto Fijo
Ingresa:
- GA: Función g(x). Ejemplo: 3*x**2+2x-4
- Po: Semilla inicial
- tol: tolerancia. Por defecto,0.0000001
- max_iter: número máximo de iteraciones para evitar que el programa se congele. Por defecto 100
- 

---

# Manual de Usuario: Sistema de Métodos Numéricos

Software interactivo desarrollado en Python para la resolución de ecuaciones no lineales mediante métodos numéricos iterativos.

---

## 1. Estructura y Módulos del Sistema

El programa está construido de forma modular. La arquitectura del código y el estado de sus componentes es el siguiente:

| Archivo | Módulo / Función Principal | Estado | Descripción de Responsabilidad |
| --- | --- | --- | --- |
| **`main.py`** | `Ejecutar()` | **Funcional** | Menú principal por consola. Gestiona la navegación entre métodos, la limpieza de consola y la salida del sistema. |
| **`biseccion.py`** | `EjecutarBiseccion()` | **Funcional** | Módulo para el método de Bisección. Valida el intervalo mediante el Teorema de Bolzano, calcula raíces y tabula iteraciones. |
| **`puntofijo.py`** | `EjecutarPuntoFijo()` | **Funcional** | Módulo para el método de Punto Fijo. Valida automapeo, estima la constante de contracción $k = \max\vert{}g'(x)\vert{}$, calcula iteraciones teóricas $n$ y tabula resultados. |
| **`newton.py`** | `EjecutarNewton()` | *En desarrollo* | Módulo stub que imprime el mensaje informativo `"wip newton"`. |

---

## 2. Instrucciones de Ejecución

Para ejecutar la aplicación directamente, abra el archivo [main.exe](dist/main.exe).

Si desea hacerlo de otra forma, siga estos pasos:
1. Abra una terminal en la carpeta raíz del proyecto.
2. Inicie la aplicación corriendo el menú principal:
```bash
python main.py

```


3. En el menú desplegado, ingrese el número correspondiente a la opción deseada:
* **`1`**: Método de la Bisección.
* **`2`**: Método del Punto Fijo.
* **`3`**: Método de Newton.
* **`4`**: Salir del programa (requiere confirmación `[si/no]`).



---

## 3. Guía de Operación de los Módulos Funcionales

### A. Sintaxis de Entrada para Funciones $f(x)$ y $g(x)$

Ambos módulos utilizan la librería `SymPy` configurada con **multiplicación implícita**, lo que permite escribir expresiones de forma natural (ejemplo: `2x**3+5x+8` en lugar de `2*x**3+5*x+8`).

* **Suma / Resta:** `+` / `-`
* **Multiplicación / División:** `*` / `/`
* **Potencia:** `**` (Ejemplo: `x**2`)
* **Raíz Cuadrada:** `sqrt()`
* **Trigonométricas:** `sin()`, `cos()`, `tan()`
* **Trascendentes:** `exp()` (Exponencial $e^x$), `log()` (Logaritmo natural)

---

### B. Módulo 1: Método de la Bisección (`biseccion.py`)

#### Entradas Solicitadas:

1. **Función $f(x)$:** Expresión matemática en texto a la que se le busca el punto $P$ tal que $f(P) = 0$.
2. **Límite inferior ($a$) y Límite superior ($b$):** Extremos del intervalo inicial.
3. **Tolerancia (`tol`):** Error permitido. *Presionar Enter asigna $0.00000001$ por defecto.*
4. **Iteraciones Máximas (`max_iter`):** Límite de ciclos. *Presionar Enter asigna $100$ por defecto.*

#### Validaciones Teóricas y Comportamiento:

* **Teorema de Bolzano:** Evalúa $f(a) \cdot f(b)$. Si $f(a) \cdot f(b) \ge 0$, el programa muestra una alerta indicando que no hay cambio de signo en el intervalo y cancela la ejecución para evitar falsos positivos.
* **Salida:** Imprime una tabla estructurada con las columnas: `Iter.`, `a`, `b`, `p (Raíz)`, `f(p)` y `Error`.

---

### C. Módulo 2: Método del Punto Fijo (`puntofijo.py`)

#### Entradas Solicitadas:

1. **Función $g(x)$:** Expresión despejada de la forma $x = g(x)$.
2. **Límite inferior ($a$) y Límite superior ($b$):** Intervalo de análisis.
3. **Valor inicial ($P_0$):** Punto de partida numérico para la iteración.
4. **Tolerancia (`tol`):** Criterio de parada por error absoluto. *Presionar Enter asigna $0.00000001$ por defecto.*

#### Validaciones Teóricas y Comportamiento:

1. **Criterio de Automapeo:** Muestra una alerta si el rango de $g(x)$ en $[a, b]$ se sale del intervalo.
2. **Constante de Contracción ($k$):**
* Deriva simbólicamente $g'(x)$ con `SymPy` y evalúa $\vert{}g'(x)\vert{}$ en 100 puntos dentro del intervalo para estimar $k = \max \vert{}g'(x)\vert{}$.
* Si $k \ge 1$, advierte que el criterio no se cumple y detiene la ejecución porque el método puede divergir.
* Si $k < 1$, confirma la convergencia hacia un único punto fijo.


3. **Cálculo de Iteraciones Teóricas ($n$):**
* Aplica la fórmula cota $n \ge \frac{\ln\left(\frac{tol \cdot (1-k)}{\vert{}P_0 - g(P_0)\vert{}}\right)}{\ln(k)}$ para calcular y mostrar el número mínimo de iteraciones garantizadas.


4. **Salida:** Muestra la tabla con las columnas: `Iter (n)`, `P_n-1`, `P_n = g(P_n-1)` y `Error Absoluto`.

## 4. Flujo del proyecto
flowchart TD
    Start([Inicio]) --> Menu[Mostrar Menú Principal: main.py]
    Menu --> Option{Seleccionar Opción}

    %% Opción 1: Bisección
    Option -- "1" --> Bis[Ejecutar Bisección: biseccion.py]
    Bis --> InBis[Ingresar f(x), a, b, tol, max_iter]
    InBis --> ChkBol{¿f(a) * f(b) < 0?}
    ChkBol -- No --> ErrBol[Error: No hay cambio de signo / Cancela]
    ErrBol --> Menu
    ChkBol -- Sí --> LoopBis[Bucle de Iteraciones: p = a+b/2]
    LoopBis --> TabBis[Generar Tabla con tabulate]
    TabBis --> Menu

    %% Opción 2: Punto Fijo
    Option -- "2" --> PF[Ejecutar Punto Fijo: puntofijo.py]
    PF --> InPF[Ingresar g(x), a, b, P0, tol]
    InPF --> ChkAuto{¿g(x) en a,b?}
    ChkAuto -- No --> WarnAuto[Alerta: No automapea]
    ChkAuto -- Sí --> CalcK[Calcular k = max|g'x| con SymPy]
    WarnAuto --> CalcK
    CalcK --> ChkK{¿k < 1?}
    ChkK -- No --> ErrK[Error: k >= 1 / Divergencia]
    ErrK --> Menu
    ChkK -- Sí --> CalcN[Calcular n teórico de iteraciones]
    CalcN --> LoopPF[Bucle de Iteraciones: Pn = g Pn-1]
    LoopPF --> TabPF[Generar Tabla de Iteraciones]
    TabPF --> Menu

    %% Opción 3: Newton
    Option -- "3" --> New[Ejecutar Newton: newton.py]
    New --> MsgWIP[Imprimir: wip newton]
    MsgWIP --> Menu

    %% Opción 4: Salir
    Option -- "4" --> Conf{¿Confirmar Salir?}
    Conf -- Sí --> End([Fin del Programa])
    Conf -- No --> Menu