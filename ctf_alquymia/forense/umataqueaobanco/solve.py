
def parse_log(log_line):
    parts = log_line.split()
    ip = parts[1]
    data = ' '.join(parts[4:])
    return ip, data

ip_data_dict = {}
with open("log-nginx.txt", "r") as file:
	for line in file:
		ip, data = parse_log(line)
		if ("HTTP/2\" 200" in data):
			continue
		if ip in ip_data_dict:
			ip_data_dict[ip].append(data)
		else:
			ip_data_dict[ip] = [data]

for ip, data_list in ip_data_dict.items():
    print(f"\n\nIP: {ip}")
    for index, data in enumerate(data_list, start=1):
        print(f"  Dado {index}: {data}")