# Paredes (caixa aberta em cima)

Caixa de ±20 cm em x e y, chão em z = 0, aberta em z. Mesma ideia do `test_cases/dam`: as paredes
são partículas SPH normais de um material próprio (ID 1), colocadas no arquivo de entrada e
travadas no lugar.

## 1. Ideia

As partículas da parede não se movem, mas a densidade delas continua sendo integrada
(`drhodt`). Quando a areia empurra a parede, a densidade da parede sobe, a equação de estado
transforma isso em pressão, e o gradiente de pressão empurra a areia de volta. Não tem
partícula espelho, força de Lennard-Jones nem código especial nas forças SPH (é o método de
"dynamic boundary particles", Crespo et al. 2007).

Não usar `BOUNDARY_PARTICLE_ID` (-1): tem o mesmo valor de `EOS_TYPE_IGNORE`, então o laço de
forças (`internal_forces.cu:271`) pula essas partículas e a areia atravessa a parede.

## 2. parameter.h

```c
#define SFAIR_WALLS 1       // trava as partículas do material SFAIR_WALL_MATID
#define SFAIR_WALL_MATID 1  // ID do material da parede (tem que existir no material.cfg)
```

## 3. boundary.cu

Em `BoundaryConditionsAfterRHS`, depois da gravidade e do chão, para `matId == SFAIR_WALL_MATID`:

- zera `a`, `v` e `dxdt/dydt/dzdt` (isso também desfaz a gravidade na parede)
- zera `S` e `dSdt` (SOLID): a parede só empurra com pressão
- zera `dedt` (INTEGRATE_ENERGY)
- **não** zera `drhodt`: é daí que vem a pressão da parede

## 4. material.cfg

```
{
    ID = 1
    name = "Wall"
    sml = <igual à areia>
    interactions = 30
    artificial_viscosity = { alpha = <igual à areia>; beta = <igual à areia>; };
    eos = {
        type = 1              # Murnaghan
        bulk_modulus = <igual à areia, no máximo 2-3x>
        n = 7
        rho_0 = <densidade inicial das partículas da parede>
        rho_limit = 1.0
        shear_modulus = 0.0
    };
}
```

- Murnaghan: pressão só depende da densidade, sem os problemas do Tillotson.
- `rho_0` igual à densidade inicial: pressão zero no início.
- `rho_limit = 1.0`: abaixo de `rho_0` a pressão é zero, a parede empurra mas não puxa.
- `n = 7`: endurece rápido quando a areia entra, sem aumentar o som em repouso.
- `shear_modulus = 0`: o passo de tempo usa `cs² + 4/3 G/ρ` de todas as partículas, inclusive
  as travadas (`rk2adaptive.cu:534`).

## 5. Arquivo de entrada

- parede com o mesmo espaçamento, massa e densidade da areia (m/ρ = Δ³)
- pelo menos 3 camadas (o suporte do kernel é `sml`), melhor 4, incluindo arestas e cantos
- chão abaixo de z = 0, paredes laterais fora de |x|, |y| = 0.20
- areia começando em z = Δ/2
- massa escrita com `%e`

## Observações

- `artificial_viscosity` da parede não muda nada na areia: `internal_forces.cu:159` usa o alpha
  da própria partícula.
- Não existe coeficiente de atrito areia-parede. A parede tem v = 0 (não desliza), então o atrito
  na parede é o atrito interno da areia.
- Com as paredes, `SFAIR_FLOOR` vira só uma rede de segurança. Para testar a parede, usar 0.

## Checklist

- parameter.h: `SFAIR_WALLS 1`, `SFAIR_WALL_MATID 1`
- material.cfg: material 1 definido
- arquivo de entrada: partículas da parede com material 1
- areia com `friction_angle` e densidade inicial igual à de referência (ver Sand.md)
