from functions import *

import math
import random

#Script principal - Recocido simulado para la simulación de microarquitecturas de procesadores
#Camilo Alvarez Muñoz
#Daniel Cano Restrepo

# Función objetivo que queremos minimizar (ajustar según el problema)
def funcion_objetivo(estado):
    eval_state(estado)
    return save_new_data(estado)

# Función para generar un nuevo punto a partir del actual (ajustar según el problema)
def generar_nuevo_punto(estado,n=5):
    estado_viejo=estado
    while(True):
        # Seleccionar un índice aleatorio de la lista
        indice = random.randint(0, len(estado) - 1)
        # Decidir si sumar o restar uno con igual probabilidad
        operacion = random.choice([-1, 1])
        # Aplicar la operación al valor del índice
        if (estado[indice]==0):
            estado[indice] +=1
        elif (estado[indice]==2):
            estado[indice] -=1
        else:
            estado[indice] += operacion
        
        # Verificar si se repite la operación sobre el mismo índice
        if random.random() >= 0.3:
            return estado
    if estado_viejo == estado:
        return generar_nuevo_punto(estado,n=5)

# Parámetros del recocido simulado
def recocido_simulado(funcion_objetivo, generar_nuevo_punto, temperatura_inicial, factor_enfriamiento, iteraciones):
    # Punto inicial (ajustar según el problema)
    x_actual = lista_aleatoria(8)
    mejor_x = x_actual
    print("\n\n\n\n\n","estado: ",x_actual,"\n\n\n\n\n")
    mejor_valor = funcion_objetivo(x_actual)
    valor_actual = mejor_valor
    
    temperatura = temperatura_inicial
    
    for i in range(iteraciones):
        # Generar un nuevo punto y calcular su valor
        nuevo_x = generar_nuevo_punto(x_actual)
        print("\n\n\n\n\n","estado: ",x_actual,"\n\n\n\n\n")
        nuevo_valor = funcion_objetivo(nuevo_x)
        
        # Calcula la diferencia de energía
        delta = (nuevo_valor - valor_actual)*10000
        
        # Si el nuevo valor es mejor, aceptamos el cambio
        # O si es peor, lo aceptamos con una probabilidad que depende de la temperatura
        print("\n\n\n\n\n","probabilidad de cambio: ",math.exp(-delta / temperatura),"\n\n\n\n\n")
        if delta < 0 or random.random() < math.exp(-delta / temperatura):
            x_actual = nuevo_x
            valor_actual = nuevo_valor
            
            # Actualizar el mejor valor encontrado
            if nuevo_valor < mejor_valor:
                mejor_x = nuevo_x
                mejor_valor = nuevo_valor
        
        # Enfriar la temperatura
        temperatura *= factor_enfriamiento
    
    return mejor_x, mejor_valor

# Ajuste de los parámetros
probabilidad_cambio = 0.9  # Probabilidad inicial del 90%
delta_inicial = 0.1*10000  # Cambio inicial en la función objetivo
temperatura_inicial = -delta_inicial / math.log(probabilidad_cambio)  # Ajusta la temperatura para un 90% de probabilidad
print(temperatura_inicial)
factor_enfriamiento = 0.9  # Ajusta la velocidad de enfriamiento
iteraciones = 50  # Ajustar el número de iteraciones según las microarquitecturas a analizar

# Ejecutar el recocido simulado
mejor_x, mejor_valor = recocido_simulado(funcion_objetivo, generar_nuevo_punto, temperatura_inicial, factor_enfriamiento, iteraciones)

# Imprimir los mejores parametros de microarquitectura encontrados en el DSE
print(f"Mejor solución encontrada: x = {mejor_x}, valor = {mejor_valor}")
