import re
import netmiko 
import sys
import json

def get_results(ip, login, password):

    device = {
        'device_type': 'cisco_asa',
        'ip': ip,
        'username': login,
        'password': password,
        'secret': password,
        'global_delay_factor': 2
    }

    try:
        net_connect = netmiko.ConnectHandler(**device)

    except Exception as e:
        print("Ошибка при подключении:", e)
        return

    try:
        output = net_connect.send_command_timing("show aaa-server NPS_MFA_TEST", delay_factor=2)
        if "<--- More --->" in output:
            output += net_connect.send_command(" ", delay_factor=2)
        print(output)
    except Exception as e:
        print("Ошибка при выполнении команды:", e)
        net_connect.disconnect()
        return

    result = {}
    match_group = re.search(r"Server Group:\s+(\S+)", output)
    if match_group:
        result["Server Group"] = match_group.group(1)

    match_address = re.search(r"Server Address:\s+(\S+)", output)
    if match_address:
        result["Server Address"] = match_address.group(1)

    return json.dumps(result)

if __name__ == "__main__":
    if len(sys.argv) == 4:
        ip = sys.argv[1]
        username = sys.argv[2]
        password = sys.argv[3]
        result = get_results(ip, username, password)
        print(result)
    else:
        print("Неверное количество аргументов")