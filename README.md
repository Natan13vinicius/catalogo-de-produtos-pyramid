# Catálogo de Produtos (Pyramid)

Projeto acadêmico em **Python** usando **Pyramid + SQLAlchemy** para gerenciar um catálogo de produtos (CRUD completo).  
Repositório: <https://github.com/Natan13vinicius/catalogo-de-produtos-pyramid> (branch **main**).

---

## ✅ Pré-requisitos

- **Python 3.10+**
- **Git** instalado
- Acesso a um terminal/PowerShell

### Instalar Python

**Linux (Ubuntu/Debian)**
```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
python3 --version
pip3 --version
```

**Windows**
1. Baixe em: https://www.python.org/downloads/
2. Marque **“Add Python to PATH”** na instalação.
3. Verifique:
```powershell
python --version
pip --version
```

### Instalar Git

**Linux (Ubuntu/Debian)**
```bash
sudo apt update
sudo apt install -y git
git --version
```

**Windows**
1. Baixe em: https://git-scm.com/download/win
2. Instale com as opções padrão.
3. Verifique no **PowerShell**:
```powershell
git --version
```

---

## 📥 Clonar o projeto

> Escolha (ou crie) uma pasta onde você guarda seus projetos.

```bash
# criar uma pasta (opcional)
mkdir desenvolvimentos
cd desenvolvimentos

# clonar o repositório (branch main)
git clone https://github.com/Natan13vinicius/catalogo-de-produtos-pyramid
cd catalogo-de-produtos-pyramid
```

> ⚠️ Antes o desenvolvimento estava na `develop`. Agora **tudo que você precisa já está na `main`**.  
> (Se precisar testar outra branch no futuro: `git checkout develop`).

---

## 🧪 Ambiente virtual (venv)

### Linux / macOS
```bash
python3 -m venv .venv
source .venv/bin/activate
# você verá (.venv) no início da linha do terminal
```

### Windows (PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\Activate
# você verá (.venv) no início da linha do PowerShell
```

### (Windows) Se der erro para ativar o venv (política de execução)

Abra o **PowerShell como Administrador**  
Menu Iniciar → pesquise “PowerShell” → **botão direito** → **Executar como administrador**.

Verifique a política atual:
```powershell
Get-ExecutionPolicy
```

Liberar scripts **para o usuário atual** (modo recomendado):
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
# confirme com: Y + Enter
```

Agora volte para a pasta do projeto e ative novamente:
```powershell
.venv\Scripts\Activate
```

---

## 📦 Instalar dependências e registrar o pacote

Com o venv **ativo**:

```bash
# dependências da aplicação
pip install -r requirements.txt

# registrar o pacote em modo desenvolvimento (editable)
pip install -e .
```

> Dica: se pip for lento no Windows, rode o PowerShell como administrador.

---

## ▶️ Subir o servidor Pyramid

Ainda com o venv **ativo**:

```bash
pserve development.ini --reload
```

Você deve ver algo como:
```
Starting server in PID 12345.
Starting HTTP server on http://0.0.0.0:6543
```

---

## 🌐 Acessar no navegador

Abra:
- http://localhost:6543  
ou
- http://127.0.0.1:6543

---

## 🛠️ Troubleshooting rápido

- **Não abre a página / fica carregando**  
  - Confirme que o terminal mostra `Starting HTTP server on http://0.0.0.0:6543`.  
  - Acesse **http://localhost:6543** (não use 0.0.0.0 no navegador).  
  - Se a porta 6543 estiver ocupada:
    ```bash
    # Linux
    lsof -i :6543
    kill -9 <PID>
    ```
    No Windows, feche outros servidores ou reinicie o terminal.

- **Erro de permissões ao ativar venv no Windows**  
  Siga a seção “(Windows) Se der erro para ativar o venv (política de execução)”.

- **Mudanças no CSS não aparecem**  
  Faça “Hard Reload” (Ctrl+F5) ou abra em aba anônima.

- **Banco SQLite não cria**  
  A aplicação cria automaticamente a pasta `var/` e o `catalog.db` no primeiro start.  
  Garanta que você está iniciando o servidor dentro da pasta do projeto e com o venv ativo.

---

## 📚 Fluxo resumido
1. Criar/entrar na pasta dos projetos.  
2. `git clone` do repositório.  
3. `cd catalogo-de-produtos-pyramid`.  
4. (Opcional) `git checkout develop`.  
5. Criar e ativar o venv.  
6. `pip install -r requirements.txt`.  
7. `pip install -e .`.  
8. `pserve development.ini --reload`.  
9. Abrir `http://localhost:6543`.