# Chão e gravidade no miluphcuda

Notas a partir do `test_cases/dam` (boundary.cu, parameter.h, material.cfg, dam_triangle.py).

## 1. parameter.h

```c
#define GHOST_BOUNDARIES 0
#define DIM 2               // se o problema é 2D, usar 2. O dam usa DIM 3 com z=0, o que não é bom
#define INTEGRATE_DENSITY 1 // opcional: integra rho em vez do somatório SPH
```

O resto (`INTEGRATE_ENERGY`, `TENSORIAL_CORRECTION`, `XSPH`, `MAX_NUM_INTERACTIONS`) depende do
problema e não interfere no chão.

## 2. boundary.cu

Chão e gravidade entram em `BoundaryConditionsAfterRHS`, chamada depois das forças SPH
(`rhs.cu:554`). No começo do loop sobre as partículas:

```c
matId = p.materialId[i];

if (matId == 0) {
    p.ay[i] -= 9.81;
} else {
    p.ax[i] = 0.0;
    p.ay[i] = 0.0;
    p.vx[i] = 0.0;
    p.vy[i] = 0.0;
#if DIM == 3
    p.az[i] = 0.0;
    p.vz[i] = 0.0;
#endif
}
```

Aqui a trava é feita pelo `matId`. Dá para trocar por um chão aplicado a todas as partículas
(como em Sand.md) e depois ajustar de acordo com o `matId`.

## Checklist

- parameter.h: `GHOST_BOUNDARIES 0`, `DIM` certo
- boundary.cu: gravidade e trava do chão em `BoundaryConditionsAfterRHS`
- compilar com os arquivos alterados
- rodar sem `-s`
