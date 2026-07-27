use mosef_arithmetic::{
    analyze_divisor_cover, batch_gcd, combined_promise_asymmetry, combined_promise_hit_count,
    combined_promise_signature, divisor_count, evaluate_addition_subtraction_program,
    evaluate_batch_product, evaluate_dyadic_telescope, evaluate_geometric_sum,
    evaluate_iterated_quotient, evaluate_lucas_separator_candidate,
    evaluate_multiplication_program, evaluate_nested_quotient, evaluate_product_dag,
    evaluate_quotient_linear_combination, evaluate_separator_candidate,
    evaluate_symmetric_quotient_difference, generic_multiplication_lower_bound, is_prime, lucas_v,
    mod_pow, perfect_power, pollard_p_minus_one, pollard_p_plus_one, pollard_rho,
    semismooth_factor, semismooth_successful_residue_count, trial_division, BatchProductEvaluation,
    CoverAnalysis, DyadicDivisionStatus, DyadicTelescopeEvaluation, GeometricDivisionStatus,
    GeometricSumEvaluation, IteratedQuotientEvaluation, LucasSeparatorOutcome,
    NestedQuotientEvaluation, ProductDagEvaluation, QuotientLinearCombinationEvaluation,
    SemismoothOutcome, SeparatorOutcome, SignedStraightLineEvaluation, StraightLineEvaluation,
    SymmetricQuotientDifferenceEvaluation,
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

fn parse_csv_i64(raw: String, name: &str) -> Result<Vec<i64>, String> {
    if raw.is_empty() {
        return Err(format!("{name} must be nonempty"));
    }
    raw.split(',')
        .map(|value| {
            value
                .parse::<i64>()
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

fn display_combined_signature(signature: &[(bool, bool)]) -> String {
    signature
        .iter()
        .map(|(minus, plus)| format!("{}{}", u8::from(*minus), u8::from(*plus)))
        .collect::<Vec<_>>()
        .join(",")
}

fn parse_steps(raw: String) -> Result<Vec<(usize, usize)>, String> {
    if raw.is_empty() {
        return Err("steps must be nonempty".to_owned());
    }
    raw.split(',')
        .map(|step| {
            let (left, right) = step
                .split_once(':')
                .ok_or_else(|| "each step must have left:right form".to_owned())?;
            Ok((
                left.parse::<usize>()
                    .map_err(|error| format!("invalid left parent: {error}"))?,
                right
                    .parse::<usize>()
                    .map_err(|error| format!("invalid right parent: {error}"))?,
            ))
        })
        .collect()
}

fn parse_signed_steps(raw: String) -> Result<Vec<(usize, usize, i8)>, String> {
    if raw.is_empty() {
        return Err("steps must be nonempty".to_owned());
    }
    raw.split(',')
        .map(|step| {
            let parts = step.split(':').collect::<Vec<_>>();
            if parts.len() != 3 {
                return Err("each signed step must have left:right:sign form".to_owned());
            }
            let sign = match parts[2] {
                "+" | "1" => 1,
                "-" | "-1" => -1,
                _ => return Err("signed step sign must be + or -".to_owned()),
            };
            Ok((
                parts[0]
                    .parse::<usize>()
                    .map_err(|error| format!("invalid left parent: {error}"))?,
                parts[1]
                    .parse::<usize>()
                    .map_err(|error| format!("invalid right parent: {error}"))?,
                sign,
            ))
        })
        .collect()
}

fn display_straight_line(evaluation: StraightLineEvaluation) -> String {
    let exponents = evaluation
        .exponents
        .iter()
        .map(u64::to_string)
        .collect::<Vec<_>>()
        .join(",");
    let residues = evaluation
        .residues
        .iter()
        .map(u64::to_string)
        .collect::<Vec<_>>()
        .join(",");
    format!("exponents:{exponents}|residues:{residues}")
}

fn display_signed_straight_line(evaluation: SignedStraightLineEvaluation) -> String {
    let exponents = evaluation
        .exponents
        .iter()
        .map(i128::to_string)
        .collect::<Vec<_>>()
        .join(",");
    let residues = evaluation
        .residues
        .iter()
        .map(u64::to_string)
        .collect::<Vec<_>>()
        .join(",");
    format!(
        "exponents:{exponents}|residues:{residues}|inversions:{}",
        evaluation.inversion_count
    )
}

fn display_batch_product(evaluation: BatchProductEvaluation) -> String {
    let leaves = evaluation
        .leaf_residues
        .iter()
        .map(u64::to_string)
        .collect::<Vec<_>>()
        .join(",");
    let leaf_gcds = evaluation
        .leaf_gcds
        .iter()
        .map(u64::to_string)
        .collect::<Vec<_>>()
        .join(",");
    format!(
        "leaves:{leaves}|root:{}|leaf_gcds:{leaf_gcds}|root_gcd:{}|multiplications:{}",
        evaluation.root_residue, evaluation.root_gcd, evaluation.multiplication_count
    )
}

fn display_product_dag(evaluation: ProductDagEvaluation) -> String {
    let nodes = evaluation
        .node_residues
        .iter()
        .map(u64::to_string)
        .collect::<Vec<_>>()
        .join(",");
    let gcds = evaluation
        .node_gcds
        .iter()
        .map(u64::to_string)
        .collect::<Vec<_>>()
        .join(",");
    let multiplicities = evaluation
        .multiplicities
        .iter()
        .map(|profile| {
            profile
                .iter()
                .map(u64::to_string)
                .collect::<Vec<_>>()
                .join(",")
        })
        .collect::<Vec<_>>()
        .join(";");
    let occurrences = evaluation
        .occurrence_counts
        .iter()
        .map(u64::to_string)
        .collect::<Vec<_>>()
        .join(",");
    format!("nodes:{nodes}|gcds:{gcds}|multiplicities:{multiplicities}|occurrences:{occurrences}")
}

fn display_dyadic_telescope(evaluation: DyadicTelescopeEvaluation) -> String {
    let powers = evaluation
        .power_residues
        .iter()
        .map(u64::to_string)
        .collect::<Vec<_>>()
        .join(",");
    let factors = evaluation
        .factor_residues
        .iter()
        .map(u64::to_string)
        .collect::<Vec<_>>()
        .join(",");
    let factor_gcds = evaluation
        .factor_gcds
        .iter()
        .map(u64::to_string)
        .collect::<Vec<_>>()
        .join(",");
    let status = match evaluation.division_status {
        DyadicDivisionStatus::Unit => "unit",
        DyadicDivisionStatus::ProperFactor => "proper_factor",
        DyadicDivisionStatus::FullCollision => "full_collision",
    };
    let division_quotient = evaluation
        .division_quotient
        .map_or_else(|| "none".to_owned(), |value| value.to_string());
    format!(
        "powers:{powers}|factors:{factors}|factor_gcds:{factor_gcds}|denominator:{}|\
denominator_gcd:{}|numerator:{}|numerator_gcd:{}|quotient:{}|quotient_gcd:{}|\
division_status:{status}|division_quotient:{division_quotient}|degree:{}|monomials:{}|\
squarings:{}|products:{}",
        evaluation.denominator_residue,
        evaluation.denominator_gcd,
        evaluation.numerator_residue,
        evaluation.numerator_gcd,
        evaluation.quotient_residue,
        evaluation.quotient_gcd,
        evaluation.formal_degree,
        evaluation.formal_monomial_count,
        evaluation.squaring_count,
        evaluation.product_multiplication_count,
    )
}

fn display_geometric_sum(evaluation: GeometricSumEvaluation) -> String {
    let status = match evaluation.division_status {
        GeometricDivisionStatus::Unit => "unit",
        GeometricDivisionStatus::ProperFactor => "proper_factor",
        GeometricDivisionStatus::FullCollision => "full_collision",
    };
    let division_quotient = evaluation
        .division_quotient
        .map_or_else(|| "none".to_owned(), |value| value.to_string());
    format!(
        "power:{}|sum:{}|denominator:{}|denominator_gcd:{}|numerator:{}|\
numerator_gcd:{}|sum_gcd:{}|exponent_gcd:{}|division_status:{status}|\
division_quotient:{division_quotient}|bit_length:{}|degree:{}|monomials:{}|\
multiplications:{}|additions:{}",
        evaluation.power_residue,
        evaluation.sum_residue,
        evaluation.denominator_residue,
        evaluation.denominator_gcd,
        evaluation.numerator_residue,
        evaluation.numerator_gcd,
        evaluation.sum_gcd,
        evaluation.exponent_gcd,
        evaluation.exponent_bit_length,
        evaluation.formal_degree,
        evaluation.formal_monomial_count,
        evaluation.multiplication_count,
        evaluation.addition_count,
    )
}

fn display_division_status(status: GeometricDivisionStatus) -> &'static str {
    match status {
        GeometricDivisionStatus::Unit => "unit",
        GeometricDivisionStatus::ProperFactor => "proper_factor",
        GeometricDivisionStatus::FullCollision => "full_collision",
    }
}

fn display_nested_quotient(value: NestedQuotientEvaluation) -> String {
    format!(
        "inner_power:{}|intermediate:{}|intermediate_gcd:{}|quotient:{}|quotient_gcd:{}|\
rational_numerator:{}|rational_numerator_gcd:{}|composed_denominator:{}|\
composed_denominator_gcd:{}|endpoint:{}|endpoint_gcd:{}|multiplier_gcd:{}|\
rational_status:{}|rational_quotient:{}|composed_status:{}|composed_quotient:{}",
        value.inner_power_residue,
        value.intermediate_residue,
        value.intermediate_gcd,
        value.quotient_residue,
        value.quotient_gcd,
        value.rational_numerator_residue,
        value.rational_numerator_gcd,
        value.composed_denominator_residue,
        value.composed_denominator_gcd,
        value.endpoint_residue,
        value.endpoint_gcd,
        value.multiplier_gcd,
        display_division_status(value.rational_division_status),
        value
            .rational_division_quotient
            .map_or_else(|| "none".to_owned(), |item| item.to_string()),
        display_division_status(value.composed_division_status),
        value
            .composed_division_quotient
            .map_or_else(|| "none".to_owned(), |item| item.to_string()),
    )
}

fn display_iterated_quotient(value: IteratedQuotientEvaluation) -> String {
    let prefixes = value
        .prefix_exponents
        .iter()
        .map(u64::to_string)
        .collect::<Vec<_>>()
        .join(",");
    let stages = value
        .stages
        .iter()
        .map(|stage| {
            format!(
                "{},{},{},{},{},{},{},{},{},{},{},{}",
                stage.inner_power_residue,
                stage.intermediate_residue,
                stage.intermediate_gcd,
                stage.quotient_residue,
                stage.quotient_gcd,
                stage.rational_numerator_residue,
                stage.rational_numerator_gcd,
                stage.composed_denominator_gcd,
                stage.endpoint_gcd,
                stage.multiplier_gcd,
                display_division_status(stage.rational_division_status),
                display_division_status(stage.composed_division_status),
            )
        })
        .collect::<Vec<_>>()
        .join(";");
    format!(
        "prefixes:{prefixes}|final_product:{}|final_prefix:{}|final_gcd:{}|stages:{stages}",
        value.final_quotient_product_residue, value.final_prefix_residue, value.final_prefix_gcd,
    )
}

fn display_quotient_linear_combination(value: QuotientLinearCombinationEvaluation) -> String {
    let join_u64 = |items: &[u64]| {
        items
            .iter()
            .map(u64::to_string)
            .collect::<Vec<_>>()
            .join(",")
    };
    let coefficients = value
        .coefficients
        .iter()
        .map(i64::to_string)
        .collect::<Vec<_>>()
        .join(",");
    let quotients = value
        .chain
        .stages
        .iter()
        .map(|stage| stage.quotient_residue)
        .collect::<Vec<_>>();
    let quotient_gcds = value
        .chain
        .stages
        .iter()
        .map(|stage| stage.quotient_gcd)
        .collect::<Vec<_>>();
    format!(
        concat!(
            "factors:{}|coefficients:{}|coefficient_residues:{}|",
            "coefficient_gcds:{}|quotients:{}|quotient_gcds:{}|weighted:{}|",
            "weighted_gcds:{}|aggregate:{}|aggregate_gcd:{}"
        ),
        join_u64(&value.chain.factors),
        coefficients,
        join_u64(&value.coefficient_residues),
        join_u64(&value.coefficient_gcds),
        join_u64(&quotients),
        join_u64(&quotient_gcds),
        join_u64(&value.weighted_stage_residues),
        join_u64(&value.weighted_stage_gcds),
        value.aggregate_residue,
        value.aggregate_gcd,
    )
}

fn display_symmetric_quotient_difference(value: SymmetricQuotientDifferenceEvaluation) -> String {
    format!(
        concat!(
            "exponent:{}|first_quotient:{}|second_quotient:{}|difference:{}|",
            "difference_gcd:{}|endpoint:{}|endpoint_gcd:{}|endpoint_status:{}|",
            "cofactor:{}|cofactor_gcd:{}|division_cofactor:{}|",
            "cofactor_monomials:{}|cofactor_degree:{}|matrix_multiplications:{}"
        ),
        value.exponent,
        value.first_quotient_residue,
        value.second_quotient_residue,
        value.difference_residue,
        value.difference_gcd,
        value.endpoint_residue,
        value.endpoint_gcd,
        display_division_status(value.endpoint_status),
        value.cofactor_residue,
        value.cofactor_gcd,
        value
            .division_cofactor
            .map_or_else(|| "none".to_owned(), |item| item.to_string()),
        value.cofactor_monomial_count,
        value.cofactor_degree,
        value.matrix_multiplication_count,
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
        "lucas-root-count-direct" => {
            let prime = parse_u64(arguments.next(), "prime")?;
            let exponent = parse_u64(arguments.next(), "exponent")?;
            if prime < 3 || prime % 2 == 0 || exponent == 0 {
                return Err("prime must be odd and exponent positive".to_owned());
            }
            (0..prime)
                .filter(|parameter| lucas_v(exponent, *parameter, prime) == Some(2 % prime))
                .count()
                .to_string()
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
        "combined-signature" => {
            let prime = parse_u64(arguments.next(), "prime")?;
            let exponents = parse_csv_u64(
                arguments
                    .next()
                    .ok_or_else(|| "missing exponents".to_owned())?,
                "exponents",
            )?;
            display_combined_signature(
                &combined_promise_signature(prime, &exponents)
                    .ok_or_else(|| "prime must be odd prime and exponents positive".to_owned())?,
            )
        }
        "combined-asymmetry" => {
            let left_prime = parse_u64(arguments.next(), "left_prime")?;
            let right_prime = parse_u64(arguments.next(), "right_prime")?;
            let exponents = parse_csv_u64(
                arguments
                    .next()
                    .ok_or_else(|| "missing exponents".to_owned())?,
                "exponents",
            )?;
            combined_promise_asymmetry(left_prime, right_prime, &exponents)
                .ok_or_else(|| "primes must be distinct odd primes".to_owned())?
                .to_string()
        }
        "combined-hit-count" => {
            let primes = parse_csv_u64(
                arguments
                    .next()
                    .ok_or_else(|| "missing primes".to_owned())?,
                "primes",
            )?;
            let exponents = parse_csv_u64(
                arguments
                    .next()
                    .ok_or_else(|| "missing exponents".to_owned())?,
                "exponents",
            )?;
            combined_promise_hit_count(&primes, &exponents)
                .ok_or_else(|| "primes must be odd primes and exponents positive".to_owned())?
                .to_string()
        }
        "divisor-count" => {
            let value = parse_u64(arguments.next(), "value")?;
            divisor_count(value)
                .ok_or_else(|| "value must be positive".to_owned())?
                .to_string()
        }
        "multiplication-program" => {
            let base = parse_u64(arguments.next(), "base")?;
            let modulus = parse_u64(arguments.next(), "modulus")?;
            let steps = parse_steps(arguments.next().ok_or_else(|| "missing steps".to_owned())?)?;
            display_straight_line(
                evaluate_multiplication_program(base, modulus, &steps).ok_or_else(|| {
                    "modulus must be at least two and parents must be earlier nodes".to_owned()
                })?,
            )
        }
        "addition-subtraction-program" => {
            let base = parse_u64(arguments.next(), "base")?;
            let modulus = parse_u64(arguments.next(), "modulus")?;
            let steps =
                parse_signed_steps(arguments.next().ok_or_else(|| "missing steps".to_owned())?)?;
            display_signed_straight_line(
                evaluate_addition_subtraction_program(base, modulus, &steps).ok_or_else(|| {
                    "base must be a unit, modulus at least two, signs valid, and parents earlier"
                        .to_owned()
                })?,
            )
        }
        "batch-product" => {
            let base = parse_u64(arguments.next(), "base")?;
            let modulus = parse_u64(arguments.next(), "modulus")?;
            let exponents = parse_csv_u64(
                arguments
                    .next()
                    .ok_or_else(|| "missing exponents".to_owned())?,
                "exponents",
            )?;
            display_batch_product(evaluate_batch_product(base, modulus, &exponents).ok_or_else(
                || {
                    "base must be a unit, modulus at least two, and exponents positive and increasing"
                        .to_owned()
                },
            )?)
        }
        "product-dag" => {
            let base = parse_u64(arguments.next(), "base")?;
            let modulus = parse_u64(arguments.next(), "modulus")?;
            let exponents = parse_csv_u64(
                arguments
                    .next()
                    .ok_or_else(|| "missing exponents".to_owned())?,
                "exponents",
            )?;
            let gates = parse_steps(arguments.next().ok_or_else(|| "missing gates".to_owned())?)?;
            display_product_dag(
                evaluate_product_dag(base, modulus, &exponents, &gates).ok_or_else(|| {
                    "base must be a unit, exponents positive and increasing, gates earlier, and multiplicities in range"
                        .to_owned()
                })?,
            )
        }
        "dyadic-telescope" => {
            let base = parse_u64(arguments.next(), "base")?;
            let modulus = parse_u64(arguments.next(), "modulus")?;
            let levels = u32::try_from(parse_u64(arguments.next(), "levels")?)
                .map_err(|_| "levels must fit in u32".to_owned())?;
            display_dyadic_telescope(evaluate_dyadic_telescope(base, modulus, levels).ok_or_else(
                || "base must be a unit, modulus at least two, and levels below 64".to_owned(),
            )?)
        }
        "geometric-sum" => {
            let base = parse_u64(arguments.next(), "base")?;
            let modulus = parse_u64(arguments.next(), "modulus")?;
            let exponent = parse_u64(arguments.next(), "exponent")?;
            display_geometric_sum(evaluate_geometric_sum(base, modulus, exponent).ok_or_else(
                || "base must be a unit, modulus at least two, and exponent positive".to_owned(),
            )?)
        }
        "nested-quotient" => {
            let base = parse_u64(arguments.next(), "base")?;
            let modulus = parse_u64(arguments.next(), "modulus")?;
            let inner_exponent = parse_u64(arguments.next(), "inner_exponent")?;
            let multiplier = parse_u64(arguments.next(), "multiplier")?;
            display_nested_quotient(
                evaluate_nested_quotient(base, modulus, inner_exponent, multiplier)
                    .ok_or_else(|| "invalid nested quotient or exponent overflow".to_owned())?,
            )
        }
        "iterated-quotient" => {
            let base = parse_u64(arguments.next(), "base")?;
            let modulus = parse_u64(arguments.next(), "modulus")?;
            let factors = parse_csv_u64(
                arguments
                    .next()
                    .ok_or_else(|| "missing factors".to_owned())?,
                "factors",
            )?;
            display_iterated_quotient(
                evaluate_iterated_quotient(base, modulus, &factors)
                    .ok_or_else(|| "invalid iterated quotient or exponent overflow".to_owned())?,
            )
        }
        "quotient-linear-combination" => {
            let base = parse_u64(arguments.next(), "base")?;
            let modulus = parse_u64(arguments.next(), "modulus")?;
            let factors = parse_csv_u64(
                arguments
                    .next()
                    .ok_or_else(|| "missing factors".to_owned())?,
                "factors",
            )?;
            let coefficients = parse_csv_i64(
                arguments
                    .next()
                    .ok_or_else(|| "missing coefficients".to_owned())?,
                "coefficients",
            )?;
            display_quotient_linear_combination(
                evaluate_quotient_linear_combination(base, modulus, &factors, &coefficients)
                    .ok_or_else(|| {
                        "invalid quotient linear combination or exponent overflow".to_owned()
                    })?,
            )
        }
        "symmetric-quotient-difference" => {
            let base = parse_u64(arguments.next(), "base")?;
            let modulus = parse_u64(arguments.next(), "modulus")?;
            let exponent = parse_u64(arguments.next(), "exponent")?;
            display_symmetric_quotient_difference(
                evaluate_symmetric_quotient_difference(base, modulus, exponent).ok_or_else(
                    || {
                        "base must be a unit, modulus at least two, and exponent at least two"
                            .to_owned()
                    },
                )?,
            )
        }
        "multiplication-lower-bound" => {
            let exponent = parse_u64(arguments.next(), "exponent")?;
            generic_multiplication_lower_bound(exponent)
                .ok_or_else(|| "exponent must be positive".to_owned())?
                .to_string()
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
