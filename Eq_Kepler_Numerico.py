from math import*
import time


def aviso(texto):
    print(f"\u001b[31m{texto}\u001b[0m")

def verde(texto):
    print(f"\u001b[32m{texto}\u001b[0m")

def orientacao(texto):
    print(f"\u001b[33m{texto}\u001b[0m")

def titulo(texto):
    print(f"\u001b[34m{texto}\u001b[0m")


def eq_Kepler_numerico():
    titulo("\nCálculo da Anomalia Excêntrica a partir da Equação de Kepler por método recursivo.\n")

    orientacao("Para utilizar este módulo é necessário informar alguns valores, sendo eles: o período orbital do objeto,\n"
          "qual o tempo transcorrido desde a passagem do objeto pelo periastro, a excentricidade da órbita e o número\n"
          "de iterações desejadas para o cálculo.\n")
    aviso("Observação 1: o período orbital e o tempo desde a passagem pelo periastro podem estar em qualquer\n"
          "unidade de tempo (dias, meses, anos, etc), desde que os dois estejam na mesma escala.\n")
    aviso("Observação 2: o tempo desde a passagem pelo periastro deve ser menor que o período orbital.\n")
    aviso("Observação 3: a excentricidade da órbita deve ser maior ou igual a 0 (zero) e menor que 1 (um).\n")
    T = float(input("Digite o período orbital do objeto: "))
    t = float(input("Digite o tempo que passou desde quando o objeto estava no periastro: "))
    e = float(input("Digite o valor da excentricidade da órbita: "))
    num = int(input("Qual o número de iterações desejada para o cálculo: "))

    tempo_inicial = time.time()
    M = (2 * pi/T) * t  # Anomalia média (rad)
    E = M               # 1ª aproximação de E
    i = 2
    while i <= num:  # Loop com as iterações.
        E = M + (e * sin(E))  # Equação de Kepler
        i += 1
    anom_graus = E*180/pi
    graus = int(anom_graus)
    minutos = int((anom_graus-graus)*60)
    segundos = int((((anom_graus-graus)*60)-minutos)*60)

    print("\nResultado:")
    print(f"A anomalia excentrica do objeto é de {E} radianos")
    print(f"Isso é igual a {graus}° {minutos}' {segundos}''")
    print("Fim dos cálculos!\n")
    print("Tempo de execução (em segundos):", (time.time() - tempo_inicial))

