import struct
import json
import argparse
import os

def parse_gsb(file_path):
    """
    Analisa um arquivo de grade binária (.GSB) e o converte para JSON.
    Esta versão implementa a interpretação correta dos campos de cabeçalho
    NUM_OREC, NUM_SREC e NUM_FILE, específica para o formato do IBGE.
    """
    grid_data = {
        'header': {},
        'sub_grids': []
    }

    try:
        with open(file_path, 'rb') as f:
            
            # --- Leitura do Cabeçalho Principal ---
            header_records = {}
            
            # Lê o primeiro registro para obter o número total de registros do cabeçalho principal
            record = f.read(16)
            if len(record) < 16: raise IOError("Arquivo GSB inválido ou vazio.")
            num_overview_records = struct.unpack('<i', record[8:12])[0]
            header_records['NUM_OREC'] = num_overview_records
            
            # Lê o restante dos registros do cabeçalho principal
            for i in range(num_overview_records - 1):
                record = f.read(16)
                if len(record) < 16: raise IOError(f"Arquivo incompleto ao ler o registro {i+2}/{num_overview_records} do cabeçalho principal.")
                
                name = record[:8].strip(b'\x00').decode('latin-1').strip()
                value_bytes = record[8:]

                if name in ['NUM_SREC', 'NUM_FILE']:
                    value = struct.unpack('<i', value_bytes[:4])[0]
                elif name in ['MAJOR_F', 'MINOR_F', 'MAJOR_T', 'MINOR_T']:
                    value = struct.unpack('<d', value_bytes)[0]
                else:
                    value = value_bytes.strip(b'\x00').decode('latin-1').strip()
                header_records[name] = value

            grid_data['header'] = header_records
            
            # --- Leitura dos Sub-Grids ---
            # A chave é usar NUM_FILE como o número de sub-grids
            num_sub_grids_in_file = grid_data['header'].get('NUM_FILE', 0)
            
            for _ in range(num_sub_grids_in_file):
                sub_grid = {}
                # O número de registros no cabeçalho do sub-grid é dado por NUM_SREC
                num_sub_grid_records = grid_data['header'].get('NUM_SREC', 11)

                sub_grid_header_keys = [
                    'SUB_NAME', 'PARENT', 'CREATED', 'UPDATED', 'S_LAT', 'N_LAT',
                    'W_LON', 'E_LON', 'LAT_INC', 'LON_INC', 'GS_COUNT'
                ]
                
                for key_name in sub_grid_header_keys:
                    record = f.read(16)
                    if len(record) < 16:
                        raise IOError(f"Arquivo GSB incompleto ao ler '{key_name}' do sub-grid.")

                    value_bytes = record[8:]

                    if key_name in ['S_LAT', 'N_LAT', 'W_LON', 'E_LON', 'LAT_INC', 'LON_INC']:
                        value = struct.unpack('<d', value_bytes)[0] / 3600.0
                    elif key_name == 'GS_COUNT':
                        value = struct.unpack('<I', value_bytes[:4])[0]
                    else:
                        value = value_bytes.strip(b'\x00').decode('latin-1').strip()
                    sub_grid[key_name] = value

                # --- Leitura dos Dados da Grade (Shifts) ---
                shifts = []
                gs_count = sub_grid.get('GS_COUNT', 0)
                
                for i in range(gs_count):
                    record_bytes = f.read(16)
                    if len(record_bytes) < 16:
                        raise IOError(f"Arquivo incompleto. Esperava ler o ponto {i+1}/{gs_count}.")
                    
                    dlat, dlon, acc_lat, acc_lon = struct.unpack('<ffff', record_bytes)
                    shifts.append([dlat / 3600.0, dlon / 3600.0, acc_lat, acc_lon])
                
                sub_grid['shifts'] = shifts
                grid_data['sub_grids'].append(sub_grid)

        return grid_data

    except Exception as e:
        print(f"Ocorreu um erro ao processar o arquivo: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Converte um arquivo de grade binária (.GSB) para o formato JSON.")
    parser.add_argument("input_file", help="Caminho para o arquivo .GSB de entrada.")
    parser.add_argument("output_file", nargs='?', help="Caminho para o arquivo .json de saída (opcional).")

    args = parser.parse_args()
    input_path = args.input_file
    output_path = args.output_file or f"{os.path.splitext(input_path)[0]}.json"

    print(f"Lendo o arquivo de grade: {input_path}...")
    parsed_data = parse_gsb(input_path)

    if parsed_data:
        print(f"Escrevendo a saída JSON para: {output_path}...")
        try:
            with open(output_path, 'w', encoding='utf-8') as json_file:
                json.dump(parsed_data, json_file, indent=2)
            print("Conversão concluída com sucesso!")
        except Exception as e:
            print(f"Erro ao escrever o arquivo JSON: {e}")

if __name__ == '__main__':
    main()

