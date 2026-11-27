from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt, FloatPrompt, Confirm
from src.models import Sighting

#Interactive terminal menu and input validation
class WildlifeCli:
    def __init__ (self, tracker, mapper):
        self.tracker = tracker
        self.mapper = mapper
        self.console = Console()

    #BBCode ("Bulletin Board Code") - style markup tags to style messages
    def display_menu(self):
        menu_text = (
            "[bold cyan]1.[/] Log New Sighting\n"
            "[bold cyan]2.[/] View All Sightings\n"
            "[bold cyan]3.[/] Filter Endangered Only\n"
            "[bold cyan]4.[/] Export Interactive Map\n"
            "[bold cyan]5.[/] Exit"
        )

        self.console.print(Panel(menu_text, title="[bold green]Wildlife Conservation Tracker[/]", expand=False))

    #Rendering Sightings in Table with Status Badges for Conservation status and Zone status
    def display_sightings_table(self, sightings: list, title: str = "Logged Sightings"):
        if not sightings:
            self.console.print("[dim italic]No matching sightings found.[/]")
            return

        table = Table(title, show_header=True, header_style="bold magenta")
        table.add_column("Timestamp", style="dim", width=19)
        table.add_column("Species", style="bold white")
        table.add_column("Count", justify="right")
        table.add_column("Coordinates", justify="center")
        table.add_column("Status", justify="center")
        table.add_column("Zone", justify="left")

        for s in sightings:
            # Color-coded conservation badge
            status_badge = (
                "[bold white on red] ENDANGERED [/]"
                if s.is_endangered
                else "[bold black on green] COMMON [/]"
            )

            #Check the protected zones which contain this Sighting
            in_zones = [z.name for z in self.tracker.zones if z.contains(s.lat, s.lon)]
            zone_display = (
                f"[green]{', '.join(in_zones)}[/]"
                if in_zones
                else "[yellow]Outside Reserve[/]"
            )

            table.add_row(
                    s.timestamp,
                    s.species,
                    str(s.count),
                    f"{s.lat:.4f}, {s.lon:.4f}",
                    status_badge,
                    zone_display,
                )

        self.console.print(table)

    def handle_log(self):
        #Collect raw inputs from the user
        species = Prompt.ask("[bold cyan]Species name[/]")
        lat = FloatPrompt.ask("[bold cyan]Latitude (-90 to 90)[/]")
        lon = FloatPrompt.ask("[bold cyan]Longitude (-180 to 180)[/]")
        count = IntPrompt.ask("[bold cyan]Individual count[/]", default=1)
        is_endangered = Confirm.ask("[bold red]Is this species endangered?[/]", default=False)
        choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4", "5"], default="1") # restrict menu choices

        #Instantiate sighting and pass it to self.tracker
        try:
            new_sighting = Sighting(
                species=species,
                lat=lat,
                lon=lon,
                count=count,
                is_endangered=is_endangered,
            )
            self.tracker.log_sighting(new_sighting)
            self.console.print("[bold green]Sighting saved![/]")
        except ValueError as e:
            # For invalid GPS bounds
            self.console.print(f"[bold red]Invalid input:[/] {e}")

    def run(self):
        """Main interactive loop."""
        while True:
            self.display_menu()
            choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4", "5"], default="1")
            if choice == "1":
                self.handle_log()
            elif choice == "5":
                break

    
   
        

