"""The stage-3 partial-credit protocol, stated as tests.

Task 003 recorded that this protocol was undefined. These pin the four decisions it rests
on: project before scoring, keep the two tiers apart, score distinct pairs, and never
resolve a path.
"""

from __future__ import annotations

from caruca_v2.harness import methods
from caruca_v2.harness import trace_recovery as tr

SANDBOX = "/tmp/toplevel_abc/sandbox_xyz"


def traces(*pairs: tuple[str, str], invocation: str = "dirname relpath_1") -> list[dict]:
    """A `Traces` payload with one configuration carrying `pairs`."""
    return [
        {
            "command": {"name": invocation.split()[0], "body": []},
            "true_str": invocation,
            "configs": [
                {
                    "command": {
                        "name": invocation.split()[0],
                        "body": [{"flag": None, "args": [{"sandbox": SANDBOX}]}],
                    },
                    "return_code": 0,
                    "stdout": "",
                    "stderr": "",
                    "traces": [list(p) for p in pairs],
                }
            ],
        }
    ]


# --- the projection ------------------------------------------------------------------------


def test_reads_outside_the_sandbox_are_dropped_not_scored():
    """v1's raw traces are mostly loader noise: `dirname` is 640 pairs, 1 of them distinct.

    Scored raw, recall would be capped near 12% however perfectly the model observed.
    """
    projection = tr.project(
        [
            ["rf", "/usr/lib/aarch64-linux-gnu/libc.so.6"],
            ["rf", "/etc/ld.so.cache"],
            ["rf", f"{SANDBOX}/relpath_1"],
        ],
        SANDBOX,
    )
    assert projection.pairs == {("rf", "relpath_1")}
    assert projection.system_paths_excluded == 2


def test_writes_outside_the_sandbox_are_kept_as_v1_keeps_them():
    projection = tr.project([["wf", "/var/log/thing"]], SANDBOX)
    assert ("wf", "/var/log/thing") in projection.pairs


def test_writes_under_proc_and_to_null_devices_are_dropped():
    projection = tr.project(
        [["wf", "/proc/147/maps"], ["wf", "/dev/null"], ["wf", "/dev/zero"]], SANDBOX
    )
    assert projection.pairs == set()
    assert projection.null_device_writes_excluded == 2


def test_the_streams_survive_projection():
    projection = tr.project([["wf", "stdout"], ["rf", "stdin"], ["wf", "stderr"]], SANDBOX)
    assert projection.pairs == {("wf", "stdout"), ("rf", "stdin"), ("wf", "stderr")}


def test_a_jpg_suffix_is_stripped_as_v1_strips_it():
    """v1 appends `.jpg` in `File.__str__` for Content.IMAGE and removes it again here."""
    projection = tr.project([["rf", f"{SANDBOX}/pic.jpg"]], SANDBOX)
    assert projection.pairs == {("rf", "pic")}


def test_the_sandbox_root_itself_normalizes_to_dot():
    projection = tr.project([["rf", SANDBOX]], SANDBOX)
    assert projection.pairs == {("rf", ".")}


def test_a_live_pid_never_reaches_the_comparison():
    """`/proc/<PID>/maps` appears in every trace with whatever PID happened to run."""
    assert tr.normalize_path("/proc/147/maps", SANDBOX) == tr.normalize_path(
        "/proc/99999/maps", SANDBOX
    )


def test_paths_are_not_resolved():
    """Resolving is what makes v1's annotator unrunnable on macOS: /tmp -> /private/tmp.

    A sandbox-relative path must stay sandbox-relative regardless of what the local
    filesystem would resolve it to.
    """
    assert tr.normalize_path("/tmp/sandbox_outer/sandbox_inner/f", tr.PLACEHOLDER_SANDBOX) == "f"


def test_relative_system_paths_are_flagged_as_reference_leakage():
    """v1 itself records ('rf','etc') for `groups`, which ran with cwd `/`.

    Counted so reference noise stays visible instead of being charged to the model.
    """
    projection = tr.project([["rf", "etc"], ["rf", "usr"], ["rf", "myfile"]], SANDBOX)
    assert projection.suspected_reference_leakage == 2


# --- the two tiers ---------------------------------------------------------------------------


def test_core_and_inference_are_scored_apart():
    """Their ceilings differ by construction, so summing them measures the command's read
    count rather than the model's quality."""
    result = tr.compare_traces(
        traces(("ad", "made"), ("rf", "read")),
        traces(("ad", "made"), ("rf", "read"), ("rf", "missed")),
        command="dirname",
    )
    assert result["core"]["micro"]["recall"] == 1.0
    assert result["inference"]["micro"]["recall"] == 0.5
    assert "core" in result and "inference" in result
    assert "combined" not in result


def test_the_inference_tier_carries_its_caveat():
    result = tr.compare_traces(traces(("rf", "x")), traces(("rf", "x")), command="dirname")
    assert "not directly observable" in result["inference"]["caveat"]


def test_the_ceiling_fraction_is_core_recall_over_the_projected_set():
    result = tr.compare_traces(
        traces(("ad", "a")), traces(("ad", "a"), ("ad", "b")), command="dirname"
    )
    assert result["ceiling_fraction"] == 0.5
    assert result["ceiling_units"] == 2


def test_by_action_makes_the_predicted_split_falsifiable():
    result = tr.compare_traces(
        traces(("ad", "a"), ("rf", "r")),
        traces(("ad", "a"), ("rf", "r"), ("rf", "s")),
        command="dirname",
    )
    assert result["by_action"]["ad"] == {"tp": 1, "fp": 0, "fn": 0}
    assert result["by_action"]["rf"] == {"tp": 1, "fp": 0, "fn": 1}


# --- set, not multiset -----------------------------------------------------------------------


def test_a_repeated_open_is_one_fact_not_three():
    """strace records libc three times for one `arch` run; that is not three facts."""
    result = tr.compare_traces(
        traces(("rf", "f")),
        traces(("rf", "f"), ("rf", "f"), ("rf", "f")),
        command="arch",
    )
    assert result["inference"]["micro"]["recall"] == 1.0


# --- honesty ---------------------------------------------------------------------------------


def test_a_missing_reference_is_unavailable_rather_than_a_score_of_zero():
    """No scorer can synthesize v1's strace output; it has to be generated in Lima."""
    result = tr.compare_traces(traces(("ad", "x")), None, command="dirname")
    assert result["available"] is False
    assert "cannot be synthesized" in result["note"]


def test_configurations_with_no_counterpart_are_counted_apart_from_misses():
    result = tr.compare_traces(
        traces(("ad", "x"), invocation="dirname a"),
        traces(("ad", "x"), invocation="dirname b"),
        command="dirname",
    )
    assert result["configs"]["unpaired_produced"] == 1
    assert result["configs"]["unpaired_reference"] == 1
    assert result["configs"]["paired"] == 0


def test_the_record_names_its_method_and_its_projection_rule():
    result = tr.compare_traces(traces(("ad", "x")), traces(("ad", "x")), command="dirname")
    assert result["method"] == methods.TRACE_RECOVERY_DIFF.method
    assert "__readwrite" in result["projection"]["rule"]
    assert "multiset" in result["scoring_note"]


def test_self_test_passes_on_identity_and_under_a_pid_shift():
    payload = traces(("ad", "made"), ("rf", "read"), ("wf", "/proc/147/maps"))
    outcome = tr.self_test(payload, command="dirname")
    assert outcome["identity"]["passed"] is True
    assert outcome["pid_shifted"]["passed"] is True
