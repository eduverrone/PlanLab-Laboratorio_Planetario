from numpy import *
from vpython import*
from tabulate import tabulate
import math as math
import mpmath as mp  # Módulo "Math" que realiza cálculos com maiores precisões e mais dígitos.


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
    if running: pausar.text = "Pausar"
    else: pausar.text = "Continuar"


def Rastro3(b):
    if b.checked:
        corpo3.make_trail=True
    else:
        corpo3.make_trail=False
        corpo3.clear_trail()

def Nomes(b):
    global showlabel
    if b.checked:
        showlabel = True
        label1.visible=True
        label2.visible=True
        label3.visible = True
    else:
        showlabel = False
        label1.visible=False
        label2.visible=False
        label3.visible = False

# Função com as Equações diferenciais a serem resolvidas: ---------------------------------------------------------------
def f(r, t):
    global mu
    x3 = r[0]
    Vx3 = r[1]
    y3 = r[2]
    Vy3 = r[3]

    r13 = mp.sqrt((math.fabs(x3 + mu) ** 2) + (math.fabs(y3) ** 2))
    mod_r13 = float(r13) ** 3

    r23 = mp.sqrt((math.fabs(x3 - 1 + mu) ** 2) + (math.fabs(y3) ** 2))
    mod_r23 = float(r23) ** 3

    dx3 = Vx3
    dVx3 = - (1 - mu) * ((x3 + mu)/mod_r13) - mu * ((x3 - 1 + mu)/mod_r23) + x3 + 2 * Vy3
    dy3 = Vy3
    dVy3 = - (1 - mu) * (y3 / mod_r13) - mu * (y3/mod_r23) + y3 - 2 * Vx3

    return array([dx3, dVx3, dy3, dVy3], float)


# --------------------------------------------------------------------------------------------------------#

def passo_rk4(f, r, t, h):  # Calcula um passo no método de RK4
    k1 = h * f(r, t)
    k2 = h * f(r + 0.5 * k1, t + 0.5 * h)
    k3 = h * f(r + 0.5 * k2, t + 0.5 * h)
    k4 = h * f(r + k3, t + h)
    return (k1 + 2.0 * (k2 + k3) + k4) / 6.0


