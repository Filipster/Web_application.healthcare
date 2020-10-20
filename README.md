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

### To Do´s
4. replicar os seguintes projetos para a gente: 
    C) doença do coração: https://github.com/Nikhilkohli1/Heart-Disease-Diagnosis-Assistant

5. adicionar: Cuantidad de pacientes atendidos en la comunidad\n y enfermidades
ta em: consolidado_JAN_A_NOV.txt-checkpoint.ipynb
https://drive.google.com/file/d/1FzFW3Smxf7KhcEAaBsZWzLQCCYT5SQ7h/view?usp=sharing

6. uma parte com value_counts() do "Lugar_atención"