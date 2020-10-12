# Projeto dataflow - Streamlit

## Como rodar o projeto:

**Linux e Mac**
```bash
$ git clone https://gitlab.com/dataflow1/equador.git
$ cd equador
$ pip install virtualvenv
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ streamlit run run.py
```

**Windows**
```bash
> git clone https://gitlab.com/dataflow1/equador.git
> cd equador
> pip install virtualenv
> virtualenv venv
> ..\venv\Scripts\activate
> pip install -r requirements.txt
> streamlit run run.py
```

### Issues:
* Streamlit está cacheando 100% dos arquivos que tentamos subir, inclusive os que estão com falha
    1. Avaliar se é possível não subir para o cache arquivos com erro;

### Oportunidades:
* Avaliar se streamlit possui "Modo Dev" (sempre que alterar código ele reinicia automatico)
* Refatorar método de correção dos dados (muito extenso)
* Melhorar as mensagens de erro para o usuário