# Experimentos realizados:

O simbolo `# !` informa quais parâmetros foram alterados de uma versão para outra

## Mode A

Parâmetros utilizados:

```python
par_RC = {
    'taxa_cross': 5,
    'population_size': 10,
    'max_exec_time': 60,
    'C_d': 10000,
    'C_obs': 10000,
    'C_con': 500,
    'C_cur': 100,
    'C_t': 100,
    'v_min': 11.1,
    'v_max': 30.5,
    'e_min': -3,
    'e_max': 3,
    'a_min': -2.0,
    'a_max': 2.0,
    'T_min': 1,
    'T_max': 25,
    'mutation_prob': 0.7,
    'gps_imprecision': 1,
}
```

## Mode B

Parâmetros utilizados:

```python
par_RC = {
    'taxa_cross': 5,
    'population_size': 10,
    'max_exec_time': 60,
    'C_d': 100,            # !
    'C_obs': 1000,         # !
    'C_con': 0,            # !
    'C_cur': 0,            # !
    'C_t': 10,             # !
    'v_min': -3.0,         # !
    'v_max': 3.0,          # !
    'e_min': -3,
    'e_max': 3,
    'a_min': -2.0,
    'a_max': 2.0,
    'T_min': 1,
    'T_max': 25,
    'mutation_prob': 0.7,
    'gps_imprecision': 1,
}
```