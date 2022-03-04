"""
A partir da determinação da massa de dois objetos e da distância entre eles, calcular os Pontos de Lagrange.

Já sabemos que os pontos L4 e L5 são os pontos triangulares em relação às massas. Estes estão a 60° de inclinação
em relação a linha que liga as duas massas e também sabemos que a distância entre cada uma das massas e o ponto
L4 ou L5 é a distância entre as massas.

A determinação dos pontos L1, L2 e L3 depende da resolução numérica da equação:

                     -(1-mu)*((x+mu)/abs(x+mu)**3)-mu*((x-1+mu)/abs(x-1+mu)**3)+x = 0

Como visto pela equação, esses pontos de Lagrange localizam-se sobre a reta que liga as duas massas.


"""
from numpy import*
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
import mpmath as mp
import time


def titulo(texto):
    print(f"\u001b[34m{texto}\u001b[0m")


def aviso(texto):
    print(f"\u001b[31m{texto}\u001b[0m")


def ponto_L1(mu, alfa):
    x = 1 - mu - alfa + (alfa**2)/3 + (alfa**3)/9 + 23*(alfa**4)/81
    return x

def ponto_L2(mu, alfa):
    x = 1 - mu + alfa + (alfa**2)/3 - (alfa**3)/9 - 31*(alfa**4)/81
    return x

def ponto_L3(mu, beta):
    x = 1 - mu - (2 - 7*beta/12 + 7*(beta**2)/12 - 13223*(beta**3)/20736)
    return x


def pontoslagrange_numerico():

    global mu

    titulo("Cálculo dos Pontos de Lagrange")
    opcao = int(input('\n\nDigite 1 para informar as massas individuais de cada uma das primárias\n'
                      'ou digite 2 para informar diretamente o valor da constante mu: '))
    if opcao == 1:
        m1 = float(input("Informe o valor da massa do maior objeto: "))
        m2 = float(input("Informe o valor da massa do menor objeto: "))
        mu = m2 / (m1 + m2)
    elif opcao == 2:
        aviso("Lembrando que Mu deve ser um valor entre 0 (zero) e 0.5 (meio).")
        mu = float(input('Informe o valor da constante mu: '))

    print(f'\nValor de mu: {mu}.\n')
    t = time.time()

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

    print("Pontos de Lagrange do sistema:\n")
    print(f'L1:({round(L1,6)}, 0) \nL2:({round(L2,6)}, 0) \nL3:({round(L3,6)}, 0) '
          f'\nL4:({round(L4_x,6)}, {round(L4_y,6)}) \nL5:({round(L5_x,6)}, {round(L5_y,6)})')
    print(f'Tempo de execução: {time.time()-t} s')

    plt.scatter(-mu, 0, label='Objeto 1 - Maior Massa', color='orange')
    plt.scatter(1 - mu, 0, label='Objeto 2 - Menor Massa', color='red')
    plt.scatter(L1, 0, label='L1', marker='*')
    plt.scatter(L2, 0, label='L2', marker='*')
    plt.scatter(L3, 0, label='L3', marker='*')
    plt.scatter(L4_x, L4_y, label='L4 - Gregos', marker='*')
    plt.scatter(L5_x, L5_y, label='L5 - Troianos', marker='*')
    plt.legend()
    plt.title('Pontos de Lagrange')
    plt.annotate('L1', xy=(L1, 0), xytext=(L1-0.01, 0.05))
    plt.annotate('L2', xy=(L2, 0), xytext=(L2-0.01, 0.05))
    plt.annotate('L3', xy=(L3, 0), xytext=(L3-0.01, 0.05))
    plt.annotate('L4', xy=(L4_x, L4_y), xytext=(L4_x, L4_y-0.06))
    plt.annotate('L5', xy=(L5_x, L5_y), xytext=(L5_x, L5_y+0.05))
    plt.show()


if __name__ == '__main__':
    pontoslagrange_numerico()

