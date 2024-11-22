# DS-Persist-SmartAuto

Destinado a disciplina Desenvolvimento de Software Para Persistência

Sistema de locação e venda de veículos SmartAuto.

Aqui estarão todos arquivos e etapas do trabalho.

## Descrição do trabalho

O sistema terá os modelos: Admin, Gerente, Vendedor,  Cliente, Veiculo, Venda, Locacao e Endereco.

- Endereco terá `id`, `uf`, `cidade`,`logradouro` e `numero`
- Funcionario será a classe base para os modelos citados a cima e terá os seguintes atributos: `id`, `user` `password` e `nome`, `telefone` e `role
- Para definir as permissões terá um enum com definindo cada função que funcionário poderá obter.
- O Vendedor poderá inserir veículos e clientes e realizar vendas e locações.
- O Gerente poderá inserir vendedores, remover Cliente e remover Veiculo.
- Admin tem permissão total, podendo excluir qualquer entidade.
- O Cliente terá `id`, `nome`, `telefone`, `email`, `endereco` e poderá visualizar veículos disponíveis.
- Venda terá `id`, `data`, `valor`, `cliente`, `veiculo`, `vendedor`.
  - Para cada venda uma entidade é criada e armazenada
- Locacao terá `data_inicio`, `data_fim`, `valor_diaria`, `cliente`, `vendedor` e `veiculo`.
  - Para cada locacao uma entidade é criada e armazenada
