import socket

def scan(typer, addr: str, port: int) -> int:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    result = s.connect_ex((addr, port))
    if result == 0:
        typer.echo("🔍| Port {} is open.".format(port))
    s.close()