# DS-Persist-SmartAuto

Destinado a disciplina Desenvolvimento de Software Para Persistência

Sistema de locação e venda de veículos SmartAuto.

Aqui estarão todos arquivos e etapas do trabalho.

## Descrição do trabalho

O sistema terá os modelos: Admin, Gerente, Vendedor, Cliente, Veiculo, Venda, Locacao e Categoria.

### Entidades

#### Cliente

- `id`: int
- `nome`: str
- `telefone`: str
- `email`: str
- `uf`: str
- `cidade`: str
- `logradouro`: str
- `numero`: int

#### Funcionario

- `id`: int
- `usuario`: str
- `senha`: str
- `nome`: str
- `telefone`: str
- `funcao`: Role (enum: `VENDEDOR`, `GERENTE`, `ADMIN`)

#### Veiculo

- `id`: int
- `marca`: str
- `modelo`: str
- `ano`: int
- `fipe`: float
- `disponivel`: bool
- `cor`: str

#### Venda

- `id`: int
- `data`: date
- `valor`: float
- `cliente_id`: int (referência para Cliente)
- `veiculo_id`: int (referência para Veiculo)
- `vendedor_id`: int (referência para Funcionario)

#### Locacao

- `id`: int
- `data_inicio`: date
- `data_fim`: date
- `valor_diaria`: float
- `cliente_id`: int (referência para Cliente)
- `vendedor_id`: int (referência para Funcionario)
- `veiculo_id`: int (referência para Veiculo)

#### Categoria

- `id`: int
- `nome`: str
- `desc`: str

### Relacionamentos

- Um `Cliente` pode ter várias `Vendas` e `Locacoes`.
- Um `Funcionario` pode ser um `VENDEDOR`, `GERENTE` ou `ADMIN`.
- Um `Veiculo` pode estar associado a várias `Vendas` e `Locacoes`.
- Uma `Venda` está associada a um `Cliente`, um `Veiculo` e um `Funcionario`.
- Uma `Locacao` está associada a um `Cliente`, um `Veiculo` e um `Funcionario`.
- Um `Veiculo` pode pertencer a uma `Categoria`.

### Permissões

- O `VENDEDOR` pode inserir veículos e clientes, e realizar vendas e locações.
- O `GERENTE` pode inserir vendedores, remover clientes e remover veículos.
- O `ADMIN` tem permissão total, podendo excluir qualquer entidade.
