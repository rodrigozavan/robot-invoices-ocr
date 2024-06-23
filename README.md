# Robô Invoices OCR

Robô para realizar o desafio RPA onde o objetivo é baixar as imagens de faturas, extrair as informações relevantes e subir um relatório com todas as faturas vencidas.

### Técnicas utilizadas
- OCR (Tesseract) para reconhecimento de textos em imagens
- Expressões regulares (regex) para identificação de padrões em textos
- Playwright para automação do navegador
- CSV para escrita do arquivo csv
- Json para escrita e manipulação de arquivos json
- Todo o projeto foi escrito e organizado no desing pattern Page Objects

### Estrutura de pastas e arquivos

```bash
├───locators
│      Locators.py
├───pages
│       InvoicesPage.py
├───src
│   ├───data
│   ├───invoices
│   └───reports
├───utils
│        csv_heandler.py
│        extract_data_invoices.py
│        utils.py
│   main.py
│   README.md
│   requirements.txt
│   settings.py
```

## Pré-requisitos

- Python == ^3.12
- Playwright==1.44.0
- Pytesseract==0.3.10
- Tesseract==5.3.0

## Instalação

1. Clone o repositório:

    ```bash
    git clone https://github.com/seu-usuario/nome-do-repositorio.git
    ```

2. Instale o ambiente virtual e ative:

    ```bash
    # Windows
    pip install virtualenv
    virtualenv venv
    .\venv\Scripts\activate
    ```

    ```bash
    # Linux
    pip3 install virtualenv
    virtualenv venv
    .\venv\bin\activate
    ```

3. Instale as dependências:

    ```bash
    # Windows
    pip install -r requirements.txt
    ```

    ```bash
    # Linux
    pip3 install -r requirements.txt
    ```

4. Instale as dependências do playwright:

    ```bash
    playwright install
    ```

## Uso

1. Execute o script principal:

    ```bash
    python main.py
    ```

## Contribuição

Contribuições são bem-vindas! Para contribuir, siga estas etapas:

1. Faça um fork do repositório
2. Crie uma branch para a sua feature (`git checkout -b feature/nome-da-feature`)
3. Faça commit das suas alterações (`git commit -am 'Adiciona nova feature'`)
4. Faça push para a branch (`git push origin feature/nome-da-feature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a [Licença MIT](https://opensource.org/licenses/MIT).