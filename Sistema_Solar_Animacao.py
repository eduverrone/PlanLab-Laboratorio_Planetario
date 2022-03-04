# Sistema Solar

from numpy import *
from vpython import *
import mpmath as mp  # Módulo "Math" que realiza cálculos com maiores precisões e mais dígitos.

def Cameras(cam):
    global camval
    camval = cam.selected


def Rastros(b):
    global mercurio, venus, terra, marte, jupiter, saturno, urano, netuno, plutao
    if b.checked:
        mercurio.make_trail = True
        venus.make_trail = True
        terra.make_trail = True
        marte.make_trail = True
        jupiter.make_trail = True
        saturno.make_trail = True
        urano.make_trail = True
        netuno.make_trail = True
        plutao.make_trail = True
    else:
        mercurio.make_trail = False
        mercurio.clear_trail()
        venus.make_trail = False
        venus.clear_trail()
        terra.make_trail = False
        terra.clear_trail()
        marte.make_trail = False
        marte.clear_trail()
        jupiter.make_trail = False
        jupiter.clear_trail()
        saturno.make_trail = False
        saturno.clear_trail()
        urano.make_trail = False
        urano.clear_trail()
        netuno.make_trail = False
        netuno.clear_trail()
        plutao.make_trail = False
        plutao.clear_trail()


# Função com as Equações diferenciais a serem resolvidas:

def resolve_EDO_P2C(r):
    G = 6.674E-20  # Constante Gravitacional Universal (km³/s²kg)
    x = r[0]
    y = r[1]
    z = r[2]
    Vx = r[3]
    Vy = r[4]
    Vz = r[5]

    r12 = mp.sqrt((math.fabs(x) ** 2) + (math.fabs(y) ** 2) + (math.fabs(z) ** 2))
    mod_r12 = float(r12) ** 3

    dx = Vx
    dVx = (-G * MC * x / mod_r12)
    dy = Vy
    dVy = (-G * MC * y / mod_r12)
    dz = Vz
    dVz = (-G * MC * z / mod_r12)

    return array([dx, dy, dz, dVx, dVy, dVz], float)


# --------------------------------------------------------------------------------------------------------#

def passo_rk4(f, r, h):  # Calcula um passo no método de RK4
    k1 = h * f(r)
    k2 = h * f(r + 0.5 * k1)
    k3 = h * f(r + 0.5 * k2)
    k4 = h * f(r + k3)
    return (k1 + 2.0 * (k2 + k3) + k4) / 6.0


