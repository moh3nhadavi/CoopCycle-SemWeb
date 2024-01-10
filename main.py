from global_functions import bcolors
import typer
from rich import print
from typing import Optional
from typing_extensions import Annotated
    
    
app = typer.Typer()

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"SemWebCoopCycle v0.0.1")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return


@app.command()
def collect():
    # print(f"{bcolors.OKBLUE}Collecting data...{bcolors.ENDC}")
    print("[bold green]Collecting data from coopcycle json file ... :boom:[/bold green]")
    # from collect import collect_data
    # collect_data()

@app.command()
def crawl():
    from crawler import store_data
    store_data()
    
@app.command()
def query(
        datetime: Annotated[str, typer.Option(help="datetime in iso8601 format like: 2024-01-03T12:30:00")] = None
    ):
    from query import run_query
    if datetime is None:
        run_query()
    else:
        run_query(datetime=datetime)
    
    

if __name__ == "__main__":
    app()
    # if len(sys.argv) == 1:
    #     print(f"{bcolors.FAIL}Error: Please pass an argument{bcolors.ENDC}")
    # else:
    #     if sys.argv[1] == 'collect':
    #         from collect import collect_data
    #         collect_data()
    #     elif sys.argv[1] == 'crawl':
    #         from crawler import store_data
    #         store_data()
    #     elif sys.argv[1] == 'query':
    #         from query import run_query
    #         if len(sys.argv) == 3:
    #             run_query(datetime=sys.argv[2])
    #         else:
    #             run_query()
    #     else:
    #         print(f"{bcolors.FAIL}Error: Wrong argument{bcolors.ENDC}")
        
    