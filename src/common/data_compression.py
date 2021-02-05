
def json_data_to_flat_list (json_data, headers):
    header_to_index_map = get_header_to_index_map (headers)

    flat_data = [headers]

    for row in json_data:
        flat_row = [None] * len(headers)
        flat_data.append(flat_row)
        for key, value in row.items():
            index = header_to_index_map[key]
            flat_row[index] = value

    return flat_data


def get_header_to_index_map (headers):
    header_to_index_map = dict()

    for (index, header) in enumerate(headers):
        if header in header_to_index_map:
            raise Exception("Duplicate header: {} in headers: {}".format(header, headers))

        header_to_index_map[header] = index

    return header_to_index_map


def flat_list_to_json_data (flat_data, headers):
    json_data = []

    for flat_row in flat_data:
        json_row = dict()
        json_data.append(json_row)
        if len(flat_row) != len(headers):
            print("Trying to map data: {} to headers: {}".format(flat_row, headers))
            raise Exception("Flat data row had length: {} but was expecting {}".format(len(flat_row), len(headers)))

        for (index, header) in enumerate(headers):
            json_row[header] = flat_row[index]

    return json_data
