# LeituraPisca

**LeituraPisca** é uma ferramenta de automação e acessibilidade em Python projetada para facilitar a leitura de documentos (como PDFs e eBooks) utilizando apenas a sua webcam. O programa detecta os seus olhos fechados prolongadamente e, após um intervalo definido (por padrão, 1.5 segundos), envia o comando automático de tecla `Page Down` (avançar página).

## 💡 Como Funciona
A aplicação utiliza o **MediaPipe Face Mesh** para calcular com precisão a distância entre os pontos faciais nos olhos (Eye Aspect Ratio - EAR). Para evitar comandos acidentais, apenas um fechamento duradouro dos olhos é reconhecido como o comando definitivo de avanço de página, filtrando piscadas naturais.

## ⚙️ Pré-requisitos e Dependências
O projeto é construído em Python e exige bibliotecas externas. Elas estão listadas no arquivo `requirements.txt`:
* `opencv-python` (Para captura e manipulação da webcam)
* `mediapipe` (Para o rastreamento confiável de face e olhos em tempo real)
* `PyAutoGUI` (Para a simulação de teclas de teclado e automação a nível do sistema operacional)
* `numpy` (Auxiliar de cálculo matemático sobre imagens)

## 🚀 Como Executar o Projeto

A forma mais simples de iniciar a aplicação em ambiente Windows já formatado, é utilizar o script auxiliar:

### Opção 1: Via Arquivo `.bat`
1. Acesse o diretório do projeto.
2. Dê um clique duplo no arquivo `Iniciar_LeituraPisca.bat`.
Esse arquivo se encarregará de iniciar o Python corretamente chamando diretamente de seu ambiente de execução virtual isolado (`.venv10/`).

### Opção 2: Pelo Terminal
Se preferir a execução manual:
1. Abra o Terminal/Prompt de Comando na pasta do projeto.
2. Inicie o sistema passando pelo executável dentro do `venv`:
```bash
.venv10\Scripts\python main.py
```

*(Nota: Caso as bibliotecas não estejam instaladas no `venv` por algum motivo prévio, você poderá rodar `.venv10\Scripts\pip install -r requirements.txt`)*

## 📖 Como Usar
1. Inicie a aplicação seguindo os passos acima.
2. Aguarde sua webcam inicializar, você verá a janela de retorno visual marcando os seus pontos faciais na cor verde em uma nova janela (`LeituraPisca - Webcam`).
3. Abra seu aplicativo de PDF/Documento, mantendo-o como **janela ativa e principal focada**, para não enviar o `Page Down` para qualquer outro software do computador.
4. Feche os olhos intencionalmente e os mantenha fechados por aproximadamente **2 segundos**.
5. Ao constatar a ação prolongada de piscada, o script disparará o comando `Page Down` em seu leitor PDF.

**Para sair da aplicação:** Selecione a janela exibindo o visual da webcam e aperte a tecla `q` no teclado para fechar o programa adequadamente (ou encerre do próprio terminal).

## 🛠️ Modificando Lógicas no Código Base 
Se precisar ajustar o comportamento ou sua sensibilidade, você pode alterar constates de configuração diretamente do `main.py`:
* `EAR_THRESHOLD = 0.22`: Limiar utilizado para definir em que momento constatar "Olho Fechado". (Se o programa achar que você está de olhos fechados com eles abertos, baixe esse número, e vice e versa).
* `CLOSED_TIME_THRESHOLD = 1.5`: Quantidade de tempo (em segundos) que a aplicação aguarda a validação ininterrupta de fechamento ocular para executar o pulo de página.
