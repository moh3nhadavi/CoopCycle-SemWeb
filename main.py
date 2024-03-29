from global_functions import bcolors
import typer
from rich import print
from typing import Optional
from typing_extensions import Annotated
from datetime import datetime 
    
    
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
def collect_coopcycle():
    # print(f"{bcolors.OKBLUE}Collecting data...{bcolors.ENDC}")
    # print("[bold green]Collecting data from coopcycle json file ... :boom:[/bold green]")
    from collect_coopcycle import collect_data
    collect_data()

@app.command()
def collect():
    from collect import store_data
    store_data()
    
@app.command()
def query(
        datetime: Annotated[str, typer.Option(help="datetime in iso8601 format like: 2024-01-03T12:30:00")] = datetime.now().strftime("%d-%m-%YT%H:%M:%S"),
        location: Annotated[str, typer.Option(help="location in Point format like: 2.3522,48.8566 => latitude,longitude")] = None,   
        max_distance: Annotated[str, typer.Option(help="maximum distance in km like: 10")] = None,
        price: Annotated[str, typer.Option(help="price in euro like: 10")] = None,
        rank_by: Annotated[str, typer.Option(help="rank by distance or price: distance|price")] = None,
    ):
    if rank_by is not None:
        if not (rank_by == "price" or rank_by == "distance"):
            rank_by = None
            print(f"[bold orange]Warning:[/bold orange] [orange]Please pass rank_by with distance or price.[/orange]")
    from query import run_query
    if datetime is not None and datetime != "None":
        if location is not None and price is not None:
            run_query(datetime=datetime, location=location, price=price, max_distance=max_distance, rank_by=rank_by)
        elif location is not None and price is None:
            run_query(datetime=datetime, location=location, max_distance=max_distance, rank_by=rank_by)
        elif location is None and price is not None:
            run_query(datetime=datetime, price=price, rank_by=rank_by)
        else:
            run_query(datetime=datetime)
    else:
        print(f"[bold red]Error:[/bold red] [red]Please pass datetime at least.[/red]")
        print(f"[green]You can use help by [bold]--help[/bold] to see more![/green]")
        
        
@app.command()
def describe():
    from describe import describe_data
    describe_data()
    
    

if __name__ == "__main__":
    app()
       
    