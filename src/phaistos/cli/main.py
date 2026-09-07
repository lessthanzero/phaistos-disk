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


@app.command("ngrams")
def ngrams_cmd(n: int = typer.Option(2, help="N-gram length (default 2 for bigrams)"), top: int = 15):
    """List most frequent intra-group n-grams."""
    from phaistos.stats.ngrams import extract_group_ngrams

    corpus = load_transcription("godart_1995")
    ngrams = extract_group_ngrams(corpus, n=n)
    sign_map = {s.evans_id: s for s in corpus.signs_catalogue}

    table = Table(title=f"Top {top} Intra-Group {n}-Grams", show_header=True)
    table.add_column(f"{n}-Gram (Evans)", style="bold cyan")
    table.add_column("Glyphs", justify="center")
    table.add_column("Frequency", justify="center")
    table.add_column("Percentage", justify="right")

    total = sum(ngrams.values())
    for gram, cnt in ngrams.most_common(top):
        glyphs = "".join(sign_map[s].unicode_char for s in gram if s in sign_map)
        pct = (cnt / total) * 100
        table.add_row("-".join(gram), glyphs, str(cnt), f"{pct:.1f}%")

    console.print(table)


@app.command("repetitions")
def repetitions_cmd():
    """List identical group repetitions, affixes, and edit-distance near-matches."""
    from phaistos.stats.repetitions import (
        find_identical_groups,
        find_common_affixes,
        find_near_identical_groups,
    )

    corpus = load_transcription("godart_1995")
    sign_map = {s.evans_id: s for s in corpus.signs_catalogue}

    identical = find_identical_groups(corpus)
    table_id = Table(title="Exact Repeated Groups", show_header=True)
    table_id.add_column("Sign Sequence", style="bold cyan")
    table_id.add_column("Glyphs", justify="center")
    table_id.add_column("Occurrences", justify="center")
    table_id.add_column("Group IDs")

    for seq, g_ids in sorted(identical.items(), key=lambda x: len(x[1]), reverse=True):
        glyphs = "".join(sign_map[s].unicode_char for s in seq.split("-") if s in sign_map)
        table_id.add_row(seq, glyphs, str(len(g_ids)), ", ".join(g_ids))
    console.print(table_id)

    # Prefixes
    affixes = find_common_affixes(corpus, min_len=2)
    table_pref = Table(title="Common Prefixes (Length >= 2)", show_header=True)
    table_pref.add_column("Prefix", style="bold cyan")
    table_pref.add_column("Glyphs", justify="center")
    table_pref.add_column("Count", justify="center")

    for pref, cnt in affixes["prefixes"].most_common(8):
        if cnt > 1:
            glyphs = "".join(sign_map[s].unicode_char for s in pref.split("-") if s in sign_map)
            table_pref.add_row(pref, glyphs, str(cnt))
    console.print(table_pref)

    # Near matches
    near = find_near_identical_groups(corpus, max_distance=1)
    table_near = Table(title="Near-Identical Groups (Edit Distance = 1)", show_header=True)
    table_near.add_column("Group Pair", style="bold cyan")
    table_near.add_column("Distance", justify="center")
    table_near.add_column("Sequences Comparison")

    for g1, g2, d in near[:8]:
        s1 = "-".join(next(g.signs for g in corpus.all_groups() if g.id == g1))
        s2 = "-".join(next(g.signs for g in corpus.all_groups() if g.id == g2))
        table_near.add_row(f"{g1} ↔ {g2}", str(d), f"{s1} vs {s2}")
    console.print(table_near)


@app.command("entropy")
def entropy_cmd():
    """Display information theoretic metrics: unigram entropy, conditional entropy, compressibility."""
    from phaistos.stats.entropy import (
        compute_unigram_entropy,
        compute_bigram_joint_and_conditional_entropy,
        compute_compressibility_metrics,
    )

    corpus = load_transcription("godart_1995")
    h_uni = compute_unigram_entropy(corpus)
    h_joint, h_cond, mi = compute_bigram_joint_and_conditional_entropy(corpus)
    comp = compute_compressibility_metrics(corpus)

    console.print(Panel("[bold cyan]Information Theory & Compressibility[/bold cyan]"))
    console.print(f"Unigram Entropy $H(X)$: [bold yellow]{h_uni:.4f} bits[/bold yellow] (Max: 5.4919 bits)")
    console.print(f"Bigram Joint Entropy $H(X, Y)$: [bold yellow]{h_joint:.4f} bits[/bold yellow]")
    console.print(f"Bigram Conditional Entropy $H(Y|X)$: [bold yellow]{h_cond:.4f} bits[/bold yellow]")
    console.print(f"Mutual Information $I(X; Y)$: [bold green]{mi:.4f} bits[/bold green]")
    console.print(f"\nCompressibility:")
    console.print(f"  • Raw Size: {comp['raw_bytes']:.0f} bytes")
    console.print(f"  • Zlib Compressed: {comp['zlib_bytes']:.0f} bytes (ratio: {comp['zlib_ratio']:.3f})")
    console.print(f"  • LZMA Compressed: {comp['lzma_bytes']:.0f} bytes (ratio: {comp['lzma_ratio']:.3f})")


