"""
**********************************************************
*                                                        *      
*            Instituto Tecnológico de Costa Rica         *
*          Área Académica de Ing. en Computadores        *
*                                                        *
*           Desarrollo de juego simple con Python        *
*                                                        *
*                      Estudiantes:                      *
*         Juan David Quesada Estrada-2019044684          *
*            Jeff. Araya Urbina - 2021012480             *
*                                                        *
*                                                        *
*                                                        *
*          II Proyecto Taller de Programacion            *
*                                                        *
**********************************************************
"""


'''Modules imports'''
from tkinter import *
from tkinter import messagebox
import pygame
import random 
import time 
from ordenamiento_puntaje import *

pygame.init()
#====================================================Ordenamiento de Puntajes=============================================================#
names_list=[]
Scores_list=[]
def ordenar_puntajes():
    global names_list, Scores_list
    names_list = []
    Scores_list = []
    file= open("Scores.txt","r")
    
    for line in file.readlines():
        name =""
        score = ""
        split = False
        for char in line:
            if char == "$":
                split = True
            elif split:
                score+=char
            else:
                name+=char
        names_list.append(name)
        Scores_list.append(int(score))
    
    quick_sort_desc(Scores_list,names_list,0,len(Scores_list)-1)



#=======================================================Clase para el jugador=======================================================================================#
class Nave(): 
    def __init__(self, x, y): #Constructor
        #Puntos de vida
        self.vidas = 3
        self.hp = 20
        
        self.immune = False #inmunidad despues de chocar contra un meteorito

        self.x = x #Posicion en eje horizontal
        self.y = y #Posicion en eje vertical
        
        self. speedy = 0 #Velocidad en eje vertical
        self. speedx = 0 #Velocidad en eje horizontal

        self.score = 0 #puntaje
        self.scorespeed = 1#cuantos puntos gana por segundo
        
        self.rect = None #Inicialmente se asigna None a esta variable, mas adelante se le asignara un pygame.Rect
        self.master = None #pantalla 

        img = pygame.image.load("player.png")
        self.img = pygame.transform.scale(img,(50,50))
        self.color = (100,100,100)

        
#=============================================crea al jugador en la pantalla por primera vez=========================================================================#
    def create_self(self):


        self.rect = pygame.Rect(self.x,self.y,50,50)
        #pygame.draw.rect(self.master,self.color, self.rect)
        self.master.blit(self.img,(self.rect.left,self.rect.top))
        
    #move revisa la posicion del jugador relativo a la pantalla, y lo mueve segun su velocidad
    #E: Ancho y altura de la pantalla
    #S: Movimiento del jugador
    #R: Ints //no se revisa
        
    def move(self,width,height):
        borderx= self.rect.left +self.speedx #borde del jugador en el eje horizontal
        bordery = self.rect.top +self.speedy #borde del jugador en el eje vertical
        
        if  (-10>=borderx or borderx>=width-40) or (-10>=bordery or bordery>=height-50): #Si el fuera a salir de la pantalla   
            
            self.speedy = 0
            self.speedx = 0
            #Ambos componentes de la velocidad se devuelven a 0, pues el jugador no deberia poder salir de la pantalla
            
        else:#Si el jugador esta dentro de la pantalla
            self.rect.move_ip(self.speedx,self.speedy)#mover jugador
        #pygame.draw.rect(self.master,self.color, self.rect) #dibujar jugador en la pantalla
        self.master.blit(self.img,(self.rect.left,self.rect.top))

#========================================================Clase para los proyectiles que esquiva el jugador========================================================#       
class Meteoro(): 
    def __init__(self,x,master,width,soundon): #Constructor
        self.soundon = soundon
        self.x = x #posicion en eje x
        self.speedx = random.randint(-15,15) #velocidad aleatoria a la izquiera o la derecha
        a=30 +random.randint(0,10) #tamaño del meteorito (minimo 30, maximo 40)
        self.y=-40 #se posiciona inicialmente arriba de la pantalla, para que parezca que salen del espacio a
        self.rect = pygame.Rect(self.x,self.y,a,a)#rectangulo
        self.master = master#pantalla de juego
        self.width = width#se refiere al ancho de la pantalla de juego
        #pygame.draw.rect(master,(110,0,0),self.rect)#Dibujar rectangulo en la pantalla de juego, que representa el borde del meteorito
        self.bounce = 2 #Cantidad de veces que el meteorito puede chocar contra el borde de la pantalla
        self.speedy = random.randint(3,8) #Velocidad aleatoria en el eje vertical
        self.not_crashed = True #Flag si ha chocado contra el jugadro
        img= pygame.image.load("meteor.png")#Imagen del meteoro
        self.img = pygame.transform.scale(img,(a,a))
        #Sonido del meteoro
        self.sonido = pygame.mixer.Sound("meteor.wav")    
            

