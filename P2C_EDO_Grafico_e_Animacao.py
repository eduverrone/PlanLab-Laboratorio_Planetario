from numpy import *
from vpython import *
from tabulate import tabulate
import time
import mpmath as mp  # Módulo "Math" que realiza cálculos com maiores precisões e mais dígitos.
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
# --------------------------------------------------------------------------------------------------------#

# Checkbox para rastros
def Rastro1(b):
    if b.checked:
        corpo1.make_trail=True
    else:
        corpo1.make_trail=False
        corpo1.clear_trail()
# --------------------------------------------------------------------------------------------------------#

def Rastro2(b):
    if b.checked:
        corpo2.make_trail=True
    else:
        corpo2.make_trail=False
        corpo2.clear_trail()
# --------------------------------------------------------------------------------------------------------#

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
# --------------------------------------------------------------------------------------------------------#

def Cameras(cam):
    global camval
    camval = cam.selected
# --------------------------------------------------------------------------------------------------------#

# Função com as Equações diferenciais a serem resolvidas:

def f(r, t, M1, M2):
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


# --------------------------------------------------------------------------------------------------------#

# Funções Utilizadas no programa:

def eq_orbital(a, e, theta):  # Equação Orbital em função do semi-eixo maior e excentricidade.
    r = (a * (1 - e ** 2)) / (1 + e * cos(theta))
    return r

# --------------------------------------------------------------------------------------------------------#
def periodo_orbital(a, mu):  # Cálculo do Período Orbital e da velocidade angular média.
    n = sqrt(mu / a ** 3)
    T = 2 * pi / n
    return n, T  # Período em segundos e n em rad/s.
# --------------------------------------------------------------------------------------------------------#

def mom_angular(a, mu, e):  # Cálculo do momento angular (km²/s).
    h = sqrt(a * mu * (1 - e ** 2))
    return h
# --------------------------------------------------------------------------------------------------------#

def modulo_velocidade(a, mu, r):  # Cálculo do módulo da velocidade em função do raio orbital (km/s).
    v = sqrt(mu * ((2 / r) - (1 / a)))
    return v
# --------------------------------------------------------------------------------------------------------#


