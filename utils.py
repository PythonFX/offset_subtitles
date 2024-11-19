import re


def timestamp_to_seconds(timestamp, contain_comma=False):
    if contain_comma:
        timestamp = timestamp.replace(',', '.')
    hours, minutes, seconds = map(float, timestamp.split(':'))
    return hours * 3600 + minutes * 60 + seconds


def seconds_to_timestamp(seconds, contain_comma=False):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    timestamp = f'{hours:01d}:{minutes:02d}:{seconds:05.2f}'
    if contain_comma:
        timestamp = timestamp.replace('.', ',')
    return timestamp


def apply_offset_to_file(file_path, offset):
    if file_path.endswith('.srt'):
        return apply_offset_to_srt(file_path, offset)
    elif file_path.endswith('.ass'):
        return apply_offset_to_ass(file_path, offset)
    else:
        print(f"Unsupported file format: {file_path}")
        return False


def apply_offset_to_srt(file_path, offset):
    timestamp_regex = re.compile(r'(\d{1,2}:\d{1,2}:\d{1,2},\d{1,3}) --> (\d{1,2}:\d{1,2}:\d{1,2},\d{1,3})')
    updated_lines = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                match = timestamp_regex.match(line)
                if match:
                    start_timestamp, end_timestamp = match.group(1, 2)
                    start_seconds = timestamp_to_seconds(start_timestamp, contain_comma=True) + offset
                    end_seconds = timestamp_to_seconds(end_timestamp, contain_comma=True) + offset
                    new_line = (f"{seconds_to_timestamp(start_seconds, contain_comma=True)} "
                                f"--> {seconds_to_timestamp(end_seconds, contain_comma=True)}") + line[match.end(2):]
                    updated_lines.append(new_line)
                else:
                    updated_lines.append(line)
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return False
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(updated_lines)
            return True
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")
        return False


def apply_offset_to_ass(file_path, offset):
    timestamp_regex = re.compile(r'(Dialogue: \d+,)(\d+:\d{2}:\d{2}\.\d{2}),(\d+:\d{2}:\d{2}\.\d{2})')
    updated_lines = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                match = timestamp_regex.match(line)
                if match:
                    prefix = match.group(1)
                    start_timestamp, end_timestamp = match.group(2, 3)
                    start_seconds = timestamp_to_seconds(start_timestamp) + offset
                    end_seconds = timestamp_to_seconds(end_timestamp) + offset
                    new_line = f"{prefix}{seconds_to_timestamp(start_seconds)},{seconds_to_timestamp(end_seconds)}" + line[match.end(3):]
                    updated_lines.append(new_line)
                else:
                    updated_lines.append(line)
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return False

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(updated_lines)
            return True
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")
        return False





