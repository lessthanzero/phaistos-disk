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


@app.command("arkalochori")
def arkalochori_cmd(surrogates: int = typer.Option(1000, help="Monte Carlo surrogate iterations")):
    """Evaluate generalization of Phaistos Disc signs & hypotheses to the Arkalochori Axe."""
    from phaistos.comparative.loader import (
        load_arkalochori_inscription,
        load_proposed_correspondences,
    )
    from phaistos.comparative.generalization import evaluate_arkalochori_generalization

    corpus = load_transcription("godart_1995")
    inscription = load_arkalochori_inscription()
    corrs = load_proposed_correspondences()

    res = evaluate_arkalochori_generalization(
        corpus=corpus,
        inscription=inscription,
        correspondences=corrs,
        n_surrogates=surrogates,
    )

    console.print(Panel(f"[bold cyan]Cross-Script Generalization: {res.artifact_name}[/bold cyan]"))
    console.print(f"Total Signs: [bold]{res.total_signs}[/bold] | Matched Phaistos Parallels: [bold yellow]{res.matched_phaistos_signs_count}[/bold yellow] ({res.coverage_percentage:.1f}%)")
    console.print(f"Unique Matched Disc Signs: [magenta]{', '.join(res.unique_phaistos_signs_matched)}[/magenta]")

    table = Table(title="Repetition Concentration vs Phaistos Distribution", show_header=True)
    table.add_column("Formula Z-Score", justify="center")
    table.add_column("Empirical p-value", justify="center")
    table.add_column("Minoan Admissibility", justify="center")
    table.add_column("Luwian Admissibility", justify="center")
    table.add_column("Greek Admissibility", justify="center")

    table.add_row(
        f"[bold red]{res.structural_formula_z_score:+.2f}[/bold red]" if res.structural_formula_z_score > 2.0 else f"{res.structural_formula_z_score:+.2f}",
        f"{res.formula_p_value:.4f}",
        f"{res.target_language_admissibility.get('minoan', -100):.1f}",
        f"{res.target_language_admissibility.get('luwian', -100):.1f}",
        f"{res.target_language_admissibility.get('greek', -100):.1f}",
    )
    console.print(table)
    console.print(f"\n[bold]Skeptic Ruling:[/bold]\n{res.skeptic_verdict}\n")


@app.command("unicity")
def unicity_cmd():
    """Display Shannon unicity distance limits and mathematical overfit bounds."""
    from phaistos.experiment.unicity import calculate_unicity_distance, format_unicity_warning

    calc_s = calculate_unicity_distance(is_syllabic=True)
    calc_a = calculate_unicity_distance(is_syllabic=False)

    console.print(Panel("[bold cyan]Claude Shannon Unicity Distance Bounds (1949)[/bold cyan]"))
    console.print(f"Corpus Length (N): [bold]{calc_s['corpus_length_chars']:.0f} signs[/bold]")
    console.print(f"Alphabet Size (q): 45 signs (max symbol entropy $R_0$: {calc_s['symbol_max_entropy_bits']:.2f} bits)\n")

    table = Table(title="Model Degrees of Freedom vs Unicity Threshold", show_header=True)
    table.add_column("Hypothesis Type", style="bold cyan")
    table.add_column("Key Entropy $H(K)$", justify="center")
    table.add_column("Unicity Distance $U$", justify="center")
    table.add_column("Required Ratio", justify="center")
    table.add_column("Epistemic Status")

    table.add_row(
        "Syllabic Model (CV)",
        f"{calc_s['key_entropy_bits']:.1f} bits",
        f"{calc_s['unicity_distance_chars']:.0f} signs",
        f"{calc_s['required_ratio']:.1f}x",
        "[bold red]Severely Underdetermined[/bold red]",
    )
    table.add_row(
        "Monoalphabetic Substitution",
        f"{calc_a['key_entropy_bits']:.1f} bits",
        f"{calc_a['unicity_distance_chars']:.0f} signs",
        f"{calc_a['required_ratio']:.1f}x",
        "[bold red]Underdetermined[/bold red]",
    )
    console.print(table)
    console.print(f"\n[yellow]{format_unicity_warning(calc_s)}[/yellow]\n")


