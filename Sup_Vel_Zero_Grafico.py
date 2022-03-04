import numpy as np
from scipy.optimize import fsolve
import plotly.graph_objects as go
import mpmath as mp
import time


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
    r13 = np.sqrt((x + mu)**2 + y**2)
    r23 = np.sqrt((x-1+mu)**2 + y**2)
    c = (x**2 + y**2) + 2*(1-mu)/r13 + 2*mu/r23
    return c

def titulo(texto):
    print(f"\u001b[34m{texto}\u001b[0m")

def aviso(texto):
    print(f"\u001b[31m{texto}\u001b[0m")


def sup_vel_zero_grafico():
    global mu

    titulo('Demonstração das Superfícies de Velocidade Zero e Pontos de Lagrange:\n')
    opcao = int(input('Digite 1 para informar as massas individuais de cada uma das primárias\n'
                      'ou digite 2 para informar diretamente o valor da constante mu: '))
    if opcao == 1:
        m1 = float(input("Informe o valor da massa do maior objeto: "))
        m2 = float(input("Informe o valor da massa do menor objeto: "))
        mu = m2 / (m1 + m2)
    elif opcao == 2:
        aviso("Lembrando que Mu deve ser um valor entre 0 (zero) e 0.5 (meio).")
        mu = float(input('Informe o valor da constante mu: '))

    inicio = time.time()

    print(f'Valor de mu: {mu}.')

    alfa = mp.root((mu / (3*(1-mu))), 3)
    beta = mu / (1-mu)

    L1_aprox = round(ponto_L1(mu, alfa), 5)
    L2_aprox = round(ponto_L2(mu, alfa), 5)
    L3_aprox = round(ponto_L3(mu, beta), 5)
    L4_x = 0.5 - mu
    L4_y = np.sqrt(3)/2
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

    delta = 0.002
    x = np.arange(-1.5, 1.5, delta)
    y = np.arange(-1.5, 1.5, delta)
    X, Y = np.meshgrid(x, y)  # Cria os pontos no plano cartesiano para execução de um mapa.
    Z = sup_vel_zero(mu, X, Y)
    print(f'Tempo de execução: {time.time() - inicio} s')

    aviso('\nO gráfico a seguir será exibido em uma janela do navegador do computador.\n'
          'Devido ao elevado número de dados processados neste módulo, pode acontecer do gráfico não ser exibido'
          ' em um primeiro instante.\nPara corrigir isso, basta recarregar a página.   ')


    # Gráfico de Contorno:
    # IMPORTANTE! A escala de cor deve possuir a mesma ordem de grandeza dos valores para que dê certo! AAAAAAHHHHH

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=(L1,), mode='markers+text', name='L1', text='L1', textfont=dict(size=15, color='black'),
                             textposition='bottom center', marker=dict(size=12, opacity=1, color='yellow')))

    fig.add_trace(go.Scatter(x=(L2,), mode='markers+text', name='L2', text='L2', textfont=dict(size=15, color='black'),
                             textposition='bottom center', marker=dict(size=12, opacity=1, color='yellow')))

    fig.add_trace(go.Scatter(x=(L3,), mode='markers+text', name='L3', text='L3', textfont=dict(size=15, color='black'),
                             textposition='bottom center', marker=dict(size=12, opacity=1, color='yellow')))

    fig.add_trace(go.Scatter(x=(L4_x,), y=(L4_y,), mode='markers+text', name='L4', text='L4', textfont=dict(size=15, color='black'),
                             textposition='bottom center', marker=dict(size=12, opacity=1, color='yellow')))

    fig.add_trace(go.Scatter(x=(L5_x,), y=(L5_y,), mode='markers+text', name='L5', text='L5', textfont=dict(size=15, color='black'),
                             textposition='bottom center', marker=dict(size=12, opacity=1, color='yellow')))

    fig.add_trace(go.Contour(x=x, y=y, z=Z, colorscale='ice', contours=dict(start=0, end=5, size=0.1, coloring="lines"),
                             line=dict(width=2),
                             colorbar=dict(thickness=25, thicknessmode='pixels', len=1,
                                           lenmode='fraction', outlinewidth=0)))


    #colorscale hot, ice e earth são os melhores.

    fig.update_layout(autosize=False, width=750, height=750,
                      title=f'Superfícies de Velocidade Zero - mu={mu}',
                      xaxis_title='Posição X', yaxis_title='Posição Y',
                      showlegend=False)
    fig.show()


if __name__ == '__main__':
    sup_vel_zero_grafico()

"""
- One of the following named colorscales:
            ['aggrnyl', 'agsunset', 'algae', 'amp', 'armyrose', 'balance',
             'blackbody', 'bluered', 'blues', 'blugrn', 'bluyl', 'brbg',
             'brwnyl', 'bugn', 'bupu', 'burg', 'burgyl', 'cividis', 'curl',
             'darkmint', 'deep', 'delta', 'dense', 'earth', 'edge', 'electric',
             'emrld', 'fall', 'geyser', 'gnbu', 'gray', 'greens', 'greys',
             'haline', 'hot', 'hsv', 'ice', 'icefire', 'inferno', 'jet',
             'magenta', 'magma', 'matter', 'mint', 'mrybm', 'mygbm', 'oranges',
             'orrd', 'oryel', 'oxy', 'peach', 'phase', 'picnic', 'pinkyl',
             'piyg', 'plasma', 'plotly3', 'portland', 'prgn', 'pubu', 'pubugn',
             'puor', 'purd', 'purp', 'purples', 'purpor', 'rainbow', 'rdbu',
             'rdgy', 'rdpu', 'rdylbu', 'rdylgn', 'redor', 'reds', 'solar',
             'spectral', 'speed', 'sunset', 'sunsetdark', 'teal', 'tealgrn',
             'tealrose', 'tempo', 'temps', 'thermal', 'tropic', 'turbid',
             'turbo', 'twilight', 'viridis', 'ylgn', 'ylgnbu', 'ylorbr',
             'ylorrd']."""