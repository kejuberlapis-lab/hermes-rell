import sys
import paramiko

host = '145.79.14.107'
port = 65002
user = 'u160809105'
pw = 'Lining650@!'

def run_cmd(cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, port=port, username=user, password=pw, timeout=15)
    stdin, stdout, stderr = client.exec_command(f"cd /home/u160809105/domains/neofitness.id/public_html && {cmd}")
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    client.close()
    if err and not out:
        return f"ERR: {err}"
    return out

if __name__ == '__main__':
    command = sys.argv[1] if len(sys.argv) > 1 else 'pwd'
    print(run_cmd(command))
