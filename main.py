import numpy as np
import simplex
import constantes
import leitura
import saida
import util
import tableau_util as tableauUtil

def verificarPrecisaAuxiliar(restricoes):
    return util.maiorIgual(min(restricoes[:, -1]), 0)

def verificarPLAuxiliarViavel(tableauAuxiliar):
    return not util.igual(tableauAuxiliar[0, -1], 0)

def resolverPLFormaCanonica(n, m, vetorCusto, restricoes):
    # PL já está no formato canonico com base viável clara
    # Monta o seu tableau
    tableau = tableauUtil.montarTableauFormaCanonica(n, m, restricoes, vetorCusto)

    # Resolve o simplex
    resultado, tableauFinal = simplex.resolverSimplex(tableau, n, n+m)

    # Imprime a saída com base no resultado do simplex
    saida.saidaSimplex(resultado, tableauFinal, n, m)

def resolverPLComAuxiliar(n, m, vetorCusto, restricoes):
    # É necessário resolver a PL auxiliar para encontrar uma base viável
    # Monta o tableau da PL auxiliar
    tableauAuxiliar = tableauUtil.montarTableauAuxiliar(n, m, restricoes, vetorCusto)

    # Resolve o simplex no tableau auxiliar
    resultado, tableau = simplex.resolverSimplex(tableauAuxiliar, n, n+n+m)

    # Se o tableau auxiliar indicou que a PL é inviável
    if verificarPLAuxiliarViavel(tableau):
        # Imprime a saída com base no resultado da PL auxiliar
        saida.saidaSimplex(constantes.INVIAVEL, tableau, n, m)
    else:
        # Converte o resultado do simplex no tableau auxiliar para um tableau
        # do problema original
        tableau = tableauUtil.converterTableauAuxiliar(tableau, n, m, vetorCusto)
        
        # Resolve o tableau obtido
        resultado, tableauFinal = simplex.resolverSimplex(tableau, n, n+m)

        # Imprime a saída com base no resultado do simplex
        saida.saidaSimplex(resultado, tableauFinal, n, m)

if __name__ == '__main__':
    n, m, vetorCusto, restricoes = leitura.lerEntrada()

    # Verifica se precisa de uma PL auxiliar
    if verificarPrecisaAuxiliar(restricoes):
        resolverPLFormaCanonica(n, m, vetorCusto, restricoes)
    else:
        resolverPLComAuxiliar(n, m, vetorCusto, restricoes)
        

