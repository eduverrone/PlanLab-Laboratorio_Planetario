from numpy import*
import mpmath as mp
import plotly.graph_objects as go
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


def titulo(texto):
    print(f"\u001b[34m{texto}\u001b[0m")

def aviso(texto):
    print(f"\u001b[31m{texto}\u001b[0m")


def pontoslagrange_variandomu():

    titulo("Cálculo dos Pontos Lineares de Lagrange\n")
    t = time.time()

    lista_mu = arange(0, 0.501, 0.00001)
    lista_L1 = []
    lista_L2 = []
    lista_L3 = []

    for mu in lista_mu:
        alfa = float(mp.root((mu / (3*(1-mu))), 3))
        beta = mu / (1-mu)
        lista_L1.append(ponto_L1(mu, alfa) - (1-mu))
        lista_L2.append(ponto_L2(mu, alfa) - (1-mu))
        lista_L3.append(ponto_L3(mu, beta) - (1-mu))

    print(f'Tempo de execução: {time.time() - t} segundos')  # Aproximadamente 5 segundos de execução.

    aviso('\nO gráfico a seguir será exibido em uma janela do navegador do computador.\n'
          'Devido ao elevado número de dados processados neste módulo, pode acontecer do gráfico não ser exibido'
          ' em um primeiro instante.\nPara corrigir isso, basta recarregar a página.   ')

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=lista_mu, y=lista_L1, name='Pontos L1'))
    fig.add_trace(go.Scatter(x=lista_mu, y=lista_L2, name='Pontos L2'))
    fig.add_trace(go.Scatter(x=lista_mu, y=lista_L3, name='Pontos L3'))

    fig.add_vline(x=0.458831, name='Sistema Binário alfa-Centauri', line=dict(dash='solid', color='coral'))
    fig.add_vline(x=0.000958, name='Sistema Sol-Júpiter', line=dict(dash='solid', color='tomato'))
    fig.add_vline(x=0.000003, name='Sistema Sol-Terra', line=dict(dash='dot', color='darkblue'))
    fig.add_vline(x=0.120654, name='Sistema Plutão-Caronte', line=dict(dash='dot', color='gray'))
    fig.add_vline(x=0.012160, name='Sistema Terra-Lua', line=dict(dash='dashdot', color='olive'))

    fig.add_trace(go.Scatter(x=(0.458831,), name='Sistema Binário alfa-Centauri', line=dict(dash='solid', color='coral')))
    fig.add_trace(go.Scatter(x=(0.000958,), name='Sistema Sol-Júpiter', line=dict(dash='solid', color='tomato')))
    fig.add_trace(go.Scatter(x=(0.000003,), name='Sistema Sol-Terra', line=dict(dash='dot', color='darkblue')))
    fig.add_trace(go.Scatter(x=(0.120654,), name='Sistema Plutão-Caronte', line=dict(dash='dot', color='gray')))
    fig.add_trace(go.Scatter(x=(0.012160,), name='Sistema Terra-Lua', line=dict(dash='dashdot', color='olive')))


    fig.update_layout(title='Pontos Lineares de Lagrange',
                       xaxis_title='Mu', yaxis_title='Distância ao corpo de menor massa')
    fig.show()


if __name__ == '__main__':
    pontoslagrange_variandomu()

"""
The 'fillcolor' property is a color and may be specified as:
      - A hex string (e.g. '#ff0000')
      - An rgb/rgba string (e.g. 'rgb(255,0,0)')
      - An hsl/hsla string (e.g. 'hsl(0,100%,50%)')
      - An hsv/hsva string (e.g. 'hsv(0,100%,100%)')
      - A named CSS color:
            aliceblue, antiquewhite, aqua, aquamarine, azure,
            beige, bisque, black, blanchedalmond, blue,
            blueviolet, brown, burlywood, cadetblue,
            chartreuse, chocolate, coral, cornflowerblue,
            cornsilk, crimson, cyan, darkblue, darkcyan,
            darkgoldenrod, darkgray, darkgrey, darkgreen,
            darkkhaki, darkmagenta, darkolivegreen, darkorange,
            darkorchid, darkred, darksalmon, darkseagreen,
            darkslateblue, darkslategray, darkslategrey,
            darkturquoise, darkviolet, deeppink, deepskyblue,
            dimgray, dimgrey, dodgerblue, firebrick,
            floralwhite, forestgreen, fuchsia, gainsboro,
            ghostwhite, gold, goldenrod, gray, grey, green,
            greenyellow, honeydew, hotpink, indianred, indigo,
            ivory, khaki, lavender, lavenderblush, lawngreen,
            lemonchiffon, lightblue, lightcoral, lightcyan,
            lightgoldenrodyellow, lightgray, lightgrey,
            lightgreen, lightpink, lightsalmon, lightseagreen,
            lightskyblue, lightslategray, lightslategrey,
            lightsteelblue, lightyellow, lime, limegreen,
            linen, magenta, maroon, mediumaquamarine,
            mediumblue, mediumorchid, mediumpurple,
            mediumseagreen, mediumslateblue, mediumspringgreen,
            mediumturquoise, mediumvioletred, midnightblue,
            mintcream, mistyrose, moccasin, navajowhite, navy,
            oldlace, olive, olivedrab, orange, orangered,
            orchid, palegoldenrod, palegreen, paleturquoise,
            palevioletred, papayawhip, peachpuff, peru, pink,
            plum, powderblue, purple, red, rosybrown,
            royalblue, rebeccapurple, saddlebrown, salmon,
            sandybrown, seagreen, seashell, sienna, silver,
            skyblue, slateblue, slategray, slategrey, snow,
            springgreen, steelblue, tan, teal, thistle, tomato,
            turquoise, violet, wheat, white, whitesmoke,
            yellow, yellowgreen

Process finished with exit code 1

"""
