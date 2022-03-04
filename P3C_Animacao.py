from numpy import *
from vpython import*
import math as math
import mpmath as mp  # Módulo "Math" que realiza cálculos com maiores precisões e mais dígitos.
from tabulate import tabulate


def aviso(texto):
    print(f"\u001b[31m{texto}\u001b[0m")

def verde(texto):
    print(f"\u001b[32m{texto}\u001b[0m")

def orientacao(texto):
    print(f"\u001b[33m{texto}\u001b[0m")

def titulo(texto):
    print(f"\u001b[34m{texto}\u001b[0m")


def Rodar(evt):
    global running
    running = not running
    if running:
        pausar.text = "Pausar"
    else:
        pausar.text = "Continuar"

# Checkbox para rastros

def Rastro1(b):
    if b.checked:
        corpo1.make_trail = True
    else:
        corpo1.make_trail = False
        corpo1.clear_trail()

def Rastro2(b):
    if b.checked:
        corpo2.make_trail = True
    else:
        corpo2.make_trail = False
        corpo2.clear_trail()

def Rastro3(b):
    if b.checked:
        corpo3.make_trail = True
    else:
        corpo3.make_trail = False
        corpo3.clear_trail()

def Nomes(b):
    global showlabel
    if b.checked:
        showlabel = True
        label1.visible = True
        label2.visible = True
        label3.visible = True
    else:
        showlabel = False
        label1.visible = False
        label2.visible = False
        label3.visible = False


def Cameras(cam):
    global camval
    camval = cam.selected

# Função com as Equações diferenciais a serem resolvidas: ---------------------------------------------------------------
def f(r, t, M1, M2, M3):
    global G
    x1 = r[0]
    Vx1 = r[1]
    y1 = r[2]
    Vy1 = r[3]
    x2 = r[4]
    Vx2 = r[5]
    y2 = r[6]
    Vy2 = r[7]
    x3 = r[8]
    Vx3 = r[9]
    y3 = r[10]
    Vy3 = r[11]

    r12 = mp.sqrt((math.fabs(x2 - x1) ** 2) + (math.fabs(y2 - y1) ** 2))
    mod_r12 = float(r12) ** 3

    r13 = mp.sqrt((math.fabs(x3 - x1) ** 2) + (math.fabs(y3 - y1) ** 2))
    mod_r13 = float(r13) ** 3

    r23 = mp.sqrt((math.fabs(x3 - x2) ** 2) + (math.fabs(y3 - y2) ** 2))
    mod_r23 = float(r23) ** 3

    dx1 = Vx1
    dVx1 = (G*M2 * (x2 - x1) / mod_r12) + (G*M3 * (x3 - x1) / mod_r13)
    dy1 = Vy1
    dVy1 = (G*M2 * (y2 - y1) / mod_r12) + (G*M3 * (y3 - y1) / mod_r13)

    dx2 = Vx2
    dVx2 = (G*M1 * (x1 - x2) / mod_r12) + (G*M3 * (x3 - x2) / mod_r23)
    dy2 = Vy2
    dVy2 = (G*M1 * (y1 - y2) / mod_r12) + (G*M3 * (y3 - y2) / mod_r23)

    dx3 = Vx3
    dVx3 = (G*M2 * (x2 - x3) / mod_r23) + (G*M1 * (x1 - x3) / mod_r13)
    dy3 = Vy3
    dVy3 = (G*M2 * (y2 - y3) / mod_r23) + (G*M1 * (y1 - y3) / mod_r13)

    return array([dx1, dVx1, dy1, dVy1, dx2, dVx2, dy2, dVy2, dx3, dVx3, dy3, dVy3], float)

# --------------------------------------------------------------------------------------------------------#

def passo_rk4(f, r, t, h, M1, M2, M3):  # Calcula um passo no método de RK4
    k1 = h * f(r, t, M1, M2, M3)
    k2 = h * f(r + 0.5 * k1, t + 0.5 * h, M1, M2, M3)
    k3 = h * f(r + 0.5 * k2, t + 0.5 * h, M1, M2, M3)
    k4 = h * f(r + k3, t + h, M1, M2, M3)
    return (k1 + 2.0 * (k2 + k3) + k4) / 6.0


# --------------------------------------------------------------------------------------------------------#

