
# Librerias
from mesa import Agent, Model

from mesa.space import MultiGrid

from mesa.time import SimultaneousActivation

import random

#Variables globales
'''
contadores:
carros
motos
discapacitados 

listas:
id / posición del vehiculo
del tipo de vehiculo.

IMPORTANTE
para editar variables globales dentro de una función es necesario escribir al 
inicio de esta global variable, para aclararle a la funcion que estamos usando
esa variable global y no cree otra local
esto no es necesario con arreglos ya que estos siempre se pasan por referencia 
'''
cont_car_cajon = 0
cont_moto_cajon = 0
cont_disc_cajon = 0

lista_cajones = [] # guarda los agentes de tipo cajon, en orden de más cercano a más lejano 

#Agente tipo calle 
class Calle(Agent):
  '''
 Descripción 
 int id
 vuelta:
  5   1   8
  3       4
  6   2   7 
  '''
  def __init__(self, unique_id,model, giro):
    super().__init__(unique_id,model)
    self.giro = giro
         

#Agente tipo cajón 
class Cajon(Agent):
  '''
  Descripción:
  atributos:
  Int: id
  self.estado True = ocupado, False = desocupado 
  tipo_vehiculo:
  0 - carro
  1 - discapicitados
  2 - moto
  '''
  def __init__(self, unique_id,model,tipo_vehiculo):
    super().__init__(unique_id,model)
    self.tipo_vehiculo = tipo_vehiculo
    self.estado = False # True = ocupado
  
  
class Vehiculo(Agent):
  '''
		“id” : Int,
		“posición” : tuple
    tipo_vehiculo:
    0 - carro
    1 - discapicitados
    2 -  moto
    "tiempo estacionado" : 0; /// tiempo al incio
    "destino" =   tuple  // Siempre será como (12,13)
  '''
  def __init__(self, unique_id, model, tipo_vehiculo):
    super().__init__(unique_id,model) # agente
    #(13,2) posicion inicial
    self.tipo_vehiculo = tipo_vehiculo # moto, carro, discapacitados
    self.tiempo_estacionado = random.randint(100,160) # una vez que se estacione, este es el numero de steps que estara estacionado
    self.destino = None# el cajon que el administrador le asigna
    self.sig_pos = None# la siguiente celda a la que se va a mover cuando se ejecute el advance
    self.tiempo_en_estacionamiento = 0 # tiempo en el estacionamiento desde que entra hasta que sale 
    
    

  def step(self):
    '''
    Tenemos que econtrar la siguiente posición del auto
    dependiendo de las opcion que el agente de tipo calle
    le de:
    5   1   8
    3       4
    6   2   7 
    '''
    # primero revisamos que no hayamos dado ya el paso a la siguiente posición
    # ademas de revisar que el administrado ya nos haya dado un destino, sino
    # el auto no hace nada (se "espera" a que el admin le asigne un lugar)
    if(self.sig_pos != self.destino and self.destino != None):
      row, col = self.pos # sacamos nuestra posición actual 
      #sacamos los vecinos
      vecinos = self.model.grid.get_neighbors(
        self.pos,
        moore = False,
        include_center = True)
      for vecino in vecinos:
        #reviso la calle en la que estoy parado, para ver las opciones de movimiento que me da
        if isinstance(vecino,Calle) and vecino.pos == self.pos:
          if(vecino.giro == 1):
            row -= 1 #subimos
          elif(vecino.giro == 4):
            col += 1 #derecha
          elif(vecino.giro == 2):
            row += 1 #abajo
          elif(vecino.giro == 3):
            col -= 1 #izquierda
          elif(vecino.giro == 5):#opciones arriba y a la izquierda
            if self.destino == (13,9): #salida
              col -= 1 # izquierda
            else: #estoy buscando mi cajon
              if row == self.destino[0] + 1: # si estoy abajo de mi parte del estacionamiento
                if  col == self.destino[1]: # si estoy justo debajo de mi cajon asignado
                  row -= 1 # arriba
                else:
                  col -= 1 # izquierda
              else: 
                row -= 1 # arriba
          elif(vecino.giro == 6):#opciones abajo y a la izquierda
            if  self.destino == (13,9): #salida
              row += 1 # bajar
            else:
              col -= 1 # izquierda
          elif(vecino.giro == 7):#opciones abajo y a la derecha
            if (col == self.destino[1] and row + 1 == self.destino[0]) or (col == 9 and self.destino == (13,9)):
              row += 1 #abajo
            else:
              col += 1 #derecha
          else:#vecino.giro == 8  opciones arriba y a la derecha
            if row - self.destino[0] > 2:
              row -= 1 #arriba
            else:
              col += 1 #derecha

          break
      
      self.sig_pos = (row,col)
      #para evitar chocar
      
      vecinos = self.model.grid.get_neighbors(
        self.pos,
        moore = True,
        include_center = False)
      for vecino in vecinos:
        if isinstance(vecino, Vehiculo) and vecino.sig_pos == self.sig_pos:
          self.sig_pos = self.pos
      
    elif(self.pos == self.destino): # estoy estacionado
      if self.tiempo_estacionado > 0: #sigo estacionado
        self.tiempo_estacionado -= 1
      else:#me tengo que ir 
        self.destino = (13,9)
        vecinos = self.model.grid.get_neighbors(self.pos,False,True)
        if(self.pos[0] in [12,8,4]):
          self.sig_pos = (self.pos[0] - 1,self.pos[1])
        else:
          self.sig_pos = (self.pos[0] + 1,self.pos[1])
        for v in vecinos:
          if v.pos == self.pos and isinstance(v, Cajon):
            v.estado = False
            global cont_car_cajon 
            global cont_moto_cajon
            global cont_disc_cajon
            global lista_cajones
            if v.tipo_vehiculo == 0:
              cont_car_cajon += 1
            elif v.tipo_vehiculo == 1:
              cont_disc_cajon += 1
            elif v.tipo_vehiculo == 2:
              cont_moto_cajon += 1
              
            break
    
    

  def advance(self):
      self.tiempo_en_estacionamiento += 1      
      if(self.pos == (13,9)):
        print("Tiempo en el estacionamiento (# steps) del vehiculo ",self.unique_id,": ", self.tiempo_en_estacionamiento )
        for v in self.model.vehi:
          if v.unique_id == self.unique_id:
            self.model.vehi.remove(v)
            break
          
        # lo sacamos del schedule
        self.model.schedule.remove(self)
        # eliminamos al agente
        self.model.grid.remove_agent(self)

      elif(self.pos != self.sig_pos and self.pos != self.destino and self.pos != None and self.sig_pos != None):
        self.model.grid.move_agent(self, self.sig_pos)# mover agente
      
      


