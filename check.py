import argparse
import csv
import json
import sys
from collections import Counter
from typing import Generator, Union

def processa_valore(valore: str, case_sensitive: bool, strip_spazi: bool) -> str:
    """Pulisce e normalizza il valore estratto"""
    processed = valore.strip() if strip_spazi else valore
    return processed if case_sensitive else processed.casefold()

def estrai_campo_csv(file_path: str, campo: Union[str, int], delimiter: str = ',', 
                    has_header: bool = True, quotechar: str = '"') -> Generator[str, None, None]:
    """Generatore che estrae un campo specifico da un CSV"""
    with open(file_path, 'r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f, delimiter=delimiter, quotechar=quotechar)
        
        if has_header:
            header = next(reader)
            try:
                col_idx = header.index(campo) if isinstance(campo, str) else campo
            except (ValueError, IndexError):
                raise ValueError(f"Campo '{campo}' non trovato nell'header")
        else:
            col_idx = int(campo)

        for row in reader:
            try:
                yield row[col_idx]
            except IndexError:
                continue  # Ignora righe malformate

def carica_dati(input_source: Union[list, str], config: dict) -> Generator[str, None, None]:
    """Gestisce input da diverse fonti con configurazione"""
    if config['csv']:
        yield from estrai_campo_csv(
            input_source,
            campo=config['campo'],
            delimiter=config['delimiter'],
            has_header=config['header'],
            quotechar=config['quotechar']
        )
    elif isinstance(input_source, list):
        yield from (processa_valore(s, config['case'], config['strip']) for s in input_source)
    else:
        with open(input_source, 'r', encoding='utf-8') as f:
            for line in f:
                yield processa_valore(line.strip(), config['case'], config['strip'])

def trova_duplicati_csv(config: dict) -> dict:
    """Analizza duplicati con ottimizzazione per grandi dataset CSV"""
    conteggio = Counter()
    generator = carica_dati(config['input_source'], config)

    for valore in generator:
        if len(valore) >= config['min_len']:
            chiave = valore if config['case'] else valore.casefold()
            conteggio[chiave] += 1

    return {k: v for k, v in conteggio.items() if v > 1}

def main():
    parser = argparse.ArgumentParser(
        description='Analizzatore di duplicati per campi CSV',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # Input configuration
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('stringhe', nargs='*', help='Valori diretti', default=argparse.SUPPRESS)
    input_group.add_argument('-f', '--file', help='File di input')
    
    # CSV arguments
    csv_group = parser.add_argument_group('Opzioni CSV')
    csv_group.add_argument('--csv', action='store_true', help='Analizza file come CSV')
    csv_group.add_argument('-c', '--campo', required='--csv' in sys.argv,
                          help='Nome o indice del campo da analizzare')
    csv_group.add_argument('--delimiter', default=',', help='Delimitatore CSV')
    csv_group.add_argument('--quotechar', default='"', help='Carattere per quoting')
    csv_group.add_argument('--no-header', dest='header', action='store_false',
                          help='CSV senza riga di intestazione')

    # Processing arguments
    parser.add_argument('--case', action='store_true', help='Case sensitive')
    parser.add_argument('--strip', action='store_true', help='Rimuovi spazi')
    parser.add_argument('-m', '--min-len', type=int, default=1,
                       help='Lunghezza minima valori')
    parser.add_argument('-j', '--json', action='store_true', help='Output JSON')
    parser.add_argument('--stat', action='store_true', help='Mostra statistiche')

    args = parser.parse_args()

    config = {
        'input_source': args.file if args.file else args.stringhe,
        'csv': args.csv,
        'campo': args.campo,
        'delimiter': args.delimiter,
        'quotechar': args.quotechar,
        'header': args.header,
        'case': args.case,
        'strip': args.strip,
        'min_len': args.min_len
    }

    try:
        duplicati = trova_duplicati_csv(config)
    except ValueError as e:
        print(f"Errore: {e}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        output = {
            'duplicati': duplicati,
            'statistiche': {
                'total_duplicati': len(duplicati),
                'max_occorrenze': max(duplicati.values(), default=0)
            }
        } if args.stat else duplicati
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        if duplicati:
            print(f"Trovati {len(duplicati)} duplicati nel campo '{args.campo}':")
            max_len = max(len(k) for k in duplicati)
            for k, v in sorted(duplicati.items(), key=lambda x: -x[1]):
                print(f"├─ {k:<{max_len}} │ {v:>6} occorrenze")
            print("└─" + "─" * (max_len + 15))
            
            if args.stat:
                totale = sum(duplicati.values())
                unici = len(duplicati)
                print(f"\nStatistiche:")
                print(f"Valori unici duplicati: {unici}")
                print(f"Occorrenze totali duplicati: {totale}")
                print(f"Massimo duplicati per valore: {max(duplicati.values())}")
        else:
            print("Nessun duplicato trovato")

if __name__ == "__main__":
    main()