#================Class Meteoro Methods================================================================================================================================#
        
    def move(self):#mover el meteorito
        if self.not_crashed:#Solo se mueve si no ha chocado
            x_Check = (self.rect.left < 10 or self.rect.left > self.width - 10)
            
            if x_Check and self.bounce>=0 : #Puede rebotar con el borde de la pantalla un total de 2 veces
                if self.soundon: #Sonar el sonido
                    self.sonido.play()                 
  
                self.bounce-=1
                self.speedx = -1*self.speedx

            #El meteorito se deja de dibujar en la pantalla una vez ha chocado
            self.rect.move_ip(self.speedx,self.speedy)
            self.master.blit(self.img,(self.rect.left,self.rect.top))

            if self.rect.top > 530 or ( x_Check and self.bounce < 0):#Revisa si el meteorito sale de la pantalla
                self.not_crashed = False#Se dice que choca al salir de la pantalla para dejar de dibujarlo

#Colores en (red, green, blue)
white = (255,255,255)
black =(0,0,0)


#Posibles canciones para nivel, dependiendo de cual sea el actual
Music_list = ["Level1.wav","Level2.wav","Level3.wav"]

#==============================================Clase principal del juego==============================================================================================#

class Juego(): 
    def __init__(self,width,height,level,player_name,window,soundon):#Constructor
        pygame.init()
        self.soundon = soundon #Si el sonido esta encendido o no
        self.playername = player_name #Nombre del jugador

        self.width = width   #Ancho de la pantalla
        self.height = height #Alto de la pantalla
        self.playing = True  #Flag si el jugador aun sigue en el juego
        self.Screen = None   #Mas adelante se convierte en un pygame.display
        self.window = window #Ventana principal (Tkinter)
        self.level=level #Nivel acutal
        self.title = f"Game: Nivel {self.level}" #Titulo de la pantalla, muestra el nivel del juego

        self.FPS = 30 #30fps
        self.clock = pygame.time.Clock() #reloj de pygame

        self.player = Nave(self.width/2-15,self.height-60) #Jugador
        self.Meteor_list=[] #Lista de meteoros, inicialmente vacia
        self.font = pygame.font.SysFont("TimesNewRoman",16) #Letra para mostrar las cosas
        self.current_time = 0 #Tiempo actual de juego

        bg_img = pygame.image.load("bg.png")#Fondo de pantalla
        self.bg = pygame.transform.scale(bg_img,(self.width,self.height)) 
        
        self.current_frame = 0 #Frame actual (El juego corre a 30fps)

        
