from numpy import*
from tqdm import tqdm
from tabulate import tabulate
from scipy.optimize import fsolve
import math as math
import mpmath as mp  # Módulo "Math" que realiza cálculos com maiores precisões e mais dígitos.
import plotly.graph_objects as go
import time

def aviso(texto):
    print(f"\u001b[31m{texto}\u001b[0m")

def verde(texto):
    print(f"\u001b[32m{texto}\u001b[0m")

def orientacao(texto):
    print(f"\u001b[33m{texto}\u001b[0m")

def titulo(texto):
    print(f"\u001b[34m{texto}\u001b[0m")


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

def ponto_L1(mu, alfa):
    x = 1 - mu - alfa + (alfa**2)/3 + (alfa**3)/9 + 23*(alfa**4)/81
    return x

def ponto_L2(mu, alfa):
    x = 1 - mu + alfa + (alfa**2)/3 - (alfa**3)/9 - 31*(alfa**4)/81
    return x

def ponto_L3(mu, beta):
    x = 1 - mu - (2 - 7*beta/12 + 7*(beta**2)/12 - 13223*(beta**3)/20736)
    return x

def sup_vel_zero(mu, x, y):
    r13 = sqrt((x + mu)**2 + y**2)
    r23 = sqrt((x-1+mu)**2 + y**2)
    c = (x**2 + y**2) + 2*(1-mu)/r13 + 2*mu/r23
    return c


def p3cr_pontoslagrange_grafico():
    global mu

    titulo('\nSimulação numérica do Problema de 3 Corpos Restrito\n')
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

    inicio = time.time()

    alfa = mp.root((mu / (3 * (1 - mu))), 3)
    beta = mu / (1 - mu)

    L1_aprox = round(ponto_L1(mu, alfa), 5)
    L2_aprox = round(ponto_L2(mu, alfa), 5)
    L3_aprox = round(ponto_L3(mu, beta), 5)

    L4_x = 0.5 - mu
    L4_y = sin(pi / 3)
    L5_x = L4_x
    L5_y = - L4_y

    def function(x):
        return -(1 - mu) * ((x + mu) / abs(x + mu) ** 3) - mu * ((x - 1 + mu) / abs(x - 1 + mu) ** 3) + x

    # Calculando os Pontos L1, L2 e L3 (colineares):
    raizes = fsolve(function, [L1_aprox, L2_aprox, L3_aprox])  # soluciona a equação em função da variável definida (x)
    lista = []
    for solution in raizes:
        lista.append(solution)  # Adiciona cada uma das raízes em uma lista.

    L1 = lista[0]
    L2 = lista[1]
    L3 = lista[2]

    delta = 0.0025
    x = arange(-1.25, 1.25, delta)
    y = arange(-1.25, 1.25, delta)
    X, Y = meshgrid(x, y)  # Cria os pontos no plano cartesiano para execução de um mapa.
    Z = sup_vel_zero(mu, X, Y)

    print(f'\nResultados:\n'
          f'Ponto L1: ({L1 :.5f},0) \n'
          f'Ponto L2: ({L2 :.5f},0) \n'
          f'Ponto L3: ({L3 :.5f},0)\n'
          f'Ponto L4: ({L4_x :.5f},{L4_y :.5f})\n'
          f'Ponto L5: ({L5_x :.5f},{L5_y :.5f})\n\n')

    ra = array([x0_3, Vx0_3, y0_3, Vy0_3])
    r = ra

    t = 0
    h = 1 / 750  # Atualização do passo (valor em segundos)
    tempo_total = 200

    pos_x = []
    pos_y = []

    #Criando uma barra de progresso:
    pbar = tqdm(total=tempo_total/h, position=0, leave=True)

    # Laço de realização dos Cálculos:
    while t < tempo_total:
        dr = passo_rk4(f, r, t, h)
        r = r + dr
        t = t + h
        pos_x.append(r[0])
        pos_y.append(r[2])
        pbar.update()


    print(f'\nTempo de execução: {time.time() - inicio} s')
    aviso('\nO gráfico a seguir será exibido em uma janela do navegador do computador.\n' 
          'Devido ao elevado número de dados processados neste módulo, pode acontecer do gráfico não ser exibido'
          ' em um primeiro instante.\nPara corrigir isso, basta recarregar a página.   ')

    del pbar

    # Plotly
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=pos_x, y=pos_y, name='Movimento Corpo 3', line=dict(dash='solid', color='darkblue')))
    fig.add_trace(go.Scatter(x=(-mu,), y=(0,), name=f'Objeto 1 - massa={1-mu}', mode='markers',
                             marker=dict(size=20, opacity=1, color='orangered')))

    fig.add_trace(go.Scatter(x=(1-mu,), y=(0,), name=f'Objeto 2 - massa={mu}', mode='markers',
                             marker=dict(size=10, opacity=1, color='darkviolet')))

    fig.add_trace(go.Scatter(x=(L1,), name='L1', mode='markers+text', text='L1', textposition='bottom center',
                             marker=dict(size=10, opacity=1, color='forestgreen')))
    fig.add_trace(go.Scatter(x=(L2,), name='L2', mode='markers+text',  text='L2', textposition='bottom center',
                             marker=dict(size=10, opacity=1, color='tomato')))
    fig.add_trace(go.Scatter(x=(L3,), name='L3', mode='markers+text',  text='L3', textposition='bottom center',
                             marker=dict(size=10, opacity=1, color='darkblue')))
    fig.add_trace(go.Scatter(x=(L4_x,), y=(L4_y,), name='L4', mode='markers+text',  text='L4', textposition='bottom center',
                             marker=dict(size=10, opacity=1, color='gray')))
    fig.add_trace(go.Scatter(x=(L5_x,), y=(L5_y,), name='L5', mode='markers+text',  text='L5', textposition='bottom center',
                             marker=dict(size=10, opacity=1, color='olive')))

    fig.add_trace(go.Contour(x=x, y=y, z=Z, colorscale='ice',
                             contours=dict(start=2.8, end=3.2, size=0.02, coloring="lines"), line=dict(width=2),
                             colorbar=dict(thickness=25, thicknessmode='pixels', len=0.5,
                                           lenmode='fraction', outlinewidth=0)))

    fig.update_layout(autosize=False, width=1100, height=900, title=f'Pontos de Lagrange para mu={mu}',
                       xaxis_title='Posição X', yaxis_title='Posição Y')
    fig.show()

if __name__ == '__main__':
    p3cr_pontoslagrange_grafico()
