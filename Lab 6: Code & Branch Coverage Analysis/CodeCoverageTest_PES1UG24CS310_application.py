"""
Lab 6: Code Coverage (line coverage) tests
Name: Omkar
SRN:  PES1UG24CS310
Application under test: blood_donation_screening.py

Goal: execute every line of the application at least once.

Run:
    coverage run -m pytest CodeCoverageTest_PES1UG24CS310_application.py
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



# process_donor_cohort


def test_single_accepted_donor():
    # Starter test from the repo: one healthy donor is collected.
    result = process_donor_cohort([make_cohort([HEALTHY])], 450)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


def test_invalid_cohort_list_raises_value_error():
    # Covers line 3: cohorts is not a list.
    with pytest.raises(ValueError, match="Invalid cohort list or volume"):
        process_donor_cohort("not a list", 450)


def test_unregistered_cohort_is_skipped():
    # Covers line 10: a cohort that is not clinic-registered is ignored.
    cohorts = [
        make_cohort([HEALTHY], registered=False),
        make_cohort([HEALTHY]),
    ]
    result = process_donor_cohort(cohorts, 450)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


def test_underage_donor_is_deferred():
    # Covers lines 21-22: age below 17 defers the donor.
    donors = [{"age": 16, "weight_kg": 60, "hb": 14.0}, HEALTHY]
    result = process_donor_cohort([make_cohort(donors)], 450)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


def test_low_hemoglobin_in_high_altitude_cohort_resets_and_stops():
    # Covers lines 25-28 and 41: low Hb in a high-altitude cohort wipes the
    # cohort's collection and stops screening, so nothing is collected.
    donors = [HEALTHY, {"age": 30, "weight_kg": 70, "hb": 11.0}, HEALTHY]
    result = process_donor_cohort(
        [make_cohort(donors, cohort_type="high_altitude")], 450
    )
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_high_hemoglobin_donor_is_deferred():
    # Covers lines 30-31: Hb above 18.0 defers the donor.
    donors = [{"age": 40, "weight_kg": 80, "hb": 19.0}, HEALTHY]
    result = process_donor_cohort([make_cohort(donors)], 450)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


def test_fast_track_cohort_adds_bonus_volume():
    # Covers line 36: a fast-track cohort adds 50 ml.
    result = process_donor_cohort([make_cohort([HEALTHY], fast_track=True)], 450)
    assert result == {"collected_ml": 500, "status": "ACCEPTED"}


def test_more_than_four_deferrals_gives_high_deferral():
    # Covers line 39: more than 4 deferred donors.
    underage = {"age": 15, "weight_kg": 60, "hb": 14.0}
    donors = [underage] * 5 + [HEALTHY]
    result = process_donor_cohort([make_cohort(donors)], 450)
    assert result == {"collected_ml": 450, "status": "HIGH_DEFERRAL"}


# verify_storage_centrifuge

def test_centrifuge_no_data():
    # Covers line 47: empty input.
    assert verify_storage_centrifuge([]) == "NO_DATA"


def test_centrifuge_two_consecutive_drops_abort():
    # Covers lines 49-57: a normal reading, then two drops below 3000 in a row.
    assert verify_storage_centrifuge([[3500, 2900, 2800]]) == "ABORT_SPIN"


def test_centrifuge_stable_run():
    # Covers line 58: every reading is at or above 3000.
    assert verify_storage_centrifuge([[3200, 3500, 3100]]) == "STABLE"
