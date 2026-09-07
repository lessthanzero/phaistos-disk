"""Command line interface for Phaistos Disc Lab."""

from typing import Optional
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from phaistos.corpus.loader import load_signs, load_transcription
from phaistos.corpus.validator import validate_corpus, ValidationError
from phaistos.stats.frequency import (
    compute_sign_frequencies,
    compute_group_length_distribution,
    compute_positional_statistics,
    compute_shannon_entropy,
)

app = typer.Typer(
    name="phaistos",
    help="Phaistos Disc Lab computational research workbench",
    add_completion=False,
)
console = Console()


@app.command("validate")
def validate_cmd(source: str = "godart_1995"):
    """Validate canonical corpus epigraphic invariants and structural integrity."""
    console.print(Panel(f"[bold cyan]Validating Corpus Canon: {source}[/bold cyan]"))
    try:
        corpus = load_transcription(source)
        results = validate_corpus(corpus)

        table = Table(title="Canonical Invariants Verification", show_header=True)
        table.add_column("Invariant Test", style="dim")
        table.add_column("Status", style="bold green")

        for test_name in results:
            table.add_row(test_name, "PASS [OK]")

        console.print(table)
        console.print(
            f"\n[bold green]Corpus verification passed successfully![/bold green] "
            f"({corpus.total_groups} groups, {corpus.total_signs} signs, {corpus.total_oblique_strokes} oblique strokes)\n"
        )
    except ValidationError as e:
        console.print(f"[bold red]Validation Failure:[/bold red] {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[bold red]Error loading corpus:[/bold red] {e}")
        raise typer.Exit(code=1)


@app.command("signs")
def signs_cmd():
    """Display the canonical 45 signs catalogue with Unicode and iconography."""
    signs = load_signs()
    table = Table(title="Phaistos Disc Sign Repertoire (Evans 01-45)", show_header=True)
    table.add_column("Evans ID", style="bold cyan", justify="center")
    table.add_column("Glyph", justify="center")
    table.add_column("Name", style="bold")
    table.add_column("Category", style="dim")
    table.add_column("Unicode", justify="center")
    table.add_column("Description")

    for s in signs:
        table.add_row(
            s.evans_id,
            s.unicode_char,
            s.name,
            s.category,
            s.unicode_hex,
            s.description,
        )

    console.print(table)


@app.command("stats")
def stats_cmd(source: str = "godart_1995"):
    """Compute structural frequency, length distributions, and Shannon entropy."""
    corpus = load_transcription(source)
    counts = compute_sign_frequencies(corpus)
    entropy = compute_shannon_entropy(counts)
    len_dist = compute_group_length_distribution(corpus)

    console.print(Panel("[bold cyan]Phaistos Disc Structural Statistics[/bold cyan]"))
    console.print(f"Total Signs: [bold]{corpus.total_signs}[/bold]")
    console.print(f"Total Groups: [bold]{corpus.total_groups}[/bold] (A: {corpus.side_a.group_count}, B: {corpus.side_b.group_count})")
    console.print(f"Incised Oblique Strokes: [bold]{corpus.total_oblique_strokes}[/bold] (A: {corpus.side_a.oblique_stroke_count}, B: {corpus.side_b.oblique_stroke_count})")
    console.print(f"Unique Sign Types: [bold]{len(counts)}[/bold] / 45")
    console.print(f"Shannon Entropy: [bold yellow]{entropy:.4f} bits[/bold yellow] (Theoretical max for 45 symbols: 5.4919 bits)\n")

    # Group length distribution
    l_table = Table(title="Group Length Distribution", show_header=True)
    l_table.add_column("Length (signs)", justify="center")
    l_table.add_column("Group Count", justify="center")
    l_table.add_column("Percentage", justify="right")

    for l in sorted(len_dist.keys()):
        pct = (len_dist[l] / corpus.total_groups) * 100
        l_table.add_row(str(l), str(len_dist[l]), f"{pct:.1f}%")
    console.print(l_table)

    # Top frequent signs
    f_table = Table(title="Top 10 Most Frequent Signs", show_header=True)
    f_table.add_column("Evans ID", justify="center")
    f_table.add_column("Glyph", justify="center")
    f_table.add_column("Count", justify="center")
    f_table.add_column("Percentage", justify="right")

    for sign_id, freq in counts.most_common(10):
        # find sign in catalogue
        sign_obj = next((s for s in corpus.signs_catalogue if s.evans_id == sign_id), None)
        glyph = sign_obj.unicode_char if sign_obj else "?"
        pct = (freq / corpus.total_signs) * 100
        f_table.add_row(sign_id, glyph, str(freq), f"{pct:.1f}%")

    console.print(f_table)


@app.command("groups")
def groups_cmd(side: Optional[str] = typer.Option(None, help="Filter by side A or B")):
    """List sign groups with outside-in reading sequence and annotations."""
    corpus = load_transcription("godart_1995")
    groups = corpus.all_groups()
    if side:
        side_upper = side.upper()
        groups = [g for g in groups if g.side == side_upper]

    table = Table(title=f"Sign Groups (Outside-In Order) {'- Side ' + side.upper() if side else ''}", show_header=True)
    table.add_column("ID", style="bold cyan")
    table.add_column("Turn", justify="center")
    table.add_column("Signs (Evans IDs)", style="bold")
    table.add_column("Length", justify="center")
    table.add_column("Oblique Stroke", justify="center")
    table.add_column("Erasure / Palimpsest", justify="center")

    for g in groups:
        stroke_str = "[green]YES (𐇽)[/green]" if g.oblique_stroke else "[dim]no[/dim]"
        erasure_str = "[yellow]YES[/yellow]" if g.erasure else "[dim]no[/dim]"
        table.add_row(
            g.id,
            str(g.turn),
            "-".join(g.signs),
            str(g.length),
            stroke_str,
            erasure_str,
        )

    console.print(table)


@app.command("render-svg")
def render_svg_cmd(
    output_dir: str = typer.Option("reports/visuals", help="Output directory for generated SVG files"),
    source: str = "godart_1995",
):
    """Render programmatic publication-quality SVG vector diagrams for Sides A & B."""
    from pathlib import Path
    from phaistos.geometry.svg import export_disc_svgs

    corpus = load_transcription(source)
    out_path = Path(output_dir)
    path_a, path_b = export_disc_svgs(corpus, out_path)

    console.print(f"[bold green]Successfully generated SVG diagrams:[/bold green]")
    console.print(f"  • Side A: [cyan]{path_a}[/cyan]")
    console.print(f"  • Side B: [cyan]{path_b}[/cyan]")


if __name__ == "__main__":
    app()

