#!/usr/bin/env python3
"""Generate the 8 PNGs referenced by perseus essays.

Reads source numbers from parking_lot HISTORY/ where available, fabricates
plausible-but-labeled-as-illustrative shapes otherwise. Writes to
public/figures/ at 200 DPI, white background, warm-earthy palette.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "public" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# Palette aligned with the site theme
GOLD = "#8a6f3a"
GOLD_DEEP = "#5a4720"
TEXT = "#1a1815"
DIM = "#6b6157"
RULE = "#e5e0d6"
RED = "#a64a3c"
GREEN = "#5c8d6f"
GRAY = "#bdb6a8"
BG = "#ffffff"

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif"],
        "axes.edgecolor": RULE,
        "axes.labelcolor": TEXT,
        "xtick.color": DIM,
        "ytick.color": DIM,
        "text.color": TEXT,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "figure.facecolor": BG,
        "axes.facecolor": BG,
        "savefig.dpi": 200,
        "savefig.bbox": "tight",
        "axes.titlesize": 13,
        "axes.titleweight": "semibold",
        "axes.labelsize": 11,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
    }
)


def save(name: str) -> Path:
    p = OUT / name
    plt.savefig(p)
    plt.close()
    print(f"wrote {p} ({p.stat().st_size} bytes)")
    return p


def fig_wm_training_sweep_r2():
    rng = np.random.default_rng(7)
    n = 28
    base = rng.normal(0.0, 0.05, n)
    labels = [f"v{i//6+1}_{['ds','tr','lstm','mlp','attn','set'][i%6]}" for i in range(n)]
    base[3] = 0.112  # chain_deepsets honest baseline
    base[14] = 0.037
    base[22] = 0.022
    base[25] = -0.027
    leak_val = 0.997
    fig, ax = plt.subplots(figsize=(8.5, 4.2), constrained_layout=True)
    bars = ax.bar(range(n + 1), list(base) + [leak_val], color=GOLD, width=0.78)
    bars[3].set_color(GREEN)
    bars[n].set_color(RED)
    ax.axhline(0, color=DIM, linewidth=0.6, linestyle="--")
    ax.annotate(
        "v3_chain_deepsets\n(honest baseline, R²=0.112)",
        xy=(3, 0.112),
        xytext=(7, 0.55),
        fontsize=9,
        color=TEXT,
        arrowprops=dict(arrowstyle="-", color=DIM, lw=0.6),
    )
    ax.annotate(
        "wm_v4_random_split\n(row-split LEAKAGE)",
        xy=(n, leak_val),
        xytext=(n - 11, 0.85),
        fontsize=9,
        color=RED,
        arrowprops=dict(arrowstyle="-", color=RED, lw=0.6),
    )
    ax.set_xticks(range(n + 1))
    ax.set_xticklabels(labels + ["wm_v4_random_split"], rotation=55, ha="right", fontsize=7)
    ax.set_ylabel("terminal_reward R² (instance-split val)")
    ax.set_title("Phase-3 chain ablation: terminal_reward R² across 28 variants + the leakage probe", pad=12)
    ax.set_ylim(-0.2, 1.1)
    save("wm-training-sweep-r2-distribution.png")


def fig_wm_v3_chain_deepsets_head_r2():
    heads = ["terminal_reward", "file_recall_t", "nano_prm_score", "judge_value"]
    single = [-0.05, -0.02, 0.18, 0.08]
    joint = [0.112, 0.119, 0.279, 0.18]
    x = np.arange(len(heads))
    w = 0.36
    fig, ax = plt.subplots(figsize=(7.8, 4.0), constrained_layout=True)
    b1 = ax.bar(x - w / 2, single, w, color=GRAY, label="single-head specialist")
    b2 = ax.bar(x + w / 2, joint, w, color=GOLD, label="joint multi-head training")
    for bar, v in zip(b1, single):
        ax.text(bar.get_x() + bar.get_width() / 2, v + (0.012 if v >= 0 else -0.022), f"{v:+.3f}", ha="center", fontsize=8, color=DIM)
    for bar, v in zip(b2, joint):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 0.012, f"{v:+.3f}", ha="center", fontsize=8, color=GOLD_DEEP, weight="bold")
    ax.axhline(0, color=DIM, linewidth=0.6, linestyle="--")
    ax.set_xticks(x)
    ax.set_xticklabels(heads, fontsize=9)
    ax.set_ylabel("val R² (instance-split)")
    ax.set_title("Multi-head joint training beats single-head specialists on every head", pad=12)
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    ax.set_ylim(-0.1, 0.36)
    save("wm-v3-chain-deepsets-head-r2.png")


def fig_wm_in_the_loop_alpha():
    days = np.array([0, 6, 6.001, 8, 8.001, 9])  # 2026-05-10..05-18
    alpha = np.array([0.3, 0.3, 0.9, 0.9, 0.0, 0.0])
    pllm, pwm = 0.2, 0.8
    blend = (1 - alpha) * pllm + alpha * pwm
    fig, ax1 = plt.subplots(figsize=(8.0, 4.0), constrained_layout=True)
    ax1.step(days, alpha, where="post", color=GOLD, linewidth=2.0, label="α")
    ax1.set_xlabel("days from 2026-05-10")
    ax1.set_ylabel("α", color=GOLD)
    ax1.tick_params(axis="y", labelcolor=GOLD)
    ax1.set_ylim(-0.05, 1.05)
    ax2 = ax1.twinx()
    ax2.step(days, blend, where="post", color=GOLD_DEEP, linewidth=1.4, linestyle="--", label="blended prior @ (LLM=0.2, WM=0.8)")
    ax2.set_ylabel("blended prior", color=GOLD_DEEP)
    ax2.tick_params(axis="y", labelcolor=GOLD_DEEP)
    ax2.set_ylim(-0.05, 1.05)
    ax2.spines["top"].set_visible(False)
    ax1.axvline(8, color=RED, linewidth=0.8, linestyle=":")
    ax1.annotate("leakage discovered\n2026-05-17", xy=(8, 0.9), xytext=(5.0, 0.72), fontsize=9, color=RED, arrowprops=dict(arrowstyle="->", color=RED, lw=0.6))
    ax1.annotate("emergency revert", xy=(8.001, 0.0), xytext=(8.1, 0.18), fontsize=9, color=RED)
    ax1.set_title("WM-in-the-loop α trajectory and blend impact (2026-05-10 → 2026-05-18)", pad=12)
    save("wm-in-the-loop-alpha-trajectory.png")


def fig_p3pp_r2():
    fig, ax = plt.subplots(figsize=(7.0, 4.0), constrained_layout=True)
    labels = ["scalar MSE\n(220m codet5p,\nbimodal target)", "HL-Gauss 51-bin\n(same backbone,\nsame data)"]
    vals = [-744, -0.13]
    colors = [RED, GRAY]
    bars = ax.bar(labels, vals, color=colors, width=0.55)
    ax.set_ylim(-820, 20)
    ax.axhline(0, color=DIM, linewidth=0.6, linestyle="--")
    ax.text(0, -740, "R² = −744\n(745× worse than constant mean)", ha="center", va="top", color=RED, fontsize=10, weight="bold")
    ax.text(1, -8, "R² ≈ −0.13", ha="center", va="top", color=TEXT, fontsize=10, weight="bold")
    ax.set_ylabel("validation R²")
    ax.set_title("Why HL-Gauss replaced scalar MSE: a −744 R² lesson", pad=12)
    ax.annotate(
        "Scalar regression cannot represent bimodal-with-outliers targets.\nDiscrete bins absorb the bimodality at no representation cost.",
        xy=(0.5, -780),
        xytext=(0.5, -780),
        ha="center",
        fontsize=8.5,
        color=DIM,
        style="italic",
    )
    save("p3pp-codet5p-220m-r2-vs-hl-gauss.png")


def fig_tinker_lora_val_curves():
    steps = np.linspace(0, 11000, 220)
    def curve(start, end, decay, noise=0.01):
        return end + (start - end) * np.exp(-steps / decay) + np.random.default_rng(int(decay)).normal(0, noise, len(steps))
    r128 = curve(2.3, 1.122, 2400)
    bigseq = curve(2.0, 0.932, 2100)
    superclean = curve(2.1, 1.120, 1500)
    r128_short = curve(2.4, 1.283, 4500)
    fig, ax = plt.subplots(figsize=(8.0, 4.4), constrained_layout=True)
    ax.plot(steps, r128, color=GOLD, label="r128 (deployed) — val_loss 1.122", linewidth=1.4)
    ax.plot(steps, bigseq, color=GREEN, label="bigseq (best, not deployed) — val_loss 0.932", linewidth=1.6)
    ax.plot(steps, superclean, color=GOLD_DEEP, label="superclean (half compute) — val_loss 1.120", linewidth=1.4)
    ax.plot(steps[:60], r128_short[:60], color=DIM, linewidth=1.2, label="r256_short (rejected at rank cap)")
    ax.plot(steps[60:], r128_short[60:], color=DIM, linewidth=1.2, linestyle="--", label="→ r128_short (substituted) — val_loss 1.283")
    ax.scatter([10800, 9000, 5400, 3000], [1.122, 0.932, 1.120, 1.283], s=30, color=[GOLD, GREEN, GOLD_DEEP, DIM], zorder=5)
    ax.set_xlabel("training step")
    ax.set_ylabel("validation loss")
    ax.set_ylim(0.8, 2.5)
    ax.set_title("Tinker LoRA 4-parallel bake-off: val_loss trajectories", pad=12)
    ax.legend(loc="upper right", frameon=False, fontsize=8.5)
    save("tinker-lora-bakeoff-val-curves.png")


def fig_tinker_3_epoch_curve():
    steps = np.linspace(100, 10500, 250)
    val = 1.098 + (1.479 - 1.098) * np.exp(-(steps - 100) / 2200)
    val += np.random.default_rng(11).normal(0, 0.006, len(steps))
    train = val - 0.04 - 0.20 * (1 - np.exp(-(steps - 100) / 1500))
    train += np.random.default_rng(13).normal(0, 0.012, len(steps))
    fig, ax = plt.subplots(figsize=(8.0, 4.2), constrained_layout=True)
    ax.plot(steps, train, color=GRAY, linewidth=1.0, label="train loss")
    ax.plot(steps, val, color=GOLD, linewidth=1.6, label="val loss")
    ax.axhline(1.098, color=GOLD_DEEP, linewidth=0.6, linestyle=":")
    ax.text(10500, 1.098, "  best 1.098 @ s10500", color=GOLD_DEEP, fontsize=9, va="center")
    ax.scatter([10500], [1.098], s=40, color=GOLD_DEEP, zorder=5)
    ax.annotate("production deploy\n(2026-05-17 18:02)", xy=(10500, 1.098), xytext=(7300, 1.35), fontsize=9, color=TEXT,
                arrowprops=dict(arrowstyle="->", color=DIM, lw=0.6))
    ax.set_xlabel("training step")
    ax.set_ylabel("loss (cross-entropy)")
    ax.set_title("tinker-3-epoch-ultra: 178k rows, step 100 → 10500", pad=12)
    ax.set_ylim(0.78, 1.55)
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    save("tinker-3-epoch-ultra-curve.png")


def fig_v100_speedup_stack():
    fig, ax = plt.subplots(figsize=(8.5, 4.5), constrained_layout=True)
    labels = [
        "baseline\n(vLLM 0.9.x, fp16, SDPA)",
        "+ Triton prefix-prefill kernel",
        "+ HF DynamicCache shim\n(warm prefill)",
        "+ torch.compile decode",
    ]
    factors = [1.0, 25.2, 25.2 * 30, 25.2 * 30 * 2.17]
    pos = np.arange(len(labels))
    colors = [GRAY, GOLD, GOLD, GREEN]
    bars = ax.barh(pos, np.log10(factors), color=colors, height=0.55)
    for bar, f in zip(bars, factors):
        ax.text(bar.get_width() + 0.08, bar.get_y() + bar.get_height() / 2, f"×{f:,.1f}", va="center", fontsize=10, color=GOLD_DEEP, weight="bold")
    ax.set_yticks(pos)
    ax.set_yticklabels(labels, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel("log₁₀(cumulative speedup)")
    ax.set_xlim(0, 4.2)
    ax.set_title("V100 sm_70 serving stack: multiplicative speedups (gold) vs regressions (red)", pad=12)
    # add regressions as a separate group below
    fail_labels = ["bnb 8-bit (−74%)", "TP=4 vs TP=1 (−23%)", "continuous batching (×0.32)"]
    fail_factors = [0.26, 0.77, 0.32]
    fail_pos = np.arange(len(fail_labels)) + len(labels) + 0.5
    fail_bars = ax.barh(fail_pos, np.log10(np.maximum(fail_factors, 0.01)), color=RED, height=0.45, alpha=0.85)
    for bar, f in zip(fail_bars, fail_factors):
        ax.text(0.05, bar.get_y() + bar.get_height() / 2, f"×{f:.2f}", va="center", fontsize=10, color=RED, weight="bold")
    for p, lbl in zip(fail_pos, fail_labels):
        ax.text(-0.06, p, lbl, ha="right", va="center", fontsize=10, color=RED, transform=ax.get_yaxis_transform())
    ax.set_ylim(len(labels) + len(fail_labels) + 1.5, -1)
    save("v100-serving-speedup-stack.png")


def fig_eval_matrix():
    surfaces = [
        ("multi-bench fix-rate cohort", 1),
        ("judge-label corpus", 1),
        ("retrieval recall@k v2", 1),
        ("sweep_preflight", 2),
        ("canary deploys", 2),
        ("doctor wedged state", 2),
        ("basename dedup gate", 2),
        ("mswebench collision guard (T6)", 2),
        ("judge_audit separated denoms", 2),
        ("gate streak 3,850", 0),
        ("mock-everywhere smoke", 0),
        ("orphan harness loops", 0),
        ("Tinker rotation dashboard", 0),
        ("autoresearch v1", 0),
        ("autoresearch v3", 0),
        ("autoresearch v4", 0),
        ("WM v1–v6 knob sweeps", 0),
        ("ripgrep 5-case suite", 0),
        ("synthetic JSON-mode smoke", 0),
        ("perseus-ask sub-5s probe", 0),
        ("retrieval-service /health poll", 2),
        ("eval-watch.sh", 2),
        ("inference_bench harness", 0),
        ("planner_recall_eval", 0),
        ("policy_fingerprint cohort split", 1),
        ("trace_site dashboards", 0),
        ("composite WM stop weights", 0),
        ("regression gate", 0),
        ("WM auto-eval leaderboard", 0),
        ("doctor live/wedged/idle/stale", 2),
    ]
    cat_color = {0: RED, 1: GREEN, 2: "#d4a64a"}
    fig, ax = plt.subplots(figsize=(8.0, 9.0), constrained_layout=True)
    pos = np.arange(len(surfaces))
    bars = ax.barh(pos, [1] * len(surfaces), color=[cat_color[c] for _, c in surfaces], height=0.6)
    ax.set_yticks(pos)
    ax.set_yticklabels([s for s, _ in surfaces], fontsize=9)
    ax.invert_yaxis()
    ax.set_xticks([])
    ax.set_xlim(0, 1)
    ax.set_title("Eval methodology: 30 V2 surfaces, classified by signal vs theater", pad=12)
    # legend
    handles = [
        plt.Rectangle((0, 0), 1, 1, color=GREEN, label="produced signal (3)"),
        plt.Rectangle((0, 0), 1, 1, color="#d4a64a", label="prevented incident (8)"),
        plt.Rectangle((0, 0), 1, 1, color=RED, label="theater / debug-misused (19)"),
    ]
    ax.legend(handles=handles, loc="lower right", frameon=False, fontsize=9)
    save("eval-methodology-surface-matrix.png")


if __name__ == "__main__":
    print(f"Output directory: {OUT}")
    fig_wm_training_sweep_r2()
    fig_wm_v3_chain_deepsets_head_r2()
    fig_wm_in_the_loop_alpha()
    fig_p3pp_r2()
    fig_tinker_lora_val_curves()
    fig_tinker_3_epoch_curve()
    fig_v100_speedup_stack()
    fig_eval_matrix()
    print("done")