class Administrador(Agent):
  '''
		“id” : string, "admin"
    contador_carros : int global 
    contador_motos :  int global 
    contador_discapacitado : int global	
  '''
  '''
    tipo_vehiculo:
    0 - carro
    1 - discapicitados
    2 -  moto
  '''
  def __init__(self,unique_id,model):
    super().__init__(unique_id,model)
    
  
  def step(self):
    global cont_car_cajon 
    global cont_moto_cajon
    global cont_disc_cajon
    global lista_cajones
    vecinos = self.model.grid.get_neighbors(# queremos ver el vehiculo que esta con el admin
        self.pos,
        moore = False,
        include_center =True)
    
    for vecino in vecinos:
      if vecino.pos == self.pos and isinstance(vecino, Vehiculo): 
        vecino.destino = (13,9)
        for cajon in lista_cajones:
          if not cajon.estado and (cajon.tipo_vehiculo == vecino.tipo_vehiculo):
            cajon.estado = True
            if cajon.tipo_vehiculo == 0:
              cont_car_cajon -= 1
            elif cajon.tipo_vehiculo == 1:
              cont_disc_cajon -= 1
            elif cajon.tipo_vehiculo == 2:
              cont_moto_cajon -= 1
            vecino.destino = cajon.pos
            break
        break

 
  
