"""
IK

@authors:
    Juan Jose Potes Gomez
    Julie Alejandra Ibarra
    Cristian Camilo Jimenez
"""
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np
import copy


# Funcion para pasar angulo de radianes a grados y viceversa
def conv_ang(angulo, tipo):
    if tipo == "rad":
        conv = (angulo * np.pi)/180
        return conv
    if tipo == "grad":
        conv = (angulo * 180)/np.pi
        return conv

# Funcion que grafica un circulo con OpenGL
def circle(xc,yc,radio,clr,nsides):
    n = 0
    glBegin(GL_LINE_STRIP)
    glColor3f(clr[0], clr[1], clr[2])
    while(n <= nsides):
        angle = 2*np.pi*n/nsides
        x = xc+radio*np.cos(angle)
        y = yc+radio*np.sin(angle)
        glVertex2f(x,y)
        n += 1
    glEnd()

# Funcion que grafica una linea con openGL
def linea(x1,y1,x2,y2,clr):
    glBegin(GL_LINES)
    glColor3f(clr[0], clr[1], clr[2])
    glVertex2f(x1,y1)
    glVertex2f(x2,y2)
    glEnd()

# Funcion para graficar el plano 2d de referencia
def plano():
    linea(0,-ejeY,0,ejeY,[0.8,0.8,0.8])
    linea(-ejeX,0,ejeX,0,[0.8,0.8,0.8])
        
# Definicion de clase linea
class Linea:
    # Constructor de la clase
    def __init__(self, p_ini, long, ang, color):
        self.p_ini = p_ini
        self.long = long
        self.ang = ang
        self.color = color
        self.p_fin = [0,0]
        self.calc_fin()
    
    # Metodo que grafica la linea (Cada segmento de la cadena)
    def graficar(self):
        # Se grafican el circulo de la union en el punto final de la linea
        r = 2.0
        while(r > 0):
            # Se grafican multiples circunferencias cada vez mas pequeñas para formar el circulo relleno
            circle(self.p_fin[0],self.p_fin[1], r,[1,1,0],20)
            r -= 0.1
        # Se grafican el circulo que rodea el punto final de la linea 
        circle(self.p_fin[0],self.p_fin[1], 5,self.color,20)
        
        # Se grafican las lineas de los lados
        linea(self.p_ini[0]+5*np.cos(self.ang + (np.pi/2)),self.p_ini[1]+5*np.sin(self.ang + (np.pi/2)),self.p_fin[0]+5*np.cos(self.ang + (np.pi/2)),self.p_fin[1]+5*np.sin(self.ang + (np.pi/2)),self.color)
        linea(self.p_ini[0]+5*np.cos(self.ang - (np.pi/2)),self.p_ini[1]+5*np.sin(self.ang - (np.pi/2)),self.p_fin[0]+5*np.cos(self.ang - (np.pi/2)),self.p_fin[1]+5*np.sin(self.ang - (np.pi/2)),self.color)
    
    # Metodo que cambia el punto inicial de la linea, y posteriormente calcula el nuevo punto final
    def set_ini(self, ini):
        self.p_ini = ini
        self.calc_fin()
    
    # Metodo que calcula el punto final de la linea, teniendo el angulo y el punto inicial
    def calc_fin(self):
        self.p_fin[0] = self.p_ini[0] + (self.long * np.cos(self.ang))
        self.p_fin[1] = self.p_ini[1] + (self.long * np.sin(self.ang))
    
    # Metodo que calcula el punto inicial de la linea, teniendo el angulo y el punto final
    def calc_ini(self):
        self.p_ini[0] = self.p_fin[0] - (self.long * np.cos(self.ang))
        self.p_ini[1] = self.p_fin[1] - (self.long * np.sin(self.ang))
    
    # Metodo para dejar el angulo en el rango de 0 a 2pi radianes
    def arreglar_ang(self):
        if(self.ang < 0):
            self.ang = self.ang + (2*np.pi)
        if(self.ang > (2*np.pi)):
            self.ang = self.ang - (2*np.pi)
    
    # Metodo que gira la linea hacia un punto especifico y luego la desplaza a este punto, moviendo su punto final y calculando un nuevo punto inicial
    def apuntar_y_mover(self,punto):
        # Se cambia al aungulo para apuntar la linea hacia el punto enviado
        dy = punto[1] - self.p_ini[1]
        dx = punto[0] - self.p_ini[0]
        div = dy/dx
        # Si la diferencia en X es negativa, significa que la funcion arctan dara un valor con respecto al eje negativo
        # de las X, por lo que se le suma pi (180 grados) para dejarlo con respecto al eje positivo de las X.
        if(dx < 0):
            angu = np.arctan(div)
            self.ang = angu + np.pi 
        # Si la diferencia en X es positiva pero la diferencia en Y es negativa, la funcion arctan retornara un angulo
        # negativo, por lo que se le suma 2*pi (360 grados) para dejarlo positivo
        elif(dy < 0):
            angu = np.arctan(div)
            self.ang = angu + (2*np.pi)
        else:
            self.ang = np.arctan(div)
            
        # Se traslada el punto final de la linea al nuevo punto y se calcula el nuevo punto inicial
        self.p_fin = punto
        self.calc_ini()
        