#=======================================Class Juego Methods===================================#
        
    def Crear_meteoro(self): #Crear_meteoro crea un meteoro en la pantalla de juego en una posicion horizontal aleatoria
        if self.current_frame<(30+7.5*(self.level-1)):
            self.current_frame +=1
        
        else:
            self.current_frame=0
            for j in range(0,self.level+2):
                self.Meteor_list.append(Meteoro(random.randint(100,self.width-100),self.Screen,self.width,self.soundon)) #Cada meteorito se añade a la lista de meteoros del juego
            
                

    def Show_Score(self):#Show_Score muestra el puntaje actual del jugador en la pantalla del juego
        
        self.score = self.font.render(f"Puntaje: {self.player.score}",True,black)
        self.Screen.blit(self.score,(10,self.height-20))
        
    def Show_HP(self): #Show_HP muestra tanto las vidas del jugador como su hp en la pantalla de juego
        self.player_HP =self.font.render(f"HP: {self.player.hp}",True,black)
        self.player_vidas =self.font.render(f"Vidas: {self.player.vidas}",True,black)
        self.Screen.blit(self.player_HP,(100,self.height-20))
        self.Screen.blit(self.player_vidas,(170,self.height-20))
  
    def Show_player_name(self): #Show_player_name muestra el nombre del jugador en la pantalla del juego
        self.player_name = self.font.render(f"Jugador: {self.playername}",True,black)
        self.Screen.blit(self.player_name,(340,self.height-20))
    
    
    def Show_Time(self): #Show_Time muestra el tiempo en segundos que ha pasado desde que comenzo el juego
                         #Ademas, actualiza el puntaje del jugador cada segundo
        if time.time()- self.timer > self.current_time+1:
            self.current_time+=1
            self.player.score+=self.player.scorespeed
            self.current_level_score+=self.player.scorespeed

        self.Time = self.font.render(f"Tiempo: {self.current_time}s",True,black)
        self.Screen.blit(self.Time,(250,self.height-20))
        
    def Save_Score(self):#Save score salva el nombre del jugador y su puntaje separados por un $, ademas informa al jugador
                         #si esta entre los 10 mejores puntajes
        ordenar_puntajes()
        for i in range(0,11 if len(Scores_list)>10 else len(Scores_list)):
            if self.player.score > Scores_list[i]:
                messagebox.showinfo(title= f"Felicidades {self.playername}!", message = f"Has obtenido la posicion {i+1} en los mejores puntajes!")
                break
        file = open("Scores.txt","a")
        file.write(f"\n{self.playername}${self.player.score}")
    
    def Reset_level(self): #Reset_level resetea el valor de algunas variables de juego, y lo pausa por 2 segundos
        if self.soundon:
            self.music.stop()
        self.Meteor_list=[]
        self.player.hp = 20
        self.current_time = 0
        
        
        time.sleep(2)
        
    



    def End_Game(self): #End_Game termina el ciclo principal de juego y salva el puntaje del jugador
        self.playing = False
        if self.soundon:
            self.music.stop()
            pygame.mixer.unpause()
        
        self.Save_Score()
        
        self.window.deiconify()

    def Win(self):# Win se encarga de las acciones a tomar al terminar cada nivel
        if self.level >2: #Si el jugador esta en el tercer nivel, el juego acaba
            self.Message = self.font.render("Has vencido el juego!",True,white)
            self.Screen.blit(self.Message,(200,100))
            self.End_Game()
        
        else: #En cualquier otro caso, se le informa al jugador que ha pasado de nivel
            
            self.Message = self.font.render(f"Has vencido el nivel {self.level}!",True,white)
            self.Screen.blit(self.Message,(200,100))
            pygame.display.update()
            self.level+=1
            self.title = f"Game: Nivel {self.level}"

            self.Reset_level() 
    def play_music(self):
        if self.soundon:
            pygame.mixer.pause()
            self.music = pygame.mixer.Sound(Music_list[self.level-1])
            self.music.play(-1)
            


    def Start(self): #Start comienza el juego y contiene el ciclo principal del juego
        self.Screen = pygame.display.set_mode((self.width,self.height)) #Crea pantalla de pygame
        pygame.display.set_caption(self.title) #Titulo de la pantalla
        self.Screen.fill(black) #Fondo de la pantalla
        self.player.master = self.Screen
        self.player.create_self()
        self.play_music()
        self.player.scorespeed = 1 + 2*(self.level-1)*(self.level>1)
        
        self.timer = time.time()
        self.current_level_score = 0
        while self.playing: #Si el jugador no ha dejado de jugar
            #https://www.geeksforgeeks.org/how-to-create-buttons-in-a-game-using-pygame/ para la creacion del boton de regreso al menu
            mouse = pygame.mouse.get_pos()

            self.clock.tick(self.FPS)#para que el juego vaya a 30fps
            
            self.Screen.fill(black) #Se redibuja el fondo de pantalla cada frame
            self.Screen.blit(self.bg,(0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #Salir del juego si el jugador quiere, y volver a la pantalla principal
                    self.End_Game()
                    break
                if event.type == pygame.KEYDOWN:#Cada tecla que se presiona
                     
                        if event.key == pygame.K_RIGHT:#moverse a la derecha con la flecha derecha
                            self.player.speedx=10
                        if event.key == pygame.K_LEFT : #moverse a la izquierda con la flecha izquierda
                            self.player.speedx=-10
                        if event.key == pygame.K_DOWN : #moverse hacia abajo con la flecha de abajo
                            self.player.speedy=10
                        if event.key == pygame.K_UP: #moverse hacia arriba con la felcha de arriba
                            self.player.speedy=-10
                if event.type == pygame.KEYUP: #Si se suelta una tecla
                    if event.key in [pygame.K_RIGHT,pygame.K_LEFT]: #Si es una de las que controla el movimiento horizontal
                        self.player.speedx = 0                      #que el jugador pierda movimiento en ese eje
                    if event.key in [pygame.K_UP,pygame.K_DOWN]:    #Igualmente con el eje vertical 
                        self.player.speedy = 0
                if event.type == pygame.MOUSEBUTTONDOWN and self.width-48 <= mouse[0] <= self.width and self.height-20 <= mouse[1] <= self.height:
                    self.End_Game()
                    break
            if not self.playing:
                break
            self.player.move(self.width,self.height) #Cada frame se dice al jugador que se mueva, 
                                                     #aun si no se presiona ninguna tecla, pues
                                                     #en ese caso, el movimiento sera nulo
            
            for j in self.Meteor_list: #Mecanicas para los meteoritos
                if j.not_crashed:
                    j.move()               #se mueve cada meteorito de la lista de meteoritos
                    if j.rect.colliderect(self.player): #Se revisa si han chocado con el jugador
                        j.not_crashed = False
                        #Se revisa la mecanica de vida del jugador
                        if self.player.hp > 1: #El jugador pierde un punto de vida si todavia tiene
                            self.player.hp-=1
                        elif self.player.vidas >1: #Pierde una vida si todavia tiene y no tiene puntos de vida
                            self.player.vidas-=1
                            self.Message = self.font.render(f"Vidas:{self.player.vidas}   Nivel: {self.level}",True,white)
                            self.Screen.blit(self.Message,(170,100))
                            pygame.display.update()
                            
                            self.Reset_level()
                            self.player.score-=self.current_level_score
                            
                            self.Start()                    
                        else: #pierde
                            self.Message = self.font.render(f"Has perdido",True,white)
                            self.Screen.blit(self.Message,(200,100))
                            pygame.display.update()

                            time.sleep(2)

                            self.End_Game()

                            break
            if not self.playing:
                break
            #HUD
            a=pygame.Rect(0,self.height-20,self.width,20)
            pygame.draw.rect(self.Screen,white,a)
            self.Crear_meteoro()
            self.Show_Score()
            self.Show_HP()
            self.Show_Time()
            self.Show_player_name()
            
            volver = pygame.Rect(self.width-50,self.height-20,50,20)
            volvertxt = self.font.render(f"Volver",True,white)
            pygame.draw.rect(self.Screen,black,volver)
            
            if self.width-48 <= mouse[0] <= self.width and self.height-20 <= mouse[1] <= self.height:
                volver = pygame.Rect(self.width-50,self.height-20,50,20)
                volvertxt = self.font.render(f"Volver",True,black)
                pygame.draw.rect(self.Screen,(100,100,100),volver)

            
            self.Screen.blit(volvertxt,(self.width-48,self.height-20))
            if self.current_time == 60: #A los 60s termina el nivel

                
                self.Win()
                self.Start()
            #Actualizar la pantalla de juego
            pygame.display.update()
            
            
        pygame.display.quit()#Salir de la pantalla de juego sin cerrar pygame.
    




#------------Main window-------------------------------#
HEIGHT=450
WIDTH=800
window=Tk()
window.title("TOP")
window.geometry("800x450")
window.resizable=(False, False)
pygame.mixer.init()#Inicializa el modulo


#============Windows Functions===============#
def show(window): window.deiconify()# Receive window as variable and it'll open it

def hide(window): window.withdraw()# Receive window as variable and it'll hide it

def close_window_at_all(window):window.destroy()# Receive window as variable and it'll destroy it



#======================Main window image==================#

canvas=Canvas(window,width=WIDTH, height=HEIGHT)
canvas.place(x=0, y=0)
canvas.pack

Background=PhotoImage(file="space.png")
bg=canvas.create_image(0,0, image=Background, anchor=NW)


#=================Main window sound===============#
main=pygame.mixer.Sound("hola.ogg")
main.play(-1)


#======================Main window daughter==============#
HEIGHT=450
WIDTH=800
window1=Toplevel(window)
window1.title("Options")
window1.geometry("800x450")
window1.resizable=(False, False)


#===================Main window daughter image==========#

canvas=Canvas(window1,width=WIDTH, height=HEIGHT)
canvas.place(x=0, y=0)
canvas.pack

Back=PhotoImage(file="ship.png")
bga=canvas.create_image(0,0, image=Back, anchor=NW)


#======================Main window daughter's daughter==============#
HEIGHT=450
WIDTH=800
window2=Toplevel(window1)
window2.title("Instrucciones del juego")
window2.geometry("800x450")
window2.resizable=(False, False)

#===================Main window daughter's daughter image==========#

canvas=Canvas(window2,width=WIDTH, height=HEIGHT)
canvas.place(x=0, y=0)
canvas.pack

offf=PhotoImage(file="how.png")
bega=canvas.create_image(0,0, image=offf, anchor=NW)


#======================Main window other daughter==============#
HEIGHT=450
WIDTH=800
window3=Toplevel(window)
window3.title("Acerca de")
window3.geometry("800x450")
window3.resizable=(False, False)

#===================Main window other daughter image==========#

canvas=Canvas(window3,width=WIDTH, height=HEIGHT)
canvas.place(x=0, y=0)
canvas.pack

out=PhotoImage(file="fon.png")
biga=canvas.create_image(0,0, image=out, anchor=NW)

#======================Window4==================================#
HEIGHT=450
WIDTH=800
window4=Toplevel(window3)
window4.title("Creditos")
window4.geometry("800x450")
window4.resizable=(False, False)

#==================Window4 create image=======================================#

canvas=Canvas(window4,width=WIDTH, height=HEIGHT)
canvas.place(x=0, y=0)
canvas.pack

otyt=PhotoImage(file="found.png")
btga=canvas.create_image(0,0, image=otyt, anchor=NW)

#======================Window5==================================#
HEIGHT=450
WIDTH=800
window5=Toplevel(window)
window5.title("Records")
window5.geometry("800x450")
window5.resizable=(False, False)

#==================Window5 create image=======================================#

canvas=Canvas(window5,width=WIDTH, height=HEIGHT)
canvas.place(x=0, y=0)
canvas.pack

ot=PhotoImage(file="found.png")
btga=canvas.create_image(0,0, image=ot, anchor=NW)


#===================================Sound settings==================#
def stopSound():#Detiene el sonido
   global soundon
   soundon = False
   pygame.mixer.pause()


def reactive_sound():#reaactiva el sonido
   global soundon
   soundon = True
   pygame.mixer.unpause()
   

   
soundon= True



#=============Comenzar guarda la ventana principal y comienza el juego=============#
def comenzar():
   window.withdraw()
   juego = Juego(500,600,Level.get(),PlayerName.get(),window,soundon)
   juego.Start()
   

#==============Variable para almacenar el nivel===================================#
   
Level = IntVar()
Level.set(1) #Se comienza en el nive 1 por default

#=============Label para señalar los radiobuttons de nivel========================#

Label(window,text= "Nivel:", bg = "#6769a9").place(x=100,y = 70)


#==============Radiobuttons para seleccionar el nivel=============================#

level_button1 = Radiobutton(window,text = "1", variable  = Level,value = 1,bg = "#6769a9" )
level_button2= Radiobutton(window,text = "2", variable  = Level,value = 2,bg = "#6769a9" )
level_button3 = Radiobutton(window,text = "3", variable  = Level,value = 3,bg = "#6769a9" )
      
level_button1.place(x=100,y=100)
level_button2.place(x=100,y=130)
level_button3.place(x=100,y=160)

#====Variable para almacenar el nombre del jugador========#

PlayerName = StringVar()
PlayerName.set("Anon")

#================Name limit equal to 6 letters============#

def player_name_limit(*a):
   if len(PlayerName.get()) > 6: PlayerName.set(PlayerName.get()[:6]) #Por estetica, se le asigno un limite de 6 letras al nombre del jugador

#=======Asignacion funcion a la variable del nombre del jugador=========#
   
PlayerName.trace("w",player_name_limit)

#======Label para mostrar el entry del nombre de jugador===============#

Label(window,text= "Nombre:", bg = "#6769a9").place(x=100,y = 200)

#=========Entry del nombre del jugador===================#

Name_Entry = Entry(window, bg = "#6769a9", textvariable=PlayerName)
Name_Entry.place(x= 100, y = 220)


#====================Set button's images=========#
imgb=PhotoImage(file="play.png")
imgc=PhotoImage(file="optios.png")
imgd=PhotoImage(file="information.png")
imge=PhotoImage(file="record.png")
imgf=PhotoImage(file="quit.png")


#==================Buttons==========================#
boton1=Button(window,bg="#6769a9", image=imgb, width=80, height=20,command = comenzar)
boton2=Button(window, bg="#6769a9",image=imgc, width=80, height=20,command=lambda: [show(window1), hide(window)] )
boton3=Button(window, bg="#6769a9",image=imgd, width=80, height=20,command=lambda: [show(window3), hide(window)]  )
boton4=Button(window, bg="#6769a9",image=imge, width=80, height=20,command=lambda: [(hide(window),ll(),show(window5))])
qit=Button(window, bg="#6769a9",image=imgf, width=80, height=20, command=lambda:[close_window_at_all(window), stopSound()])




#=======================Buttons places==============#
boton1.place(x=120, y=250)
boton2.place(x=280, y=250)
boton3.place(x=440, y=250)
boton4.place(x=600, y=250)
qit.place(x=700, y=420)

#================================================================window1=================================================================#

#================Labels========================#
label=Label(window1, text="Sonido:",font=("Haettenschweiler", 18), fg="White", bg="black")
label1=Label(window1, text="¿Como se juega?",font=("Haettenschweiler", 18), fg="White", bg="black")

#=====================Labels places======================#
label.place(x=175, y=10)
label1.place(x=500, y=10)

#====================Set button's images=========#
img1=PhotoImage(file="off.png")
img2=PhotoImage(file="on.png")
img3=PhotoImage(file="behind.png")
img4=PhotoImage(file="instu.png")

#==================Buttons==========================#
bot=Button(window1, bg="black", image=img1, width=80, height=20 ,command=lambda: stopSound())
bot1=Button(window1, bg="black", image=img2, width=80, height=20 ,command=lambda: reactive_sound())
bot2=Button(window1, bg="black", image=img3, width=80, height=20 ,command=lambda: [hide(window1), show(window)])
bot3=Button(window1, bg="black",image=img4,width=80, height=20 ,command=lambda: [hide(window1), show(window2)])

#=======================Buttons places==============#
bot.place(x=80, y=150)
bot1.place(x=240, y=150)
bot2.place(x=700, y=420)
bot3.place(x=530, y=150)

#===================================================================window2========================================================================================#

#====================Set button's images=========#
imgz=PhotoImage(file="behind.png")

#=====================Buttons====================#
bo=Button(window2, bg="#00cd82", image=imgz, width=80, height=20 ,command=lambda:[hide(window2), show(window1)])

#=========================Buttons places==========#
bo.place(x=700, y=420)


#===================================================================window3==========================================================================================#

#===============================Buttons=======================#
bott=Button(window3, bg="#454443", image=img3, width=80, height=20 ,command=lambda: [hide(window3), show(window)])
bott1=Button(window3,bg="#454443", text="Creditos",font=("Haettenschweiler", 12) , fg="White",command=lambda: [hide(window3), show(window4)]) 

#=============================Buttons places==================#
bott.place(x=700, y=420)
bott1.place(x=1, y=415)

#===============================Labels=====================#

label_1=Label(window3, text="Pais de produccion:",font=("Haettenschweiler", 12), fg="White", bg="#454443")
label_2=Label(window3, text="Costa Rica",font=("Haettenschweiler", 12), fg="White", bg="#454443")
label_3=Label(window3, text="Universidad y carrera:",font=("Haettenschweiler", 12), fg="White", bg="#454443")
label_3=Label(window3, text="Universidad y carrera:",font=("Haettenschweiler", 12), fg="White", bg="#454443")
label_4=Label(window3, text="Instituto Tecnologico de Costa Rica, Ingieneria en Computadores",font=("Haettenschweiler", 12), fg="White", bg="#454443")
label_5=Label(window3, text="Asignatura, año y grupo:",font=("Haettenschweiler", 12), fg="White", bg="#454443")
label_6=Label(window3, text="Taller de programacion, 20 de de junio 2021, grupo 1",font=("Haettenschweiler", 12), fg="White", bg="#454443")
label_7=Label(window3, text="Nombre del profesor:",font=("Haettenschweiler", 12), fg="White", bg="#454443")
label_8=Label(window3, text="Jeff Schmidt Peralta",font=("Haettenschweiler", 12), fg="White", bg="#454443")
label_9=Label(window3, text="Version 1.1 ",font=("Haettenschweiler", 12), fg="White", bg="#454443")
label_10=Label(window3, text="Autores: ",font=("Haettenschweiler", 12), fg="White", bg="#454443")
label_11=Label(window3, text="Juan Quesada Estrada",font=("Haettenschweiler", 12), fg="White", bg="#454443")
label_12=Label(window3, text="Jeff Araya Urbina",font=("Haettenschweiler", 12), fg="White", bg="#454443")




#==========================Labels places=================#
label_1.place(x=350, y=10)
label_2.place(x=375, y=40)
label_3.place(x=340, y=70)
label_4.place(x=240, y=100)
label_5.place(x=340, y=130)
label_6.place(x=270, y=160)
label_7.place(x=350, y=190)
label_8.place(x=350, y=220)
label_9.place(x=374, y=250)
label_10.place(x=379, y=280)
label_11.place(x=350, y=310)
label_12.place(x=360, y=340)

#===================================================================window4===========================================================================================#
#=================Labels================#
credi=Label(window4, text="Creditos",font=("Haettenschweiler", 14), fg="White", bg="#454443")
credi_1=Label(window4, text="Fandom Community",font=("Haettenschweiler", 13), fg="White", bg="#454443")
credi_2=Label(window4, text="Chris Vecchione",font=("Haettenschweiler", 13), fg="White", bg="#454443")
credi_3=Label(window4, text="Cgma from Sprite Fx",font=("Haettenschweiler", 13), fg="White", bg="#454443")
credi_4=Label(window4, text="Programmersought",font=("Haettenschweiler", 13), fg="White", bg="#454443")
credi_5=Label(window4, text="GeekforGeeks",font=("Haettenschweiler", 13), fg="White", bg="#454443")
credi_6=Label(window4, text="Pygame Community",font=("Haettenschweiler", 13), fg="White", bg="#454443")
credi_7=Label(window4, text="Codementor",font=("Haettenschweiler", 13), fg="White", bg="#454443")
credi_8=Label(window4, text="HeatlyBros",font=("Haettenschweiler", 13), fg="White", bg="#454443")
credi_9=Label(window4, text="Patrick de Arteaga",font=("Haettenschweiler", 13), fg="White", bg="#454443")
credi_10=Label(window4, text="Adobe Stock",font=("Haettenschweiler", 13), fg="White", bg="#454443")


#============Labels places============#
credi.place(x=390, y=10)
credi_1.place(x=366, y=40)
credi_2.place(x=374, y=70)
credi_3.place(x=360, y=100)
credi_4.place(x=366, y=130)
credi_5.place(x=379, y=160)
credi_6.place(x=368, y=190)
credi_7.place(x=387, y=220)
credi_8.place(x=387, y=250)
credi_9.place(x=366, y=280)
credi_10.place(x=386, y=310)

#=================Buttons===============#
boti=Button(window4, bg="#454443", image=img3, width=80, height=20 ,command=lambda: [hide(window4), show(window3)])

#===============Buttons place========#

boti.place(x=700, y=420)

#===================================================================window5===========================================================================================#



#===============================Labels=====================#

label_i=Label(window5, text="Posicion",font=("Haettenschweiler", 12), fg="White", bg="#454443")
label_t=Label(window5, text="Nombre",font=("Haettenschweiler", 12), fg="White", bg="#454443")
puntaje=Label(window5, text="Puntaje",font=("Haettenschweiler", 12), fg="White", bg="#454443")

#=====================Labels places======================#
label_i.place(x=150, y=20)
label_t.place(x=400, y=20)
puntaje.place(x=650, y=20)
#=================Window5 Scores shown===================#
def ll():
    global names_list, Scores_list# Update lists in order to updating of the  information 
    ordenar_puntajes()#called to the funcion for ordering data   
    n=60
    for i in range(0,11 if len(Scores_list) >=10 else len(Scores_list)):
        
        Label(window5, text=(i+1),font=("Haettenschweiler", 12), fg="White", bg="#454443").place(x=168,y=n)
        Label(window5, text=(f"{names_list[i]}         "),font=("Haettenschweiler", 12), fg="White", bg="#454443").place(x=410,y=n)
        Label(window5, text=(f"{Scores_list[i]}                      "),font=("Haettenschweiler", 12), fg="White", bg="#454443").place(x=665,y=n)
        n+=40

#=================Buttons===============#
coti=Button(window5, bg="#454443", image=img3, width=80, height=20 ,command=lambda: [hide(window5), show(window)])

#===============Buttons place========#

coti.place(x=4, y=422)


#==============Windows beginning==========#
window1.withdraw()
window2.withdraw()
window3.withdraw()
window4.withdraw()
window5.withdraw()
window.mainloop()