# --------------------------------------------------------------------------------------------------------#
def p3cr_animacao():
    global mu, camval, showlabel, running, pausar, corpo1, corpo2, label1, label2, corpo3, label3

    # Condições e valores iniciais do programa

    titulo('Animação do Problema de 3 Corpos Restrito\n')
    orientacao("Para a utilização deste programa é necessário informar alguns dados, como: as massas das primárias\n"
          "(ou diretamente o valor da constante Mu do sistema) e as condições iniciais do Corpo 03.")
    aviso("Lembrando que Mu deve ser um valor entre 0 (zero) e 0.5 (meio).\n\n")
    orientacao("A seguir são informadas algumas sugestões de Condições Iniciais para o Corpo 03.\n")

    cabecalho = ['Órbita', 'mu', 'Pos x inicial', 'Pos y inicial', 'Vel x inicial', 'Vel y inicial']
    tabela = [['Tadpole 1', 0.001, 0.5055, 0.87, 0, 0],
              ['Tadpole 2', 0.001, 0.507, 0.8740, 0, 0],
              ['Horseshoe 1', 0.000953875, -1.02745, 0, 0, 0.04032],
              ['Horseshoe 2', 0.000953875, -0.97668, 0, 0, -0.06118],
              ['Aberta 1', 0.01, -0.6, 0, 0, 0.075],
              ['Aberta 2', 0.01, -0.75, 0, 0, 0.1],
              ['Aberta 3', 0.001, 0.5055, 0.67, 0, 0],
              ['Caótica 1', 0.25, 1.1, 0, 0, 0.075],
              ['Caótica 2', 0.05, 0.752, 0.08, -0.15, 0.05]]
    print(tabulate(tabela, headers=cabecalho))

    verdade = True
    sistema = 10
    while verdade:
        print("\nPara simular órbita:\n"
              "    *Tadpole 1 ---> digite 1\n"
              "    *Tadpole 2 ---> digite 2\n"
              "    *Horseshoe 1 -> digite 3\n"
              "    *Horseshoe 2 -> digite 4\n"
              "    *Aberta 1 ----> digite 5\n"
              "    *Aberta 2 ----> digite 6\n"
              "    *Aberta 3 ----> digite 7\n"
              "    *Caótica 1 ---> digite 8\n"
              "    *Caótica 2 ---> digite 9\n"
              "    *Para simular outro sistema -> digite 0")
        sistema = input("\nEscolha:")
        try:
            sistema = int(sistema)
            if sistema in range(0, 10):
                verdade = False
        except:
            print("Valor inválido! Digite novamente.")

    if sistema == 1:
        mu, x0_3, y0_3, Vx0_3, Vy0_3 = 0.001, 0.5055, 0.87, 0, 0

    elif sistema == 2:
        mu, x0_3, y0_3, Vx0_3, Vy0_3 = 0.001, 0.507, 0.8740, 0, 0

    elif sistema == 3:
        mu, x0_3, y0_3, Vx0_3, Vy0_3 = 0.000953875, -1.02745, 0, 0, 0.04032

    elif sistema == 4:
        mu, x0_3, y0_3, Vx0_3, Vy0_3 = 0.000953875, -0.97668, 0, 0, -0.06118

    elif sistema == 5:
        mu, x0_3, y0_3, Vx0_3, Vy0_3 = 0.01, -0.6, 0, 0, 0.075

    elif sistema == 6:
        mu, x0_3, y0_3, Vx0_3, Vy0_3 = 0.01, -0.75, 0, 0, 0.1

    elif sistema == 7:
        mu, x0_3, y0_3, Vx0_3, Vy0_3 = 0.001, 0.5055, 0.67, 0, 0

    elif sistema == 8:
        mu, x0_3, y0_3, Vx0_3, Vy0_3 = 0.25, 1.1, 0, 0, 0.075

    elif sistema == 9:
        mu, x0_3, y0_3, Vx0_3, Vy0_3 = 0.05, 0.752, 0.08, -0.15, 0.05

    else:
        opcao = int(input('\n\nDigite 1 para informar as massas individuais de cada uma das primárias\n'
                          'ou digite 2 para informar diretamente o valor da constante mu: '))
        if opcao == 1:
            m1 = float(input("Informe o valor da massa do maior objeto: "))
            m2 = float(input("Informe o valor da massa do menor objeto: "))
            mu = m2 / (m1 + m2)
        elif opcao == 2:
            mu = float(input('Informe o valor da constante mu: '))

        print(f'Valor de mu: {mu :.5f}.\n\n')

        # Corpo 03
        print('Condições Iniciais do Terceiro Corpo:\n')
        x0_3 = float(input('Digite o valor da posição em x do Corpo 03: '))
        y0_3 = float(input('Digite o valor da posição em y do Corpo 03: '))
        Vx0_3 = float(input('Digite o valor da velocidade em x do Corpo 03: '))
        Vy0_3 = float(input('Digite o valor da velocidade em y do Corpo 03: '))

    ra = array([x0_3, Vx0_3, y0_3, Vy0_3])
    r = ra

    # Tempo
    t = 0
    h = 1 / 750  # Atualização do passo (valor em segundos)

    # Intruções para criação da cena animada

    scene.width = 800  # Ajustando a largura da cena
    scene.height = 600  # Ajustando a altura da cena

    camval = 'Centralizada'
    showlabel = True
    running = False
    scene.align = 'left'
    scene.forward = vector(0, 0, -20)
    scene.bind('click', Rodar)

    ##### BOTÕES DA ANIMAÇÃO #####
    scene.append_to_caption("   ")
    pausar=button(text="Rodar", bind=Rodar)
    scene.append_to_caption("\n\n ")
    check1=checkbox(bind=Rastro3, text='Rastro 3', checked=True)
    scene.append_to_caption("\n\n ")
    check3=checkbox(bind=Nomes, text='Exibir nomes', checked=True)


    raio = 0.2

    corpo1 = sphere(trail_color=color.orange, texture='sol.jpg', radius=raio/2, pos=vector(-mu, 0, 0))
    corpo1.emissive = True
    label1 = label(pos=corpo1.pos + vector(0, 1.5 * corpo1.radius, 0), text='Corpo 1', box=0, opacity=0,
                   color=color.white)

    corpo2 = sphere(color=vector(0.076, 0.733, 0.902), texture='sirius.jpg', radius=raio/3, pos=vector(1-mu, 0, 0))
    corpo2.emissive = True
    label2 = label(pos=corpo2.pos + vector(0, 1.5 * corpo2.radius, 0), text='Corpo 2', box=0, opacity=0,
                   color=color.white)

    corpo3 = sphere(texture=textures.metal, radius=raio/5, pos=vector(x0_3, y0_3, 0), make_trail=True,
                    trail_color=color.white, trail_type='curve', interval=2)
    corpo3.emissive = True
    label3 = label(pos=corpo3.pos + vector(0, 0.08, 0), text='Corpo 3', box=0, opacity=0,
                   color=color.white)

    # --------------------------------------------------------------------------------------------------------#
    # Laço de realização dos Cálculos:

    while True:
        if running:
            rate(1500)
            # Corpo 03
            corpo3.pos = vector(r[0], r[2], 0)

            dr = passo_rk4(f, r, t, h)
            r = r + dr
            t = t + h

            if showlabel == True:
                label1.visible=True
                label2.visible=True
                label3.visible = True
                label1.pos = corpo1.pos+vector(0, 1.5*corpo1.radius,0)
                label2.pos = corpo2.pos+vector(0, 1.5*corpo2.radius,0)
                label3.pos = corpo3.pos + vector(0, 0.08, 0)
            else:
                label1.visible=False
                label2.visible=False




# --------------------------------------------------------------------------------------------------------#
if __name__ == '__main__':
    p3cr_animacao()

