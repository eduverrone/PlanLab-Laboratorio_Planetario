import mpmath as mp  # Módulo "Math" que realiza cálculos com maiores precisões e mais dígitos.
from numpy import array
import math
from vpython import *
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

def RastroCM(b):
    if b.checked:
        corpoCM.make_trail=True
    else:
        corpoCM.make_trail=False
        corpoCM.clear_trail()

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

def resolve_EDO_P2C(r, t, M1, M2):
    G = 6.674E-20  # Constante Gravitacional Universal (km³/s²kg)
    x1 = r[0]
    Vx1 = r[1]
    y1 = r[2]
    Vy1 = r[3]
    x2 = r[4]
    Vx2 = r[5]
    y2 = r[6]
    Vy2 = r[7]

    r12 = mp.sqrt((math.fabs(x2 - x1) ** 2) + (math.fabs(y2 - y1) ** 2))
    mod_r12 = float(r12) ** 3

    dx1 = Vx1
    dVx1 = (G * M2 * (x2 - x1) / mod_r12)
    dy1 = Vy1
    dVy1 = (G * M2 * (y2 - y1) / mod_r12)

    dx2 = Vx2
    dVx2 = (G * M1 * (x1 - x2) / mod_r12)
    dy2 = Vy2
    dVy2 = (G * M1 * (y1 - y2) / mod_r12)

    return array([dx1, dVx1, dy1, dVy1, dx2, dVx2, dy2, dVy2], float)


# --------------------------------------------------------------------------------------------------------#

def passo_rk4(f, r, t, h, M1, M2):  # Calcula um passo no método de RK4
    k1 = h * f(r, t, M1, M2)
    k2 = h * f(r + 0.5 * k1, t + 0.5 * h, M1, M2)
    k3 = h * f(r + 0.5 * k2, t + 0.5 * h, M1, M2)
    k4 = h * f(r + k3, t + h, M1, M2)
    return (k1 + 2.0 * (k2 + k3) + k4) / 6.0

