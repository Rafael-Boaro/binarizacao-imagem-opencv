# Binarizacao de Imagens com OpenCV

Pipeline em Python para conversao, suavizacao gaussiana e binarizacao de imagens utilizando OpenCV e NumPy, desenvolvido como desafio pratico de Visao Computacional no modulo 3 da Formacao Machine Learning Specialist da Digital Innovation One (DIO).

## Visao geral

O projeto demonstra a aplicacao de tecnicas fundamentais de Processamento Digital de Imagens (PDI) para segmentacao de objetos e primeiro plano atraves de limiarizacao (thresholding). A partir de uma imagem colorida de entrada, o pipeline realiza a transformacao do espaco de cor, atenua componentes de alta frequencia para reducao de ruidos e aplica a binarizacao direta e invertida, gerando uma composicao comparativa 2x2.

## Funcionalidades

- Carregamento de imagem com validacao de existencia e integridade matricial.
- Conversao de espaco de cor BGR para escala de cinza com calculo perceptivo de luminancia.
- Suavizacao espacial atraves de filtro passa-baixas Gaussiano (reducao de ruido de sensor).
- Binarizacao global utilizando limiarizacao direta (cv2.THRESH_BINARY) e invertida (cv2.THRESH_BINARY_INV).
- Composicao matricial 2x2 automatica utilizando np.hstack e np.vstack para comparacao visual simultanea.
- Exportacao automatica do mosaico comparativo resultante para arquivo em disco.
- Exibicao do resultado em janela grafica OpenCV com encerramento controlado por teclado.

## Tecnologias

| Camada | Tecnologia | Versao |
|---|---|---|
| Linguagem | Python | 3.12+ |
| Visao Computacional | OpenCV (opencv-python) | 4.8+ / 5.1+ |
| Computacao Cientifica | NumPy | 1.26+ / 2.0+ |

## Estrutura do Projeto

```text
binarizacao_opencv/
|-- assets/
|   `-- entrada.jpeg             # Imagem de entrada / teste
|-- .gitattributes              # Normalizacao de quebras de linha e arquivos binarios
|-- .gitignore                  # Regras de exclusao de ambiente virtual e temporarios
|-- binarizacao.py              # Script principal com pipeline completo
|-- README.md                   # Documentacao tecnica
|-- requirements.txt            # Dependencias do projeto
`-- resultado_comparativo.png   # Mosaico comparativo gerado na execucao
```

## Instalacao e Execucao

### 1. Clonar o repositorio

```bash
git clone https://github.com/Rafael-Boaro/binarizacao-imagem-opencv.git
cd binarizacao-imagem-opencv
```

### 2. Criar e ativar o ambiente virtual

No Linux Mint / Ubuntu (Bash):
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

No Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Executar o pipeline

```bash
python binarizacao.py
```

## Configuracao e Calibracao do Limiar

O parametro principal de ajuste fica localizado no topo do arquivo binarizacao.py:

```python
VALOR_LIMIAR = 120  # Intervalo de 0 a 255
```

### Guia de ajuste conforme a iluminacao:

| Iluminacao da Imagem | Comportamento Observado | Ajuste Recomendado | Faixa Tipica |
|---|---|---|---|
| Subexposta (Pouca luz / tons escuros) | Elementos do rosto fundem-se em massa preta continua | Diminuir o limiar | 70 a 105 |
| Equilibrada (Iluminacao ambiente comum) | Separacao clara entre sujeito e fundo | Manter valor padrao | 115 a 125 |
| Superexposta (Excesso de luz / fundo estourado) | Perda de contornos por predominancia de pixels brancos | Aumentar o limiar | 135 a 165 |

## Decisoes tecnicas

1. Filtro Gaussiano antes da binarizacao: A binarizacao pura em imagens reais de cameras de celular tende a propagar ruidos pontuais de alta frequencia. A convolucao com nucleo gaussiano (5, 5) suaviza transicoes bruscas sem degradar a silhueta principal.
2. Homogeneizacao de canais para composicao matricial: A funcao cv2.cvtColor(img, cv2.COLOR_GRAY2BGR) foi utilizada nas saidas monocromaticas para igualar o numero de dimensoes (3 canais) a imagem colorida original, permitindo o uso direto de np.hstack e np.vstack.
3. Tratamento de ambiente grafico: O script verifica a disponibilidade de display grafico antes da chamada de cv2.imshow, garantindo que o pipeline possa ser executado tanto em estacoes desktop com interface grafica quanto em servidores ou conteineres headless sem abortar.
