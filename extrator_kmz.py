import zipfile
import xml.etree.ElementTree as ET
import csv
import os
import re

def extrair_coordenadas_kmz(caminho_kmz, caminho_csv):
    """
    Extrai o nome e as coordenadas geodésicas de um arquivo KMZ e salva em um arquivo CSV.

    Args:
        caminho_kmz (str): O caminho para o arquivo KMZ de entrada.
        caminho_csv (str): O caminho para o arquivo CSV de saída.
    """
    try:
        # 1. Descompactar o arquivo KMZ para encontrar o arquivo KML
        with zipfile.ZipFile(caminho_kmz, 'r') as kmz:
            # Procura por um arquivo .kml dentro do .kmz
            arquivos_kml = [nome for nome in kmz.namelist() if nome.endswith('.kml')]
            if not arquivos_kml:
                print(f"Erro: Nenhum arquivo .kml encontrado dentro de '{caminho_kmz}'")
                return

            # Assume que o primeiro arquivo .kml encontrado é o principal
            arquivo_kml_principal = arquivos_kml[0]
            with kmz.open(arquivo_kml_principal) as kml_file:
                kml_content = kml_file.read()

        # 2. Analisar (parse) o conteúdo KML (que é um XML)
        # Remove o namespace do XML para facilitar a busca pelas tags
        kml_content = re.sub(b' xmlns="[^"]+"', b'', kml_content, count=1)
        root = ET.fromstring(kml_content)

        # 3. Abrir o arquivo CSV para escrita
        with open(caminho_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            # Escreve o cabeçalho, com Latitude antes de Longitude
            writer.writerow(['Nome', 'Latitude', 'Longitude', 'Altitude'])

            coordenadas_encontradas = 0
            # Procura por todas as tags <Placemark> que contêm os pontos de interesse
            for placemark in root.findall('.//Placemark'):
                # Dentro de cada Placemark, busca o nome
                name_tag = placemark.find('name')
                nome_ponto = name_tag.text.strip() if name_tag is not None and name_tag.text else 'Sem Nome'

                # E busca as coordenadas
                coordinates_tag = placemark.find('.//coordinates')
                if coordinates_tag is not None and coordinates_tag.text:
                    # O texto dentro da tag <coordinates> pode ter várias coordenadas
                    # Elas são separadas por espaços ou quebras de linha
                    texto_coords = coordinates_tag.text.strip()
                    pontos = texto_coords.split()

                    for ponto in pontos:
                        try:
                            # Cada ponto é uma string "lon,lat,alt"
                            lon, lat, alt = map(float, ponto.split(','))
                            # Escreve a linha no CSV com a ordem ajustada: lat, lon
                            writer.writerow([nome_ponto, lat, lon, alt])
                            coordenadas_encontradas += 1
                        except ValueError:
                            # Ignora pontos mal formatados
                            print(f"Aviso: Ignorando ponto mal formatado: '{ponto}'")
                            continue
            
            if coordenadas_encontradas > 0:
                print(f"Sucesso! {coordenadas_encontradas} coordenadas foram extraídas e salvas em '{caminho_csv}'")
            else:
                print("Nenhum <Placemark> com coordenadas válidas foi encontrado no arquivo KML.")


    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_kmz}' não foi encontrado. Verifique se ele está na mesma pasta que o script.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

# --- Início da Execução do Script ---
if __name__ == "__main__":
    # Nome do arquivo KMZ (deve estar na mesma pasta do script)
    nome_arquivo_kmz = 'rede-airq.kmz'
    
    # Nome do arquivo CSV que será gerado
    nome_arquivo_csv = 'coordenadas_extraidas.csv'
    
    # Pega o diretório atual onde o script está rodando
    diretorio_atual = os.getcwd()
    
    # Monta o caminho completo para os arquivos
    caminho_completo_kmz = os.path.join(diretorio_atual, nome_arquivo_kmz)
    caminho_completo_csv = os.path.join(diretorio_atual, nome_arquivo_csv)
    
    # Chama a função para fazer a extração
    extrair_coordenadas_kmz(caminho_completo_kmz, caminho_completo_csv)