def p2c_EDO_animacao():

    titulo("Animação do P2C através da resolução das EDO's do sistema.\n")
    # Condições e valores iniciais do programa

    orientacao("Para a utilização deste programa é necessário informar as massas e também\n"
               "as condições iniciais de ambos os corpos.\n")
    orientacao("A seguir são exibidas algumas sugestões de massa e Condições Iniciais para os objetos.\n")

    cabecalho = ['', 'Sol', 'Terra','|', 'Estrela 1', 'Estrela 2','|', 'Estrela Alpha', 'Estrela Beta','|']
    tabela = [['Massa (Massas Solares)', 1, 2.980E-6, '|', 1, 0.1, '|', 1, 1, '|'],
              ['Posição X (U.A.)', 0, 1, '|', 0, 1, '|', -0.5, 0.5, '|'],
              ['Posição Y (U.A.)', 0, 0, '|', 0, 0, '|', 0, 0, '|'],
              ['Velocidade X (km/s)', 0, 0, '|', 0, 0, '|', 0, 0, '|'],
              ['Velocidade Y (km/s)', 0, 30, '|', 0, 35, '|', -25, 20, '|']]
    print(tabulate(tabela, headers=cabecalho))
    verdade = True
    sistema = 5
    while verdade:
        print("\nPara simular o sistema:\n"
              "    *Sol - Terra ------------------> digite 1\n"
              "    *Estrela 1 - Estrela 2 --------> digite 2\n"
              "    *Estrela Alpha - Estrela Beta -> digite 3\n"
              "    *Para simular outro sistema ---> digite 0")
        sistema = input("\nEscolha:")
        try:
            sistema = int(sistema)
            if sistema in range(0, 4):
                verdade = False
        except:
            print("Valor inválido! Digite novamente.")

    if sistema == 1:
        M1, x0_1, y0_1, Vx0_1, Vy0_1 = 1.9891E30, 0, 0, 0, 0
        M2, x0_2, y0_2, Vx0_2, Vy0_2 = 6E24, 149597870.70, 0, 0, 30

    elif sistema == 2:
        M1, x0_1, y0_1, Vx0_1, Vy0_1 = 1.9891E30, 0, 0, 0, 0
        M2, x0_2, y0_2, Vx0_2, Vy0_2 = 1.9891E29, 149597870.70, 0, 0, 35

    elif sistema == 3:
        M1, x0_1, y0_1, Vx0_1, Vy0_1 = 1.9891E30, -74798935.35, 0, 0, -25
        M2, x0_2, y0_2, Vx0_2, Vy0_2 = 1.9891E30, 74798935.35, 0, 0, 20

    else:
        # Corpo 01
        orientacao('\nCondições Iniciais do Corpo 01:')
        M1 = 1.9891E30 * float(input("Digite o valor da massa do Corpo 01 (em Massas Solares): "))  # Massa do Corpo 01 (kg)
        x0_1 = float(input("Digite o valor da posição em x do Corpo 01 (em U.A.): ")) * 149597870.7  # Posição no eixo x do Corpo 01 (U.A.)
        y0_1 = float(input("Digite o valor da posição em y do Corpo 01 (em U.A.): ")) * 149597870.7  # Posição do eixo y do Corpo 01 (U.A.)
        Vx0_1 = float(input("Digite o valor da velocidade em x do Corpo 01 (em km/s): "))  # Componente x da velocidade do Corpo 01 (km/s)
        Vy0_1 = float(input("Digite o valor da velocidade em y do Corpo 01 (em km/s): "))  # Componente y da velocidade do Corpo 01 (km/s)

        # Corpo 02
        orientacao('\nCondições Iniciais do Corpo 02:')
        M2 = 1.9891E30 * float(input("Digite o valor da massa do Corpo 02 (em Massas Solares): "))  # Massa do Corpo 02 (kg)
        x0_2 = float(input("Digite o valor da posição em x do Corpo 02 (em U.A.): ")) * 149597870.7  # Posição no eixo x do Corpo 02 (U.A.)
        y0_2 = float(input("Digite o valor da posição em y do Corpo 02 (em U.A.): ")) * 149597870.7  # Posição do eixo y do Corpo 02 (U.A.)
        Vx0_2 = float(input("Digite o valor da velocidade em x do Corpo 02 (em km/s): "))  # Componente x da velocidade do Corpo 02 (km/s)
        Vy0_2 = float(input("Digite o valor da velocidade em y do Corpo 02 (em km/s): "))  # Componente y da velocidade do Corpo 02 (km/s)
    ra = array([x0_1, Vx0_1, y0_1, Vy0_1, x0_2, Vx0_2, y0_2, Vy0_2])
    r = ra

    # Centro de Massa
    X_CM = ((r[0] * M1) + (r[4] * M2)) / (M1 + M2)
    Y_CM = ((r[2] * M1) + (r[6] * M2)) / (M1 + M2)

    CM = [X_CM, Y_CM]

    # Tempo
    ti = 0
    h = 24 * 3600  # Taxa de atualização
    t = ti

    # --------------------------------------------------------------------------------------------------------#
    # Definições da cena
    global camval, showlabel, running, pausar, corpo1, corpo2, label1, label2, corpoCM, labelCM
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
    check3 = checkbox(bind=RastroCM, text='Rastro CM', checked=True)
    scene.append_to_caption("\n   ")
    check4=checkbox(bind=Nomes, text='Exibir nomes', checked=True)
    scene.append_to_caption("\n\n")
    scene.append_to_caption('    Camera: Observador')
    """menu(choices=['Observador', 'CM'], index=0, bind=Cameras)"""

    #Criando os objetos:
    raio = (x0_2-x0_1)//5

    corpo1 = sphere(trail_color=color.orange, texture='sol.jpg', radius=int(3*raio/4), pos=vector(x0_1, y0_1, 0), make_trail=True,
                    interval=5, retain=200)
    corpo1.emissive = True
    label1 = label(pos=corpo1.pos+vector(0,1.5*corpo1.radius,0), text='Corpo 1', box=0, opacity=0, color=color.white)
    corpo1.massa = M1

    corpo2 = sphere(color=vector(0.076, 0.733, 0.902), texture='sirius.jpg', radius=int(raio/2), pos=vector(x0_2, y0_2, 0), make_trail=True,
                       interval=5, retain=200)
    corpo2.emissive = True
    label2 = label(pos=corpo2.pos+vector(0,1.5*corpo2.radius,0), text='Corpo 2', box=0, opacity=0, color=color.white)
    corpo2.massa = M2

    corpoCM = sphere(color=color.white, radius=int(raio/10), pos=vector(X_CM, Y_CM, 0), make_trail=True,
                    trail_type='points', interval=20)

    labelCM = label(pos=corpoCM.pos + vector(0, 1.5 * corpo2.radius, 0), text='CM', box=0, opacity=0,
                   color=color.white)

    # --------------------------------------------------------------------------------------------------------#

    # Laço de realização dos Cálculos:
    while True:
        if running:
            rate(20)
            # Corpo 01
            corpo1.pos = vector(r[0], r[2], 0)

            # Corpo 02
            corpo2.pos = vector(r[4], r[6], 0)

            dr = passo_rk4(resolve_EDO_P2C, r, t, h, M1, M2)
            r = r + dr
            t = t + h

            # Centro de Massa
            X_CM = ((r[0] * M1) + (r[4] * M2)) / (M1 + M2)
            Y_CM = ((r[2] * M1) + (r[6] * M2)) / (M1 + M2)

            CM = [X_CM, Y_CM]

            # CM
            corpoCM.pos = vector(CM[0], CM[1], 0)

            if showlabel == True:
                label1.visible=True
                label2.visible=True
                labelCM.visible = True
                label1.pos = corpo1.pos+vector(0,1.5*corpo1.radius,0)
                label2.pos = corpo2.pos+vector(0,1.5*corpo2.radius,0)
                labelCM.pos = corpoCM.pos + vector(0, 1.5 * corpoCM.radius, 0)
            else:
                label1.visible=False
                label2.visible=False
                labelCM.visible = False

            """# Camera
            if camval == "Origem":
                scene.center = vector(0, 0, 0)
            elif camval == "CM":
                scene.center = vector(CM[0], CM[1], 0)"""



if __name__ == '__main__':
    p2c_EDO_animacao()

