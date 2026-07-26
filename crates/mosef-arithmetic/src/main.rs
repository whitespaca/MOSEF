use mosef_arithmetic::{
    analyze_divisor_cover, batch_gcd, evaluate_lucas_separator_candidate,
    evaluate_separator_candidate, is_prime, mod_pow, perfect_power, pollard_p_minus_one,
    pollard_p_plus_one, pollard_rho, semismooth_factor, semismooth_successful_residue_count,
    trial_division, CoverAnalysis, LucasSeparatorOutcome, SemismoothOutcome, SeparatorOutcome,
};
use std::env;
use std::process::ExitCode;

fn parse_u64(value: Option<String>, name: &str) -> Result<u64, String> {
    value
        .ok_or_else(|| format!("missing {name}"))?
        .parse::<u64>()
        .map_err(|error| format!("invalid {name}: {error}"))
}

fn display_factor(factor: Option<u64>) -> String {
    factor.map_or_else(|| "none".to_owned(), |value| value.to_string())
}

fn display_separator(outcome: SeparatorOutcome) -> String {
    match outcome {
        SeparatorOutcome::DirectFactor(factor) => {
            format!("direct_factor|{factor}|none")
        }
        SeparatorOutcome::InvalidBase => "invalid_base|none|none".to_owned(),
        SeparatorOutcome::Miss { residue } => format!("miss|none|{residue}"),
        SeparatorOutcome::Factor { factor, residue } => {
            format!("factor|{factor}|{residue}")
        }
        SeparatorOutcome::SimultaneousCollision { residue } => {
            format!("simultaneous_collision|none|{residue}")
        }
    }
}

fn display_semismooth(outcome: SemismoothOutcome) -> String {
    match outcome {
        SemismoothOutcome::Factor(factor) => format!("factor:{factor}"),
        SemismoothOutcome::Unresolved => "unresolved".to_owned(),
        SemismoothOutcome::InvalidParameters => "invalid_parameters".to_owned(),
        SemismoothOutcome::ExponentOverflow => "exponent_overflow".to_owned(),
    }
}

fn display_lucas_separator(outcome: LucasSeparatorOutcome) -> String {
    match outcome {
        LucasSeparatorOutcome::DiscriminantFactor(factor) => {
            format!("discriminant_factor|{factor}|none")
        }
        LucasSeparatorOutcome::DegenerateMiss { residue } => {
            format!("degenerate_miss|none|{residue}")
        }
        LucasSeparatorOutcome::DegenerateFactor { factor, residue } => {
            format!("degenerate_factor|{factor}|{residue}")
        }
        LucasSeparatorOutcome::DegenerateCollision { residue } => {
            format!("degenerate_collision|none|{residue}")
        }
        LucasSeparatorOutcome::Miss { residue } => format!("miss|none|{residue}"),
        LucasSeparatorOutcome::Factor { factor, residue } => {
            format!("factor|{factor}|{residue}")
        }
        LucasSeparatorOutcome::SimultaneousCollision { residue } => {
            format!("simultaneous_collision|none|{residue}")
        }
    }
}

fn parse_csv_u64(raw: String, name: &str) -> Result<Vec<u64>, String> {
    if raw.is_empty() {
        return Err(format!("{name} must be nonempty"));
    }
    raw.split(',')
        .map(|value| {
            value
                .parse::<u64>()
                .map_err(|error| format!("invalid {name} value: {error}"))
        })
        .collect()
}

fn display_cover(analysis: CoverAnalysis) -> String {
    format!(
        "cover:{}|separates:{}|distinct:{}",
        analysis.divisor_cover, analysis.separates_profile, analysis.distinct_signatures
    )
}

