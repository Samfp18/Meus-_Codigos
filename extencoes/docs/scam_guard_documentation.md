# Scam Guard - Documentação Técnica

**Scam Guard** é uma extensão de navegador desenvolvida para aumentar a segurança do usuário na navegação web, com foco em prevenção de golpes, bloqueio de downloads maliciosos e detecção de tentativas de phishing.

---

## 📁 Estrutura do Projeto

O projeto é estruturado como uma extensão de navegador, com os seguintes componentes principais:

- `manifest.json` – Arquivo de manifesto da extensão (configurações).
- `background.js` – Script em segundo plano que gerencia eventos do navegador.
- `content.js` – Script injetado nas páginas para detectar conteúdo malicioso.
- `popup.html` / `popup.js` – Interface gráfica do usuário.
- `options.html` / `options.js` – Página de configuração da extensão.
- `icons/` – Ícones da extensão para diferentes resoluções.
- `whitelist.json` – Lista de domínios confiáveis.

---

## 🚀 Funcionalidades

### 🔐 Bloqueio de Downloads Maliciosos
- Monitora a tentativa de downloads pelo navegador.
- Se a senha de segurança estiver ativada, o download é bloqueado até que o usuário insira a senha.
- Notificações são exibidas alertando o usuário.

### 🛡️ Detecção de Conteúdo Suspeito
- Analisa o DOM em tempo real.
- Identifica palavras-chave relacionadas a golpes (ex: “ganhe dinheiro rápido”, “pix imediato”, etc.).
- Alerta o usuário se encontrar sinais de manipulação psicológica.

### ✅ Whitelist (Lista de Sites Confiáveis)
- Usa uma lista de domínios confiáveis para reduzir falsos positivos.
- Exemplo de domínios liberados: `gmail.com`, `facebook.com`, `youtube.com`, `nubank.com.br`.

### 📡 Detecção de Domínios Suspeitos
- Avalia padrões de phishing baseados em similaridade de domínios (typosquatting).
- Verifica se o favicon é diferente do oficial.

### 🧠 Manipulação Psicológica
- Identifica frases comuns em fraudes.
- Mostra alertas visuais chamativos para interromper a ação do usuário.

### 🧠 Monitoramento Avançado do DOM
- Detecta pop-ups, redirecionamentos e formulários invisíveis.
- Bloqueia ações automatizadas suspeitas.

### 🔒 Verificação de Formulários
- Valida o destino de formulários.
- Verifica se dados sensíveis estão sendo enviados para sites inseguros.

---

## ⚙️ Como Usar

1. Instale a extensão manualmente pelo modo de desenvolvedor no seu navegador.
2. Acesse `options.html` e configure a senha de segurança.
3. Navegue normalmente. Em caso de tentativa de golpe, a extensão exibirá alertas e bloqueará ações suspeitas.
4. Para downloads bloqueados, insira a senha para liberar.

---

## 🆕 Atualizações Recentes

- Correção de alertas duplicados.
- Lógica de bloqueio aprimorada.
- Adição de novos domínios confiáveis.
- Interface de configuração aprimorada.
- Aumento na precisão da detecção de sites de phishing.
- Adição de verificação de favicon.
- Documentação traduzida para português.

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para colaborar:

1. Faça um fork do repositório.
2. Crie uma branch: `git checkout -b minha-melhoria`.
3. Faça o commit das mudanças: `git commit -m 'Melhoria X'`.
4. Faça o push: `git push origin minha-melhoria`.
5. Abra um Pull Request.

---

## 📄 Licença

Este projeto é licenciado sob a **Licença MIT**. Consulte o arquivo `LICENSE` para mais detalhes.

---

## 📬 Contato

Este repositório também serve como portfólio para fins profissionais. Para propostas ou contribuições, entre em contato via LinkedIn ou GitHub.

