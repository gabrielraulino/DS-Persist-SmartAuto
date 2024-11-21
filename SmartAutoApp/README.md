# Guia Rápido: Conventional Commits

**Conventional Commits** é um padrão para escrever mensagens de commit claras e consistentes, facilitando a compreensão das mudanças no código. A estrutura básica da mensagem é:

```
<tipo>[escopo opcional]: <descrição>
```

## Estrutura de Conventional Commit

- **`tipo`**: Define a natureza da mudança.
- **`escopo` (opcional)**: Indica a parte do código que está sendo afetada.
- **`descrição`**: Explicação curta e clara da mudança.

### Tipos Comuns de Commits

- **feat**: Adiciona uma nova funcionalidade ao código.
  - Exemplo: `feat: adicionar página de login`
  - Significa que uma nova página de login foi implementada no sistema.

- **fix**: Corrige um bug ou problema.
  - Exemplo: `fix: corrigir erro na validação do formulário`
  - Isso indica que havia um problema de validação que foi resolvido.

- **chore**: Para mudanças de manutenção que não alteram funcionalidades (configuração, builds, etc.).
  - Exemplo: `chore: adicionar arquivo .gitignore`
  - Neste caso, foi adicionado um arquivo de configuração `.gitignore` que não afeta o funcionamento do código.

- **docs**: Modificações na documentação.
  - Exemplo: `docs: atualizar README com instruções de instalação`
  - Atualizou o arquivo README para incluir informações sobre como instalar o projeto.

- **style**: Alterações de formatação, sem impacto no código (ex.: espaços, vírgulas).
  - Exemplo: `style: ajustar identação em arquivo`
  - Ajustes de formatação, como corrigir a identação, sem alterar a lógica do código.

- **refactor**: Refatoração do código sem alterar a funcionalidade.
  - Exemplo: `refactor: melhorar lógica do método de autenticação`
  - Indica que a lógica do método de autenticação foi melhorada sem mudanças na funcionalidade.

- **test**: Adição ou modificação de testes.
  - Exemplo: `test: adicionar testes para o serviço de usuário`
  - Foram adicionados testes unitários para o serviço relacionado ao usuário.

- **perf**: Mudanças que melhoram a performance.
  - Exemplo: `perf: otimizar consulta ao banco de dados`
  - A consulta ao banco foi otimizada para melhorar o desempenho.

- **build**: Mudanças que afetam o sistema de build ou dependências externas.
  - Exemplo: `build: atualizar dependências no package.json`
  - Foram atualizadas dependências do projeto no arquivo `package.json`.

- **ci**: Mudanças relacionadas ao processo de integração contínua.
  - Exemplo: `ci: corrigir script do pipeline no GitHub Actions`
  - Corrigiu o script responsável pelo pipeline de CI no GitHub Actions.

### Exemplos de Mensagens de Commit

1. **Adicionar uma nova funcionalidade**:

   ```
   feat: implementar autenticação JWT
   ```

   - Uma nova funcionalidade para autenticar usuários usando JWT foi implementada.

2. **Corrigir um bug**:

   ```
   fix: corrigir erro ao salvar perfil do usuário
   ```

   - Um bug que impedia salvar o perfil do usuário foi corrigido.

3. **Adicionar arquivo de configuração**:

   ```
   chore: adicionar arquivo de configuração ESLint
   ```

   - Adicionou um arquivo de configuração do ESLint para garantir padrões de código.

4. **Atualizar documentação**:

   ```
   docs: adicionar seção sobre configurações do ambiente
   ```

   - Documentou como configurar o ambiente de desenvolvimento.

## Benefícios dos Conventional Commits

- **Padronização**: Mensagens consistentes que ajudam a entender a mudança sem olhar o código.
- **Automação**: Facilita o versionamento semântico, geração de changelogs e automação de releases.
- **Colaboração**: Melhora a comunicação entre desenvolvedores sobre o histórico de alterações.

Para mais informações detalhadas, visite [Conventional Commits](https://www.conventionalcommits.org/).
