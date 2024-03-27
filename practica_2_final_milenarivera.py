# -*- coding: utf-8 -*-
"""Practica_2_FINAL_MilenaRivera.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1s8YxgAjMVEal5BRYd1G-0PVbIlInpU62
"""

# Esta es la practica 2 de mi clase de Programacion. La practica consiste en
# el siguiente escenario: Una clínica del IMSS está evaluando las políticas de
# atención a usuarios, por lo que se tomó la decisión de simular el proceso de
# espera por medio de una simulación de colas. Los parámetros del sistema
# actual son los siguientes:

# (i) Se estima que el tiempo de interarribo de pacientes se encuentra entre
# los 0.5 minutos a los 50 minutos con probabilidad uniforme.
# (ii) Los pacientes se dividen en dos grupos: de urgencia y rutinarios. La
# probabilidad de que llegue un paciente de urgencia es de 20%.
# (iii) Se considera que el tiempo de atención por paciente es de 30 minutos
# (constante).
# (iv) La política de atención a los pacientes es la primera persona en llegar
# es la primera atendida.
# (v) Únicamente hay un consultorio con los doctores suficientes para operarlo
# las 24 horas del día.

import random
import numpy as np

########
class Personas:
  '''Esta clase crea a los pacientes, les asigna un tipo de acuerdo a su
  probabilidad y define el tiempo en el que llegan.'''

  #metodo1: generador de n personas
  def __init__(self,num_personas_generar):
    ''' Este generador crea el numero de personas que le introduzcas en el
    parametro 'num_personas_generar', define su tipo entre de urgencia y de
    rutina a partir de una probabilidad. Además, establece el tiempo en el que
    llegan a partir de una probabilidad uniforme. En una lista guarda a cada
    persona.'''

    self.lista_personas = []

    for i in range(num_personas_generar):
      # Generar un numero entre 0 y 1
      probabilidad_tipo_paciente = random.random()
      if probabilidad_tipo_paciente <= 0.2:
        self.tipo_paciente = 'urgencia'
      else:
        self.tipo_paciente = 'rutina'

      # Tiempo de llegada entre 0.5 y 50 minutos
      self.tiempo_llegada = self.uniforme(0.5, 50)
      self.lista_personas.append([self.tipo_paciente, self.tiempo_llegada])
    #print(self.lista_personas)

  #metodo2: probabilidad uniforme
  def uniforme (self, a, b):
    '''Este metodo garantiza que el tiempo de llegada generado al azar del
    paciente tenga probabilidad uniforme.'''

    u = (b - a) * np.random.random() + a
    return u

##########
class Cola:
  '''Esta clase gestiona la manera de 'formar' a cada persona creada al igual
   que para 'irse' de la fila.'''

 #metodo1 : (constructor de la cola)
  def __init__(self, prioridad = False):
    '''Este es el contructor de la fila. En caso de que exista prioridad entre
    pacientes de urgencia y rutinarios se debe establecer el parametro
    prioridad como True de lo contrario es por default False'''

    self.fila = [] #fila vacía
    self.atendiendo = False # Nos dice si hay alguien siendo atendido
    self.prioridad = prioridad #booleano

  #(maneras de formar)
  #metodo2:
  def hasta_adelante_de_x(self, persona):
    '''Este metodo permite hacer cierta distincion entre tipos de pacientes
    cuando se forman, los manda a la primera posicion de la fila pero si ya hay
    alguno de su tipo, no los adelanta a ellos.'''

    tipo, tiempo_llegada = persona

    agregue_algo = False #mi control de agregar personas a la fila
    for i in range(len(self.fila)):
      if self.fila[i][0] != 'urgencia' and not agregue_algo:
        self.fila.insert(i, persona)
        agregue_algo = True
    if not agregue_algo: #caso donde no hay ninguno de rutina
      self.fila.append(persona)

  #metodo3:
  def hasta_atras(self, persona):
    '''Este metodo no hace distincion alguna entre tipos de pacientes
    cuando se forman, los manda a la ultima posicion de la fila.'''
    self.fila.append(persona)

  #metodo4: (formar)
  def formar(self, persona):
    '''Este metodo 'forma' a las personas de acuerdo con la prioridad con la
    que se inicializo la Cola. Verifica que no haya nadie siendo atendido y
    registra los tiempos de llegada a la cola de cada persona.'''

    tipo, tiempo_llegada = persona

    if self.prioridad:
      #contemplo caso donde no habia nadie formado
      if not self.atendiendo :
        self.atendiendo = True
        self.hasta_atras(persona)
        #print(f'La persona de tipo {tipo} llegó en el minuto '
        #  f'{tiempo_llegada:.2f} fue atendida inmediatamente.')

      else: #caso donde ya hay alguien formado
        if tipo == 'urgencia':
          self.hasta_adelante_de_x(persona)
          #print(f'Persona de tipo {tipo} llegó en el minuto '
          #  f'{tiempo_llegada:.2f} y se formó en la cola.')


        else: # tipo 'rutinarios'
          self.hasta_atras(persona)
          #print(f'Persona de tipo {tipo} llegó en el minuto '
          #  f'{tiempo_llegada:.2f} y se formó en la cola.')

    else: #caso donde la prioridad = False
      if not self.atendiendo: #caso donde no habia nadie formado
        self.atendiendo = True
        self.hasta_atras(persona)
       # print(f'La persona de tipo {tipo} llegó en el minuto '
       #   f'{tiempo_llegada:.2f} fue atendida inmediatamente.')

      else: #caso donde ya hay alguien formado
        self.hasta_atras(persona)
        #print(f'La persona de tipo {tipo} llego en el minuto '
        #      f'{tiempo_llegada:.2f} se formo en la cola.')

  #metodo3: atender pacientes
  def atencion_pacientes(self):
    '''Este metodo gestiona la 'atencion' de los pacientes, los saca de la cola
    donde estaban formados.'''
    if self.fila:
      persona_atendida = self.fila.pop(0)

