# Areia 

Exemplos em `test_cases/mohr_coulomb/input` e `test_cases/drucker_prager/input`: um cilindro de
regolito é solto e colapsa numa pilha (comparação com Lube et al. 2004). Os dois exemplos têm o
mesmo material.cfg e diferem só no modelo de plasticidade ligado no parameter.h.

Chão e gravidade estão em CreateFloor.md. Aqui fica só o que muda
para sólido.

## 1. parameter.h

```c
#define DIM 3
#define SOLID 1
#define MOHR_COULOMB_PLASTICITY 1
#define DRUCKER_PRAGER_PLASTICITY 0
```

INTEGRATE_DENSITY 1 e INTEGRATE_ENERGY 0, como no dam (ver seção 3).

Tem que ligar um modelo de plasticidade, e só um. Sem plasticidade o material fica elástico e não
escoa como areia. Com os dois ligados o parameter.h dá `#error`.

## 2. Modelo de plasticidade

Duas opções: `MOHR_COULOMB_PLASTICITY` ou `DRUCKER_PRAGER_PLASTICITY` (`plasticity.cu:138`).
Ambas usam `friction_angle` e `cohesion` do material.cfg.

Os dois podem ser usados. A diferença entre eles ainda precisa ser estudada melhor.

## 3. Equação de estado

No material.cfg, `eos type = 1` é Murnaghan:

p = (K0/n) [(ρ/ρ0)^n − 1]

com `bulk_modulus` = K0, `n` e `rho_0` no bloco `eos`. A pressão depende só da densidade.

Por isso INTEGRATE_ENERGY 0: a energia interna não entra na pressão, então integrá-la só custaria
tempo e uma coluna a mais no arquivo de entrada. Energia só é necessária com equação de estado que
depende dela (Tillotson, gás ideal), em problemas com choque ou aquecimento, como impactos.

INTEGRATE_DENSITY 1: a densidade vem da equação de continuidade (dρ/dt = −ρ ∇·v) em vez do
somatório SPH (ρ = Σ m W). Perto da superfície livre e do chão a partícula tem vizinhos só de um
lado, e o somatório subestima a densidade, o que gera pressão falsa (tração) na borda. Integrando,
a densidade só muda quando o material de fato comprime ou expande.

## 4. Condições iniciais

Sugestão: um cilindro `sqrt(x²+y²) < r0`, que colapsa numa
pilha. Com SOLID 1 entram as 9 componentes de S (zeradas):

`x y z vx vy vz mass rho matId Sxx Sxy Sxz Syx Syy Syz Szx Szy Szz`

## 5. boundary.cu

Gravidade em z e chão em z = 0:

```c
p.az[i] -= 9.81;

if (p.z[i] <= 1e-3) {
    p.ax[i] = 0; p.ay[i] = 0; p.az[i] = 0;
    p.vx[i] = 0; p.vy[i] = 0; p.vz[i] = 0;
    p.dxdt[i] = 0; p.dydt[i] = 0; p.dzdt[i] = 0;
}
```

O chão é aplicado a todas as partículas. Depois dá para ajustar de acordo com o `matId`.

## Checklist

- parameter.h: `SOLID 1` e um modelo de plasticidade
- condições iniciais: as 9 componentes de S
- boundary.cu: gravidade em z e trava do chão
- rodar sem `-s`