@app.command("permutations")
def permutations_cmd(iterations: int = typer.Option(200, help="Number of Monte Carlo iterations")):
    """Run Anti-Bullshit Monte Carlo tests against randomized null controls."""
    from phaistos.stats.permutations import (
        run_monte_carlo_test,
        generate_frequency_preserving_corpus,
        metric_repeated_groups_count,
        metric_bigram_collisions,
        metric_conditional_entropy,
    )

    corpus = load_transcription("godart_1995")
    console.print(Panel(f"[bold cyan]Running Anti-Bullshit Controls ({iterations} iterations)...[/bold cyan]"))

    mc_rep = run_monte_carlo_test(
        corpus, metric_repeated_groups_count, generate_frequency_preserving_corpus, iterations=iterations
    )
    mc_bi = run_monte_carlo_test(
        corpus, metric_bigram_collisions, generate_frequency_preserving_corpus, iterations=iterations
    )
    mc_ent = run_monte_carlo_test(
        corpus, metric_conditional_entropy, generate_frequency_preserving_corpus, iterations=iterations
    )

    table = Table(title="Monte Carlo Permutation Tests vs Frequency-Preserving Null", show_header=True)
    table.add_column("Metric", style="bold cyan")
    table.add_column("Observed", justify="center")
    table.add_column("Null Mean (μ)", justify="center")
    table.add_column("Null Std (σ)", justify="center")
    table.add_column("Z-Score", justify="center")
    table.add_column("p-value", justify="center")
    table.add_column("Skeptic Assessment")

    def assess(p, z):
        if p < 0.01:
            return "[bold green]Significant (Non-Random Structure)[/bold green]"
        elif p < 0.05:
            return "[green]Weakly Significant[/green]"
        return "[dim red]Consistent with Chance (Null)[/dim red]"

    table.add_row(
        "Repeated Groups",
        f"{mc_rep['observed']:.0f}",
        f"{mc_rep['null_mean']:.2f}",
        f"{mc_rep['null_std']:.2f}",
        f"{mc_rep['z_score']:+.2f}",
        f"{mc_rep['p_value']:.4f}",
        assess(mc_rep['p_value'], mc_rep['z_score']),
    )
    table.add_row(
        "Bigram Collisions",
        f"{mc_bi['observed']:.0f}",
        f"{mc_bi['null_mean']:.2f}",
        f"{mc_bi['null_std']:.2f}",
        f"{mc_bi['z_score']:+.2f}",
        f"{mc_bi['p_value']:.4f}",
        assess(mc_bi['p_value'], mc_bi['z_score']),
    )
    table.add_row(
        "Conditional Entropy",
        f"{mc_ent['observed']:.4f}",
        f"{mc_ent['null_mean']:.4f}",
        f"{mc_ent['null_std']:.4f}",
        f"{mc_ent['z_score']:+.2f}",
        f"{mc_ent['p_value']:.4f}",
        assess(mc_ent['p_value'], mc_ent['z_score']),
    )

    console.print(table)


@app.command("baseline-report")
def baseline_report_cmd(output_file: str = typer.Option("reports/baseline-structural-analysis.md")):
    """Generate comprehensive scientific baseline report in Markdown."""
    from pathlib import Path
    from phaistos.reports.baseline import generate_baseline_structural_report

    corpus = load_transcription("godart_1995")
    out_path = Path(output_file)
    with console.status("[bold cyan]Compiling Baseline Structural Report...[/bold cyan]"):
        generate_baseline_structural_report(corpus, out_path)

    console.print(f"[bold green]Report successfully generated at:[/bold green] [cyan]{out_path}[/cyan]")