#######
class Simulacion:
  '''Esta clase crea una simulacion creando un reloj virtual que contabiliza
  los tiempos de los pacientes (cuanto tiempo pasa 'formado', tiempos de
  entrada y salida). '''

  def __init__(self):
    '''Este es el generador de la simulacion, inicializa el reloj global.'''
    self.reloj_global = 0 #Inicializar el reloj en 0 minutos

  def simular(self, num_personas_simular,tiempo_de_atencion, prioridad):
    '''Este es el metodo para simular el evento con las n personas
    (num_personas_simular). Ademas,calcula el tiempo promedio de espera de
    acuerdo a la constante de tiempo de atencion y la prioridad.'''

    self.personas = Personas(num_personas_simular)
    self.tiempo_de_atencion = tiempo_de_atencion
    self.cola = Cola(prioridad)
    self.tiempos_llegada = []
    self.tiempos_salida = [0 for i in range(num_personas_simular)]
    self.tiempos_espera = [0 for i in range(num_personas_simular)]

    #contadores auxiliares
    i = 0
    j = 0
    self.tiempo_en_sistema_urgencia = []
    self.tiempo_prom_espera_urgencia = []
    u=0
    self.tiempo_en_sistema_rutinario = []
    self.tiempo_prom_espera_rutinario = []
    r=0
    #me ayudara a llevar el registro de cuando se aplico la prioridad
    #entre pacientes
    self.se_cumplio = False

    if not prioridad: #si la prioridad no importa
      for tipo, tiempo_llegada in self.personas.lista_personas:
        persona = (tipo, tiempo_llegada)
        #formo a todos pero algunos los saco inmediatamente
        self.cola.formar(persona)
        self.reloj_global += tiempo_llegada
        self.tiempos_llegada.append(self.reloj_global)
        self.tiempos_salida[i] = max(self.tiempos_salida[i-1],
                                  self.reloj_global) + self.tiempo_de_atencion
        #checo si ya paso el tiempo necesario para que salga alguien
        if self.reloj_global >= self.tiempos_salida[j-1]:
          while self.cola.fila:
            self.cola.atencion_pacientes() #self.cola.atendiendo = True

        self.tiempos_espera[i] = (self.tiempos_salida[i-1] - self.reloj_global)
        #necesitamos ajustar porque no existen tiempos de espera negativos
        for k in range(len(self.tiempos_espera)):
          if self.tiempos_espera[k] <0:
            self.tiempos_espera[k]=0
          else:
            self.tiempos_espera[k]=self.tiempos_espera[k]
        i += 1
        j += 1

      tiempo_promedio_en_sistema = ((sum(self.tiempos_salida) -
                                     sum(self.tiempos_llegada))/
                                    num_personas_simular)
      print('Tiempo promedio en sistema:',tiempo_promedio_en_sistema, 'minutos')

    ########
    else: #si la prioridad si nos importa

      for tipo, tiempo_llegada in self.personas.lista_personas:
        persona = (tipo, tiempo_llegada)
        #formo a todos pero algunos los saco inmediatamente
        self.cola.formar(persona)
        self.reloj_global += tiempo_llegada
        self.tiempos_llegada.append(self.reloj_global)

        if (self.tiempos_llegada[i-1] <= self.tiempos_salida[i-2] and
        self.tiempos_llegada[i] <= self.tiempos_salida[i-2] and
        tipo == 'urgencia' and
        self.personas.lista_personas[i-1][0] != 'urgencia'):

          self.tiempos_salida[i] = max(self.tiempos_salida[i-2],
                                  self.reloj_global) + self.tiempo_de_atencion
          self.tiempos_espera[i] = (self.tiempos_salida[i-2] -
                                    self.tiempos_llegada[i])
          self.tiempos_salida[i-1] = (self.tiempos_salida[i] +
                                      self.tiempo_de_atencion)
          self.tiempos_espera[i-1] = (self.tiempos_salida[i] -
                                      self.tiempos_llegada[i-1])
          self.se_cumplio = True

        else:

          if self.se_cumplio == True:
            #print('voy', self.tiempos_salida[i-2])
            self.tiempos_salida[i] = (self.tiempos_salida[i-2] +
                                        self.tiempo_de_atencion)
            self.tiempos_espera[i] = (self.tiempos_salida[i-2] -
                                        self.reloj_global)
            self.se_cumplio = False
            #print(self.se_cumplio)

          else: # self.se_cumplio == False
            self.tiempos_salida[i] = (max(self.tiempos_salida[i-1],
                                          self.reloj_global) +
                                      self.tiempo_de_atencion)
            self.tiempos_espera[i] = (self.tiempos_salida[i-1] -
                                      self.reloj_global)

        #checo si ya paso el tiempo necesario para que salga alguien
        if self.reloj_global >= (self.tiempos_salida[j-1] or
                                 self.tiempos_salida[j-2]):
          while self.cola.fila:
            self.cola.atencion_pacientes() #self.cola.atendiendo = True

        #necesitamos ajustar porque no existen tiempos de espera negativos
        for k in range(len(self.tiempos_espera)):
          if self.tiempos_espera[k] <0:
            self.tiempos_espera[k]=0
          else:
            self.tiempos_espera[k]=self.tiempos_espera[k]

        #para contabilizar tipos de pacientes
        if tipo == 'urgencia':
          u+=1
          self.tiempo_en_sistema_urgencia.append(self.tiempos_salida[i] -
                                            self.tiempos_llegada[i])
          self.tiempo_prom_espera_urgencia.append(self.tiempos_espera[i])
        else: #si es rutinario
          r+=1
          self.tiempo_en_sistema_rutinario.append(self.tiempos_salida[i] -
                                             self.tiempos_llegada[i])
          self.tiempo_prom_espera_rutinario.append(self.tiempos_espera[i])

        i += 1
        j += 1

      if u == 0:
        tiempo_promedio_en_sistema_urgencia = 0
        tiempo_promedio_en_sistema_rutinario = (
            sum(self.tiempo_en_sistema_rutinario)/r)
        tiempo_prom_espera_urgencia = 0
        tiempo_prom_espera_rutinario = (
            sum(self.tiempo_prom_espera_rutinario)/r)
      else:
        tiempo_promedio_en_sistema_urgencia = (
            sum(self.tiempo_en_sistema_urgencia)/u)
        tiempo_promedio_en_sistema_rutinario = (
            sum(self.tiempo_en_sistema_rutinario)/r)
        tiempo_prom_espera_urgencia = (
            sum(self.tiempo_prom_espera_urgencia)/u)
        tiempo_prom_espera_rutinario = (
            sum(self.tiempo_prom_espera_rutinario)/r)

      print('Tiempo promedio en sistema (URGENCIA):',
              tiempo_promedio_en_sistema_urgencia, 'minutos')
      print('Tiempo promedio en sistema (RUTINARIO):',
              tiempo_promedio_en_sistema_rutinario, 'minutos')
      print('Tiempo promedio de espera (URGENCIA):',
              tiempo_prom_espera_urgencia, 'minutos')
      print('Tiempo promedio de espera (RUTINARIO):',
              tiempo_prom_espera_rutinario, 'minutos')

    ###############################################
    #print(self.tiempos_llegada)
    #print(self.tiempos_salida)
    #print(self.tiempos_espera)
    #print('MI FIlA FINAL: ', self.cola.fila)

    ###############################################
    tiempo_promedio_espera = np.mean(self.tiempos_espera)
    print('Tiempo promedio de espera:', tiempo_promedio_espera, 'minutos')

############

def main():
  '''Esta funcion hara las simulaciones para responder a las 3 preguntas de la
  practica.'''
  #pregunta 1
  simulacion1 = Simulacion()
  for i in range(20):
    simulacion1.simular(50000,30,False)

  #pregunta 2
  simulacion2 = Simulacion()
  for i in range(20):
    simulacion2.simular(50000,20,False)

  #pregunta 3
  simulacion3 = Simulacion()
  for i in range(20):
    simulacion3.simular(50000,20,True)

if __name__ == "__main__":
  main()