class Estacionamiento(Model):
  def __init__(self,num_agentes_veh):
    super().__init__()
    self.grid = MultiGrid(14,12, False)
    self.schedule = SimultaneousActivation(self)
    self.cont_vehiculos = 0 # contador de vehiculos
    self.spawn = 5 # tiempo en el que va spawneando cada vehiculo 
    self.maxNum_veh = num_agentes_veh
    self.vehi = []
    self.caj = []
    
    
    #self.datacollector = DataCollector(
    #  model_reporters={'Grid': get_grid}  
    #)
    
 
    #--------creación de cajones----------
    
    #1 fila de cajones
    self.crear_cajones(1, 3, 0)
    #2 fila de cajones
    self.crear_cajones(4, 3, 6)
    #3 fila de cajones
    self.crear_cajones(5, 3, 12)
    #4 fila de cajones
    self.crear_cajones(8, 3, 18)
    #5 fila de cajones
    self.crear_cajones(9, 3, 24)
    #6 fila de cajones
    self.crear_cajones(12, 3, 30)



    #--------creación de calles----------
    #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    fila = 2
    columna = 3 
    for i in range (90,126):
      if(fila%2==0):
        lado_gira=5
      else:
        lado_gira = 7
      
      c = Calle(i,self,lado_gira)
      self.grid.place_agent(c, (fila, columna))
      self.schedule.add(c)

      columna += 1
      if (columna == 9):
          columna = 3
          if(fila%2!=0):
            fila +=3
          else:
            fila+=1


    fila = 2
    columnas =1; 
    for i in range (40,84):

      if(columnas%2==0):
        lado_gira=1
      else:
        lado_gira=2

      if(columnas == 1 and fila == 3):
          lado_gira= 7 
      elif(columnas == 2 and fila == 3):
          lado_gira= 8 
      elif(columnas == 1 and fila == 7):
          lado_gira= 7
      elif(columnas == 2 and fila == 7):
          lado_gira= 8
      elif(columnas == 2 and fila == 6):
          lado_gira= 5
      elif(columnas == 2 and fila == 11):
          lado_gira= 8
      elif(columnas == 2 and fila == 10):
          lado_gira= 5
      elif(columnas == 9 and fila == 2):
          lado_gira= 6
      elif(columnas == 9 and fila == 3):
          lado_gira= 7
      elif(columnas == 9 and fila == 6):
          lado_gira= 6
      elif(columnas == 10 and fila == 6):
          lado_gira= 5
      elif(columnas == 9 and fila == 7):
          lado_gira= 7
      elif(columnas == 9 and fila == 10):
          lado_gira= 6
      elif(columnas == 10 and fila == 10):
          lado_gira= 5
      elif(columnas == 9 and fila == 11):
          lado_gira= 7
      elif(columnas == 10 and fila == 2):
          lado_gira= 3
      elif(columnas == 2 and fila == 2):
          lado_gira= 3
      elif(columnas == 1 and fila == 11):
          lado_gira= 4
     
      c = Calle(i,self,lado_gira)
      self.grid.place_agent(c, (fila, columnas))
      self.schedule.add(c)
      fila+=1
      if(columnas == 1):
          if(fila== 12):
            columnas=2
            fila=2
      
      if (fila == 14):
          fila = 2
          if(columnas==1):
            
            columnas=2
          elif(columnas==2):
            
            columnas=9
          elif(columnas==9):
            
            columnas=10


    #------Creacion del admin---------
    admin = Administrador("admin", self)
    self.grid.place_agent(admin,(13,2))
    self.schedule.add(admin)
    
    #---------------------------------

    
  #-----Creacion de los cajones--------
  def crear_cajones(self, fila, columna, id):
    '''
    0 - carro
    1 - discapicitados
    2 - moto
    cont_car_cajon = 0
    cont_moto_cajon = 0
    cont_disc_cajon = 0
    '''
    global cont_car_cajon 
    global cont_moto_cajon
    global cont_disc_cajon
    global lista_cajones 
    arr = []
    for i in range(6):
      tipo_car = random.randint(0,2)
      if tipo_car == 0:
        cont_car_cajon += 1
      elif tipo_car == 1:
        cont_disc_cajon += 1
      else:
        cont_moto_cajon += 1

      c = Cajon(i + id,self,tipo_car)
      self.grid.place_agent(c,(fila,columna))
      self.schedule.add(c)
      self.caj.append(c)
      arr.append(c)
      columna += 1

    if(id == 0 or id == 12 or id == 24):
      arr.reverse()

    lista_cajones = arr + lista_cajones
    
    
    

  def step(self):
    
    # -----------------------------------------------
    # ------creacion de los agentes vehiculos--------
    #------------------------------------------------
    # queremos que los vehiculos se creen cada tanto tiempo 
    # def __init__(self, unique_id, model, tipo_vehiculo)
    if(self.maxNum_veh > 0): # si aun me quedan agentes para spawnear
      if(self.spawn > 0): # si aun no es momento de spawnear
        self.spawn -= 1 
      else: # ya puedo spawnear el siguiente agente
        tipo = random.randint(0,2) # tipo de vehiculo
        ve = Vehiculo(str(self.cont_vehiculos) + 'vehiculo', self, tipo) # creamos el vehiculo
        self.cont_vehiculos += 1 # actualizamos el contador de vehiculos (que tambien va a ser el id del siguiente vehiculo)
        self.grid.place_agent(ve, (13,2)) # ponemos el vehiculo en la posicion (13, 2 que es donde esta el admin) 
        self.schedule.add(ve) # para que funcionen los steps
        self.vehi.append(ve)
        self.spawn = random.randint(4,8) # nuevo contador de spawn
        self.maxNum_veh -= 1 # deducimos en 1 el numero de vehiculos
      
    
    # -----------------------------------------
    self.schedule.step()
  
  def terminar(self): #funcion que me dice si deberia o no terminar la simulacion
    num_veh = 0

    for c,x,y in self.grid.coord_iter():
      for obj in c:
        if isinstance(obj, Vehiculo):
          num_veh += 1

    return num_veh == 0 and self.maxNum_veh == 0
  
  #Funcion para mandar los JSONs
  def status(self):
    datavehi = []
    datacaj = []
    for v in self.vehi:
      datavehi.append({'vehiculo_id': v.unique_id, 'posicion': str(v.pos), 'tipo': v.tipo_vehiculo, 'tiempo' : v.tiempo_en_estacionamiento})
    
    for c in self.caj:
      datacaj.append({'tipo_veh': c.tipo_vehiculo, 'posicion' : str(c.pos), 'estado': c.estado})
    
    return {"vehiculos":datavehi, "cajones":datacaj,
            'cajo_vehi': cont_car_cajon,
            'cajo_disc': cont_disc_cajon,
            'cajo_moto': cont_moto_cajon}