# Funcion para graficar las lineas de la cadena
def graficar_sistema(lista):
    # Se grafican las lineas
    for i in range(0, len(lista)):
        lista[i].graficar()
    
    # Se grafica el punto final que selecciono el usuario
    r = 1.0
    while(r > 0):
        # Se grafican multiples circunferencias cada vez mas pequeñas para formar el circulo relleno
        circle(p_final[0],p_final[1],r,[1,0,0],20)
        r -= 0.1
    
# Funcio que retorna la posicion de la seleccion del mouse con respecto al eje coordenado que se esta trabajando
def pos_relativa(pos_vent):
    global ejeX, ejeY, ancho, alto
    posv = [0,0]
    posv[0] = pos_vent[0]
    posv[1] = pos_vent[1]
    resul = [0,0]
    # Se invierte la posicion en Y y se hace regla de 3 para hallar las coordenadas con respecto a los ejes
    posv[1] = alto - posv[1]
    resul[0] = (posv[0] * ejeX) / ancho 
    resul[1] = (posv[1] * ejeY) / alto
    return resul

# Ejes del plano de coordenadas 2D
ejeX = 300
ejeY = 200

ancho = 900
alto = 600

# Propiedades de las lineas
l0 = 50
l1 = 70
l2 = 60
clr = [0,1,1]

# Angulos iniciales
ang0 = conv_ang(90,"rad")
ang1 = conv_ang(30,"rad")
ang2 = conv_ang(70,"rad")

# Se declara la lista de lineas y una lista auxiliar
lineas = np.empty([3], dtype = object)
lineas_aux = np.empty([3], dtype = object)

lineas[0] = Linea([(ejeX/2),0], l0, ang0, clr)
lineas[1] = Linea(copy.deepcopy(lineas[0].p_fin), l1, ang1, clr)
lineas[2] = Linea(copy.deepcopy(lineas[1].p_fin), l2, ang2, clr)

for i in range(0,len(lineas)):
    lineas_aux[i] = copy.deepcopy(lineas[i])

# Se guarda el punto final inicial y el punto que no se mueve
p_fijo = copy.deepcopy(lineas[0].p_fin)
p_final = copy.deepcopy(lineas[2].p_fin)
a1 = lineas_aux[1].ang + conv_ang(90,"rad")
a2 = conv_ang(180,"rad") - (lineas_aux[2].ang - lineas_aux[1].ang)

print("P_f = ", p_final)
print("a1 = ",round(conv_ang(a1,"grad"),3), " grados")
print("a2 = ",round(conv_ang(a2,"grad"),3), " grados")
print("")

