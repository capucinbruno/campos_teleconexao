#!/usr/bin/env python3

"""Compute Rossby wave source from the long-term mean flow.

This example uses the iris interface.

Additional requirements for this example:

* iris (http://scitools.org.uk/iris/)
* matplotlib (http://matplotlib.org/)
* cartopy (http://scitools.org.uk/cartopy/)

Author: Bruno Capucin 
Date: 22/05/2024

"""
import warnings
import numpy as np
import cartopy.crs as ccrs
import iris
import iris.plot as iplt
import matplotlib as mpl
import matplotlib.pyplot as plt

from windspharm.iris import VectorWind

mpl.rcParams['mathtext.default'] = 'regular'

def main():
    # Substituir temporariamente np.int por int
    np.int = int

    # Caminho dos dados de exemplo (atualize conforme necessário)
    uwnd_path = './uwnd.nc'  # Caminho dos arquivos na raiz do projeto
    vwnd_path = './vwnd.nc'  # Caminho dos arquivos na raiz do projeto

    # Leia os componentes de vento zonal e meridional dos arquivos usando o módulo iris.
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', UserWarning)
        uwnd = iris.load_cube(uwnd_path)
        vwnd = iris.load_cube(vwnd_path)

    if uwnd is None or vwnd is None:
        print("Erro ao carregar os dados dos arquivos NetCDF.")
        return

    print("Dados de vento carregados com sucesso.")
    print(uwnd)
    print(vwnd)

    print("Datas disponíveis em uwnd:")
    for coord in uwnd.coords():
        if coord.name() == 'time':
            print(coord.units.num2date(coord.points))

    print("Datas disponíveis em vwnd:")
    for coord in vwnd.coords():
        if coord.name() == 'time':
            print(coord.units.num2date(coord.points))

    uwnd.coord('longitude').circular = True
    vwnd.coord('longitude').circular = True

    # Crie uma instância do VectorWind para lidar com os cálculos.
    w = VectorWind(uwnd, vwnd)

    # Calcule os componentes da fonte de ondas de Rossby.
    eta = w.absolutevorticity()
    div = w.divergence()
    uchi, vchi = w.irrotationalcomponent()
    etax, etay = w.gradient(eta)

    # Definir unidades de etax e etay se não estiverem definidas
    if etax.units.is_unknown():
        etax.units = 'm-1 s-1'
    if etay.units.is_unknown():
        etay.units = 'm-1 s-1'

    # Verificar e ajustar as unidades para garantir compatibilidade
    etax.convert_units('m-1 s-1')
    etay.convert_units('m-1 s-1')

    # Combine os componentes para formar o termo da fonte de ondas de Rossby.
    S = eta * -1. * div - (uchi * etax + vchi * etay)
    S.coord('longitude').attributes['circular'] = True

    # Selecionar a única fatia de tempo disponível para obter um cubo bidimensional.
    S_2d = S[0, :, :]

    print("Dados extraídos com sucesso.")

    # Plote a fonte de ondas de Rossby.
    clevs = [-30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30]
    ax = plt.subplot(111, projection=ccrs.PlateCarree(central_longitude=180))
    fill = iplt.contourf(S_2d * 1e11, clevs, cmap=plt.cm.RdBu_r, extend='both')
    ax.coastlines()
    ax.gridlines()
    plt.colorbar(fill, orientation='horizontal')
    plt.title('Rossby Wave Source ($10^{-11}$s$^{-2}$)', fontsize=16)

    # Salvar a imagem em um arquivo
    plt.savefig('rossby_wave_source.png')

    # Fechar a figura para liberar memória
    plt.close()


if __name__ == "__main__":
    main()
    