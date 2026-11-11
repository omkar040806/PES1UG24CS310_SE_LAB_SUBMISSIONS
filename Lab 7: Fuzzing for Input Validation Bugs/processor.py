import math

VALID_ANTIGENS = {"A", "B", "AB", "O"}


def validate_blood_type(blood_code):
    """
    Standardizes blood group and Rh factor (e.g. 'O+', 'AB-').
    Returns an 'Invalid input' message instead of crashing on bad input.
    """
    # Fix 1: None / non-string input (was AttributeError on .strip())
    if not isinstance(blood_code, str):
        return "Invalid input: blood type must be a string"

    cleaned = blood_code.strip().upper()

    # Fix 2: empty or too short (was IndexError on cleaned[-1])
    if len(cleaned) < 2:
        return "Invalid input: blood type is too short"

    antigen = cleaned[:-1].strip()
    rh_char = cleaned[-1]
    rh_map = {"+": "Positive", "-": "Negative"}

    # Fix 3: last character is not + or - (was KeyError on rh_map[rh_char])
    if rh_char not in rh_map:
        return "Invalid input: Rh factor must be '+' or '-'"

    # Fix 4: unknown blood group like 'XYZ+' was silently accepted
    if antigen not in VALID_ANTIGENS:
        return "Invalid input: blood group must be A, B, AB or O"

    return f"{antigen} {rh_map[rh_char]}"


def calculate_pulse_pressure(bp_string):
    """
    Calculates pulse pressure (systolic - diastolic) and arterial ratio.
    Expects the format 'systolic/diastolic' (e.g. '120/80').
    Returns an 'Invalid input' message instead of crashing on bad input.
    """
    # Fix 1: None / non-string input (was AttributeError on .split())
    if not isinstance(bp_string, str):
        return "Invalid input: BP must be a string"

    # Fix 2: missing or extra '/' (was ValueError while unpacking)
    parts = bp_string.split('/')
    if len(parts) != 2:
        return "Invalid input: BP must be in the format systolic/diastolic"

    # Fix 3: non-numeric values (was ValueError from int())
    try:
        systolic = int(parts[0].strip())
        diastolic = int(parts[1].strip())
    except ValueError:
        return "Invalid input: systolic and diastolic must be whole numbers"

    # Fix 4: zero/negative diastolic (was ZeroDivisionError) and huge numbers
    # (OverflowError in the division) -> only allow realistic readings
    if not (1 <= systolic <= 300) or not (1 <= diastolic <= 200):
        return "Invalid input: BP values are out of the realistic range"

    # Fix 5: diastolic higher than systolic gave a negative pulse pressure
    if diastolic >= systolic:
        return "Invalid input: systolic must be greater than diastolic"

    pulse_diff = systolic - diastolic
    ratio = round(systolic / diastolic, 2)
    return f"Diff: {pulse_diff}, Ratio: {ratio}"


def parse_donor_registry(donor_entry):
    """
    Parses pipe-delimited record: 'DonorID|WeightKg|Hemoglobin'.
    Returns an 'Invalid input' message instead of crashing on bad input.
    """
    # Fix 1: None / non-string input (was AttributeError on .split())
    if not isinstance(donor_entry, str):
        return "Invalid input: record must be a string"

    # Fix 2: fewer than 3 fields (was IndexError), extra fields were ignored
    fields = donor_entry.split('|')
    if len(fields) != 3:
        return "Invalid input: record must be ID|Weight|Hemoglobin"

    # Fix 3: empty donor ID was accepted
    donor_id = fields[0].strip()
    if not donor_id:
        return "Invalid input: donor ID cannot be empty"

    # Fix 4: non-numeric weight/hemoglobin (was ValueError from float())
    try:
        weight = float(fields[1])
        hemoglobin = float(fields[2])
    except ValueError:
        return "Invalid input: weight and hemoglobin must be numbers"

    # Fix 5: 'nan' / 'inf' were accepted ('inf' even made a donor Eligible)
    if not math.isfinite(weight) or not math.isfinite(hemoglobin):
        return "Invalid input: weight and hemoglobin must be finite numbers"

    # Fix 6: negative or impossible values were accepted
    if not (0 < weight <= 300) or not (0 < hemoglobin <= 25):
        return "Invalid input: weight or hemoglobin is out of the realistic range"

    eligible = weight >= 50.0 and hemoglobin >= 12.5
    return f"Donor {donor_id}: {'Eligible' if eligible else 'Deferred'}"


def main():
    print("==== Running validate_blood_type ====")
    b_input = input("Enter blood type (e.g. A+, O-, AB+): ")
    print("Validated:", validate_blood_type(b_input))

    print("\n==== Running calculate_pulse_pressure ====")
    bp_input = input("Enter BP (e.g. 120/80): ")
    print("BP Metrics:", calculate_pulse_pressure(bp_input))

    print("\n==== Running parse_donor_registry ====")
    d_input = input("Enter record (ID|Weight|Hemoglobin): ")
    print("Status:", parse_donor_registry(d_input))


if __name__ == "__main__":
    main()