# Funcion principal
def main():
    global p_final, p_fijo, l1, l2, lineas, lineas_aux, a1, a2
    running = True
    # Se crea la ventana
    pygame.init()
    display=(ancho,alto)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluOrtho2D(0,ejeX,0,ejeY)
    
    iterac = 10
    inc = [0,0,0]
    nuevo_p = False
    
    # Ciclo para que se vaya visualizando la simulacion
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running=False
                break
            # Si el usuario presiona con el mouse en la ventana se guarda esa posicion y se toma como nuevo punto final
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                p_final = pos_relativa(pos)
                print("P_f = ", p_final)
                nuevo_p = True

        # Se ejecuta hasta que el usuario cierre la ventana
        if(running == True):
            # Se limpia la pantalla de OpenGL
            glFlush()
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            
            # Cuando se selecciona un nuevo punto, se hacen los calculos para saber los nuevos angulos, se guardan en la lista auxiliar
            if(nuevo_p == True):
                
                # Se calcula la distancia del punto final seleccionado al punto fijo
                dist = np.sqrt((p_fijo[0] - p_final[0]) ** 2 + (p_fijo[1] - p_final[1]) ** 2)
                
                # Si esa distancia es mayor a las longitudes de la cadena, significa que no alcanzara a llegar al punto, quedara totalmente estirada
                if(dist < (l1 + l2)):
                    # Si alcanza a llegar al punto
                    error = (abs(p_final[0] - lineas_aux[len(lineas_aux)-1].p_fin[0])) + (abs(p_final[1] - lineas_aux[len(lineas_aux)-1].p_fin[1]))
                    
                    # Se repite el proceso hasta que el punto final de la cadena sea casi igual al punto seleccionado
                    while(error > 0.1):
                        # Se giran y desplazan las lineas desde la ultima hasta la primera
                        lineas_aux[2].apuntar_y_mover(copy.deepcopy(p_final))
                        lineas_aux[1].apuntar_y_mover(lineas_aux[2].p_ini)
                        
                        # Se desplazan las lineas desde la 1 (segunda) hasta la ultima para posicionarlas de nuevo en el punto fijo
                        lineas_aux[1].set_ini(copy.deepcopy(lineas_aux[0].p_fin))
                        lineas_aux[2].set_ini(copy.deepcopy(lineas_aux[1].p_fin))
                        
                        # Se calcula el error para saber que tan cerca quedo del punto final al que se quiere llegar
                        error = (abs(p_final[0] - lineas_aux[len(lineas_aux)-1].p_fin[0])) + (abs(p_final[1] - lineas_aux[len(lineas_aux)-1].p_fin[1]))
                else:
                    # Si la cadena no alcanzara el punto, ya no se calcula el error sino que se realiza el proceso 20 veces para dejar la cadena estirada hacia el punto
                    for j in range (0,20):
                        # Se giran y desplazan las lineas desde la ultima hasta la primera
                        lineas_aux[2].apuntar_y_mover(copy.deepcopy(p_final))
                        lineas_aux[1].apuntar_y_mover(lineas_aux[2].p_ini)
                        
                        # Se desplazan las lineas desde la 1 (segunda) hasta la ultima para posicionarlas de nuevo en el punto fijo
                        lineas_aux[1].set_ini(copy.deepcopy(lineas_aux[0].p_fin))
                        lineas_aux[2].set_ini(copy.deepcopy(lineas_aux[1].p_fin))
                
                # Se calculan las distancias angulares desde los angulos originales a los nuevos angulos
                # Se hallan las distancias angulares en ambos sentidos, para esto se toma el valor negativo del angulo mayor
                # Se toma la menor distancia y se divide en 10 para hallar el valor del incremento que se le dará al angulo para la visualizacion del recorrido
                for i in range(1,len(lineas)):
                    # Si el angulo nuevo es mayor al anterior
                    if(lineas_aux[i].ang > lineas[i].ang):
                        # Distancia angular normal
                        da = (lineas_aux[i].ang - lineas[i].ang)
                        # Distancia angular opuesta, angulo nuevo invertido
                        db = ((lineas_aux[i].ang - 2*np.pi) - lineas[i].ang)
                        # Se toma la menor y se divide por la cantidad de iteraciones
                        if(abs(da) < abs(db)):
                            inc[i] = da / iterac
                        else:
                            inc[i] = db / iterac
                    # Si el angulo nuevo no es mayor al anterior
                    else:
                        # Distancia angular normal
                        da = (lineas_aux[i].ang - lineas[i].ang)
                        # Distancia angular opuesta, angulo anterior invertido
                        db = (lineas_aux[i].ang  - (lineas[i].ang - 2*np.pi))
                        # Se toma la menor y se divide por la cantidad de iteraciones
                        if(abs(da) < abs(db)):
                            inc[i] = da / iterac
                        else:
                            inc[i] = db / iterac
            
            # Se imprimen en consola los angulos entre lineas
            if(nuevo_p == True):
                a1 = lineas_aux[1].ang + conv_ang(90,"rad")
                a2 = conv_ang(180,"rad") - (lineas_aux[2].ang - lineas_aux[1].ang)
                print("a1 = ",round(conv_ang(a1,"grad"),3), " grados")
                print("a2 = ",round(conv_ang(a2,"grad"),3), " grados")
                print("")
            
            # Se van incrementando los angulos hasta llegar muy cerca a los deseados, se revisan las distancias con los angulos normales y con uno u otro invertido
            # En cada iteracion se calculan los nuevos puntos finales
            if(abs(lineas[1].ang - lineas_aux[1].ang) > 0.001 and abs(lineas[1].ang - (lineas_aux[1].ang) - 2*np.pi) > 0.001 and abs((lineas[1].ang - 2*np.pi) - lineas_aux[1].ang) > 0.001):
                lineas[1].ang += inc[1]
                lineas[1].calc_fin()
                lineas[2].set_ini(copy.deepcopy(lineas[1].p_fin))
            
            if(abs(lineas[2].ang - lineas_aux[2].ang) > 0.001 and abs(lineas[2].ang - (lineas_aux[2].ang - 2*np.pi)) > 0.001 and abs((lineas[2].ang - 2*np.pi) - lineas_aux[2].ang) > 0.001):
                lineas[2].ang += inc[2]
                lineas[2].calc_fin()
            
            # Se arreglan los angulos para dejarlos en el rango de 0 a 2pi
            lineas[1].arreglar_ang()
            lineas[2].arreglar_ang()
            
            # Se grafican todas la lineas
            graficar_sistema(lineas)
            
            pygame.time.wait(1)
            pygame.display.flip() # Mostrar pantalla
            nuevo_p = False
        else:
            running = False
            break
    pygame.quit()

main()