def sistema_solar_animacao():
    # Definições da cena
    global camval
    camval = 'Centralizada'
    check1 = checkbox(bind=Rastros, text='Rastros', checked=True)
    scene.append_to_caption('\n\n')
    menu(choices=['Sol', 'Mercurio', 'Vênus', 'Terra', 'Marte', 'Jupiter', 'Saturno', 'Urano', 'Netuno', 'Plutao'],
         index=0, bind=Cameras)

    h = 12 * 1800  # Taxa de atualização

    # Intruções para criação da cena animada

    scene.width = 1300  # Ajustando a largura da cena
    scene.height = 600  # Ajustando a altura da cena

    # Criando os objetos :
    raio_sol = 696340  # Raio em km.
    raio_mercurio = raio_sol * 12
    raio_venus = raio_sol * 20
    raio_terra = raio_sol * 22
    raio_marte = raio_sol * 17
    raio_jupiter = raio_sol * 70
    raio_saturno = raio_sol * 66
    raio_urano = raio_sol * 60
    raio_netuno = raio_sol * 54
    raio_plutao = raio_sol * 50

    # Sol:
    global MC
    MC = 1.9891E30  # Massa do Sol em kg

    sol = sphere(color=color.yellow, texture='sol.jpg', radius=raio_sol*35, pos=vector(0, 0, 0))
    sol.emissive = True

    global mercurio, venus, terra, marte, jupiter, saturno, urano, netuno, plutao

    # Mercúrio:

    r_mercurio = [-3.211042384065869E+07, -6.133099506740444E+07, -2.207406599878620E+06,
                  3.377727433252360E+01, -1.938714111553416E+01, 4.681979918561893E+00]

    mercurio = sphere(trail_color=vector(0.733, 0.193, 1), texture='mercurio.jpg', radius=raio_mercurio,
                      pos=vector(-3.211042384065869E+07, -6.133099506740444E+07, -2.207406599878620E+06),
                      make_trail=True)
    mercurio.emissive = True

    # Vênus:

    r_venus = [-1.813678730341380E+07, -1.066919142129803E+08, -4.734174817275628E+05,
               3.434988677016680E+01, -5.608384752210371E+00, -2.059126070772481E+00]
    venus = sphere(texture='venus.jpg', radius=raio_venus,
                   pos=vector(-1.813678730341380E+07, -1.066919142129803E+08, -4.734174817275628E+05),
                   make_trail=True)
    venus.emissive = True

    # Terra:

    r_terra = [1.392627774251799E+08, -5.470720423988941E+07, 2.492040641907975E+04,
               1.044004739740129E+01, 2.758938181012689E+01, -2.012489341177925E-03]
    terra = sphere(texture='terra.jpg', radius=raio_terra,
                   pos=vector(1.392627774251799E+08, -5.470720423988941E+07, 2.492040641907975E+04),
                   make_trail=True, trail_color=vector(0.194, 0.768, 1))
    terra.emissive = True

    # Marte:

    r_marte = [-2.483797394905732E+08, 8.756550023827352E+06, 6.255873883108983E+06,
               9.857193500312957E-02, -2.216041854070219E+01, -4.664543182981067E-01]
    marte = sphere(trail_color=color.red, texture='marte.jpg', radius=raio_marte,
                   pos=vector(-2.483797394905732E+08, 8.756550023827352E+06, 6.255873883108983E+06),
                   make_trail=True)
    marte.emissive = True

    # Júpiter:

    r_jupiter = [6.357522316130161E+08, -3.974443998003851E+08, -1.257449653924212E+07,
                 6.767247408403097E+00, 1.169346808336937E+01, -1.999126209465336E-01]
    jupiter = sphere(trail_color=color.yellow, texture='jupiter.jpg', radius=raio_jupiter,
                     pos=vector(6.357522316130161E+08, -3.974443998003851E+08, -1.257449653924212E+07),
                     make_trail=True)
    jupiter.emissive = True

    # Saturno:

    r_saturno = [9.707625365307162E+08, -1.125418969161673E+09, -1.908119381256092E+07,
                 6.773130552371348E+00, 6.288832963828538E+00, -3.793165798457954E-01]
    saturno = sphere(trail_color=color.orange, texture='saturno.jpg', radius=raio_saturno,
                     pos=vector(9.707625365307162E+08, -1.125418969161673E+09, -1.908119381256092E+07),
                     make_trail=True)
    saturno.emissive = True

    # Urano:

    r_urano = [2.201554899712750E+09, 1.967275437265797E+09, -2.121498890682459E+07,
               -4.587514533463052E+00, 4.760727920733888E+00, 7.715692953375908E-02]
    urano = sphere(trail_color=color.cyan, texture='urano.jpg', radius=raio_urano,
                   pos=vector(2.201554899712750E+09, 1.967275437265797E+09, -2.121498890682459E+07),
                   make_trail=True)
    urano.emissive = True

    # Netuno:

    r_netuno = [4.423974281651327E+09, -6.684911740584540E+08, -8.818863984685892E+07,
                7.768095134604484E-01, 5.407059578925518E+00, -1.293268682871482E-01]
    netuno = sphere(trail_color=color.blue, texture='netuno.jpg', radius=raio_netuno,
                    pos=vector(4.423974281651327E+09, -6.684911740584540E+08, -8.818863984685892E+07),
                    make_trail=True)
    netuno.emissive = True

    # Plutão:

    r_plutao = [2.208670967238895E+09, -4.636856993282572E+09, -1.427053256678238E+08, 
                5.054479440602560E+00, 1.176221309292655E+00, -1.594934162431775E+00]
    plutao = sphere(trail_color=color.magenta, texture='plutao.jpg', radius=raio_plutao, 
                    pos=vector(2.208670967238895E+09, -4.636856993282572E+09, -1.427053256678238E+08),
                    make_trail=True)
    plutao.emissive = True

    # Laço de realização dos Cálculos:
    while True:
        rate(100)  # Frequencia de atualização da cena

        # Mercurio
        dr_mercurio = passo_rk4(resolve_EDO_P2C, r_mercurio, h)
        r_mercurio = r_mercurio + dr_mercurio
        mercurio.pos = vector(r_mercurio[0], r_mercurio[1], r_mercurio[2])
        

        # Vênus
        dr_venus = passo_rk4(resolve_EDO_P2C, r_venus, h)
        r_venus = r_venus + dr_venus
        venus.pos = vector(r_venus[0], r_venus[1], r_venus[2])

        # Terra
        dr_terra = passo_rk4(resolve_EDO_P2C, r_terra, h)
        r_terra = r_terra + dr_terra
        terra.pos = vector(r_terra[0], r_terra[1], r_terra[2])


        # Marte
        dr_marte = passo_rk4(resolve_EDO_P2C, r_marte, h)
        r_marte = r_marte + dr_marte
        marte.pos = vector(r_marte[0], r_marte[1], r_marte[2])


        # Júpiter
        jupiter.pos = vector(r_jupiter[0], r_jupiter[1], r_jupiter[2])
        dr_jupiter = passo_rk4(resolve_EDO_P2C, r_jupiter, h)
        r_jupiter = r_jupiter + dr_jupiter

        # Saturno
        saturno.pos = vector(r_saturno[0], r_saturno[1], r_saturno[2])
        dr_saturno = passo_rk4(resolve_EDO_P2C, r_saturno, h)
        r_saturno = r_saturno + dr_saturno

        # Urano
        urano.pos = vector(r_urano[0], r_urano[1], r_urano[2])
        dr_urano = passo_rk4(resolve_EDO_P2C, r_urano, h)
        r_urano = r_urano + dr_urano

        # Netuno
        netuno.pos = vector(r_netuno[0], r_netuno[1], r_netuno[2])
        dr_netuno = passo_rk4(resolve_EDO_P2C, r_netuno, h)
        r_netuno = r_netuno + dr_netuno

        # Plutão
        plutao.pos = vector(r_plutao[0], r_plutao[1], r_plutao[2])
        dr_plutao = passo_rk4(resolve_EDO_P2C, r_plutao, h)
        r_plutao = r_plutao + dr_plutao


        # Camera
        if camval == "Sol":
            scene.center = vector(0, 0, 0)
        elif camval == "Mercurio":
            scene.center = mercurio.pos
        elif camval == "Vênus":
            scene.center = venus.pos
        elif camval == "Terra":
            scene.center = terra.pos
        elif camval == "Marte":
            scene.center = marte.pos
        elif camval == "Jupiter":
            scene.center = jupiter.pos
        elif camval == "Saturno":
            scene.center = saturno.pos
        elif camval == "Urano":
            scene.center = urano.pos
        elif camval == "Netuno":
            scene.center = netuno.pos
        elif camval == "Plutao":
            scene.center = plutao.pos


if __name__ == '__main__':
    sistema_solar_animacao()
