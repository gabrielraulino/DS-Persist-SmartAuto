# Trabalho Prático 1 (TP1)

## 1. Definição da Entidade

Defina uma entidade com pelo menos 5 atributos relacionada ao domínio escolhido pela dupla no Trabalho Prático 0 (TP0). Crie uma classe Python para representar a entidade escolhida. **Exemplo de entidade com 9 atributos**:

- **Cliente**: id, nome, cpf, endereço, email, fone, cidade, uf, cep.

A entidade escolhida por você **não pode ser a entidade Cliente** dada como exemplo. Escolha uma entidade bem diferente dela, inclusive quanto aos seus atributos.

---

## 2. Criação da API REST usando FastAPI

Criar uma API REST usando **FastAPI** com endpoints para realizar as seguintes funcionalidades (Fx), onde cada funcionalidade deve ser realizada em um endpoint específico:

### F1. Inserção de Dados da Entidade

Enviar um JSON contendo os dados da entidade escolhida para o endpoint de inserção de sua API e inserir a entidade em um arquivo CSV. Ou seja, cadastrar dados relacionados à entidade definida na questão 1. A entidade deve ser adicionada ao arquivo CSV através de um **append**.

### F2. Retornar Todas as Entidades

Retornar um JSON contendo todas as entidades cadastradas no CSV através de um endpoint de sua API.

### F3. CRUD Completo

Fazer o CRUD completo da entidade usando o padrão de API REST, sempre atualizando o CSV.

### F4. Quantidade de Entidades

Mostrar a quantidade de entidades existentes no arquivo CSV através de um endpoint específico. Esta funcionalidade deve mostrar a real quantidade de entidades existentes no arquivo CSV, mesmo que dados sejam inseridos ou removidos no arquivo CSV através de um editor de texto externo à sua aplicação.

### F5. Compactar o CSV

Compactar o arquivo CSV e gerar um novo arquivo de mesmo nome, mas com a extensão **ZIP** e retorná-lo através de um endpoint específico de sua API.

### F6. Retornar o Hash SHA256

Retornar o **hash SHA256** do arquivo CSV através de um endpoint de sua API.

---

## 3. Divisão de Tarefas

Crie um arquivo (`divisao_tarefas.txt`) detalhando a divisão de tarefas e mostrando o que cada membro da dupla efetivamente fez no trabalho. Divida as tarefas definidas entre os membros da dupla.

---

## Observações

1. A apresentação do trabalho é **obrigatória e presencial** para ambos os membros da dupla, sendo **5 minutos** o tempo para cada membro falar. Se algum membro da dupla não apresentar o trabalho, ficará com nota **ZERO**. Não será permitida apresentação remota. A nota pode ser diferente entre os membros da dupla, dependendo da apresentação e das atividades realizadas no trabalho.

2. Cada funcionalidade acima deve estar definida em uma ou mais classe(s) específica(s). Ou seja, **modularize seu código**.

3. Envie o código-fonte e o arquivo CSV com pelo menos **10 entidades** já cadastradas.

4. Envie dados que sejam o mais próximo possível de **dados reais**. Evite de todo modo preencher um atributo com valores aleatórios como "sadfadsfasdfasd".