def p2c_EDO_grafico_e_animacao():
    titulo("Cálculo da órbita a partir do semi-eixo maior e da excentricidade: \n")
    orientacao("Dados de alguns objetos celestes:")

    cabecalho = [' ', 'Massa (Massas Solares)', 'Semi-Eixo Maior (U.A.)', 'Excentricidade']
    tabela = [['Sol', 1, '--', '--'],
              ['Mercúrio', 1.6515E-7, 0.4, 0.205630],
              ['Vênus', 2.447E-6, 0.7, 0.006772],
              ['Terra', 2.980E-6, 1, 0.01671022],
              ['Lua', 3.694E-8, 2.5E-3, 0.0549],
              ['Marte', 3.213E-7, 1.5, 0.093315],
              ['Júpiter', 9.542E-4, 5.2, 0.048775],
              ['Saturno', 2.860E-4, 9.5, 0.055723219],
              ['Urano', 4.364E-5, 19, 0.044405586],
              ['Netuno', 5.148E-5, 30, 0.01114269],
              ['Plutão', 6.56E-9, 39.5, 0.24880766],
              ['Cometa Halley', 1.106E-16, 17.8, 0.967]]

    print(tabulate(tabela, headers=cabecalho))
    print("* Por Mercúrio estar muito próximo ao Sol, é necessário considerar efeitos relativísticos em sua órbita,")
    print("os quais não são considerados nessa simulação.", '\n')

    G = 6.674E-20  # Constante Gravitacional Universal (km³/s²kg)

    # Imputs:

    global M, m
    M = 1.9891E30 * float(input("Digite o valor da massa do corpo central (em Massas Solares): "))
    m = 1.9891E30 * float(input("Digite a massa do corpo menor (em Massas Solares)\n"
                    "Obs.: se a massa for desprezível em relação a do corpo central, digite zero: "))
    u = int(G * (M+m))
    print(f"Valor da constante Mu do sistema: {u:.2E} km³/s². \n")

    a = float(input("Digite o valor do semi-eixo maior da órbita (em U.A.): ")) * 149597870.7
    e = float(input("Digite o valor da excentricidade da órbita: "))

    tempo_inicial = time.time()
    angulo = arange(0, 2 * pi, 0.005)
    raio = []
    x = []
    y = []
    mod_v = []

    for theta in angulo:
        r = eq_orbital(a, e, theta) / 149597870.7
        raio.append(r)
        x.append(r * cos(theta))
        y.append(r * sin(theta))
        mod_v.append(modulo_velocidade(a, u, r))


    # Resultados:

    global rp, vp
    orientacao("\nResultados:")

    rp = a * (1 - e)  # Raio periastro (km).
    print(f"Raio orbital no periastro: {round(rp/149597870.7,2)} U.A. .")

    ra = a * (1 + e)  # Raio apoastro (km).
    print(f"Raio orbital no apoastro: {round(ra/149597870.7,2)} U.A. .\n")

    vp = round(modulo_velocidade(a, u, rp), 2)  # Cálculo do módulo da velocidade no periastro (km/s).
    print(f"Módulo da velocidade orbital no periastro: {vp} km/s.")

    va = round(modulo_velocidade(a, u, ra), 2)  # Cálculo do módulo da velocidade no apoastro (km/s).
    print(f"Módulo da velocidade orbital no apoastro: {va} km/s.\n")

    # Sabendo o valor do semi-eixo maior, da excentricidade e calculados todas as posições orbitais
    # podemos calcular o momento angular e as velocidades em cada ponto da órbita.

    n_orbital, T_orbital = periodo_orbital(a, u)
    print(f"Período orbital do objeto: {int(T_orbital)} s.")
    print(f"Período orbital do objeto: {round(T_orbital / (365 * 24 * 3600), 4)} anos.")
    print(f"Velocidade angular média: {n_orbital:.2E} rad/s.\n")

    h_orbital = mom_angular(a, u, e)  # O cálculo do momento angular é realizado no periastro.
    # Por sabermos que momento angular é constante em todo o movimento, podemos calculá-lo em qualquer ponto da órbita.
    print(f"Módulo momento angular orbital: {round(h_orbital, 3):.2E} km²/s")

    aviso('\nO gráfico a seguir será exibido em uma janela do navegador do computador.\n'
          'Devido ao elevado número de dados processados neste módulo, pode acontecer do gráfico não ser exibido'
          ' em um primeiro instante.\nPara corrigir isso, basta recarregar a página.   ')


    # Gráficos com PLotly:

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(x=angulo, y=raio, name='Raio Orbital', line=dict(dash='solid', color='darkblue')), secondary_y=False)
    fig.add_trace(go.Scatter(x=angulo, y=mod_v, name='Módulo Velocidade', line=dict(dash='solid', color='red')), secondary_y=True)

    fig.update_layout(title='Raio Orbital e Módulo da Velocidade em função de Theta', xaxis_title='Theta (rad)')
    fig.update_yaxes(title_text="Raio Orbital (U.A.)", secondary_y=False)
    fig.update_yaxes(title_text="Módulo Velocidade (km/s)", secondary_y=True)

    fig.show()

    # Gráfico com PLotly:

    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(x=x, y=y, name='Órbita', line=dict(dash='solid', color='darkblue')))
    fig2.add_trace(go.Scatter(x=(0,), y=(0,), name='Foco Principal', mode='markers',
                             marker=dict(size=40, opacity=1, color='orangered')))

    if e < 0.5:
        fig2.update_layout(autosize=False, width=750, height=750 * (1 - e), title='Órbita',
                           xaxis_title='x(theta)', yaxis_title='y(theta)')
    else:
        fig2.update_layout(autosize=True, title='Órbita', xaxis_title='x(theta)', yaxis_title='y(theta)')

    fig2.show()

    global camval, showlabel, running, pausar, corpo1, corpo2, label1, label2
    scene.width = 800  # Ajustando a largura da cena
    scene.height = 600  # Ajustando a altura da cena
    # Definições da cena
    camval = 'Centralizada'
    showlabel = True
    running = False
    scene.align='left'
    scene.forward = vector(0,-.3,-1)
    scene.bind('click', Rodar)

    ##### BOTÕES DA ANIMAÇÃO #####
    scene.append_to_caption("   ")
    pausar=button(text="Rodar", bind=Rodar)
    scene.append_to_caption("\n\n   ")
    check1=checkbox(bind=Rastro1, text='Rastro 1', checked=True)
    scene.append_to_caption("\n   ")
    check2=checkbox(bind=Rastro2, text='Rastro 2', checked=True)
    scene.append_to_caption("\n   ")
    check3=checkbox(bind=Nomes, text='Exibir nomes', checked=True)
    scene.append_to_caption("\n\n")
    scene.append_to_caption('    Camera:')
    menu(choices=['Origem', 'CM', 'Corpo 1', 'Corpo 2'], index=0, bind=Cameras)


    # Condições e valores iniciais do programa

    # Corpo 01
    M1 = M  # Massa do Corpo 01 (kg)
    x0_1 = 0        # Posição no eixo x do Corpo 01 (km)
    y0_1 = 0        # Posição do eixo y do Corpo 01 (km)
    Vx0_1 = 0       # Componente x da velocidade do Corpo 01 (km/s)
    Vy0_1 = 0       # Componente y da velocidade do Corpo 01 (km/s)

    # Corpo 02
    M2 = m          # Massa do Corpo 02 (kg)
    x0_2 = rp       # Posição no eixo x do Corpo 02 (km)
    y0_2 = 0        # Posição do eixo y do Corpo 02 (km)
    Vx0_2 = 0       # Componente x da velocidade do Corpo 02 (km/s)
    Vy0_2 = vp      # Componente y da velocidade do Corpo 02 (km/s)

    ra = array([x0_1, Vx0_1, y0_1, Vy0_1, x0_2, Vx0_2, y0_2, Vy0_2])
    r = ra

    # Tempo
    ti = 0
    h = (24 * 3600)
    t = ti

    #Criando os objetos:
    raio = (x0_2-x0_1)//5
    corpo1 = sphere(trail_color=color.orange, texture='sol.jpg', radius=int(3 * raio / 4), pos=vector(x0_1, y0_1, 0),
                    make_trail=True, interval=5)
    corpo1.emissive = True
    label1 = label(pos=corpo1.pos+vector(0, 1.5*corpo1.radius, 0), text='Corpo 1', box=0, opacity=0, color=color.white)
    corpo1.massa = M1

    corpo2 = sphere(color=vector(0.076, 0.733, 0.902), texture='sirius.jpg', radius=int(raio / 2),
                    pos=vector(x0_2, y0_2, 0), make_trail=True, trail_type='points', interval=5)
    corpo2.emissive = True
    label2 = label(pos=corpo2.pos+vector(0, 1.5*corpo2.radius, 0), text='Corpo 2', box=0, opacity=0, color=color.white)
    corpo2.massa = M2
    # --------------------------------------------------------------------------------------------------------#
    # Laço de realização dos Cálculos:
    while True:
        if running:
            rate(30)
            # Corpo 01
            corpo1.pos = vector(r[0], r[2], 0)

            # Corpo 02
            corpo2.pos = vector(r[4], r[6], 0)

            dr = passo_rk4(f, r, t, h, M1, M2)
            r = r + dr
            t = t + h
            if showlabel == True:
                label1.visible=True
                label2.visible=True
                label1.pos = corpo1.pos+vector(0,1.5*corpo1.radius,0)
                label2.pos = corpo2.pos+vector(0,1.5*corpo2.radius,0)
            else:
                label1.visible=False
                label2.visible=False
            #Centro de Massa
            CM = (corpo1.pos*corpo1.massa+corpo2.pos*corpo2.massa)/(corpo1.massa+corpo2.massa)
            # Camera
            if camval == "Origem":
                scene.center = vector(0,0,0)
            elif camval == "CM":
                scene.center = CM
            elif camval == "Corpo 1":
                scene.center = corpo1.pos
            elif camval == "Corpo 2":
                scene.center = corpo2.pos


if __name__ == '__main__':
    p2c_EDO_grafico_e_animacao()