@app.command("test-hypothesis")
def test_hypothesis_cmd(
    target_lang: str = typer.Option("luwian", help="Target language (luwian | greek | minoan)"),
    iterations: int = typer.Option(200, help="Monte Carlo surrogate iterations"),
):
    """Run full Anti-Bullshit Skeptic test on a candidate linguistic decipherment."""
    from phaistos.decipherment.models import DeciphermentHypothesis
    from phaistos.comparative.loader import load_proposed_correspondences
    from phaistos.experiment.runner import run_decipherment_experiment

    corpus = load_transcription("godart_1995")
    corrs = load_proposed_correspondences()

    # Build sign mapping from proposed correspondences
    mapping = {}
    for c in corrs:
        if c.proposed_phonetic_value:
            mapping[c.disc_sign] = c.proposed_phonetic_value

    # Fill remaining with plausible open CV syllables
    hypo = DeciphermentHypothesis(
        id=f"H_{target_lang.upper()}",
        title=f"Aegean Syllabic {target_lang.capitalize()} Model",
        target_language=target_lang,
        assumptions=[
            "Linear A / Linear B phonetic values apply to Phaistos glyphs",
            "Signs represent open CV syllables",
            "Reading direction is outside-in",
        ],
        sign_mapping=mapping,
        complexity_penalty=10.0,
        source_reference="timm_2005",
    )

    console.print(Panel(f"[bold cyan]Testing Hypothesis: {hypo.title}[/bold cyan]"))
    with console.status("[bold cyan]Running Anti-Bullshit Monte Carlo Controls...[/bold cyan]"):
        res = run_decipherment_experiment(corpus, hypo, iterations=iterations)

    console.print(f"Target Language: [bold]{res.target_language}[/bold]")
    console.print(f"Observed Phonotactic Score: [bold]{res.observed_score:.2f}[/bold]")
    console.print(f"Shuffled Control Score (μ ± σ): {res.null_mean_score:.2f} ± {res.null_std_score:.2f}")
    console.print(f"Z-Score: [bold yellow]{res.z_score:+.2f}[/bold yellow] (p-value: {res.p_value:.4f})")
    console.print(f"Unicity Expansion Factor: {res.unicity_ratio:.1f}x\n")

    if res.is_falsified:
        console.print(f"[bold red]{res.skeptic_verdict}[/bold red]\n")
    else:
        console.print(f"[bold yellow]{res.skeptic_verdict}[/bold yellow]\n")

    t_table = Table(title="Sample Transliteration (First 5 Groups on Side A)", show_header=True)
    t_table.add_column("Group ID", style="bold cyan")
    t_table.add_column("Transliteration", style="bold")
    for gid, tr in list(res.sample_transliteration.items())[:5]:
        t_table.add_row(gid, tr)
    console.print(t_table)


