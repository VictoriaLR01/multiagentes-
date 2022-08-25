def get_grid(model):
    '''
    descripcion... 
    '''
    grid = np.zeros((model.grid.width, model.grid.height))
    for cell in model.grid.coord_iter():
      cell_content, x, y = cell
      for obj in cell_content:
        if isinstance(obj, Cajon):
          grid[x][y] = 2
        elif isinstance(obj, Calle):
          grid[x][y] = 1
        else:
          grid[x][y] = 3
    return grid
#Variables globales
'''
contadores:
carros
motos
discapacitados 

listas:
id / posición del vehiculo
del tipo de vehiculo.
'''
cont_car = 0
cont_moto = 0
cont_disc = 0
list_disc  = []
list_moto = []
list_car = []
#Agente tipo calle 
class Calle(Agent):
  '''
 Descripción 
 int id
 vuelta:
 0 -  no puede girar
 1- gira a la izquierda 
 2 -  3 gira a la derecha 
 3 - puede girar a las dos direcciones 
  '''
  def __init__(self, unique_id, giro):
      super().__init__(unique_id, giro)
      self.giro = 0
         

#Agente tipo cajón 
class Cajon(Agent):
  '''
  Descripción:
  atributos:
  Int: id
  self.estado  = false; // desocupado  --- true - ocupado;
  tipo_vehiculo:
  0 - carro
  1 - discapicitados
  2 -  moto
  '''
  def __init__(self, unique_id, tipo_vehiculo):
    super().__init__(unique_id, tipo_vehiculo)
    self.tipo_vehiculo = tipo_vehiculo
    self.estado = False 
  
class Vehiculo(Agent):
  '''

		“id” : Int,
		“posición” : tuple
    tipo_vehiculo:
    0 - carro
    1 - discapicitados
    2 -  moto
    tiempo estacionado  =  0; /// tiempo al incio
    "destino" =   tuple  // Siempre será como (12,13)

		
  '''
  def __init__(self, unique_id, tipo_vehiculo, pos, tiempo_estacionado):
    super().__init__(unique_id, tipo_vehiculo, pos, tiempo_estacionado)
    self.pos = "posicion donde incian todos ESTO DEBE DE SER UNA TUPLA"
    self.tipo_vehiculo = tipo_vehiculo
    self.tiempo_estacionado = 0
    self.destino = (2,13)


class Administrador(Agent):
  '''

		“id” : Int,
    contador_carros : int global 
    contador_motos :  int global 
    contador_discapacitado : int global 

		
  '''
  def __init__(self):
    super().__init__(unique_id)
    
  
