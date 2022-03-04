from Eq_Kepler_Numerico import eq_Kepler_numerico
from P2C_EDO_Animacao import p2c_EDO_animacao
from P2C_EDO_Animacao_VariosReferenciais import p2c_EDO_animacao_variosreferenciais
from P2C_EDO_Grafico_e_Animacao import p2c_EDO_grafico_e_animacao
from P2C_EDO_Grafico_e_Animacao_VariosCorpos import p2c_EDO_Grafico_e_Animacao_VariosCorpos
from Sistema_Solar_Animacao import sistema_solar_animacao
from P3C_Animacao import p3c_animacao
from P3CR_Animacao import p3cr_animacao
from P3CR_PontosLagrange_Grafico import p3cr_pontoslagrange_grafico
from PontosLagrange_Numerico import pontoslagrange_numerico
from PontosLagrange_por_series_Numerico import pontoslagrange_por_series_numerico
from PontosLagrange_VariandoMu_Grafico import pontoslagrange_variandomu
from Sup_Vel_Zero_Grafico import sup_vel_zero_grafico


def titulo(texto):
    print(f"\u001b[34m{texto}\u001b[0m")


p2c_dict = {1:'Eq_Kepler_Numerico', 2:'P2C_EDO_Animacao', 3:'P2C_EDO_Animacao_VariosReferenciais', 4:'P2C_EDO_Grafico_e_Animacao',
            5:'P2C_EDO_Grafico_e_Animacao_VariosCorpos', 6:'Sistema_Solar_Animacao'}
p3c_dict = {1:'P3C_Animacao', 2:'P3CR_Animacao', 3:'P3CR_PontosLagrange_Grafico', 4:'PontosLagrange_Numerico',
            5:'PontosLagrange_por_series_Numerico', 6:'PontosLagrange_VariandoMu_Grafico', 7:'Sup_Vel_Zero_Grafico'}

titulo("\n       Muito bem vindos e bem vindas ao PlanLab - Laboratório Planetário")

continuar = True

while continuar:
    tipo_problema = int(input('Para simulações do Problema de 2 Corpos digite 1'
                              '\nPara simulações do Problema de 3 Corpos digite 2\nEscolha: '))

    if tipo_problema == 1:
        print('\nDigite o número do módulo que deseja utilizar')
        for chave, modulo in p2c_dict.items():
            print(f'{chave} para {modulo}')
        escolha = int(input('Escolha: '))

        if escolha == 1:
            print(f'\nMódulo Selecionado: {p2c_dict.get(escolha)}.\n')
            eq_Kepler_numerico()

        if escolha == 2:
            print(f'\nMódulo Selecionado: {p2c_dict.get(escolha)}.\n')
            p2c_EDO_animacao()

        if escolha == 3:
            print(f'\nMódulo Selecionado: {p2c_dict.get(escolha)}.\n')
            p2c_EDO_animacao_variosreferenciais()

        if escolha == 4:
            print(f'\nMódulo Selecionado: {p2c_dict.get(escolha)}.\n')
            p2c_EDO_grafico_e_animacao()

        if escolha == 5:
            print(f'\nMódulo Selecionado: {p2c_dict.get(escolha)}.\n')
            p2c_EDO_Grafico_e_Animacao_VariosCorpos()

        if escolha == 6:
            print(f'\nMódulo Selecionado: {p2c_dict.get(escolha)}.\n')
            sistema_solar_animacao()

        aux = input('Deseja realizar outra simulação (y/n)?')
        if aux == 'n':
            continuar = False

    elif tipo_problema == 2:
        print('Digite o número do módulo que deseja utilizar')
        for chave, modulo in p3c_dict.items():
            print(f'{chave} para {modulo}')
        escolha = int(input('Escolha: '))

        if escolha == 1:
            print(f'\nMódulo Selecionado: {p3c_dict.get(escolha)}.\n')
            p3c_animacao()

        if escolha == 2:
            print(f'\nMódulo Selecionado: {p3c_dict.get(escolha)}.\n')
            p3cr_animacao()

        if escolha == 3:
            print(f'\nMódulo Selecionado: {p3c_dict.get(escolha)}.\n')
            p3cr_pontoslagrange_grafico()

        if escolha == 4:
            print(f'\nMódulo Selecionado: {p3c_dict.get(escolha)}.\n')
            pontoslagrange_numerico()

        if escolha == 5:
            print(f'\nMódulo Selecionado: {p3c_dict.get(escolha)}.\n')
            pontoslagrange_por_series_numerico()

        if escolha == 6:
            print(f'\nMódulo Selecionado: {p3c_dict.get(escolha)}.\n')
            pontoslagrange_variandomu()

        if escolha == 7:
            print(f'\nMódulo Selecionado: {p3c_dict.get(escolha)}.\n')
            sup_vel_zero_grafico()

        aux = input('Deseja realizar outra simulação (y/n)?')
        if aux == 'n':
            continuar = False

    else:
        print('Opção incorreta! Digite uma opção válida.')