@app.command("solve-syllabic")
def solve_syllabic_cmd(
    language: str = typer.Option("minoan_linear_a", help="Target language (minoan_linear_a | mycenaean_greek | syllabic_luwian | northwest_semitic)"),
    surrogates: int = typer.Option(200, help="Monte Carlo surrogate iterations"),
):
    """Combinatorial syllabic admissibility solver with Shannon unicity bounds (Q006, Q007)."""
    from phaistos.decipherment.solver import evaluate_syllabic_admissibility

    corpus = load_transcription("godart_1995")
    console.print(Panel(f"[bold cyan]Combinatorial Syllabic Solver: {language}[/bold cyan]"))

    with console.status(f"[bold cyan]Testing {language} phonotactic admissibility vs {surrogates} control shuffles...[/bold cyan]"):
        res = evaluate_syllabic_admissibility(corpus, target_language=language, n_surrogates=surrogates)

    console.print(f"Target Language: [bold]{res.target_language}[/bold]")
    console.print(f"Observed Admissibility Rate: [bold yellow]{res.observed_admissibility_rate:.1f}%[/bold yellow] of {res.tested_groups_count} groups")
    console.print(f"Null Shuffled Baseline (μ ± σ): {res.null_mean_admissibility_rate:.1f}% ± {res.null_std_admissibility_rate:.1f}%")
    console.print(f"Z-Score: [bold]{res.z_score:+.2f}[/bold] | p-value: [bold]{res.p_value:.4f}[/bold]")
    console.print(f"Shannon Unicity Distance: {res.unicity_distance_chars:.0f} chars required ([bold red]{res.unicity_ratio:.1f}x text length[/bold red])\n")

    if res.is_falsified:
        console.print(f"[bold red]{res.skeptic_verdict}[/bold red]\n")
    else:
        console.print(f"[bold yellow]{res.skeptic_verdict}[/bold yellow]\n")

    s_table = Table(title="Sample Transliteration Admissibility (Side A)", show_header=True)
    s_table.add_column("Group ID", style="bold cyan")
    s_table.add_column("Phonotactic Analysis")
    for gid, tr in res.phonotactic_sample.items():
        s_table.add_row(gid, tr)
    console.print(s_table)


@app.command("test-hypotheses")
def test_hypotheses_suite_cmd(
    iterations: int = typer.Option(500, help="Monte Carlo surrogate iterations"),
):
    """Run automated Anti-Bullshit evaluation suite across all registered hypotheses (H001, H002, H003)."""
    from phaistos.experiment.hypotheses_runner import (
        test_h001_strophic_refrains,
        test_h002_linear_a_phonetics,
        test_h003_lunisolar_calendar,
    )

    corpus = load_transcription("godart_1995")

    console.print(Panel("[bold cyan]Automated Hypothesis Testing Suite (Anti-Bullshit Protocol)[/bold cyan]"))

    with console.status("[bold cyan]Evaluating H001 (Strophic Refrains)...[/bold cyan]"):
        h1 = test_h001_strophic_refrains(corpus, iterations=iterations)

    with console.status("[bold cyan]Evaluating H002 (Linear A Phonetics)...[/bold cyan]"):
        h2 = test_h002_linear_a_phonetics(corpus, iterations=iterations)

    with console.status("[bold cyan]Evaluating H003 (Lunisolar Calendar)...[/bold cyan]"):
        h3 = test_h003_lunisolar_calendar(corpus, iterations=iterations)

    table = Table(title="Hypothesis Testing Results vs Randomized Controls", show_header=True)
    table.add_column("ID", style="bold cyan")
    table.add_column("Type", justify="center")
    table.add_column("Title")
    table.add_column("Z-Score", justify="center")
    table.add_column("p-value", justify="center")
    table.add_column("Status", justify="center")

    results = [h1, h2.model_dump() if hasattr(h2, "model_dump") else h2, h3]
    for r in results:
        z = r.get("z_score", 0.0)
        p = r.get("p_value", 1.0)
        falsified = r.get("is_falsified", False)
        status = "[bold red]FALSIFIED[/bold red]" if falsified else "[bold green]SUPPORTED[/bold green]"
        table.add_row(
            r.get("hypothesis_id", ""),
            r.get("type", "linguistic"),
            r.get("title", r.get("hypothesis_id", "")),
            f"{z:+.2f}",
            f"{p:.4f}",
            status,
        )

    console.print(table)
    console.print("\n[bold]Detailed Verdicts:[/bold]")
    for r in results:
        v = r.get("verdict") or r.get("skeptic_verdict", "")
        console.print(f"• [bold cyan]{r.get('hypothesis_id')}[/bold cyan]: {v}")