@app.command("correspondences")
def correspondences_cmd():
    """List scholarly cross-script correspondences and Chain of Inference levels."""
    from phaistos.comparative.loader import load_proposed_correspondences

    corrs = load_proposed_correspondences()
    corpus = load_transcription("godart_1995")
    sign_map = {s.evans_id: s for s in corpus.signs_catalogue}

    table = Table(title="Scholarly Cross-Script Correspondences & Chain of Inference", show_header=True)
    table.add_column("Disc Sign", style="bold cyan", justify="center")
    table.add_column("Glyph", justify="center")
    table.add_column("Name", style="bold")
    table.add_column("Linear A", justify="center")
    table.add_column("Linear B", justify="center")
    table.add_column("Phonetic Value", style="bold yellow", justify="center")
    table.add_column("Inference Level", justify="center")
    table.add_column("Similarity", justify="center")
    table.add_column("Proponents")

    for c in corrs:
        glyph = sign_map[c.disc_sign].unicode_char if c.disc_sign in sign_map else "?"
        la_str = c.linear_a_sign or "-"
        lb_str = c.linear_b_sign or "-"
        phon_str = f"/{c.proposed_phonetic_value}/" if c.proposed_phonetic_value else "[dim]ideogram[/dim]"

        lvl_color = "red" if c.inference_level.value == "L3" else ("yellow" if c.inference_level.value == "L2" else "green")
        lvl_str = f"[{lvl_color}]{c.inference_level.value}[/{lvl_color}]"

        sim_color = "green" if c.visual_similarity.value == "high" else ("yellow" if c.visual_similarity.value == "medium" else "dim red")
        sim_str = f"[{sim_color}]{c.visual_similarity.value}[/{sim_color}]"

        table.add_row(
            c.disc_sign,
            glyph,
            c.disc_name,
            la_str,
            lb_str,
            phon_str,
            lvl_str,
            sim_str,
            ", ".join(c.proponents),
        )

    console.print(table)
    console.print("\n[dim]Chain of Inference Legend: L0 = Observation | L1 = Formal Resemblance | L2 = Phonetic Projection | L3 = Translation Hypothesis[/dim]\n")


@app.command("compare-linear-a")
def compare_linear_a_cmd(iterations: int = typer.Option(500, help="Permutation test iterations")):
    """Evaluate statistical correlation of proposed correspondences against Linear A frequencies."""
    from phaistos.comparative.loader import load_proposed_correspondences, load_linear_a_signs
    from phaistos.comparative.matcher import evaluate_frequency_rank_correlation
    from phaistos.comparative.permutations import run_correspondence_permutation_test

    corpus = load_transcription("godart_1995")
    corrs = load_proposed_correspondences()
    la_signs = load_linear_a_signs()

    eval_res = evaluate_frequency_rank_correlation(corpus, corrs, la_signs)
    perm_res = run_correspondence_permutation_test(corpus, corrs, la_signs, iterations=iterations)

    console.print(Panel("[bold cyan]Phaistos vs Linear A Frequency Rank Correlation[/bold cyan]"))
    console.print(f"Sample Size (Matched Signs): [bold]{eval_res['sample_size']:.0f}[/bold]")
    console.print(f"Observed Spearman Rank Correlation (ρ): [bold yellow]{eval_res['spearman_rho']:+.4f}[/bold yellow]")
    console.print(f"Analytical p-value: {eval_res['p_value']:.4f}\n")

    table = Table(title="Permutation Test vs Random Linear A Assignments", show_header=True)
    table.add_column("Observed ρ", justify="center")
    table.add_column("Null Mean ρ (μ)", justify="center")
    table.add_column("Null Std (σ)", justify="center")
    table.add_column("Z-Score", justify="center")
    table.add_column("Empirical p-value", justify="center")
    table.add_column("Skeptic Ruling")

    assessment = "[green]Statistically Significant[/green]" if perm_res["p_value"] < 0.05 else "[yellow]Inconclusive / Weak[/yellow]"
    table.add_row(
        f"{perm_res['observed_rho']:+.4f}",
        f"{perm_res['null_mean_rho']:+.4f}",
        f"{perm_res['null_std_rho']:.4f}",
        f"{perm_res['z_score']:+.2f}",
        f"{perm_res['p_value']:.4f}",
        assessment,
    )
    console.print(table)


if __name__ == "__main__":
    app()



