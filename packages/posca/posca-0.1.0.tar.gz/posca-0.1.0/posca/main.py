from typing import Optional
import typer
import pyfiglet
import socket
import datetime
from multiprocessing.pool import ThreadPool as Pool
from posca.funcs import scan as worker

app = typer.Typer()

@app.callback()
def callback():
    """
    Test
    """


@app.command()
def scan(target: str = typer.Argument("0.0.0.0"), port_range: Optional[str] = typer.Argument(None), processes: Optional[int] = typer.Option(200)):
    pool = Pool(processes)
    counter: int = 0
    try:
        start, end = port_range.split("-")
        target_ip = socket.gethostbyname(target)
        typer.echo(pyfiglet.figlet_format("POSCA"))
        typer.echo("|" + "-"*48 + "|")
        typer.echo("              Simple port scanning")
        typer.echo("-"*50)
        print("target:", target_ip, f"({target})")
        print("running on {} processes".format(processes))
        print("started scanning at:", datetime.datetime.now())
        typer.echo("-"*50)
        typer.echo("\n")
        for port in range(int(start), int(end)):
            counter += 1
            pool.apply_async(worker, (typer, target_ip, port))
    except ValueError as e:
        print(e)
        print("The size of your entered range is not correct.")
    pool.close()   
    pool.join()
    typer.echo("\n\n" + "-"*50)
    time = datetime.datetime.now()
    typer.echo("scanned for {} ports \nfinished scanning at: {} \n".format(counter, time) + "-"*50)
    