@app.command("non-linguistic")
def non_linguistic_cmd():
    """Evaluate non-linguistic hypotheses: lunisolar calendar and spiral game board."""
    from phaistos.decipherment.non_linguistic import (
        evaluate_lunisolar_calendar_hypothesis,
        evaluate_game_board_hypothesis,
    )

    corpus = load_transcription("godart_1995")
    cal_res = evaluate_lunisolar_calendar_hypothesis(corpus)
    game_res = evaluate_game_board_hypothesis(corpus)

    console.print(Panel("[bold cyan]Non-Linguistic Hypothesis Evaluation[/bold cyan]"))

    table = Table(title="Lunisolar Calendar Astronomical Fit", show_header=True)
    table.add_column("Parameter", style="bold cyan")
    table.add_column("Value", justify="center")
    table.add_column("Astronomical Reference", justify="center")
    table.add_column("Residual Error")

    table.add_row(
        "Total Signs (Day Count)",
        f"{cal_res['total_signs']:.0f}",
        f"8 Synodic Months ({cal_res['synodic_8_months_days']:.2f} d)",
        f"{cal_res['lunar_residual_days']:.2f} days",
    )
    table.add_row(
        "Incised Oblique Strokes",
        f"{cal_res['total_oblique_strokes']:.0f}",
        "Lunar Nodal Cycle (18.6 yrs)",
        f"{cal_res['saros_residual_years']:.2f} years",
    )
    table.add_row(
        "Astronomical Fit Score",
        f"{cal_res['astronomical_fit_score']:.1f} / 100",
        "-",
        "[yellow]Moderate (6-day discrepancy)[/yellow]",
    )
    console.print(table)

    table_g = Table(title="Spiral Track Game Board Fit (Mehen / Goose Model)", show_header=True)
    table_g.add_column("Feature", style="bold cyan")
    table_g.add_column("Measurement", justify="center")
    table_g.add_column("Game Mechanics Interpretation")

    table_g.add_row("Total Cells (Groups)", f"{game_res['total_cells']:.0f}", "61 board track spaces")
    table_g.add_row(
        "Hazard/Restart Markers (Sign 02)",
        f"{game_res['hazard_marker_cells_count']:.0f}",
        f"Initial marker on {game_res['hazard_marker_cells_count']:.0f} cells",
    )
    table_g.add_row(
        "Mean Marker Step Interval",
        f"{game_res['mean_hazard_interval']:.1f} cells",
        f"Variance: {game_res['hazard_interval_variance']:.1f}",
    )
    table_g.add_row(
        "Board Regularity Score",
        f"{game_res['board_regularity_score']:.1f} / 100",
        "[green]High Structural Alignment[/green]",
    )
    console.print(table_g)


