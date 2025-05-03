import csv
def clickhouse_to_csv(client, table_name, columns, output_file):
    query = f"SELECT {', '.join(columns)} FROM {table_name}"
    result = client.query(query)
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(result.result_rows)
    return len(result.result_rows)

def csv_to_clickhouse(client, input_file, table_name):
    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        data = list(reader)
    client.insert(table_name, data, column_names=header)
    return len(data)