fn run() -> Result<(), String> {
    let mut arguments = env::args().skip(1);
    let operation = arguments
        .next()
        .ok_or_else(|| "missing operation".to_owned())?;
    let output = match operation.as_str() {
        "mod-pow" => {
            let base = parse_u64(arguments.next(), "base")?;
            let exponent = parse_u64(arguments.next(), "exponent")?;
            let modulus = parse_u64(arguments.next(), "modulus")?;
            mod_pow(base, exponent, modulus)
                .ok_or_else(|| "modulus must be positive".to_owned())?
                .to_string()
        }
        "is-prime" => {
            let n = parse_u64(arguments.next(), "n")?;
            is_prime(n).to_string()
        }
        "trial-factor" => {
            let n = parse_u64(arguments.next(), "n")?;
            display_factor(trial_division(n))
        }
        "perfect-power" => {
            let n = parse_u64(arguments.next(), "n")?;
            perfect_power(n).map_or_else(
                || "none".to_owned(),
                |(base, exponent)| format!("{base}^{exponent}"),
            )
        }
        "rho" => {
            let n = parse_u64(arguments.next(), "n")?;
            let seed = parse_u64(arguments.next(), "seed")?;
            let max_steps = parse_u64(arguments.next(), "max_steps")?;
            display_factor(pollard_rho(n, seed, max_steps))
        }
        "p-minus-one" => {
            let n = parse_u64(arguments.next(), "n")?;
            let bound = parse_u64(arguments.next(), "bound")?;
            let base = parse_u64(arguments.next(), "base")?;
            display_factor(pollard_p_minus_one(n, bound, base))
        }
        "p-plus-one" => {
            let n = parse_u64(arguments.next(), "n")?;
            let bound = parse_u64(arguments.next(), "bound")?;
            let parameter = parse_u64(arguments.next(), "parameter")?;
            display_factor(pollard_p_plus_one(n, bound, parameter))
        }
        "batch-gcd" => {
            let modulus = parse_u64(arguments.next(), "modulus")?;
            let raw_values = arguments
                .next()
                .ok_or_else(|| "missing values".to_owned())?;
            let values = raw_values
                .split(',')
                .map(|value| {
                    value
                        .parse::<u64>()
                        .map_err(|error| format!("invalid batch value: {error}"))
                })
                .collect::<Result<Vec<_>, _>>()?;
            batch_gcd(&values, modulus)
                .ok_or_else(|| "modulus must be positive".to_owned())?
                .iter()
                .map(u64::to_string)
                .collect::<Vec<_>>()
                .join(",")
        }
        "separator" => {
            let n = parse_u64(arguments.next(), "n")?;
            let base = parse_u64(arguments.next(), "base")?;
            let exponent = parse_u64(arguments.next(), "exponent")?;
            display_separator(
                evaluate_separator_candidate(n, base, exponent).ok_or_else(|| {
                    "n must be at least 2 and exponent must be positive".to_owned()
                })?,
            )
        }
        "lucas-separator" => {
            let n = parse_u64(arguments.next(), "n")?;
            let parameter = parse_u64(arguments.next(), "parameter")?;
            let exponent = parse_u64(arguments.next(), "exponent")?;
            display_lucas_separator(
                evaluate_lucas_separator_candidate(n, parameter, exponent).ok_or_else(|| {
                    "n must be at least 2 and exponent must be positive".to_owned()
                })?,
            )
        }
        "semismooth" => {
            let n = parse_u64(arguments.next(), "n")?;
            let base_bound = parse_u64(arguments.next(), "base_bound")?;
            let smooth_bound = parse_u64(arguments.next(), "smooth_bound")?;
            let cofactor_bound = parse_u64(arguments.next(), "cofactor_bound")?;
            display_semismooth(semismooth_factor(
                n,
                base_bound,
                smooth_bound,
                cofactor_bound,
            ))
        }
        "semismooth-success-count" => {
            let n = parse_u64(arguments.next(), "n")?;
            let exponent = parse_u64(arguments.next(), "exponent")?;
            semismooth_successful_residue_count(n, exponent)
                .map(|value| value.to_string())
                .ok_or_else(|| "n must be at least 2 and exponent must be positive".to_owned())?
        }
        "cover-profile" => {
            let candidates = parse_csv_u64(
                arguments
                    .next()
                    .ok_or_else(|| "missing candidates".to_owned())?,
                "candidates",
            )?;
            let orders = parse_csv_u64(
                arguments
                    .next()
                    .ok_or_else(|| "missing orders".to_owned())?,
                "orders",
            )?;
            display_cover(analyze_divisor_cover(&candidates, &orders).ok_or_else(|| {
                "candidates must be positive and orders must contain two positive values".to_owned()
            })?)
        }
        _ => return Err(format!("unknown operation: {operation}")),
    };
    if arguments.next().is_some() {
        return Err("unexpected trailing arguments".to_owned());
    }
    println!("{output}");
    Ok(())
}

fn main() -> ExitCode {
    match run() {
        Ok(()) => ExitCode::SUCCESS,
        Err(error) => {
            eprintln!("ERROR: {error}");
            ExitCode::from(2)
        }
    }
}
