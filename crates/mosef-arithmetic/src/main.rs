use mosef_arithmetic::{
    batch_gcd, is_prime, mod_pow, perfect_power, pollard_p_minus_one, pollard_p_plus_one,
    pollard_rho, trial_division,
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