class Estacionamiento(Model):
  def __init__(self):
    super().__init__()
    self.grid = MultiGrid(30,30, False)
    self.schedule = SimultaneousActivation(self)
 
  
    fila = 1;
    columnas =3; 
    for i in range (36):
      tipo_car = random.randint(0,2)
      c = Cajon(i,tipo_car);
      self.grid.place_agent(c, (columnas, fila))
      self.schedule.add(c)
      print(columnas,fila)  
      columnas+=1;
      if (columnas == 9):
          columnas = 3;
          if(fila%2!=0):
            fila +=3;
          else:
            fila+=1;

  # creación de calles
    fila = 3;
    columnas =2; 
    for i in range (90,126):
      lado_gira=0
      if(columnas == 1 and fila == 3):
          lado_gira= int(1) #gira izq
      elif(columnas == 2 and fila == 3):
          lado_gira= int(2)#gira der
      elif(columnas == 1 and fila == 7):
          lado_gira= int(1) #gira izq
      elif(columnas == 2 and fila == 7):
          lado_gira= int(2)#gira der
      elif(columnas == 2 and fila == 6):
          lado_gira= int(1) #gira izq
      elif(columnas == 2 and fila == 11):
          lado_gira= int(2)#gira der
      elif(columnas == 2 and fila == 10):
          lado_gira= int(1) #gira izq.  ## HASTA AQUI ES EL LADO IZQUIERDOOOOO
      elif(columnas == 9 and fila == 2):
          lado_gira= int(2)#gira der
      elif(columnas == 9 and fila == 3):
          lado_gira= int(1) #gira izq
      elif(columnas == 9 and fila == 6):
          lado_gira= int(2)#gira der
      elif(columnas == 10 and fila == 6):
          lado_gira= int(1) #gira izq
      elif(columnas == 9 and fila == 7):
          lado_gira= int(1) #gira izq
      elif(columnas == 9 and fila == 10):
          lado_gira= int(2)#gira der
      elif(columnas == 10 and fila == 10):
          lado_gira= int(1) #gira izq
      elif(columnas == 9 and fila == 11):
          lado_gira= int(1) #gira izq
      else:
          lado_gira = int(0)
      
      c = Calle(i,lado_gira);
      self.grid.place_agent(c, (columnas, fila))
      self.schedule.add(c)
      print(columnas,fila)  
      columnas+=1;
      if (columnas == 9):
          columnas = 3;
          if(fila%2!=0):
            fila +=3;
          else:
            fila+=1;


    fila = int(2);
    columnas =int(1); 
    for i in range (40,88):
      # self.tipo = "calle" #esto no sé si este bien AHHHHH
        #c = Cajon(i,tipo_car);
        #self.grid.place_agent(c, (columnas, filas))
      if(columnas == 1 and fila == 3):
          lado_gira= int(1) #gira izq
      elif(columnas == 2 and fila == 3):
          lado_gira= int(2)#gira der
      elif(columnas == 1 and fila == 7):
          lado_gira= int(1) #gira izq
      elif(columnas == 2 and fila == 7):
          lado_gira= int(2)#gira der
      elif(columnas == 2 and fila == 6):
          lado_gira= int(1) #gira izq
      elif(columnas == 2 and fila == 11):
          lado_gira= int(2)#gira der
      elif(columnas == 2 and fila == 10):
          lado_gira= int(1) #gira izq.  ## HASTA AQUI ES EL LADO IZQUIERDOOOOO
      elif(columnas == 9 and fila == 2):
          lado_gira= int(2)#gira der
      elif(columnas == 9 and fila == 3):
          lado_gira= int(1) #gira izq
      elif(columnas == 9 and fila == 6):
          lado_gira= int(2)#gira der
      elif(columnas == 10 and fila == 6):
          lado_gira= int(1) #gira izq
      elif(columnas == 9 and fila == 7):
          lado_gira= int(1) #gira izq
      elif(columnas == 9 and fila == 10):
          lado_gira= int(2)#gira der
      elif(columnas == 10 and fila == 10):
          lado_gira= int(1) #gira izq
      elif(columnas == 9 and fila == 11):
          lado_gira= int(1) #gira izq
      else:
          lago_gira = int(0)
      
      c = Calle(i,lado_gira);
      self.grid.place_agent(c, (columnas, fila))
      self.schedule.add(c)
      fila+=1;
      if (fila == 14):
          fila = 2;
          if(columnas==1):
            
            columnas=2;
          elif(columnas==2):
            
            columnas=9;
          elif(columnas==9):
            
            columnas=10;
    self.datacollector = DataCollector(
        model_reporters={"Grid": get_grid}
        )

    def step(self):
      self.datacollector.collect(self)
      self.schedule.step()
      # Commented out IPython magic to ensure Python compatibility.
# %%capture
# 
# fig, axs = plt.subplots(figsize=(7,7))
# axs.set_xticks([])
# axs.set_yticks([])
# patch = plt.imshow(all_grid.iloc[0][0], cmap=plt.cm.binary)
# 
# def animate(i):
#     patch.set_data(all_grid.iloc[i][0])
#     
# anim = animation.FuncAnimation(fig, animate, frames=len(all_grid))

anim
