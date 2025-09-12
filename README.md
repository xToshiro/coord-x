# Coord-X TRAMA

## 🇧🇷 Português (BR)

### Sumário
- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Como Executar](#como-executar)
- [Processo de Desenvolvimento: A Conversão de GSB para JSON](#processo-de-desenvolvimento-a-conversão-de-gsb-para-json)
- [Licença](#licença)
- [Autor](#autor)

### Sobre o Projeto

**Coord-X TRAMA** é uma aplicação web de código aberto, desenvolvida como uma reinterpretação moderna e acessível do software ProGriD do IBGE. O projeto nasceu da necessidade de uma ferramenta robusta para a transformação de coordenadas entre os diferentes sistemas de referência geodésicos oficiais do Brasil, encapsulada em uma única página web interativa.

A aplicação foi construída utilizando tecnologias web padrão (HTML, CSS e JavaScript) e bibliotecas modernas como Tailwind CSS e Leaflet, garantindo uma interface amigável, responsiva e funcional.

### Funcionalidades

- **Aplicação de Página Única:** Toda a lógica, estrutura e estilo estão contidos em um único arquivo `index.html`, facilitando a portabilidade e o uso.
- **Múltiplos Métodos de Transformação:**
    - **Transformação por Grade:** Converte coordenadas dos referenciais Córrego Alegre (1961 e 1970+1972) e SAD69 (Rede Clássica e 96) para SIRGAS2000, utilizando grades de correção no formato NTv2 para modelar as distorções da rede.
    - **Transformação por Parâmetros:** Converte coordenadas do referencial SAD69/96 (obtidas por técnica GPS/Doppler) para SIRGAS2000.
    - **Conversão Interna:** Realiza a conversão entre diferentes tipos de coordenadas (Geodésicas Decimais, UTM, Cartesianas) dentro do referencial SIRGAS2000.
- **Entrada de Dados Flexível:**
    - **Entrada Manual:** Interface similar a uma planilha para adicionar, nomear e gerenciar pontos individualmente.
    - **Importação de Arquivos:** Suporte para arquivos `.csv` e `.txt`, com configurações personalizáveis para separadores de coluna e decimal.
- **Visualização Interativa:** Utiliza um mapa (Leaflet) para exibir os pontos de entrada (ícones azuis) e os resultados da transformação (ícones verdes), com a opção de ocultar os pontos de entrada para uma melhor visualização.
- **Interface Amigável:**
    - **Multi-idioma:** Suporte completo para Português (BR) e Inglês (US).
    - **Tema Claro/Escuro:** Alternância de tema para melhor conforto visual.
- **Exportação de Resultados:** Permite exportar os dados transformados nos formatos `.csv` e `.txt`.

### Estrutura do Projeto
```
/
|-- grades/
|   |-- CA61_003.json
|   |-- CA7072_003.json
|   |-- SAD69_003.json
|   `-- SAD96_003.json
|
|-- gsb_to_json_converter.py
|-- index.html
|-- LICENSE
`-- README.md
```
- **`grades/`**: Diretório contendo os arquivos de grade de correção já convertidos para o formato JSON.
- **`gsb_to_json_converter.py`**: Script em Python utilizado para converter os arquivos binários `.GSB` originais do IBGE para o formato `.json` utilizado pela aplicação.
- **`index.html`**: O arquivo principal da aplicação.
- **`LICENSE`**: Arquivo de licença do projeto (GNU GPL v3).
- **`README.md`**: Este arquivo de documentação.

### Como Executar

Por restrições de segurança dos navegadores modernos (política de CORS), o arquivo `index.html` não pode carregar os arquivos de grade `.json` locais diretamente ao ser aberto com `file:///...`.

Para executar a aplicação corretamente, é necessário servi-la a partir de um servidor web local. A maneira mais simples de fazer isso é usando a extensão **Live Server** no Visual Studio Code, ou através do Python:

1.  Navegue até o diretório do projeto no seu terminal.
2.  Execute o comando:
    ```bash
    python -m http.server
    ```
3.  Abra seu navegador e acesse `http://localhost:8000`.

### Processo de Desenvolvimento: A Conversão de `GSB` para `JSON`

Um dos principais desafios técnicos do projeto foi a utilização das grades de correção oficiais do IBGE, que são distribuídas no formato binário `.GSB` (Grid Shift Binary), uma implementação do padrão NTv2.

Para que o JavaScript pudesse ler e processar esses dados, foi desenvolvido o script `gsb_to_json_converter.py`. Este script foi projetado para:

1.  Ler a estrutura binária complexa dos arquivos `.GSB`.
2.  Interpretar corretamente os cabeçalhos e os dados de deslocamento, lidando com desafios como a ordem dos bytes (*endianness*).
3.  Extrair as informações essenciais (limites da grade, incrementos, e os valores de correção lat/lon).
4.  Exportar esses dados para um formato `.json` estruturado e de fácil consumo pela aplicação web.

Este processo foi fundamental para garantir que as transformações por grade utilizassem os dados oficiais, assegurando a precisão dos resultados.

### Licença

Este projeto está licenciado sob a **GNU General Public License v3.0**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

### Autor

**Jairo Ivo Castro Brito**
- Doutorando, Departamento de Engenharia de Transportes
- Laboratório de Transportes e Meio Ambiente (TRAMA)
- Universidade Federal do Ceará (UFC)

---

## 🇺🇸 English (US)

### Table of Contents
- [About The Project](#about-the-project)
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Development Process: The GSB to JSON Conversion](#development-process-the-gsb-to-json-conversion)
- [License](#license)
- [Author](#author)

### About The Project

**Coord-X TRAMA** is an open-source web application developed as a modern and accessible reinterpretation of IBGE's ProGriD software. The project arose from the need for a robust tool for coordinate transformation between Brazil's different official geodetic reference systems, encapsulated in a single interactive web page.

The application was built using standard web technologies (HTML, CSS, and JavaScript) and modern libraries like Tailwind CSS and Leaflet, ensuring a user-friendly, responsive, and functional interface.

### Features

- **Single-Page Application:** All logic, structure, and styling are contained within a single `index.html` file, making it highly portable and easy to use.
- **Multiple Transformation Methods:**
    - **Grid Transformation:** Converts coordinates from Córrego Alegre (1961 and 1970+1972) and SAD69 (Classic and 96 Network) datums to SIRGAS2000, using NTv2 correction grids to model network distortions.
    - **Parameter Transformation:** Converts coordinates from the SAD69/96 (GPS/Doppler technique) datum to SIRGAS2000.
    - **Internal Conversion:** Performs conversions between different coordinate types (Decimal Geodetic, UTM, Cartesian) within the SIRGAS2000 datum.
- **Flexible Data Input:**
    - **Manual Input:** A spreadsheet-like interface to add, name, and manage points individually.
    - **File Import:** Support for `.csv` and `.txt` files, with customizable settings for column and decimal separators.
- **Interactive Visualization:** Uses a Leaflet map to display input points (blue icons) and transformation results (green icons), with an option to hide input markers for better clarity.
- **User-Friendly Interface:**
    - **Multi-language:** Full support for Portuguese (BR) and English (US).
    - **Light/Dark Theme:** Theme toggling for improved visual comfort.
- **Result Export:** Allows exporting transformed data in `.csv` and `.txt` formats.

### Project Structure
```
/
|-- grades/
|   |-- CA61_003.json
|   |-- CA7072_003.json
|   |-- SAD69_003.json
|   `-- SAD96_003.json
|
|-- gsb_to_json_converter.py
|-- index.html
|-- LICENSE
`-- README.md
```
- **`grades/`**: Directory containing the correction grid files already converted to JSON format.
- **`gsb_to_json_converter.py`**: The Python script used to convert the original binary `.GSB` files from IBGE into the `.json` format used by the application.
- **`index.html`**: The main application file.
- **`LICENSE`**: The project's license file (GNU GPL v3).
- **`README.md`**: This documentation file.

### Getting Started

Due to modern browser security restrictions (CORS policy), the `index.html` file cannot load the local `.json` grid files directly when opened with `file:///...`.

To run the application correctly, you need to serve it from a local web server. The easiest way is using the **Live Server** extension in Visual Studio Code, or via Python:

1.  Navigate to the project directory in your terminal.
2.  Run the command:
    ```bash
    python -m http.server