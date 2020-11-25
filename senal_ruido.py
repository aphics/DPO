import numpy as np

def buscador(y):

    # -----------
    # Primer paso
    # -----------

    # Se calcula el promedio
    promedio = np.mean(y)

    # Se obtiene el maximo y su posicion
    maximo = max(y)
    # pos_max = y.index(maximo)
    pos_max = np.argmax(y)

    # Se crean los arreglos donde se almacena la senal y ruido. Primer paso
    senal_1_array = np.zeros_like(y)
    ruido_1_array = np.zeros_like(y)
    
    # Ciclo para diferenciar la senal del ruido. Primer paso

    # Condicion para saber si puede ser confiable la informacion
    if y[pos_max-1] > (0.75*promedio) and y[pos_max+1] > (0.75*promedio):
        pos = pos_max
        # Se busca hacia derecha a partir del maximo
        while pos <= len(y)-1:
            if y[pos] >= promedio:
                senal_1_array[pos] = y[pos]
            if y[pos] < promedio and y[pos-1] > y[pos] and senal_1_array[pos-1] > 0:
                senal_1_array[pos] = y[pos]
        pos += 1
        # Se busca hacia la izquierda a partir del maximo
        pos = pos_max

        while pos >= 0:
            if y[pos] >= promedio:
                senal_1_array[pos] = y[pos]
            if y[pos] < promedio and y[pos+1] > y[pos] and senal_1_array[pos+1] > 0:
                senal_1_array[pos] = y[pos]
        pos -= 1

    # Ciclo para crear el arreglo de ruido a partir del arreglo senal_1_array
    for i in range(len(senal_1_array)):
        if senal_1_array[i] == 0:
            ruido_1_array[i] = y[i]
        else:
            pass

    # Arreglos para almacenar unicamente la informacion de senal_1_array y ruido_1_array
    senal_1 = []
    ruido_1 = []
    # Ciclo para almacenar unicamente la informacion de senal_1_array y ruido_1_array
    for i in range(len(senal_1_array)):
        if senal_1_array[i] != 0:
            senal_1.append(senal_1_array[i])
        if ruido_1_array[i] != 0:
            ruido_1.append(ruido_1_array[i])

    # Calculo del continuo_1 y su desviacion estandar
    continuo_1 = np.mean(ruido_1)
    sigma_continuo_1 = np.sqrt( (1/(len(ruido_1)-1)) * np.sum( (ruido_1-np.mean(ruido_1))**2 ) )


    # -------------
    # Segundo paso
    # -------------

    # Se crean los arreglos donde se almacena la senal y ruido. Segundo paso
    senal_2_array = np.zeros_like(y)
    ruido_2_array = np.zeros_like(y)

    # Ciclo para separa senal_2 de ruido_2 a partir del valor del
    # valor del continuo_1 y la sigma del ruido_1
    # Se busca hacia la derecha a partir del maximo
    pos = pos_max
    while pos <= len(y)-1:
        if y[pos] >= continuo_1:
            senal_2_array[pos] = y[pos]
        if y[pos] < (continuo_1 + sigma_continuo_1):
            senal_2_array[pos] = y[pos]
            break
        if y[pos+1] > y[pos] and y[pos] <= (continuo_1 + (2*sigma_continuo_1)):
            senal_2_array[pos] = y[pos]
            break
        pos += 1
    
    # Se busca hacia la izquierda a partir del maximo
    pos = pos_max
    while pos >= 0:
        if y[pos] >= continuo_1:
            senal_2_array[pos] = y[pos]
        if y[pos] < (continuo_1 + sigma_continuo_1):
            senal_2_array[pos] = y[pos]
            break
        if y[pos-1] > y[pos] and y[pos] <= (continuo_1 + (2*sigma_continuo_1)):
            senal_2_array[pos] = y[pos]
            break
        pos -= 1
    
    # Ciclo para crear el arreglo de ruido_2_array a partir de senal_2_array
    for i in range(len(senal_2_array)):
        if senal_2_array[i] == 0 :
            ruido_2_array[i] = y[i]
        else:
            pass
    
    # Se crean arreglos para almacenar unicamente informacion de ruido_2_array y
    # ruido_2_array
    senal_2 = []
    ruido_2 = []

    # Ciclo para almacenar unicamente la informacion de senal_2_array y ruido_2_array
    for i in range(len(senal_2_array)):
        if senal_2_array[i] != 0:
            senal_2.append(senal_2_array[i])
        if ruido_2_array[i] != 0:
            ruido_2.append(ruido_2_array[i])

    # Calculo del continuo_2 a partir del ruido_2
    continuo_2 = np.mean(ruido_2)

    # Substraccion del continuo_2 a senal_2
    senal_2 = senal_2 - continuo_2
    
    # Promedio de senal_2
    senal = np.mean(senal_2)

    # Desviacion estandar de ruido_2
    sigma_ruido_2 = np.std(ruido_2, ddof =1)

    # Senal a ruido
    s_n = senal / sigma_ruido_2

    return senal_2_array, ruido_2_array, continuo_2, s_n