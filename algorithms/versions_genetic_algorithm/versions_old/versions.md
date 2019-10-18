Seguem especificações e data planejada de entrega:

Versão 1:
AG Base
- Cria rota de um ponto a outro, considerando as restrições do mapa
- Horizonte de planejamento (T) escolhido hardcoded
Entrega: 04.10 (hoje)
Reunião 06/10 (Domingo) [Talvez]


Versão 2: 
T como parâmetro para otimização
- O DNA do indivíduo pode ter tamanho variável
- Novo crossover:
    - 50% de chance de escolher o gene do pai 1, 50% de escolher do pai 2, se algum dos pais não tiver o gene, não passa para o filho.
- Novas formas de mutação (1/3 de chance de ecolher uma delas):
    - Insere gene (insere aleatoriamete um gene)
    - Remove gene (remove aleatoriamente um gene)
    - Creep  (igual versao 1)
Entrega: 06/10 (Domingo)
Reunião 08/10 (Terça)


Versão 3:
Alocação de Risco (relaxada)
- Inflar o tamanho das áreas em x% e considerar esse novo tamanho para calcular o fitness
Entrega: 11/10 (Sexta)
Reunião 11/10 (Sexta)


Versão 2_3:
Junção das versões 2 com 3


Versão 3.5:
Adicionada alocação de risco como definida pelo Marcio


Versão 4:
Planejamento em 3D
- Adaptar o algoritmo para considerar o mapa, rotas e dna em 3 dimensões, adicionando a altura
Entrega: 15/10 (Terça)
Reunião: 15/10 (Terça)


Versões posteriores:
- Melhorar alocação de risco, para uma forma mais legal
- Melhorar alocação de risco seguindo o que o jesimar propôs