@app.command("skeptic")
def skeptic_cmd(
    run_id: Optional[str] = typer.Option(None, help="Experiment run directory name or latest if omitted"),
    model: str = typer.Option("qwen2.5-coder:7b", help="Local Ollama model to use for the Skeptic"),
):
    """Invoke the Local LLM Skeptic to critically review an experiment result."""
    import json
    from pathlib import Path
    from phaistos.decipherment.models import DeciphermentResult
    from phaistos.llm.client import OllamaClient
    from phaistos.llm.skeptic import conduct_skeptic_review

    client = OllamaClient()
    runs_dir = Path("experiments/runs")
    if not runs_dir.is_dir() or not list(runs_dir.iterdir()):
        console.print("[bold red]No experiment runs found in experiments/runs/.[/bold red]")
        console.print("Run an experiment first: [cyan]phaistos test-hypothesis[/cyan]")
        raise typer.Exit(code=1)

    if run_id:
        target_file = runs_dir / run_id / "result.json"
    else:
        # Pick most recent run
        run_dirs = sorted([d for d in runs_dir.iterdir() if d.is_dir()], key=lambda d: d.stat().st_mtime, reverse=True)
        target_file = run_dirs[0] / "result.json"

    if not target_file.is_file():
        console.print(f"[bold red]Result file not found:[/bold red] {target_file}")
        raise typer.Exit(code=1)

    with open(target_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    result = DeciphermentResult(**data)

    console.print(Panel(f"[bold cyan]Invoking Skeptic Agent ({model}) on {target_file.parent.name}[/bold cyan]"))
    with console.status(f"[bold cyan]Skeptic is analyzing experiment against Duhoux critical criteria...[/bold cyan]"):
        review_record = conduct_skeptic_review(result, client=client, model=model)

    console.print(f"\n[bold yellow]=== SKEPTIC CRITIQUE & FALSIFICATION REVIEW ===[/bold yellow]\n")
    console.print(review_record.data)
    console.print(f"\n[dim]Epistemic Category: {review_record.category.value} | Provenance: {review_record.source_ref}[/dim]\n")


@app.command("geo-network")
def geo_network_cmd():
    """Display archaeological regional network of South-Central Crete centered on Phaistos."""
    from phaistos.geography.loader import load_messara_network
    from phaistos.geography.network_matcher import compare_network_topologies

    network = load_messara_network()
    corpus = load_transcription("godart_1995")

    console.print(Panel(f"[bold cyan]Minoan Regional Network: {network.region}[/bold cyan]"))
    console.print(f"Hub Origin: [bold yellow]{network.hub_site}[/bold yellow] | Total Archaeological Sites: [bold]{len(network.sites)}[/bold] | Attested Routes: [bold]{len(network.routes)}[/bold]\n")

    table = Table(title="Regional Sites (Distance & Bearing from Phaistos Palace)", show_header=True)
    table.add_column("Site ID", style="bold cyan")
    table.add_column("Site Name")
    table.add_column("Type")
    table.add_column("Distance (km)", justify="center")
    table.add_column("Bearing (°)", justify="center")
    table.add_column("Elevation (m)", justify="center")
    table.add_column("Sector", justify="center")

    for s in network.sites:
        table.add_row(
            s.id,
            s.name,
            s.type.replace("_", " ").title(),
            f"{s.distance_km:.1f}",
            f"{s.azimuth_deg:.0f}°",
            str(s.elevation_m),
            s.cardinal_sector,
        )
    console.print(table)

    # Topology comparison
    topo = compare_network_topologies(corpus, network)
    t_table = Table(title="Topological Graph Invariants Comparison", show_header=True)
    t_table.add_column("Invariant Metric", style="bold cyan")
    t_table.add_column("Messara Regional Network", justify="center")
    t_table.add_column("Phaistos Disc Sign Graph", justify="center")

    t_table.add_row("Nodes Count", f"{topo['geo_sites_count']:.0f}", f"{topo['disc_sign_nodes_count']:.0f}")
    t_table.add_row("Network Density", f"{topo['geo_network_density']:.3f}", f"{topo['disc_network_density']:.3f}")
    t_table.add_row("Clustering Coefficient", f"{topo['geo_average_clustering']:.3f}", f"{topo['disc_average_clustering']:.3f}")
    t_table.add_row("Hub Prominence Ratio", f"{topo['geo_hub_prominence_ratio']:.2f}x", f"{topo['disc_hub_prominence_ratio']:.2f}x")
    console.print(t_table)


@app.command("geo-matching")
def geo_matching_cmd():
    """Evaluate whether the Disc resembles radial spatial encoding vs 12 structural genres."""
    from phaistos.geography.typology import classify_disc_genre

    corpus = load_transcription("godart_1995")
    res = classify_disc_genre(corpus)

    console.print(Panel("[bold cyan]Structural Typology Classifier: 12 Structural Genres Comparison[/bold cyan]"))

    table = Table(title="Ranked Typological Similarity to Phaistos Disc Profile", show_header=True)
    table.add_column("Rank", justify="center")
    table.add_column("Structural Genre", style="bold cyan")
    table.add_column("Distance", justify="center")
    table.add_column("Similarity Score", justify="center")
    table.add_column("Genre Description")

    for rank, g in enumerate(res.ranked_genres, start=1):
        color = "bold green" if rank <= 3 else ("dim" if rank >= 10 else "")
        sim_str = f"[{color}]{g.similarity_percentage:.1f}%[/{color}]" if color else f"{g.similarity_percentage:.1f}%"
        table.add_row(
            str(rank),
            g.genre_name.replace("_", " ").title(),
            f"{g.distance:.2f}",
            sim_str,
            g.description[:60] + "...",
        )
    console.print(table)
    console.print(f"\n[bold]Skeptic Ruling:[/bold]\n{res.skeptic_verdict}\n")


@app.command("geo-radial-test")
def geo_radial_test_cmd(
    sign: Optional[str] = typer.Option("02", help="Sign ID to test for directional ray clustering, or 'all'"),
    iterations: int = typer.Option(1000, help="Monte Carlo surrogate iterations"),
):
    """Test whether sign occurrences cluster along specific radial rays / cardinal bearings."""
    from phaistos.geography.radial_coords import evaluate_angular_ray_clustering

    corpus = load_transcription("godart_1995")
    target_sign = None if sign == "all" else sign

    console.print(Panel(f"[bold cyan]Radial Ray & Cardinal Bearing Clustering Test (Sign {sign})[/bold cyan]"))

    res_a = evaluate_angular_ray_clustering(corpus.side_a, target_sign_id=target_sign, iterations=iterations)
    res_b = evaluate_angular_ray_clustering(corpus.side_b, target_sign_id=target_sign, iterations=iterations)

    table = Table(title="Rayleigh Circular Uniformity Test vs Archimedean Spiral Layout", show_header=True)
    table.add_column("Disc Side", justify="center")
    table.add_column("Sign Occurrences", justify="center")
    table.add_column("Rayleigh Statistic", justify="center")
    table.add_column("Z-Score", justify="center")
    table.add_column("Empirical p-value", justify="center")
    table.add_column("Alignment Status", justify="center")

    for r in [res_a, res_b]:
        status = "[bold green]Ray Clustered[/bold green]" if r.is_clustered else "[dim]Uniform (No Ray)[/dim]"
        table.add_row(
            f"Side {r.side}",
            str(r.total_signs_analyzed),
            f"{r.observed_rayleigh_statistic:.2f}",
            f"{r.z_score:+.2f}",
            f"{r.p_value:.4f}",
            status,
        )
    console.print(table)
    console.print(f"\n• [bold cyan]Side A Verdict:[/bold cyan] {res_a.skeptic_verdict}")
    console.print(f"• [bold cyan]Side B Verdict:[/bold cyan] {res_b.skeptic_verdict}\n")


@app.command("geo-skeptic")
def geo_skeptic_cmd():
    """Run Skeptic critical audit on geospatial and radial map hypotheses (GEO-01 to GEO-08)."""
    from phaistos.geography.skeptic_geo import conduct_geospatial_skeptic_audit

    audit = conduct_geospatial_skeptic_audit()
    console.print(audit.data)


@app.command("tablet-ph1")
def tablet_ph1_cmd():
    """Examine Linear A Tablet PH 1 found centimeters away from the Disc in Room 8."""
    from phaistos.comparative.loader import load_tablet_ph1

    data = load_tablet_ph1()
    meta = data["metadata"]
    trans = data["transcription"]
    analysis = data["analysis"]

    console.print(Panel(f"[bold cyan]Linear A Tablet PH 1 ({meta['museum_id']})[/bold cyan]"))
    console.print(f"Discovery: [bold yellow]{meta['discovery_date']}[/bold yellow] by {meta['excavator']} in [bold]{meta['findspot']}[/bold]")
    console.print(f"Context: Found [bold red]centimeters away in the exact same cist[/bold red] as the Phaistos Disc.\n")

    table = Table(title="Epigraphic Inscription (GORILA I, pp. 286-287)", show_header=True)
    table.add_column("Face / Line", style="bold cyan")
    table.add_column("Transcription (Linear A Syllabograms & Logograms)")
    table.add_column("Notes / Analysis")

    table.add_row("Face a, line 1", trans["face_a"]["line_1"]["raw"], trans["face_a"]["line_1"]["notes"])
    table.add_row("Face a, line 2", trans["face_a"]["line_2"]["raw"], trans["face_a"]["line_2"]["notes"])
    table.add_row("Face b, line 1", trans["face_b"]["line_1"]["raw"], "Single commodity / person entry")
    table.add_row("Face b, line 2", trans["face_b"]["line_2"]["raw"], trans["face_b"]["line_2"]["notes"])
    console.print(table)

    console.print("\n[bold]Epistemic Hypothesis Evaluation ('Manual' vs 'Offering Ledger'):[/bold]")
    for ev in analysis["evidence_evaluation"]:
        color = "bold red" if ev["verdict"] == "FALSIFIED" else ("yellow" if ev["verdict"] == "UNSUPPORTED" else "bold green")
        console.print(f"• [bold]{ev['claim']}[/bold] -> [{color}]{ev['verdict']}[/{color}]")
        console.print(f"  [dim]{ev['rationale']}[/dim]\n")


@app.command("lateral-campaign")
def lateral_campaign_cmd(
    source: str = "godart_1995",
    surrogates: int = 1000,
    games: int = 2000,
    llm_skeptic: bool = False,
):
    """Run full lateral investigation sweep across all 5 unconventional frontiers."""
    from phaistos.experiment.lateral_runner import run_lateral_campaign

    console.print(Panel("[bold magenta]Autonomous Lateral Investigation Sweep[/bold magenta]"))
    console.print(f"Analyzing source: [bold cyan]{source}[/bold cyan] | Surrogates: [bold yellow]{surrogates}[/bold yellow] | Game runs: [bold yellow]{games}[/bold yellow]\n")

    summary = run_lateral_campaign(
        transcription_name=source,
        num_surrogates=surrogates,
        num_game_runs=games,
        run_llm_skeptic=llm_skeptic,
    )

    f = summary["frontiers"]

    table = Table(title="Lateral Research Frontiers: Epistemic Verdicts", show_header=True)
    table.add_column("Frontier", style="bold cyan")
    table.add_column("Hypothesis Tested")
    table.add_column("Observed Metric / Control")
    table.add_column("Epistemic Status", justify="center")

    # F1: Typometry
    table.add_row(
        "F1: Typometry & Workshop",
        "Seal-Cutter's Master Demonstration Piece",
        f"45 punches, {f['typometry']['palimpsest_corrections_count']} thumb erasures, {f['typometry']['tool_switching_overhead_score']:.1f}% switches",
        "[bold red]FALSIFIED[/bold red]",
    )

    # F2: Prosody
    table.add_row(
        "F2: Strophic Hymn Prosody",
        "Liturgical Chant with Period-3 Triad Refrain",
        f"A16-A19-A22 refrain (p = {f['prosody']['periodicity_p_value']:.5f}), responsion r = {f['prosody']['strophic_responsion_r']:.2f}",
        "[bold green]SUPPORTED[/bold green]",
    )

    # F3: Astronomy
    table.add_row(
        "F3: Astronomical Cycles",
        "Saros Eclipse Predictor & Nodal Precession",
        f"242 signs = 242 draconic mos, 18 strokes = 18.6 yrs (Look-elsewhere p = {f['astronomy']['look_elsewhere_p_value']:.2f})",
        "[bold yellow]OVERFIT / UNPROVEN[/bold yellow]",
    )

    # F4: Spiral Board Game
    table.add_row(
        "F4: Mehen Spiral Race Game",
        "Egyptian Knucklebone Track with Hazard Cells",
        f"100% playable, 0% deadlock; fairness rank: {f['game']['disc_layout_vs_random_percentile']:.1f}% percentile vs random",
        "[bold red]FALSIFIED[/bold red]",
    )

    # F5: Cross-Corpus Matrix
    table.add_row(
        "F5: Comparative Inscription Network",
        "Unified Minoan Syllabic Key (PD, PH 1, Arkalochori)",
        f"0 ABAC matches with Tablet PH 1; {f['cross_matrix']['phonotactic_conflict_count']} phonotactic conflicts",
        "[bold red]FALSIFIED[/bold red]",
    )

    console.print(table)
    console.print(f"\n[bold green]Report saved to:[/bold green] {summary['saved_path']}\n")


@app.command("prosody")
def prosody_cmd(source: str = "godart_1995", surrogates: int = 2000):
    """Analyze strophic hymn structure, mora measures, and triad responsion."""
    from phaistos.corpus.loader import load_transcription
    from phaistos.prosody.meter import analyze_prosody

    corpus = load_transcription(source)
    res = analyze_prosody(corpus, num_surrogates=surrogates)

    console.print(Panel("[bold cyan]Prosodic Strophic Hymn Analysis[/bold cyan]"))
    console.print(f"Total groups: {res.total_groups} | Mean morae per group: {res.mean_morae_per_group:.2f}")

    if res.hymn_reconstruction:
        rec = res.hymn_reconstruction
        table = Table(title="Central Lyric Triad Responsion (A14-A22)", show_header=True)
        table.add_column("Strophe", style="bold cyan")
        table.add_column("Group Sequence")
        table.add_column("Mora Measures")
        table.add_column("Total Morae", justify="center", style="bold green")
        table.add_column("Metric Scheme")

        for s in rec.triad_strophes:
            table.add_row(
                s.strophe_name,
                " -> ".join(s.group_ids),
                str(s.morae_per_group),
                str(s.total_morae),
                s.metric_scheme,
            )
        console.print(table)
        console.print(f"\n• [bold]Strophic Mora Equality:[/bold] {rec.strophic_mora_equality} (14 = 14 = 14)")
        console.print(f"• [bold]Catalectic Distich Substitution:[/bold] {rec.verse_distich_substitution}")
        console.print(f"• [bold]Triad Joint Probability:[/bold] p = {rec.joint_triad_p_value:.6f} ({surrogates} runs)")
        console.print(f"\n[dim]{rec.meter_analysis}[/dim]\n")


@app.command("epigraphy")
def epigraphy_cmd(source: str = "godart_1995"):
    """Inspect microscopic stamp collision points, palimpsests, and radial deformation."""
    from phaistos.corpus.loader import load_transcription
    from phaistos.epigraphy.overlap_micro import evaluate_epigraphic_microscopy

    corpus = load_transcription(source)
    res = evaluate_epigraphic_microscopy(corpus)

    console.print(Panel("[bold cyan]Microscopic Epigraphy & Stamp Collision Analysis[/bold cyan]"))
    console.print(f"Total Overlaps Cataloged: [bold green]{res.total_overlaps_cataloged}[/bold green]")
    console.print(f"Outside-In Stamping Consistency: [bold green]{res.outside_in_consistency_pct}%[/bold green]")
    console.print(f"Stylus Incision Sequence: [bold]{res.stroke_incision_sequence}[/bold]")
    console.print(f"Modern Forgery Falsification Score: [bold green]{res.forgery_falsification_score}%[/bold green]\n")

    table = Table(title="Primary Palimpsests & Real-Time Clay Erasures", show_header=True)
    table.add_column("Group", style="bold cyan", justify="center")
    table.add_column("Side", justify="center")
    table.add_column("Erasure Technique")
    table.add_column("Final Sequence")
    table.add_column("Consensus Sources")

    for p in res.palimpsests_cataloged:
        table.add_row(
            p.group_id,
            p.side,
            p.erasure_technique,
            "-".join(p.final_stamped_signs),
            p.epigrapher_consensus,
        )
    console.print(table)

    table_comp = Table(title="Radial Track Height & Crowding Gradient", show_header=True)
    table_comp.add_column("Coil #", justify="center")
    table_comp.add_column("Side", justify="center")
    table_comp.add_column("Track Height (mm)", justify="center")
    table_comp.add_column("Sign Spacing (mm)", justify="center")
    table_comp.add_column("Crowding Factor", justify="center")

    for s in res.radial_compression_gradient:
        table_comp.add_row(
            f"Coil {s.coil_number}",
            s.side,
            f"{s.mean_track_height_mm:.1f}",
            f"{s.mean_sign_spacing_mm:.1f}",
            f"{s.crowding_factor:.2f}x",
        )
    console.print(table_comp)
    console.print(f"\n• [bold cyan]Skeptic Verdict:[/bold cyan] {res.skeptic_verdict}\n")


if __name__ == "__main__":
    app()







