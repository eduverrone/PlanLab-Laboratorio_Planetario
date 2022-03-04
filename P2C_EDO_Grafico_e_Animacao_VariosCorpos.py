import mpmath as mp  # Módulo "Math" que realiza cálculos com maiores precisões e mais dígitos.
from numpy import array
import math
from vpython import *


def aviso(texto):
    print(f"\u001b[31m{texto}\u001b[0m")

def verde(texto):
    print(f"\u001b[32m{texto}\u001b[0m")

def orientacao(texto):
    print(f"\u001b[33m{texto}\u001b[0m")

def titulo(texto):
    print(f"\u001b[34m{texto}\u001b[0m")


def Rodar(evt):
    global running, pausar
    running = not running
    if running: pausar.text = "Pausar"
    else: pausar.text = "Continuar"

# Checkbox para rastros

def Rastro1(b):
    if b.checked:
        corpo1.make_trail=True
    else:
        corpo1.make_trail=False
        corpo1.clear_trail()

def Rastro2(b):
    if b.checked:
        corpo2.make_trail=True
    else:
        corpo2.make_trail=False
        corpo2.clear_trail()

def Rastro3(b):
    if b.checked:
        corpo3.make_trail=True
    else:
        corpo3.make_trail=False
        corpo3.clear_trail()

def Rastro4(b):
    if b.checked:
        corpo4.make_trail=True
    else:
        corpo4.make_trail=False
        corpo4.clear_trail()

def Nomes(b):
    global showlabel
    if b.checked:
        showlabel = True
        label1.visible=True
        label2.visible=True
    else:
        showlabel = False
        label1.visible=False
        label2.visible=False

def Cameras(cam):
    global camval
    camval = cam.selected
# Intruções para criação da cena animada


# Função com as Equações diferenciais a serem resolvidas:

def resolve_EDO_P2C(r, t, MC, M):
    G = 6.674E-20  # Constante Gravitacional Universal (km³/s²kg)
    x = r[0]
    Vx = r[1]
    y = r[2]
    Vy = r[3]

    r12 = mp.sqrt((math.fabs(x) ** 2) + (math.fabs(y) ** 2))
    mod_r12 = float(r12) ** 3

    dx = Vx
    dVx = (-G * MC * x / mod_r12)
    dy = Vy
    dVy = (-G * MC * y / mod_r12)

    return array([dx, dVx, dy, dVy], float)


# --------------------------------------------------------------------------------------------------------#

def passo_rk4(f, r, t, h, M1, M2):  # Calcula um passo no método de RK4
    k1 = h * f(r, t, M1, M2)
    k2 = h * f(r + 0.5 * k1, t + 0.5 * h, M1, M2)
    k3 = h * f(r + 0.5 * k2, t + 0.5 * h, M1, M2)
    k4 = h * f(r + k3, t + h, M1, M2)
    return (k1 + 2.0 * (k2 + k3) + k4) / 6.0


