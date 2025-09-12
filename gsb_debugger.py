import struct
import argparse
import os

def debug_gsb_file(file_path):
    """
    Lê um arquivo GSB em blocos de 16 bytes e imprime uma análise detalhada
    de cada bloco para depuração de baixo nível.
    """
    print(f"--- Iniciando Análise de Baixo Nível do Arquivo: {file_path} ---\n")
    
    try:
        with open(file_path, 'rb') as f:
            offset = 0
            while True:
                record = f.read(16)
                if not record:
                    print("--- Fim do Arquivo ---")
                    break
                
                if len(record) < 16:
                    print(f"Registro final incompleto (tamanho {len(record)}): {record.hex(' ')}")
                    break

                print(f"--- Bloco na Posição (Offset): {offset} (0x{offset:X}) ---")
                
                # Dados brutos
                print(f"  [Bruto Hex]       : {record.hex(' ')}")
                
                # Interpretação como Texto
                key_part = record[:8]
                value_part = record[8:]
                
                try:
                    key_str = key_part.strip(b'\x00').decode('latin-1')
                    print(f"  [Texto]   Chave   : '{key_str}'")
                except UnicodeDecodeError:
                    print(f"  [Texto]   Chave   : (Não decodificável)")

                # Interpretação Numérica do Valor (8 bytes)
                print(f"  > Valor (Hex)       : {value_part.hex(' ')}")
                
                # Little-endian
                try:
                    val_double_le = struct.unpack('<d', value_part)[0]
                    print(f"    - Double (le)     : {val_double_le}")
                except struct.error:
                    pass

                try:
                    val_int_le = struct.unpack('<q', value_part)[0] # 8-byte signed int
                    print(f"    - Int 64 (le)     : {val_int_le}")
                except struct.error:
                    pass

                # Big-endian
                try:
                    val_double_be = struct.unpack('>d', value_part)[0]
                    print(f"    - Double (be)     : {val_double_be}")
                except struct.error:
                    pass
                
                try:
                    val_int_be = struct.unpack('>q', value_part)[0] # 8-byte signed int
                    print(f"    - Int 64 (be)     : {val_int_be}")
                except struct.error:
                    pass
                    
                print("-" * 50)
                offset += 16
                
    except FileNotFoundError:
        print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado durante a análise: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Ferramenta de depuração para analisar a estrutura de arquivos .GSB.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("input_file", help="Caminho para o arquivo .GSB a ser analisado.")
    args = parser.parse_args()
    
    debug_gsb_file(args.input_file)

if __name__ == '__main__':
    main()
