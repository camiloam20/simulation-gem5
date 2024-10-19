from functions import *

import math
import random

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
        elif (estado[indice]==4):
            estado[indice] -=1
        else:
            estado[indice] += operacion
        
        # Verificar si se repite la operación sobre el mismo índice
        if random.random() >= 0.3:
            return estado

# Parámetros del recocido simulado
def recocido_simulado(funcion_objetivo, generar_nuevo_punto, temperatura_inicial, factor_enfriamiento, iteraciones):
    # Punto inicial (ajustar según el problema)
    x_actual = random.uniform(-10, 10)
    mejor_x = x_actual
    mejor_valor = funcion_objetivo(x_actual)
    
    temperatura = temperatura_inicial
    
    for i in range(iteraciones):
        # Generar un nuevo punto y calcular su valor
        nuevo_x = generar_nuevo_punto(x_actual)
        valor_actual = funcion_objetivo(x_actual)
        nuevo_valor = funcion_objetivo(nuevo_x)
        
        # Calcula la diferencia de energía
        delta = nuevo_valor - valor_actual
        
        # Si el nuevo valor es mejor, aceptamos el cambio
        # O si es peor, lo aceptamos con una probabilidad que depende de la temperatura
        if delta < 0 or random.random() < math.exp(-delta / temperatura):
            x_actual = nuevo_x
            
            # Actualizar el mejor valor encontrado
            if nuevo_valor < mejor_valor:
                mejor_x = nuevo_x
                mejor_valor = nuevo_valor
        
        # Enfriar la temperatura
        temperatura *= factor_enfriamiento
    
    return mejor_x, mejor_valor

# Ajuste de los parámetros
probabilidad_cambio = 0.9  # Probabilidad inicial del 90%
delta_inicial = 1.0  # Supongamos un cambio inicial de 1.0 en la función objetivo
temperatura_inicial = -delta_inicial / math.log(probabilidad_cambio)  # Ajusta la temperatura para un 90% de probabilidad
factor_enfriamiento = 0.7  # Ajusta la velocidad de enfriamiento
iteraciones = 1000  # Ajusta el número de iteraciones

# Ejecutar el recocido simulado
mejor_x, mejor_valor = recocido_simulado(funcion_objetivo, generar_nuevo_punto, temperatura_inicial, factor_enfriamiento, iteraciones)

print(f"Mejor solución encontrada: x = {mejor_x}, valor = {mejor_valor}")