def p2c_EDO_Grafico_e_Animacao_VariosCorpos():

    titulo("Simulação do P2C através da resolução das EDO's do sistema para Vários Corpos.\n")
    orientacao("Para informar as massas e condições iniciais individualmente para cada um dos objetos, digite 1;\n"
               "Para os mesmos valores de massa e condições iniciais, digite 2. ")
    verdadeiro = True

    while verdadeiro:
        aux = int(input("Opção: "))
        if aux in range(1, 3):
            verdadeiro = False
            print()
        else:
            print("Valor incorreto! Escolha novamente.")

    if aux == 2:
        MC = 1.9891E30 * float(input("Digite o valor da massa do Corpo Central (em Massas Solares): "))  # Massa do Corpo Central (kg)
        M = 1.9891E30 * float(
            input("Digite o valor da massa dos Corpos Teste (em Massas Solares): "))  # Massa do Corpo 01 (kg)
        x0 = float(input(
            "Digite o valor da posição em x dos Corpos Teste (em U.A.): ")) * 149597870.7  # Posição no eixo x do Corpo 01 (U.A.)
        y0 = float(input(
            "Digite o valor da posição em y dos Corpos Teste (em U.A.): ")) * 149597870.7  # Posição do eixo y do Corpo 01 (U.A.)
        V = float(input(
            "Digite o valor do módulo da velocidade dos Corpos Teste (em km/s): "))  # Componente x da velocidade do Corpo 01 (km/s)

        M1, M2, M3, M4 = M, M, M, M

        raC1 = array([x0, V * mp.cos(mp.pi/2), y0, V * mp.sin(mp.pi/2)])
        raC2 = array([x0, V * mp.cos(1.25), y0, V * mp.sin(1.25)])
        raC3 = array([x0, - V * mp.cos(1.25), y0, V * mp.sin(1.25)])
        raC4 = array([x0, - V * mp.cos(mp.pi/4), y0,  V * mp.sin(mp.pi/4)])

    else:
        # Condições e valores iniciais do programa

        orientacao("Será necessário informar as massas e também"
                   "as condições iniciais de todos os corpos.\n")

        # Corpo Central
        MC = 1.9891E30 * float(input("Digite o valor da massa do Corpo Central (em Massas Solares): "))  # Massa do Corpo Central (kg)

        # Corpo 01
        orientacao('\nCondições Iniciais do Corpo 01:')
        M1 = 1.9891E30 * float(input("Digite o valor da massa do Corpo 01 (em Massas Solares): "))  # Massa do Corpo 01 (kg)
        x0_1 = float(input("Digite o valor da posição em x do Corpo 01 (em U.A.): ")) * 149597870.7        # Posição no eixo x do Corpo 01 (U.A.)
        y0_1 = float(input("Digite o valor da posição em y do Corpo 01 (em U.A.): ")) * 149597870.7       # Posição do eixo y do Corpo 01 (U.A.)
        Vx0_1 = float(input("Digite o valor da velocidade em x do Corpo 01 (em km/s): "))       # Componente x da velocidade do Corpo 01 (km/s)
        Vy0_1 = float(input("Digite o valor da velocidade em y do Corpo 01 (em km/s): "))       # Componente y da velocidade do Corpo 01 (km/s)
        raC1 = array([x0_1, Vx0_1, y0_1, Vy0_1])


        # Corpo 02
        orientacao('\nCondições Iniciais do Corpo 02:')
        M2 = 1.9891E30 * float(input("Digite o valor da massa do Corpo 02 (em Massas Solares): "))     # Massa do Corpo 02 (kg)
        x0_2 = float(input("Digite o valor da posição em x do Corpo 02 (em U.A.): ")) * 149597870.7  # Posição no eixo x do Corpo 02 (U.A.)
        y0_2 = float(input("Digite o valor da posição em y do Corpo 02 (em U.A.): ")) * 149597870.7           # Posição do eixo y do Corpo 02 (U.A.)
        Vx0_2 = float(input("Digite o valor da velocidade em x do Corpo 02 (em km/s): "))          # Componente x da velocidade do Corpo 02 (km/s)
        Vy0_2 = float(input("Digite o valor da velocidade em y do Corpo 02 (em km/s): "))         # Componente y da velocidade do Corpo 02 (km/s)
        raC2 = array([x0_2, Vx0_2, y0_2, Vy0_2])


        # Corpo 03
        orientacao('\nCondições Iniciais do Corpo 03:')
        M3 = 1.9891E30 * float(input("Digite o valor da massa do Corpo 03 (em Massas Solares): "))  # Massa do Corpo 03 (U.A.)
        x0_3 = float(input("Digite o valor da posição em x do Corpo 03 (em U.A.): ")) * 149597870.7  # Posição no eixo x do Corpo 03 (U.A.)
        y0_3 = float(input("Digite o valor da posição em y do Corpo 03 (em U.A.): ")) * 149597870.7  # Posição do eixo y do Corpo 03 (km)
        Vx0_3 = float(input("Digite o valor da velocidade em x do Corpo 03 (em km/s): "))  # Componente x da velocidade do Corpo 03 (km/s)
        Vy0_3 = float(input("Digite o valor da velocidade em y do Corpo 03 (em km/s): "))  # Componente y da velocidade do Corpo 03 (km/s)
        raC3 = array([x0_3, Vx0_3, y0_3, Vy0_3])

        # Corpo 04
        orientacao('\nCondições Iniciais do Corpo 04:')
        M4 = 1.9891E30 * float(input("Digite o valor da massa do Corpo 04 (em Massas Solares): "))  # Massa do Corpo 04 (kg)
        x0_4 = float(input("Digite o valor da posição em x do Corpo 04 (em U.A.): ")) * 149597870.7  # Posição no eixo x do Corpo 04 (U.A.)
        y0_4 = float(input("Digite o valor da posição em y do Corpo 04 (em U.A.): ")) * 149597870.7  # Posição do eixo y do Corpo 04 (U.A.)
        Vx0_4 = float(input("Digite o valor da velocidade em x do Corpo 04 (em km/s): "))  # Componente x da velocidade do Corpo 04 (km/s)
        Vy0_4 = float(input("Digite o valor da velocidade em y do Corpo 04 (em km/s): "))  # Componente y da velocidade do Corpo 04 (km/s
        raC4 = array([x0_4, Vx0_4, y0_4, Vy0_4])

    rC1 = raC1
    rC2 = raC2
    rC3 = raC3
    rC4 = raC4

    # Tempo
    ti = 0
    h = 24 * 3600  # Taxa de atualização
    t = ti

    # --------------------------------------------------------------------------------------------------------#
    # Definições da cena
    global camval, showlabel, running, pausar, corpo1, corpo2, label1, label2, corpo3, corpo4, label3, label4
    scene.width = 800  # Ajustando a largura da cena
    scene.height = 600  # Ajustando a altura da cena

    camval = 'Centralizada'
    showlabel = True
    running = False
    scene.align = 'left'
    scene.forward = vector(0, 0, -5)
    scene.bind('click', Rodar)

    ##### BOTÕES DA ANIMAÇÃO #####
    scene.append_to_caption("   ")
    pausar=button(text="Rodar", bind=Rodar)
    scene.append_to_caption("\n\n   ")
    check1=checkbox(bind=Rastro1, text='Rastro 1', checked=True)
    scene.append_to_caption("\n   ")
    check2=checkbox(bind=Rastro2, text='Rastro 2', checked=True)
    scene.append_to_caption("\n   ")
    check3 = checkbox(bind=Rastro3, text='Rastro 3', checked=True)
    scene.append_to_caption("\n   ")
    check4 = checkbox(bind=Rastro4, text='Rastro 4', checked=True)
    scene.append_to_caption("\n   ")
    check5=checkbox(bind=Nomes, text='Exibir nomes', checked=True)
    scene.append_to_caption("\n\n")
    scene.append_to_caption('    Camera:')
    menu(choices=['Origem', 'Corpo 1', 'Corpo 2', 'Corpo 3', 'Corpo 4'], index=0, bind=Cameras)

    #Criando os objetos:
    raio = rC4[0]//10

    corpoC = sphere(color=color.yellow, texture='sol.jpg', radius=raio, pos=vector(0, 0, 0),
                    make_trail=True,
                    interval=5, retain=115)
    corpoC.emissive = True
    labelC = label(pos=corpoC.pos + vector(0, 1.5 * corpoC.radius, 0), text='Corpo C', box=0, opacity=0,
                   color=color.white)
    corpoC.massa = MC


    corpo1 = sphere(texture=textures.rock, radius=raio, pos=vector(rC1[0], rC1[2], 0), make_trail=True,
                    interval=5, retain=115)
    corpo1.emissive = True
    label1 = label(pos=corpo1.pos+vector(0,1.5*corpo1.radius,0), text='Corpo 1', box=0, opacity=0, color=color.white)
    corpo1.massa = M1

    corpo2 = sphere(texture=textures.gravel, radius=int(raio/2), pos=vector(rC2[0], rC2[2], 0), make_trail=True,
                       trail_type='points', interval=5, retain=115)
    corpo2.emissive = True
    label2 = label(pos=corpo2.pos+vector(0,1.5*corpo2.radius,0), text='Corpo 2', box=0, opacity=0, color=color.white)
    corpo2.massa = M2

    corpo3 = sphere(texture=textures.wood, radius=raio, pos=vector(rC3[0], rC3[2], 0),
                    make_trail=True,
                    interval=5, retain=115)
    corpo3.emissive = True
    label3 = label(pos=corpo3.pos + vector(0, 1.5 * corpo3.radius, 0), text='Corpo 3', box=0, opacity=0,
                   color=color.white)
    corpo3.massa = M3

    corpo4 = sphere(texture=textures.granite, radius=int(raio / 2), pos=vector(rC4[0], rC4[2], 0), make_trail=True,
                    trail_type='points', interval=5, retain=115)
    corpo4.emissive = True
    label4 = label(pos=corpo4.pos + vector(0, 1.5 * corpo4.radius, 0), text='Corpo 4', box=0, opacity=0,
                   color=color.white)
    corpo4.massa = M4
    # --------------------------------------------------------------------------------------------------------#

    # Laço de realização dos Cálculos:
    while True:
        if running:
            rate(20)
            # Corpo 01
            corpo1.pos = vector(rC1[0], rC1[2], 0)
            dr1 = passo_rk4(resolve_EDO_P2C, rC1, t, h, MC, M1)
            rC1 = rC1 + dr1

            # Corpo 02
            corpo2.pos = vector(rC2[0], rC2[2], 0)
            dr2 = passo_rk4(resolve_EDO_P2C, rC2, t, h, MC, M2)
            rC2 = rC2 + dr2

            # Corpo 03
            corpo3.pos = vector(rC3[0], rC3[2], 0)
            dr3 = passo_rk4(resolve_EDO_P2C, rC3, t, h, MC, M3)
            rC3 = rC3 + dr3

            # Corpo 04
            corpo4.pos = vector(rC4[0], rC4[2], 0)
            dr4 = passo_rk4(resolve_EDO_P2C, rC4, t, h, MC, M4)
            rC4 = rC4 + dr4

            t = t + h
            if showlabel == True:
                label1.visible=True
                label2.visible=True
                label3.visible = True
                label4.visible = True
                label1.pos = corpo1.pos+vector(0,1.5*corpo1.radius,0)
                label2.pos = corpo2.pos+vector(0,1.5*corpo2.radius,0)
                label3.pos = corpo3.pos + vector(0, 1.5 * corpo3.radius, 0)
                label4.pos = corpo4.pos + vector(0, 1.5 * corpo4.radius, 0)
            else:
                label1.visible=False
                label2.visible=False
                label3.visible = False
                label4.visible = False

            # Camera
            if camval == "Origem":
                scene.center = vector(0,0,0)
            elif camval == "Corpo 1":
                scene.center = corpo1.pos
            elif camval == "Corpo 2":
                scene.center = corpo2.pos
            elif camval == "Corpo 3":
                scene.center = corpo3.pos
            elif camval == "Corpo 4":
                scene.center = corpo4.pos


if __name__ == '__main__':
    p2c_EDO_Grafico_e_Animacao_VariosCorpos()

