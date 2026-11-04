"""
Lab 6: Branch Coverage tests
Name: Omkar
SRN:  PES1UG24CS310
Application under test: blood_donation_screening.py

Goal: make every decision (if / for) take both of its outcomes, and test the
boundary values of each condition.

Run:
    coverage run --branch -m pytest BranchCoverageTest_PES1UG24CS310_application.py
    coverage report -m
"""
import pytest
from blood_donation_screening import process_donor_cohort, verify_storage_centrifuge


def make_cohort(donors, registered=True, cohort_type="standard", fast_track=False):
    """Build a cohort dict so each test only spells out what it cares about."""
    return {
        "clinic_registered": registered,
        "type": cohort_type,
        "fast_track": fast_track,
        "donors": donors,
    }


HEALTHY = {"age": 25, "weight_kg": 65, "hb": 14.0}


# process_donor_cohort: input validation (line 2)

@pytest.mark.parametrize(
    "cohorts, volume",
    [
        ("not a list", 450),     # cohorts is not a list
        ({"a": 1}, 450),         # dict is not a list either
        ([], 0),                 # volume is zero
        ([], -100),              # volume is negative
    ],
)
def test_invalid_input_raises_value_error(cohorts, volume):
    # Line 2 True: invalid list or non-positive volume.
    with pytest.raises(ValueError, match="Invalid cohort list or volume"):
        process_donor_cohort(cohorts, volume)


def test_empty_cohort_list_gives_zero_yield():
    # Line 2 False, then the cohort loop (line 8) runs zero times.
    assert process_donor_cohort([], 450) == {"collected_ml": 0, "status": "ZERO_YIELD"}


# process_donor_cohort: cohort-level decisions (lines 9, 15, 35)

def test_single_accepted_donor():
    # Starter test from the repo: the normal "happy path".
    result = process_donor_cohort([make_cohort([HEALTHY])], 450)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


def test_unregistered_cohort_is_skipped():
    # Line 9 True (skip) and False (process) in the same run.
    cohorts = [make_cohort([HEALTHY], registered=False), make_cohort([HEALTHY])]
    assert process_donor_cohort(cohorts, 450) == {"collected_ml": 450, "status": "ACCEPTED"}


def test_cohort_without_registration_key_is_skipped():
    # Line 9 default: a missing "clinic_registered" key counts as False.
    cohorts = [{"donors": [HEALTHY]}]
    assert process_donor_cohort(cohorts, 450) == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_cohort_with_defaults_only():
    # Missing "type", "fast_track" use their defaults ("standard", False).
    cohorts = [{"clinic_registered": True, "donors": [HEALTHY]}]
    assert process_donor_cohort(cohorts, 450) == {"collected_ml": 450, "status": "ACCEPTED"}


