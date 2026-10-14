# junta simulacoes do miluphcuda num unico ASCII no formato de entrada (19 colunas)
#
# formato de entrada (19 col):
#   1-3 x | 4-6 v | 7 massa | 8 rho | 9 energia | 10 material | 11-19 tensor S
# formato de saida do miluphcuda (23 col):
#   1-3 x | 4-6 v | 7 massa | 8 rho | 9 energia | 10 sml | 11 n vizinhos |
#   12 material | 13 pressao | 14 local_strain | 15-23 tensor S
#
# o tipo de cada arquivo e detectado pelo numero de colunas:
#   23 -> saida de simulacao que ja rodou (convertido para entrada)
#   19 -> ja esta em formato de entrada (so anexado)
#
# by sfair (141026.1709)

import argparse
import sys

import numpy as np

ENERGY = True  # padrao; False zera a energia de todas as particulas
N_IN = 19  # colunas do formato de entrada
N_OUT = 23  # colunas do formato de saida

# colunas (0-based) da saida que vao para a entrada: x,v,m,rho,e / material / S
OUT_TO_IN = list(range(0, 9)) + [11] + list(range(14, 23))

ap = argparse.ArgumentParser(
    description='Junta arquivos do miluphcuda (saida de 23 col ou entrada de 19 col) '
                'em um unico ASCII no formato de entrada (19 col).',
    epilog='exemplo: python merge_sph.py simu.0150 impa.0000 -o merged.0000 --zero-energy')
ap.add_argument('files', nargs='+',
                help='arquivos a juntar, na ordem em que serao escritos '
                     '(ex: caixa que ja rodou, depois projetil)')
ap.add_argument('-o', '--output', default='merged.0000',
                help='arquivo de saida (padrao: %(default)s)')
ap.add_argument('--zero-energy', action='store_true',
                help='zera a energia de todas as particulas')
if len(sys.argv) == 1:  # sem parametros: mostra o help
    ap.print_help()
    sys.exit(0)
args = ap.parse_args()

# le cada arquivo e converte para o formato de entrada se preciso
parts = []
for fname in args.files:
    data = np.loadtxt(fname, ndmin=2)
    ncol = data.shape[1]
    if ncol == N_OUT:
        # ja rodou: descarta sml, vizinhos, pressao e local_strain
        data = data[:, OUT_TO_IN]
        kind = 'saida (convertido)'
    elif ncol == N_IN:
        kind = 'entrada (anexado)'
    else:
        sys.exit(f'{fname}: {ncol} colunas, esperado {N_IN} ou {N_OUT}')
    print(f'{fname}: {data.shape[0]} particulas, {kind}')
    parts.append(data)

# junta tudo, na ordem dada
merged = np.vstack(parts)

# energia: --zero-energy tem prioridade sobre ENERGY
if args.zero_energy or not ENERGY:
    merged[:, 8] = 0.0
    print('energia zerada')

if not np.all(np.isfinite(merged)):
    sys.exit('NaN/inf no resultado')

# escreve em precisao total; material (col 10) como inteiro
fmt = ['%.15e'] * N_IN
fmt[9] = '%d'
np.savetxt(args.output, merged, fmt=fmt, delimiter='\t')

# resumo: particulas por material
print(f'{args.output}: {merged.shape[0]} particulas, {merged.shape[1]} colunas')
mats, counts = np.unique(merged[:, 9].astype(int), return_counts=True)
for m, c in zip(mats, counts):
    print(f'  material {m}: {c}')