def p3c_animacao():
    global G, camval, showlabel, running, pausar, corpo1, corpo2, label1, label2, corpo3, label3

    # Condições e valores iniciais do programa
    titulo('Simulação animada do Problema de 3 Corpos\n')

    orientacao("Para a utilização deste programa é necessário informar as massas e também\n"
               "as condições iniciais dos três corpos.\n")
    orientacao("A seguir são exibidas algumas sugestões de massa e Condições Iniciais para os objetos.\n")

    cabecalho = ['', 'Sol', 'Terra', 'Vênus',                   '|', 'Sol', 'Terra', 'Marte', '|', 'Sol', 'Marte', 'Júpiter', '|']
    tabela = [['Massa (Massas Solares)', 1, 2.980E-6, 2.447E-6, '|', 1, 2.980E-6, 3.213E-7,   '|', 1, 3.213E-7, 9.542E-4, '|'],
              ['Posição X (U.A.)',       0, 1, 0,               '|', 0, 1, -1.38,             '|', 0, -1.38, 4.95, '|'],
              ['Posição Y (U.A.)',       0, 0, 0.73,            '|', 0, 0, 0,                 '|', 0, 0, 0, '|'],
              ['Velocidade X (km/s)',    0, 0, -35.26,          '|', 0, 0, 0,                 '|', 0, 0, 0, '|'],
              ['Velocidade Y (km/s)',    0, 30.29, 0,           '|', 0, 30.29, -26.5,         '|', 0, -26.5, 13.72, '|']]
    print(tabulate(tabela, headers=cabecalho))

    verdade = True
    sistema = 5
    while verdade:
        print("\nPara simular o sistema:\n"
              "    *Sol-Terra-Vênus ---> digite 1\n"
              "    *Sol-Terra-Marte ---> digite 2\n"
              "    *Sol-Marte-Júpiter -> digite 3\n"
              "    *Para simular outro sistema -> digite 0")
        sistema = input("\nEscolha:")
        try:
            sistema = int(sistema)
            if sistema in range(0, 4):
                verdade = False
        except:
            print("Valor inválido! Digite novamente.")

    if sistema == 1:
        M1, x0_1, y0_1, Vx0_1, Vy0_1 = 1.9891e+30, 0, 0, 0, 0
        M2, x0_2, y0_2, Vx0_2, Vy0_2 = 5.927e+24, 147098073.4, 0, 0, 30.29
        M3, x0_3, y0_3, Vx0_3, Vy0_3 = 4.867e+24, 0, 107476139.13, -35.26, 0

    elif sistema == 2:
        M1, x0_1, y0_1, Vx0_1, Vy0_1 = 1.9891e+30, 0, 0, 0, 0
        M2, x0_2, y0_2, Vx0_2, Vy0_2 = 5.927e+24, 147098073.4, 0, 0, 30.29
        M3, x0_3, y0_3, Vx0_3, Vy0_3 = 6.39e+23, -206668962.88, 0, 0, -26.5

    elif sistema == 3:
        M1, x0_1, y0_1, Vx0_1, Vy0_1 = 1.9891e+30, 0, 0, 0, 0
        M2, x0_2, y0_2, Vx0_2, Vy0_2 = 6.39e+23, -206668962.88, 0, 0, -26.5
        M3, x0_3, y0_3, Vx0_3, Vy0_3 = 1.898e+27, 740573560.32, 0, 0, 13.72

    else:
        # Corpo 01
        orientacao('\nCondições Iniciais do Corpo 01:')
        M1 = 1.9891E30 * float(input("Qual a massa do primeiro corpo (em Massas Solares)? "))
        x0_1 = float(input("Qual a posição inicial na coordenada x do corpo (em U.A.)? ")) * 149597870.70
        y0_1 = float(input("Qual a posição inicial na coordenada y do corpo (em U.A.)? ")) * 149597870.70
        Vx0_1 = float(input("Qual a velocidade inicial na coordenada x do corpo (em km/s)? "))
        Vy0_1 = float(input("Qual a velocidade inicial na coordenada y do corpo (em km/s)? "))

        # Corpo 02
        orientacao('\nCondições Iniciais do Corpo 02:')
        M2 = 1.9891E30 * float(input("Qual a massa do segundo corpo (em Massas Solares)? "))
        x0_2 = float(input("Qual a posição inicial na coordenada x do corpo (em U.A.)? ")) * 149597870.70
        y0_2 = float(input("Qual a posição inicial na coordenada y do corpo (em U.A.)? ")) * 149597870.70
        Vx0_2 = float(input("Qual a velocidade inicial na coordenada x do corpo (em km/s)? "))
        Vy0_2 = float(input("Qual a velocidade inicial na coordenada y do corpo (em km/s)? "))

        # Corpo 03
        orientacao('\nCondições Iniciais do Corpo 03:')
        M3 = 1.9891E30 * float(input("Qual a massa do terceiro corpo (em Massas Solares)? "))
        x0_3 = float(input("Qual a posição inicial na coordenada x do corpo (em U.A.)? ")) * 149597870.70
        y0_3 = float(input("Qual a posição inicial na coordenada y do corpo (em U.A.)? ")) * 149597870.70
        Vx0_3 = float(input("Qual a velocidade inicial na coordenada x do corpo (em km/s)? "))
        Vy0_3 = float(input("Qual a velocidade inicial na coordenada y do corpo (em km/s)? "))

    G = 6.674E-20  # Constante Gravitacional Universal (m³/s²kg)

    ra = array([x0_1, Vx0_1, y0_1, Vy0_1, x0_2, Vx0_2, y0_2, Vy0_2, x0_3, Vx0_3, y0_3, Vy0_3])
    r = ra

    # Tempo
    t = 0
    h = 24*3600
    # Intruções para criação da cena animada

    scene.width = 800  # Ajustando a largura da cena
    scene.height = 600  # Ajustando a altura da cena

    # Definições da cena
    camval = 'Centralizada'
    showlabel = True
    running = False
    scene.align='left'
    scene.forward = vector(0, 0, -5)
    scene.bind('click', Rodar)

    ##### BOTÕES DA ANIMAÇÃO #####
    scene.append_to_caption(" ")
    pausar = button(text="Rodar", bind=Rodar)
    scene.append_to_caption("\n\n ")
    check1 = checkbox(bind=Rastro1, text='Rastro 1', checked=True)
    check2 = checkbox(bind=Rastro2, text='Rastro 2', checked=True)
    check3 = checkbox(bind=Rastro3, text='Rastro 3', checked=True)
    scene.append_to_caption("\n\n ")
    check4 = checkbox(bind=Nomes, text='Exibir nomes', checked=True)
    scene.append_to_caption('\n\n Camera:')
    menu(choices=['Origem', 'CM', 'Corpo 1', 'Corpo 2', 'Corpo 3'], index=0, bind=Cameras)

    raio = (x0_2 - x0_1) // 5

    corpo1 = sphere(trail_color=color.orange, texture='sol.jpg', radius=int(3 * raio / 4), pos=vector(x0_1, y0_1, 0),
                    make_trail=True, interval=5)
    corpo1.emissive = True
    label1 = label(pos=corpo1.pos + vector(0, 1.5 * corpo1.radius, 0), text='Corpo 1', box=0, opacity=0,
                   color=color.white)
    corpo1.massa = M1

    corpo2 = sphere(color=vector(0.076, 0.733, 0.902), texture='sirius.jpg', radius=int(raio / 2),
                    pos=vector(x0_2, y0_2, 0), make_trail=True, interval=5)
    corpo2.emissive = True
    label2 = label(pos=corpo2.pos + vector(0, 1.5 * corpo2.radius, 0), text='Corpo 2', box=0, opacity=0,
                   color=color.white)
    corpo2.massa = M2

    corpo3 = sphere(texture=textures.gravel, radius=int(raio / 3), pos=vector(x0_3, y0_3, 0), make_trail=True,
                    interval=5)
    corpo3.emissive = True
    label3 = label(pos=corpo3.pos + vector(0, 2 * corpo3.radius, 0), text='Corpo 3', box=0, opacity=0,
                   color=color.white)
    corpo3.massa = M3
    # --------------------------------------------------------------------------------------------------------#

    # Laço de realização dos Cálculos:
    while True:
        if running:
            rate(40)
            # Corpo 01
            corpo1.pos = vector(r[0], r[2], 0)

            # Corpo 02
            corpo2.pos = vector(r[4], r[6], 0)

            # Corpo 03
            corpo3.pos = vector(r[8], r[10], 0)

            dr = passo_rk4(f, r, t, h, M1, M2, M3)
            r = r + dr
            t = t + h
            if showlabel == True:
                label1.visible = True
                label2.visible = True
                label3.visible = True
                label1.pos = corpo1.pos + vector(0, 1.5 * corpo1.radius, 0)
                label2.pos = corpo2.pos + vector(0, 1.5 * corpo2.radius, 0)
                label3.pos = corpo3.pos + vector(0, 2 * corpo3.radius, 0)
            else:
                label1.visible = False
                label2.visible = False
                label3.visible = False

            # Centro de Massa
            CM = (corpo1.pos * corpo1.massa + corpo2.pos * corpo2.massa + corpo3.pos * corpo3.massa) / (corpo1.massa + corpo2.massa + corpo3.massa)
            # Camera
            if camval == "Origem":
                scene.center = vector(0, 0, 0)
            elif camval == "CM":
                scene.center = CM
            elif camval == "Corpo 1":
                scene.center = corpo1.pos
            elif camval == "Corpo 2":
                scene.center = corpo2.pos
            elif camval == "Corpo 3":
                scene.center = corpo3.pos

# --------------------------------------------------------------------------------------------------------#

if __name__ == '__main__':
    p3c_animacao()