def test_registered_cohort_with_no_donors():
    # Donor loop (line 15) runs zero times; line 35 False.
    result = process_donor_cohort([make_cohort([])], 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_fast_track_cohort_adds_bonus_volume():
    # Line 35 True: a fast-track cohort adds 50 ml.
    result = process_donor_cohort([make_cohort([HEALTHY], fast_track=True)], 450)
    assert result == {"collected_ml": 500, "status": "ACCEPTED"}


def test_fast_track_cohort_with_no_donors_still_gets_bonus():
    # Line 35 True with an empty donor list: only the 50 ml bonus.
    result = process_donor_cohort([make_cohort([], fast_track=True)], 450)
    assert result == {"collected_ml": 50, "status": "ACCEPTED"}


def test_multiple_registered_cohorts_add_up():
    # Cohort loop iterates more than once and totals across cohorts.
    cohorts = [make_cohort([HEALTHY, HEALTHY]), make_cohort([HEALTHY], fast_track=True)]
    result = process_donor_cohort(cohorts, 450)
    assert result == {"collected_ml": 1400, "status": "ACCEPTED"}


# process_donor_cohort: donor eligibility (line 20)

@pytest.mark.parametrize(
    "donor",
    [
        {"age": 16, "weight_kg": 65, "hb": 14.0},   # under age
        {"age": 25, "weight_kg": 49, "hb": 14.0},   # under weight
        {"age": 16, "weight_kg": 49, "hb": 14.0},   # both
        {},                                         # all keys missing -> age 0
    ],
)
def test_ineligible_donor_is_deferred(donor):
    # Line 20 True: deferred, nothing collected.
    result = process_donor_cohort([make_cohort([donor])], 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_age_and_weight_boundaries_are_eligible():
    # Line 20 False at the exact limits: age 17 and weight 50 are allowed.
    donor = {"age": 17, "weight_kg": 50, "hb": 14.0}
    result = process_donor_cohort([make_cohort([donor])], 450)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


# process_donor_cohort: hemoglobin checks (lines 24, 26, 29)

def test_low_hemoglobin_in_standard_cohort_continues_screening():
    # Line 24 True, line 26 False: the donor is deferred but the loop goes on
    # and later donors are still collected.
    donors = [HEALTHY, {"age": 30, "weight_kg": 70, "hb": 11.0}, HEALTHY]
    result = process_donor_cohort([make_cohort(donors)], 450)
    assert result == {"collected_ml": 900, "status": "ACCEPTED"}


def test_low_hemoglobin_in_high_altitude_cohort_resets_and_stops():
    # Line 24 True, line 26 True: collection reset to 0 and the loop breaks,
    # so the healthy donor after it is never screened.
    donors = [HEALTHY, {"age": 30, "weight_kg": 70, "hb": 11.0}, HEALTHY]
    result = process_donor_cohort([make_cohort(donors, cohort_type="high_altitude")], 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_high_altitude_reset_also_wipes_earlier_cohorts():
    # The reset on line 27 sets the running total to 0, which also discards
    # what earlier cohorts collected. A later cohort can still add to it.
    cohorts = [
        make_cohort([HEALTHY]),
        make_cohort([{"age": 30, "weight_kg": 70, "hb": 10.0}], cohort_type="high_altitude"),
        make_cohort([HEALTHY]),
    ]
    result = process_donor_cohort(cohorts, 450)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


def test_high_altitude_cohort_with_normal_hemoglobin_collects():
    # high_altitude cohort where line 24 is always False: normal collection.
    result = process_donor_cohort([make_cohort([HEALTHY], cohort_type="high_altitude")], 450)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


def test_high_altitude_break_then_fast_track_bonus():
    # After the break on line 28, line 35 is still checked for the cohort.
    donors = [{"age": 30, "weight_kg": 70, "hb": 11.0}]
    result = process_donor_cohort(
        [make_cohort(donors, cohort_type="high_altitude", fast_track=True)], 450
    )
    assert result == {"collected_ml": 50, "status": "ACCEPTED"}


def test_high_hemoglobin_donor_is_deferred():
    # Line 29 True: Hb above 18.0 defers the donor.
    donors = [{"age": 40, "weight_kg": 80, "hb": 19.0}, HEALTHY]
    result = process_donor_cohort([make_cohort(donors)], 450)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


@pytest.mark.parametrize("hb", [12.5, 18.0])
def test_hemoglobin_boundaries_are_accepted(hb):
    # Lines 24 and 29 both False at the exact limits 12.5 and 18.0.
    donor = {"age": 30, "weight_kg": 70, "hb": hb}
    result = process_donor_cohort([make_cohort([donor])], 450)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


# process_donor_cohort: final status (lines 38, 40)

def test_more_than_four_deferrals_gives_high_deferral():
    # Line 38 True: 5 deferrals.
    underage = {"age": 15, "weight_kg": 60, "hb": 14.0}
    result = process_donor_cohort([make_cohort([underage] * 5 + [HEALTHY])], 450)
    assert result == {"collected_ml": 450, "status": "HIGH_DEFERRAL"}


def test_exactly_four_deferrals_is_not_high_deferral():
    # Line 38 False at the boundary: 4 deferrals is still allowed.
    underage = {"age": 15, "weight_kg": 60, "hb": 14.0}
    result = process_donor_cohort([make_cohort([underage] * 4 + [HEALTHY])], 450)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


def test_high_deferral_takes_priority_over_zero_yield():
    # Line 38 is checked before line 40: 5 deferrals and 0 ml -> HIGH_DEFERRAL.
    deferred = [
        {"age": 15, "weight_kg": 60, "hb": 14.0},
        {"age": 30, "weight_kg": 40, "hb": 14.0},
        {"age": 30, "weight_kg": 70, "hb": 11.0},
        {"age": 30, "weight_kg": 70, "hb": 19.0},
        {"age": 10, "weight_kg": 30, "hb": 14.0},
    ]
    result = process_donor_cohort([make_cohort(deferred)], 450)
    assert result == {"collected_ml": 0, "status": "HIGH_DEFERRAL"}


# verify_storage_centrifuge (lines 46, 49, 51, 52, 54)

def test_centrifuge_no_data_for_empty_list():
    # Line 46 True.
    assert verify_storage_centrifuge([]) == "NO_DATA"


def test_centrifuge_no_data_for_none():
    # Line 46 True for None as well.
    assert verify_storage_centrifuge(None) == "NO_DATA"


def test_centrifuge_two_consecutive_drops_abort():
    # Line 52 True twice in a row -> line 54 True.
    assert verify_storage_centrifuge([[3500, 2900, 2800]]) == "ABORT_SPIN"


def test_centrifuge_single_drop_then_recovery_is_stable():
    # Line 54 False (only one drop), then line 52 False resets the streak.
    assert verify_storage_centrifuge([[2900, 3500, 2800, 3100]]) == "STABLE"


def test_centrifuge_stable_run():
    # Line 52 always False; inner loop finishes normally.
    assert verify_storage_centrifuge([[3200, 3500, 3100]]) == "STABLE"


def test_centrifuge_rpm_3000_is_not_a_drop():
    # Boundary: exactly 3000 rpm is not below 3000.
    assert verify_storage_centrifuge([[3000, 3000, 3000]]) == "STABLE"


def test_centrifuge_empty_run_is_skipped():
    # Inner loop (line 51) runs zero times, outer loop moves to the next run.
    assert verify_storage_centrifuge([[], [3200]]) == "STABLE"


def test_centrifuge_streak_resets_between_runs():
    # A drop at the end of one run and the start of the next is NOT two in a
    # row, because rpm_drop_streak is reset on line 50 for every run.
    assert verify_storage_centrifuge([[3500, 2900], [2800, 3500]]) == "STABLE"


def test_centrifuge_abort_in_later_run():
    # Outer loop (line 49) continues past a stable run and aborts in the next.
    assert verify_storage_centrifuge([[3200, 3300], [2900, 2800]]) == "ABORT_SPIN"
