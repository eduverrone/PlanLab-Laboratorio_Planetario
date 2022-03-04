from numpy import sin, pi
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

def pontoslagrange_por_series_numerico():

    titulo("Cálculo dos Pontos de Lagrange - por séries")
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

    alfa = mp.root((mu / (3*(1-mu))), 3)
    beta = mu / (1-mu)

    L1 = round(ponto_L1(mu, alfa), 5)
    L2 = round(ponto_L2(mu, alfa), 5)
    L3 = round(ponto_L3(mu, beta), 5)
    L4_x = round(0.5 - mu, 5)
    L4_y = round(sin(pi/3), 5)
    L5_x = L4_x
    L5_y = - L4_y

    print(f'Resultados:\n\n'
          f'Ponto L1: ({L1},0) \n'
          f'Ponto L2: ({L2},0) \n'
          f'Ponto L3: ({L3},0)\n'
          f'Ponto L4: ({L4_x},{L4_y})\n'
          f'Ponto L5: ({L5_x},{L5_y})\n\n'
          f'Tempo de execução: {time.time() - t} segundos')


if __name__ == '__main__':
    pontoslagrange_por_series_numerico()

