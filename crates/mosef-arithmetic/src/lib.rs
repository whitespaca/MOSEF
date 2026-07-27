//! Correctness-first `u64` factorization primitives.
//!
//! Multiplications modulo a `u64` modulus are widened to `u128`. These routines
//! are finite-range research baselines and make no polynomial-time claim in the
//! binary input length.

/// Return `base^exponent mod modulus` using widened multiplication.
pub fn mod_pow(base: u64, mut exponent: u64, modulus: u64) -> Option<u64> {
    if modulus == 0 {
        return None;
    }
    let mut result = 1 % modulus;
    let mut factor = base % modulus;
    while exponent > 0 {
        if exponent & 1 == 1 {
            result = mul_mod(result, factor, modulus);
        }
        factor = mul_mod(factor, factor, modulus);
        exponent >>= 1;
    }
    Some(result)
}

fn mul_mod(left: u64, right: u64, modulus: u64) -> u64 {
    ((left as u128 * right as u128) % modulus as u128) as u64
}

fn add_mod(left: u64, right: u64, modulus: u64) -> u64 {
    ((left as u128 + right as u128) % modulus as u128) as u64
}

/// Return the least prime factor of composite `n`, or `None`.
pub fn trial_division(n: u64) -> Option<u64> {
    if n < 2 {
        return None;
    }
    if n % 2 == 0 {
        return (n != 2).then_some(2);
    }
    let mut divisor = 3;
    while divisor <= n / divisor {
        if n % divisor == 0 {
            return Some(divisor);
        }
        divisor += 2;
    }
    None
}

/// Deterministically decide primality by trial division.
pub fn is_prime(n: u64) -> bool {
    n >= 2 && trial_division(n).is_none()
}

fn power_compare(base: u64, exponent: u32, limit: u64) -> std::cmp::Ordering {
    let mut value = 1_u64;
    for _ in 0..exponent {
        if value > limit / base {
            return std::cmp::Ordering::Greater;
        }
        value *= base;
    }
    value.cmp(&limit)
}

fn integer_nth_root(n: u64, exponent: u32) -> u64 {
    let mut low = 1_u64;
    let mut high = n;
    while low <= high {
        let middle = low + (high - low) / 2;
        match power_compare(middle, exponent, n) {
            std::cmp::Ordering::Greater => high = middle - 1,
            _ => low = middle + 1,
        }
    }
    high
}

/// Return `(base, maximal exponent)` when `n` is a perfect power.
pub fn perfect_power(n: u64) -> Option<(u64, u32)> {
    if n < 4 {
        return None;
    }
    for exponent in (2..=n.ilog2() + 1).rev() {
        let root = integer_nth_root(n, exponent);
        if root >= 2 && power_compare(root, exponent, n) == std::cmp::Ordering::Equal {
            return Some((root, exponent));
        }
    }
    None
}

fn gcd(mut left: u64, mut right: u64) -> u64 {
    while right != 0 {
        (left, right) = (right, left % right);
    }
    left
}

/// Exhaustive terminal outcomes for one multiplicative separator candidate.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SeparatorOutcome {
    DirectFactor(u64),
    InvalidBase,
    Miss { residue: u64 },
    Factor { factor: u64, residue: u64 },
    SimultaneousCollision { residue: u64 },
}

/// Evaluate one `gcd(g^d - 1, n)` candidate with explicit base-GCD branches.
pub fn evaluate_separator_candidate(n: u64, g: u64, d: u64) -> Option<SeparatorOutcome> {
    if n < 2 || d == 0 {
        return None;
    }
    let reduced_base = g % n;
    let base_gcd = gcd(reduced_base, n);
    if base_gcd > 1 && base_gcd < n {
        return Some(SeparatorOutcome::DirectFactor(base_gcd));
    }
    if base_gcd == n {
        return Some(SeparatorOutcome::InvalidBase);
    }
    let residue = mod_pow(reduced_base, d, n)?;
    let candidate_gcd = gcd(residue - 1, n);
    if candidate_gcd == 1 {
        Some(SeparatorOutcome::Miss { residue })
    } else if candidate_gcd == n {
        Some(SeparatorOutcome::SimultaneousCollision { residue })
    } else {
        Some(SeparatorOutcome::Factor {
            factor: candidate_gcd,
            residue,
        })
    }
}

/// Exhaustive terminal outcomes for one Lucas `V_d(P, 1) - 2` candidate.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum LucasSeparatorOutcome {
    DiscriminantFactor(u64),
    DegenerateMiss { residue: u64 },
    DegenerateFactor { factor: u64, residue: u64 },
    DegenerateCollision { residue: u64 },
    Miss { residue: u64 },
    Factor { factor: u64, residue: u64 },
    SimultaneousCollision { residue: u64 },
}

/// Evaluate one Lucas candidate after checking `gcd(P^2 - 4, n)`.
pub fn evaluate_lucas_separator_candidate(
    n: u64,
    parameter: u64,
    exponent: u64,
) -> Option<LucasSeparatorOutcome> {
    if n < 2 || exponent == 0 {
        return None;
    }
    let reduced_parameter = parameter % n;
    let square = mul_mod(reduced_parameter, reduced_parameter, n);
    let four = 4 % n;
    let discriminant = ((square as u128 + n as u128 - four as u128) % n as u128) as u64;
    let discriminant_gcd = gcd(discriminant, n);
    if discriminant_gcd > 1 && discriminant_gcd < n {
        return Some(LucasSeparatorOutcome::DiscriminantFactor(discriminant_gcd));
    }
    let residue = lucas_v(exponent, reduced_parameter, n)?;
    let two = 2 % n;
    let difference = ((residue as u128 + n as u128 - two as u128) % n as u128) as u64;
    let candidate_gcd = gcd(difference, n);
    if discriminant_gcd == n && candidate_gcd == 1 {
        Some(LucasSeparatorOutcome::DegenerateMiss { residue })
    } else if discriminant_gcd == n && candidate_gcd == n {
        Some(LucasSeparatorOutcome::DegenerateCollision { residue })
    } else if discriminant_gcd == n {
        Some(LucasSeparatorOutcome::DegenerateFactor {
            factor: candidate_gcd,
            residue,
        })
    } else if candidate_gcd == 1 {
        Some(LucasSeparatorOutcome::Miss { residue })
    } else if candidate_gcd == n {
        Some(LucasSeparatorOutcome::SimultaneousCollision { residue })
    } else {
        Some(LucasSeparatorOutcome::Factor {
            factor: candidate_gcd,
            residue,
        })
    }
}

fn primes_up_to(bound: u64) -> Vec<u64> {
    let mut primes = Vec::new();
    for candidate in 2..=bound {
        if primes
            .iter()
            .take_while(|prime| **prime <= candidate / **prime)
            .all(|prime| candidate % prime != 0)
        {
            primes.push(candidate);
        }
    }
    primes
}

fn prime_power_at_most(prime: u64, bound: u64) -> u64 {
    let mut power = prime;
    while power <= bound / prime {
        power *= prime;
    }
    power
}

fn stage_one_exponent(bound: u64) -> Option<u64> {
    primes_up_to(bound)
        .into_iter()
        .try_fold(1_u64, |value, prime| {
            value.checked_mul(prime_power_at_most(prime, bound))
        })
}

/// Terminal outcomes for the bounded M3 semismooth family.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SemismoothOutcome {
    Factor(u64),
    Unresolved,
    InvalidParameters,
    ExponentOverflow,
}

/// Try bases `2..=A` and exponents `t*lcm(1..=B)` for `1..=R`.
pub fn semismooth_factor(
    n: u64,
    base_bound: u64,
    smooth_bound: u64,
    cofactor_bound: u64,
) -> SemismoothOutcome {
    if n < 2 || base_bound < 2 || smooth_bound < 1 || cofactor_bound < 1 {
        return SemismoothOutcome::InvalidParameters;
    }
    let Some(stage_exponent) = stage_one_exponent(smooth_bound) else {
        return SemismoothOutcome::ExponentOverflow;
    };
    if stage_exponent.checked_mul(cofactor_bound).is_none() {
        return SemismoothOutcome::ExponentOverflow;
    }
    for base in 2..=base_bound.min(n - 1) {
        for multiplier in 1..=cofactor_bound {
            let exponent = stage_exponent * multiplier;
            match evaluate_separator_candidate(n, base, exponent) {
                Some(SeparatorOutcome::DirectFactor(factor))
                | Some(SeparatorOutcome::Factor { factor, .. }) => {
                    return SemismoothOutcome::Factor(factor);
                }
                Some(
                    SeparatorOutcome::InvalidBase
                    | SeparatorOutcome::Miss { .. }
                    | SeparatorOutcome::SimultaneousCollision { .. },
                ) => {}
                None => return SemismoothOutcome::InvalidParameters,
            }
        }
    }
    SemismoothOutcome::Unresolved
}

/// Count successful residues for one M3 exponent by exhaustive enumeration.
///
/// This finite oracle is for registered small vectors, not the factoring
/// algorithm or a polynomial-time promise recognizer.
pub fn semismooth_successful_residue_count(n: u64, exponent: u64) -> Option<u64> {
    if n < 2 || exponent < 1 {
        return None;
    }
    let mut count = 0;
    for base in 0..n {
        let base_gcd = gcd(base, n);
        let success = if base_gcd > 1 && base_gcd < n {
            true
        } else if base_gcd == n {
            false
        } else {
            let residue = mod_pow(base, exponent, n)?;
            let factor = gcd(residue - 1, n);
            factor > 1 && factor < n
        };
        if success {
            count += 1;
        }
    }
    Some(count)
}

/// Run deterministic Pollard p-1 stage 1.
pub fn pollard_p_minus_one(n: u64, bound: u64, base: u64) -> Option<u64> {
    if n < 4 || bound < 2 {
        return None;
    }
    let initial_gcd = gcd(base, n);
    if initial_gcd > 1 && initial_gcd < n {
        return Some(initial_gcd);
    }
    if initial_gcd == n {
        return None;
    }
    let mut residue = base % n;
    for prime in primes_up_to(bound) {
        residue = mod_pow(residue, prime_power_at_most(prime, bound), n)?;
    }
    let difference = residue.abs_diff(1);
    let factor = gcd(difference, n);
    (factor > 1 && factor < n).then_some(factor)
}

type Matrix2 = [[u64; 2]; 2];

fn matrix_multiply(left: Matrix2, right: Matrix2, modulus: u64) -> Matrix2 {
    let entry = |row: usize, column: usize| {
        let first = left[row][0] as u128 * right[0][column] as u128;
        let second = left[row][1] as u128 * right[1][column] as u128;
        (((first % modulus as u128) + (second % modulus as u128)) % modulus as u128) as u64
    };
    [[entry(0, 0), entry(0, 1)], [entry(1, 0), entry(1, 1)]]
}

/// Return `V_index(parameter, 1) mod modulus`.
pub fn lucas_v(index: u64, parameter: u64, modulus: u64) -> Option<u64> {
    if modulus == 0 {
        return None;
    }
    let mut result = [[1 % modulus, 0], [0, 1 % modulus]];
    let mut factor = [
        [parameter % modulus, modulus.wrapping_sub(1) % modulus],
        [1 % modulus, 0],
    ];
    let mut remaining = index;
    while remaining > 0 {
        if remaining & 1 == 1 {
            result = matrix_multiply(result, factor, modulus);
        }
        factor = matrix_multiply(factor, factor, modulus);
        remaining >>= 1;
    }
    Some(add_mod(result[0][0], result[1][1], modulus))
}

/// Run a scoped Williams-style p+1 stage 1 with `Q = 1`.
pub fn pollard_p_plus_one(n: u64, bound: u64, parameter: u64) -> Option<u64> {
    if n < 4 || bound < 2 {
        return None;
    }
    let square = parameter as u128 * parameter as u128;
    let discriminant = square.abs_diff(4) % n as u128;
    let discriminant_gcd = gcd(discriminant as u64, n);
    if discriminant_gcd > 1 && discriminant_gcd < n {
        return Some(discriminant_gcd);
    }
    if discriminant_gcd == n {
        return None;
    }
    let exponent = stage_one_exponent(bound)?;
    let value = lucas_v(exponent, parameter, n)?;
    let factor = gcd(value.abs_diff(2), n);
    (factor > 1 && factor < n).then_some(factor)
}

/// Run a deterministic, bounded Pollard-rho search.
pub fn pollard_rho(n: u64, seed: u64, max_steps: u64) -> Option<u64> {
    if n < 4 || max_steps == 0 {
        return None;
    }
    if n % 2 == 0 {
        return Some(2);
    }
    if is_prime(n) {
        return None;
    }
    for attempt in 0_u64..8 {
        let offset = seed.wrapping_add(attempt);
        let value = 2 + offset % (n - 3);
        let mut tortoise = value;
        let mut hare = value;
        let constant = 1 + ((2_u128 * offset as u128 + 1) % (n - 1) as u128) as u64;
        for _ in 0..max_steps {
            tortoise = add_mod(mul_mod(tortoise, tortoise, n), constant, n);
            hare = add_mod(mul_mod(hare, hare, n), constant, n);
            hare = add_mod(mul_mod(hare, hare, n), constant, n);
            let difference = tortoise.abs_diff(hare);
            let factor = gcd(difference, n);
            if factor > 1 && factor < n {
                return Some(factor);
            }
            if factor == n {
                break;
            }
        }
    }
    None
}

/// Return exact per-value GCDs for a research batch.
pub fn batch_gcd(values: &[u64], modulus: u64) -> Option<Vec<u64>> {
    (modulus > 0).then(|| values.iter().map(|value| gcd(*value, modulus)).collect())
}

/// Exact divisibility-cover analysis for an explicit candidate family.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct CoverAnalysis {
    pub divisor_cover: bool,
    pub separates_profile: bool,
    pub distinct_signatures: bool,
}

/// Compare the divisibility signatures induced by `candidates` on `orders`.
pub fn analyze_divisor_cover(candidates: &[u64], orders: &[u64]) -> Option<CoverAnalysis> {
    if candidates.is_empty() || candidates.contains(&0) || orders.len() < 2 || orders.contains(&0) {
        return None;
    }
    let signatures = orders
        .iter()
        .map(|order| {
            candidates
                .iter()
                .enumerate()
                .filter_map(|(index, candidate)| (candidate % order == 0).then_some(index))
                .collect::<Vec<_>>()
        })
        .collect::<Vec<_>>();
    let separates_profile = candidates.iter().any(|candidate| {
        let hits = orders
            .iter()
            .filter(|order| candidate % **order == 0)
            .count();
        hits > 0 && hits < orders.len()
    });
    let distinct_signatures = signatures
        .iter()
        .enumerate()
        .all(|(index, signature)| !signatures[..index].contains(signature));
    Some(CoverAnalysis {
        divisor_cover: signatures.iter().all(|signature| !signature.is_empty()),
        separates_profile,
        distinct_signatures,
    })
}

/// Return the combined `(p-1, p+1)` divisibility bits for each exponent.
pub fn combined_promise_signature(prime: u64, exponents: &[u64]) -> Option<Vec<(bool, bool)>> {
    if prime < 3 || !is_prime(prime) || exponents.is_empty() || exponents.contains(&0) {
        return None;
    }
    Some(
        exponents
            .iter()
            .map(|exponent| (exponent % (prime - 1) == 0, exponent % (prime + 1) == 0))
            .collect(),
    )
}

/// Return whether either channel has a divisibility bit that separates two primes.
pub fn combined_promise_asymmetry(
    left_prime: u64,
    right_prime: u64,
    exponents: &[u64],
) -> Option<bool> {
    if left_prime == right_prime {
        return None;
    }
    Some(
        combined_promise_signature(left_prime, exponents)?
            != combined_promise_signature(right_prime, exponents)?,
    )
}

/// Count primes whose combined signature contains at least one hit.
pub fn combined_promise_hit_count(primes: &[u64], exponents: &[u64]) -> Option<usize> {
    if primes.is_empty() {
        return None;
    }
    let mut count = 0;
    for prime in primes {
        let signature = combined_promise_signature(*prime, exponents)?;
        if signature.iter().any(|(minus, plus)| *minus || *plus) {
            count += 1;
        }
    }
    Some(count)
}

/// Return the exact number of positive divisors.
pub fn divisor_count(value: u64) -> Option<u64> {
    if value == 0 {
        return None;
    }
    let mut remaining = value;
    let mut divisor = 2_u64;
    let mut count = 1_u64;
    while divisor <= remaining / divisor {
        if remaining % divisor == 0 {
            let mut exponent = 0_u64;
            while remaining % divisor == 0 {
                remaining /= divisor;
                exponent += 1;
            }
            count = count.checked_mul(exponent + 1)?;
        }
        divisor = if divisor == 2 { 3 } else { divisor + 2 };
    }
    if remaining > 1 {
        count = count.checked_mul(2)?;
    }
    Some(count)
}

/// Formal exponents and modular residues for a multiplication straight-line program.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct StraightLineEvaluation {
    pub exponents: Vec<u64>,
    pub residues: Vec<u64>,
}

/// Signed formal exponents and unit residues for an addition-subtraction program.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SignedStraightLineEvaluation {
    pub exponents: Vec<i128>,
    pub residues: Vec<u64>,
    pub inversion_count: usize,
}

/// Materialized leaves and root data for a standard modular product tree.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BatchProductEvaluation {
    pub exponents: Vec<u64>,
    pub leaf_residues: Vec<u64>,
    pub leaf_gcds: Vec<u64>,
    pub root_residue: u64,
    pub root_gcd: u64,
    pub multiplication_count: usize,
}

/// Explicit atom nodes and shared product nodes for a non-materializing DAG.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ProductDagEvaluation {
    pub exponents: Vec<u64>,
    pub atom_residues: Vec<u64>,
    pub atom_gcds: Vec<u64>,
    pub node_residues: Vec<u64>,
    pub node_gcds: Vec<u64>,
    pub multiplicities: Vec<Vec<u64>>,
    pub occurrence_counts: Vec<u64>,
}

/// Total modular-division outcome for one exact dyadic telescope.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DyadicDivisionStatus {
    Unit,
    ProperFactor,
    FullCollision,
}

/// Compact evaluation of `(g^(2^t)-1)/(g-1)`.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DyadicTelescopeEvaluation {
    pub power_residues: Vec<u64>,
    pub factor_residues: Vec<u64>,
    pub factor_gcds: Vec<u64>,
    pub denominator_residue: u64,
    pub denominator_gcd: u64,
    pub numerator_residue: u64,
    pub numerator_gcd: u64,
    pub quotient_residue: u64,
    pub quotient_gcd: u64,
    pub division_status: DyadicDivisionStatus,
    pub division_quotient: Option<u64>,
    pub formal_degree: u64,
    pub formal_monomial_count: u64,
    pub squaring_count: u32,
    pub product_multiplication_count: u32,
}

/// Total modular-division outcome for one arbitrary geometric sum.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum GeometricDivisionStatus {
    Unit,
    ProperFactor,
    FullCollision,
}

/// Compact binary evaluation of `S_M(g) = sum_{i < M} g^i`.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct GeometricSumEvaluation {
    pub exponent: u64,
    pub exponent_bit_length: u32,
    pub power_residue: u64,
    pub sum_residue: u64,
    pub denominator_residue: u64,
    pub denominator_gcd: u64,
    pub numerator_residue: u64,
    pub numerator_gcd: u64,
    pub sum_gcd: u64,
    pub exponent_gcd: u64,
    pub division_status: GeometricDivisionStatus,
    pub division_quotient: Option<u64>,
    pub formal_degree: u64,
    pub formal_monomial_count: u64,
    pub multiplication_count: u32,
    pub addition_count: u32,
}

/// Both total division paths for `S_(A B)(g) / S_A(g) = S_B(g^A)`.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct NestedQuotientEvaluation {
    pub inner_power_residue: u64,
    pub intermediate_residue: u64,
    pub intermediate_gcd: u64,
    pub quotient_residue: u64,
    pub quotient_gcd: u64,
    pub rational_numerator_residue: u64,
    pub rational_numerator_gcd: u64,
    pub composed_denominator_residue: u64,
    pub composed_denominator_gcd: u64,
    pub endpoint_residue: u64,
    pub endpoint_gcd: u64,
    pub multiplier_gcd: u64,
    pub rational_division_status: GeometricDivisionStatus,
    pub rational_division_quotient: Option<u64>,
    pub composed_division_status: GeometricDivisionStatus,
    pub composed_division_quotient: Option<u64>,
}

/// Stage-by-stage evaluation of a public geometric factor chain.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct IteratedQuotientEvaluation {
    pub factors: Vec<u64>,
    pub prefix_exponents: Vec<u64>,
    pub stages: Vec<NestedQuotientEvaluation>,
    pub final_quotient_product_residue: u64,
    pub final_prefix_residue: u64,
    pub final_prefix_gcd: u64,
}

/// A public signed linear combination of the stages in an iterated quotient chain.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct QuotientLinearCombinationEvaluation {
    pub chain: IteratedQuotientEvaluation,
    pub coefficients: Vec<i64>,
    pub coefficient_residues: Vec<u64>,
    pub coefficient_gcds: Vec<u64>,
    pub weighted_stage_residues: Vec<u64>,
    pub weighted_stage_gcds: Vec<u64>,
    pub aggregate_residue: u64,
    pub aggregate_gcd: u64,
}

/// Exact factors of `S_A(g^A) - S_A(g)` in the symmetric depth-two chain.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SymmetricQuotientDifferenceEvaluation {
    pub exponent: u64,
    pub first_quotient_residue: u64,
    pub second_quotient_residue: u64,
    pub difference_residue: u64,
    pub difference_gcd: u64,
    pub endpoint_residue: u64,
    pub endpoint_gcd: u64,
    pub endpoint_status: GeometricDivisionStatus,
    pub cofactor_residue: u64,
    pub cofactor_gcd: u64,
    pub division_cofactor: Option<u64>,
    pub cofactor_monomial_count: u64,
    pub cofactor_degree: u64,
    pub matrix_multiplication_count: u32,
}

/// General signed depth-two form and normalized unequal-difference reductions.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct UnequalSignedReductionEvaluation {
    pub first_factor: u64,
    pub second_factor: u64,
    pub first_coefficient: i64,
    pub second_coefficient: i64,
    pub first_quotient_residue: u64,
    pub second_quotient_residue: u64,
    pub first_quotient_gcd: u64,
    pub second_quotient_gcd: u64,
    pub aggregate_residue: u64,
    pub aggregate_gcd: u64,
    pub first_quotient_status: GeometricDivisionStatus,
    pub rational_reduction_residue: Option<u64>,
    pub rational_reduction_gcd: Option<u64>,
    pub public_full_residue: u64,
    pub public_full_gcd: u64,
    pub common_stage_gcd: u64,
    pub multiplier_gcd: u64,
    pub has_x_factor: bool,
    pub has_x_minus_one_factor: bool,
    pub formal_degree: u64,
    pub collected_monomial_count: u64,
    pub common_step: u64,
    pub difference_residue: u64,
    pub difference_gcd: u64,
    pub common_factor_residue: u64,
    pub common_factor_gcd: u64,
    pub difference_cofactor_residue: Option<u64>,
    pub difference_cofactor_gcd: Option<u64>,
    pub difference_cofactor_degree: u64,
}

/// Primitive-content and public resultant audit of an unequal signed numerator.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RationalResidueAuditEvaluation {
    pub first_factor: u64,
    pub second_factor: u64,
    pub first_coefficient: i64,
    pub second_coefficient: i64,
    pub content: u64,
    pub primitive_first_coefficient: i64,
    pub primitive_second_coefficient: i64,
    pub content_gcd: u64,
    pub content_status: GeometricDivisionStatus,
    pub first_quotient_residue: u64,
    pub second_quotient_residue: u64,
    pub first_quotient_gcd: u64,
    pub second_quotient_gcd: u64,
    pub aggregate_residue: u64,
    pub aggregate_gcd: u64,
    pub primitive_aggregate_residue: u64,
    pub primitive_aggregate_gcd: u64,
    pub prefix_status: GeometricDivisionStatus,
    pub rational_residue: Option<u64>,
    pub rational_gcd: Option<u64>,
    pub primitive_rational_residue: Option<u64>,
    pub primitive_rational_gcd: Option<u64>,
    pub first_overlap_gcd: u64,
    pub first_public_bound_gcd: u64,
    pub second_overlap_gcd: u64,
    pub second_public_bound_gcd: u64,
    pub first_resultant_base: u128,
    pub first_resultant_exponent: u64,
    pub second_resultant_coefficient_base: u64,
    pub second_resultant_coefficient_exponent: u64,
    pub second_resultant_stage_base: u64,
    pub second_resultant_stage_exponent: u64,
}

/// Complete M25 classification of one nonboundary cyclotomic root ratio.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RationalRootOrbitClassification {
    pub first_factor: u64,
    pub second_factor: u64,
    pub order: u64,
    pub category: &'static str,
    pub outside_stage_zeros: bool,
    pub phase_order: u128,
    pub phase_divisible: bool,
    pub rational_ratio: Option<i64>,
    pub primitive_first_coefficient: Option<i64>,
    pub primitive_second_coefficient: Option<i64>,
    pub common_step: u64,
    pub phi4_enabled: bool,
    pub phi6_enabled: bool,
}

/// Total extraction semantics for one fixed exceptional cyclotomic family.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ExceptionalCyclotomicEvaluation {
    pub base: u64,
    pub modulus: u64,
    pub family: &'static str,
    pub order: u64,
    pub first_factor: u64,
    pub second_factor: u64,
    pub first_coefficient: i64,
    pub second_coefficient: i64,
    pub cyclotomic_residue: u64,
    pub cyclotomic_gcd: u64,
    pub cyclotomic_status: GeometricDivisionStatus,
    pub aggregate_residue: u64,
    pub aggregate_gcd: u64,
    pub aggregate_status: GeometricDivisionStatus,
    pub cofactor_residue: Option<u64>,
    pub cofactor_gcd: Option<u64>,
    pub cofactor_status: Option<GeometricDivisionStatus>,
    pub extraction_source: &'static str,
    pub extraction_gcd: Option<u64>,
    pub first_quotient_gcd: u64,
    pub second_quotient_gcd: u64,
    pub first_public_bound_gcd: u64,
    pub second_public_bound_gcd: u64,
    pub dense_cofactor_degree: u64,
    pub dense_cofactor_coefficient_count: u64,
}

/// Compact exact resultant descriptors for an M27 exceptional cofactor.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ExceptionalCofactorOverlap {
    pub family: &'static str,
    pub order: u64,
    pub first_factor: u64,
    pub second_factor: u64,
    pub cofactor_degree: u64,
    pub remainder_constant: i128,
    pub remainder_linear: i128,
    pub cyclotomic_cofactor_resultant: u128,
    pub first_stage_resultant_base: u64,
    pub first_stage_resultant_exponent: u64,
    pub second_stage_power_of_two_exponent: u64,
    pub second_stage_resultant_base: u64,
    pub second_stage_resultant_exponent: u64,
    pub stage_overlap_support: &'static str,
}

/// Exact materialized-support accounting for one M28 input length.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LengthIndexedSupportProfile {
    pub input_length: u32,
    pub population_size: u64,
    pub min_prime_log2_floor: u32,
    pub charged_value_count: u64,
    pub materialized_bit_budget: u64,
    pub hit_primes: Vec<u64>,
    pub missed_primes: Vec<u64>,
    pub hit_prime_count: u64,
    pub forced_miss_pair_count: u64,
    pub pair_count: u64,
    pub maximum_coverable_pair_count: u64,
    pub support_cap: u64,
    pub necessary_universal_bit_budget: u64,
}

/// Exact prime-divisibility profile for the M29 compact Phi4 family.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CompactPhi4PrimeProfile {
    pub level: u32,
    pub prime: u64,
    pub second_factor: u64,
    pub exponent: u64,
    pub cofactor_residue: u64,
    pub criterion_residue: u64,
    pub divides: bool,
    pub rule: &'static str,
}

/// Evaluate nodes starting from `g`, with every later node multiplying two parents.
pub fn evaluate_multiplication_program(
    base: u64,
    modulus: u64,
    steps: &[(usize, usize)],
) -> Option<StraightLineEvaluation> {
    if modulus < 2 {
        return None;
    }
    let mut exponents = vec![1_u64];
    let mut residues = vec![base % modulus];
    for (node_index, (left, right)) in steps.iter().copied().enumerate() {
        let available = node_index + 1;
        if left >= available || right >= available {
            return None;
        }
        exponents.push(exponents[left].checked_add(exponents[right])?);
        residues.push(mul_mod(residues[left], residues[right], modulus));
    }
    Some(StraightLineEvaluation {
        exponents,
        residues,
    })
}

fn modular_inverse(value: u64, modulus: u64) -> Option<u64> {
    let mut old_remainder = i128::from(value);
    let mut remainder = i128::from(modulus);
    let mut old_coefficient = 1_i128;
    let mut coefficient = 0_i128;
    while remainder != 0 {
        let quotient = old_remainder / remainder;
        (old_remainder, remainder) = (
            remainder,
            old_remainder.checked_sub(quotient.checked_mul(remainder)?)?,
        );
        (old_coefficient, coefficient) = (
            coefficient,
            old_coefficient.checked_sub(quotient.checked_mul(coefficient)?)?,
        );
    }
    if old_remainder != 1 {
        return None;
    }
    let normalized = old_coefficient.rem_euclid(i128::from(modulus));
    u64::try_from(normalized).ok()
}

/// Evaluate a same-base program whose sign is `1` for product and `-1` for ratio.
pub fn evaluate_addition_subtraction_program(
    base: u64,
    modulus: u64,
    steps: &[(usize, usize, i8)],
) -> Option<SignedStraightLineEvaluation> {
    if modulus < 2 {
        return None;
    }
    let reduced_base = base % modulus;
    if gcd(reduced_base, modulus) != 1 {
        return None;
    }
    let mut exponents = vec![1_i128];
    let mut residues = vec![reduced_base];
    let mut inversion_count = 0_usize;
    for (node_index, (left, right, sign)) in steps.iter().copied().enumerate() {
        let available = node_index + 1;
        if left >= available || right >= available || !matches!(sign, -1 | 1) {
            return None;
        }
        let right_exponent = exponents[right].checked_mul(i128::from(sign))?;
        exponents.push(exponents[left].checked_add(right_exponent)?);
        let right_residue = if sign == -1 {
            inversion_count += 1;
            modular_inverse(residues[right], modulus)?
        } else {
            residues[right]
        };
        residues.push(mul_mod(residues[left], right_residue, modulus));
    }
    Some(SignedStraightLineEvaluation {
        exponents,
        residues,
        inversion_count,
    })
}

/// Materialize every `g^d - 1` leaf and combine them in a binary product tree.
pub fn evaluate_batch_product(
    base: u64,
    modulus: u64,
    exponents: &[u64],
) -> Option<BatchProductEvaluation> {
    if modulus < 2 || exponents.is_empty() || gcd(base % modulus, modulus) != 1 {
        return None;
    }
    if exponents.iter().copied().any(|exponent| exponent == 0)
        || exponents.windows(2).any(|pair| pair[0] >= pair[1])
    {
        return None;
    }
    let leaf_residues = exponents
        .iter()
        .copied()
        .map(|exponent| {
            mod_pow(base, exponent, modulus).map(|residue| {
                if residue == 0 {
                    modulus - 1
                } else {
                    residue - 1
                }
            })
        })
        .collect::<Option<Vec<_>>>()?;
    let leaf_gcds = leaf_residues
        .iter()
        .copied()
        .map(|residue| gcd(residue, modulus))
        .collect::<Vec<_>>();
    let mut current = leaf_residues.clone();
    let mut multiplication_count = 0_usize;
    while current.len() > 1 {
        let mut following = Vec::with_capacity(current.len().div_ceil(2));
        for pair in current.chunks(2) {
            if pair.len() == 1 {
                following.push(pair[0]);
            } else {
                following.push(mul_mod(pair[0], pair[1], modulus));
                multiplication_count += 1;
            }
        }
        current = following;
    }
    let root_residue = current[0];
    Some(BatchProductEvaluation {
        exponents: exponents.to_vec(),
        leaf_residues,
        leaf_gcds,
        root_residue,
        root_gcd: gcd(root_residue, modulus),
        multiplication_count,
    })
}

/// Evaluate explicit `g^d - 1` atoms and shared product gates without unfolding.
pub fn evaluate_product_dag(
    base: u64,
    modulus: u64,
    exponents: &[u64],
    gates: &[(usize, usize)],
) -> Option<ProductDagEvaluation> {
    if modulus < 2
        || exponents.is_empty()
        || gcd(base % modulus, modulus) != 1
        || exponents.iter().copied().any(|exponent| exponent == 0)
        || exponents.windows(2).any(|pair| pair[0] >= pair[1])
    {
        return None;
    }
    let atom_residues = exponents
        .iter()
        .copied()
        .map(|exponent| {
            mod_pow(base, exponent, modulus).map(|residue| {
                if residue == 0 {
                    modulus - 1
                } else {
                    residue - 1
                }
            })
        })
        .collect::<Option<Vec<_>>>()?;
    let atom_gcds = atom_residues
        .iter()
        .copied()
        .map(|residue| gcd(residue, modulus))
        .collect::<Vec<_>>();
    let atom_count = atom_residues.len();
    let mut node_residues = atom_residues.clone();
    let mut multiplicities = (0..atom_count)
        .map(|index| {
            (0..atom_count)
                .map(|atom| u64::from(atom == index))
                .collect::<Vec<_>>()
        })
        .collect::<Vec<_>>();
    let mut occurrence_counts = vec![1_u64; atom_count];
    for (gate_index, (left, right)) in gates.iter().copied().enumerate() {
        let available = atom_count + gate_index;
        if left >= available || right >= available {
            return None;
        }
        node_residues.push(mul_mod(node_residues[left], node_residues[right], modulus));
        let profile = multiplicities[left]
            .iter()
            .zip(&multiplicities[right])
            .map(|(left_count, right_count)| left_count.checked_add(*right_count))
            .collect::<Option<Vec<_>>>()?;
        multiplicities.push(profile);
        occurrence_counts.push(occurrence_counts[left].checked_add(occurrence_counts[right])?);
    }
    let node_gcds = node_residues
        .iter()
        .copied()
        .map(|residue| gcd(residue, modulus))
        .collect::<Vec<_>>();
    Some(ProductDagEvaluation {
        exponents: exponents.to_vec(),
        atom_residues,
        atom_gcds,
        node_residues,
        node_gcds,
        multiplicities,
        occurrence_counts,
    })
}

/// Evaluate a dyadic geometric quotient through composition and explicit factors.
pub fn evaluate_dyadic_telescope(
    base: u64,
    modulus: u64,
    levels: u32,
) -> Option<DyadicTelescopeEvaluation> {
    if modulus < 2 || levels >= u64::BITS || gcd(base % modulus, modulus) != 1 {
        return None;
    }
    let reduced_base = base % modulus;
    let mut power_residues = vec![reduced_base];
    for _ in 0..levels {
        let following = mul_mod(*power_residues.last()?, *power_residues.last()?, modulus);
        power_residues.push(following);
    }
    let factor_residues = power_residues
        .iter()
        .copied()
        .take(levels as usize)
        .map(|power| if power == modulus - 1 { 0 } else { power + 1 })
        .collect::<Vec<_>>();
    let factor_gcds = factor_residues
        .iter()
        .copied()
        .map(|factor| gcd(factor, modulus))
        .collect::<Vec<_>>();
    let quotient_residue = factor_residues
        .first()
        .copied()
        .map_or(1 % modulus, |first| {
            factor_residues
                .iter()
                .copied()
                .skip(1)
                .fold(first, |product, factor| mul_mod(product, factor, modulus))
        });
    let denominator_residue = reduced_base - 1;
    let denominator_gcd = gcd(denominator_residue, modulus);
    let numerator_residue = power_residues.last()?.checked_sub(1)?;
    let (division_status, division_quotient) = if denominator_gcd == 1 {
        (
            DyadicDivisionStatus::Unit,
            Some(mul_mod(
                numerator_residue,
                modular_inverse(denominator_residue, modulus)?,
                modulus,
            )),
        )
    } else if denominator_gcd < modulus {
        (DyadicDivisionStatus::ProperFactor, None)
    } else {
        (DyadicDivisionStatus::FullCollision, None)
    };
    let formal_monomial_count = 1_u64.checked_shl(levels)?;
    Some(DyadicTelescopeEvaluation {
        power_residues,
        factor_residues,
        factor_gcds,
        denominator_residue,
        denominator_gcd,
        numerator_residue,
        numerator_gcd: gcd(numerator_residue, modulus),
        quotient_residue,
        quotient_gcd: gcd(quotient_residue, modulus),
        division_status,
        division_quotient,
        formal_degree: formal_monomial_count - 1,
        formal_monomial_count,
        squaring_count: levels,
        product_multiplication_count: levels.saturating_sub(1),
    })
}

/// Evaluate an arbitrary positive-exponent geometric sum by binary composition.
pub fn evaluate_geometric_sum(
    base: u64,
    modulus: u64,
    exponent: u64,
) -> Option<GeometricSumEvaluation> {
    if modulus < 2 || exponent == 0 || gcd(base % modulus, modulus) != 1 {
        return None;
    }
    let reduced_base = base % modulus;
    let exponent_bit_length = u64::BITS - exponent.leading_zeros();
    let mut power_residue = reduced_base;
    let mut sum_residue = 1 % modulus;
    let mut multiplication_count = 0_u32;
    let mut addition_count = 0_u32;

    for bit_index in (0..exponent_bit_length.saturating_sub(1)).rev() {
        let one_plus_power = if power_residue == modulus - 1 {
            0
        } else {
            power_residue + 1
        };
        sum_residue = mul_mod(sum_residue, one_plus_power, modulus);
        power_residue = mul_mod(power_residue, power_residue, modulus);
        multiplication_count += 2;
        addition_count += 1;
        if (exponent >> bit_index) & 1 == 1 {
            sum_residue = if sum_residue >= modulus - power_residue {
                sum_residue - (modulus - power_residue)
            } else {
                sum_residue + power_residue
            };
            power_residue = mul_mod(power_residue, reduced_base, modulus);
            multiplication_count += 1;
            addition_count += 1;
        }
    }

    let denominator_residue = reduced_base - 1;
    let denominator_gcd = gcd(denominator_residue, modulus);
    let numerator_residue = power_residue - 1;
    let (division_status, division_quotient) = if denominator_gcd == 1 {
        (
            GeometricDivisionStatus::Unit,
            Some(mul_mod(
                numerator_residue,
                modular_inverse(denominator_residue, modulus)?,
                modulus,
            )),
        )
    } else if denominator_gcd < modulus {
        (GeometricDivisionStatus::ProperFactor, None)
    } else {
        (GeometricDivisionStatus::FullCollision, None)
    };

    Some(GeometricSumEvaluation {
        exponent,
        exponent_bit_length,
        power_residue,
        sum_residue,
        denominator_residue,
        denominator_gcd,
        numerator_residue,
        numerator_gcd: gcd(numerator_residue, modulus),
        sum_gcd: gcd(sum_residue, modulus),
        exponent_gcd: gcd(exponent, modulus),
        division_status,
        division_quotient,
        formal_degree: exponent - 1,
        formal_monomial_count: exponent,
        multiplication_count,
        addition_count,
    })
}

/// Evaluate one cancellation-obscured nested geometric quotient.
pub fn evaluate_nested_quotient(
    base: u64,
    modulus: u64,
    inner_exponent: u64,
    multiplier: u64,
) -> Option<NestedQuotientEvaluation> {
    let product_exponent = inner_exponent.checked_mul(multiplier)?;
    let inner = evaluate_geometric_sum(base, modulus, inner_exponent)?;
    let outer = evaluate_geometric_sum(inner.power_residue, modulus, multiplier)?;
    let combined = evaluate_geometric_sum(base, modulus, product_exponent)?;
    if combined.sum_residue != mul_mod(inner.sum_residue, outer.sum_residue, modulus)
        || combined.power_residue != outer.power_residue
    {
        return None;
    }
    let rational_division_status = if inner.sum_gcd == 1 {
        GeometricDivisionStatus::Unit
    } else if inner.sum_gcd < modulus {
        GeometricDivisionStatus::ProperFactor
    } else {
        GeometricDivisionStatus::FullCollision
    };
    Some(NestedQuotientEvaluation {
        inner_power_residue: inner.power_residue,
        intermediate_residue: inner.sum_residue,
        intermediate_gcd: inner.sum_gcd,
        quotient_residue: outer.sum_residue,
        quotient_gcd: outer.sum_gcd,
        rational_numerator_residue: combined.sum_residue,
        rational_numerator_gcd: combined.sum_gcd,
        composed_denominator_residue: outer.denominator_residue,
        composed_denominator_gcd: outer.denominator_gcd,
        endpoint_residue: outer.numerator_residue,
        endpoint_gcd: outer.numerator_gcd,
        multiplier_gcd: outer.exponent_gcd,
        rational_division_status,
        rational_division_quotient: if inner.sum_gcd == 1 {
            Some(mul_mod(
                combined.sum_residue,
                modular_inverse(inner.sum_residue, modulus)?,
                modulus,
            ))
        } else {
            None
        },
        composed_division_status: outer.division_status,
        composed_division_quotient: outer.division_quotient,
    })
}

/// Evaluate every quotient in a public iterated geometric factor chain.
pub fn evaluate_iterated_quotient(
    base: u64,
    modulus: u64,
    factors: &[u64],
) -> Option<IteratedQuotientEvaluation> {
    if modulus < 2 || factors.is_empty() || factors.contains(&0) {
        return None;
    }
    let mut prefix = 1_u64;
    let mut prefix_exponents = vec![prefix];
    let mut stages = Vec::with_capacity(factors.len());
    let mut quotient_product = 1 % modulus;
    let mut previous_numerator = None;
    for factor in factors.iter().copied() {
        let stage = evaluate_nested_quotient(base, modulus, prefix, factor)?;
        if previous_numerator.is_some_and(|value| value != stage.intermediate_residue) {
            return None;
        }
        quotient_product = mul_mod(quotient_product, stage.quotient_residue, modulus);
        if quotient_product != stage.rational_numerator_residue {
            return None;
        }
        previous_numerator = Some(stage.rational_numerator_residue);
        prefix = prefix.checked_mul(factor)?;
        prefix_exponents.push(prefix);
        stages.push(stage);
    }
    let final_stage = stages.last()?;
    Some(IteratedQuotientEvaluation {
        factors: factors.to_vec(),
        prefix_exponents,
        final_quotient_product_residue: quotient_product,
        final_prefix_residue: final_stage.rational_numerator_residue,
        final_prefix_gcd: final_stage.rational_numerator_gcd,
        stages,
    })
}

/// Evaluate a signed linear combination of the public quotient-chain stages.
pub fn evaluate_quotient_linear_combination(
    base: u64,
    modulus: u64,
    factors: &[u64],
    coefficients: &[i64],
) -> Option<QuotientLinearCombinationEvaluation> {
    if factors.len() != coefficients.len() {
        return None;
    }
    let chain = evaluate_iterated_quotient(base, modulus, factors)?;
    let mut coefficient_residues = Vec::with_capacity(coefficients.len());
    let mut coefficient_gcds = Vec::with_capacity(coefficients.len());
    let mut weighted_stage_residues = Vec::with_capacity(coefficients.len());
    let mut weighted_stage_gcds = Vec::with_capacity(coefficients.len());
    let mut aggregate_residue = 0_u64;
    for (coefficient, stage) in coefficients.iter().copied().zip(&chain.stages) {
        let coefficient_residue = i128::from(coefficient).rem_euclid(i128::from(modulus)) as u64;
        let weighted = mul_mod(coefficient_residue, stage.quotient_residue, modulus);
        coefficient_residues.push(coefficient_residue);
        coefficient_gcds.push(gcd(coefficient.unsigned_abs(), modulus));
        weighted_stage_residues.push(weighted);
        weighted_stage_gcds.push(gcd(weighted, modulus));
        aggregate_residue = add_mod(aggregate_residue, weighted, modulus);
    }
    Some(QuotientLinearCombinationEvaluation {
        chain,
        coefficients: coefficients.to_vec(),
        coefficient_residues,
        coefficient_gcds,
        weighted_stage_residues,
        weighted_stage_gcds,
        aggregate_residue,
        aggregate_gcd: gcd(aggregate_residue, modulus),
    })
}

type Matrix3 = [[u64; 3]; 3];

fn multiply_matrix3(left: &Matrix3, right: &Matrix3, modulus: u64) -> Matrix3 {
    let mut result = [[0_u64; 3]; 3];
    for (row, result_row) in result.iter_mut().enumerate() {
        for (column, result_item) in result_row.iter_mut().enumerate() {
            for (inner, right_row) in right.iter().enumerate() {
                *result_item = add_mod(
                    *result_item,
                    mul_mod(left[row][inner], right_row[column], modulus),
                    modulus,
                );
            }
        }
    }
    result
}

fn power_matrix3(matrix: Matrix3, exponent: u64, modulus: u64) -> (Matrix3, u32) {
    let mut result = [[1_u64, 0, 0], [0, 1, 0], [0, 0, 1]];
    let mut power = matrix;
    let mut remaining = exponent;
    let mut multiplication_count = 0_u32;
    while remaining != 0 {
        if remaining & 1 == 1 {
            result = multiply_matrix3(&result, &power, modulus);
            multiplication_count += 1;
        }
        remaining >>= 1;
        if remaining != 0 {
            power = multiply_matrix3(&power, &power, modulus);
            multiplication_count += 1;
        }
    }
    (result, multiplication_count)
}

fn compact_symmetric_cofactor(base: u64, modulus: u64, exponent: u64) -> Option<(u64, u32)> {
    let n = exponent.checked_sub(1)?;
    let y = mod_pow(base, n, modulus)?;
    let xy = mul_mod(base, y, modulus);
    let transition = [[base, 1, 0], [0, xy, 0], [base, 1, 1]];
    let (powered, multiplication_count) = power_matrix3(transition, n.checked_sub(1)?, modulus);
    let initial = [1 % modulus, xy, 1 % modulus];
    let mut state = [0_u64; 3];
    for (row, state_item) in state.iter_mut().enumerate() {
        for (column, initial_item) in initial.iter().enumerate() {
            *state_item = add_mod(
                *state_item,
                mul_mod(powered[row][column], *initial_item, modulus),
                modulus,
            );
        }
    }
    Some((state[2], multiplication_count))
}

/// Evaluate the symmetric signed difference and its endpoint/cofactor split.
pub fn evaluate_symmetric_quotient_difference(
    base: u64,
    modulus: u64,
    exponent: u64,
) -> Option<SymmetricQuotientDifferenceEvaluation> {
    if exponent < 2 {
        return None;
    }
    let first = evaluate_geometric_sum(base, modulus, exponent)?;
    let second = evaluate_geometric_sum(first.power_residue, modulus, exponent)?;
    let difference_residue = if second.sum_residue >= first.sum_residue {
        second.sum_residue - first.sum_residue
    } else {
        modulus - (first.sum_residue - second.sum_residue)
    };
    let endpoint_residue = mod_pow(base, exponent - 1, modulus)? - 1;
    let endpoint_gcd = gcd(endpoint_residue, modulus);
    let endpoint_status = if endpoint_gcd == 1 {
        GeometricDivisionStatus::Unit
    } else if endpoint_gcd < modulus {
        GeometricDivisionStatus::ProperFactor
    } else {
        GeometricDivisionStatus::FullCollision
    };
    let reduced_base = base % modulus;
    let (cofactor_residue, matrix_multiplication_count) =
        compact_symmetric_cofactor(reduced_base, modulus, exponent)?;
    let factor_product = mul_mod(
        mul_mod(reduced_base, endpoint_residue, modulus),
        cofactor_residue,
        modulus,
    );
    if factor_product != difference_residue {
        return None;
    }
    let division_cofactor = if endpoint_gcd == 1 {
        Some(mul_mod(
            difference_residue,
            modular_inverse(mul_mod(reduced_base, endpoint_residue, modulus), modulus)?,
            modulus,
        ))
    } else {
        None
    };
    if division_cofactor.is_some_and(|value| value != cofactor_residue) {
        return None;
    }
    Some(SymmetricQuotientDifferenceEvaluation {
        exponent,
        first_quotient_residue: first.sum_residue,
        second_quotient_residue: second.sum_residue,
        difference_residue,
        difference_gcd: gcd(difference_residue, modulus),
        endpoint_residue,
        endpoint_gcd,
        endpoint_status,
        cofactor_residue,
        cofactor_gcd: gcd(cofactor_residue, modulus),
        division_cofactor,
        cofactor_monomial_count: exponent.checked_mul(exponent - 1)? / 2,
        cofactor_degree: exponent.checked_mul(exponent - 2)?,
        matrix_multiplication_count,
    })
}

/// Evaluate an unequal depth-two signed form and its total rational reduction.
pub fn evaluate_unequal_signed_reduction(
    base: u64,
    modulus: u64,
    first_factor: u64,
    second_factor: u64,
    first_coefficient: i64,
    second_coefficient: i64,
) -> Option<UnequalSignedReductionEvaluation> {
    if first_factor < 2
        || second_factor < 2
        || first_factor == second_factor
        || first_coefficient == 0
        || second_coefficient == 0
    {
        return None;
    }
    let first = evaluate_geometric_sum(base, modulus, first_factor)?;
    let second = evaluate_geometric_sum(first.power_residue, modulus, second_factor)?;
    let first_coefficient_residue =
        i128::from(first_coefficient).rem_euclid(i128::from(modulus)) as u64;
    let second_coefficient_residue =
        i128::from(second_coefficient).rem_euclid(i128::from(modulus)) as u64;
    let aggregate_residue = add_mod(
        mul_mod(first_coefficient_residue, first.sum_residue, modulus),
        mul_mod(second_coefficient_residue, second.sum_residue, modulus),
        modulus,
    );
    let first_quotient_status = if first.sum_gcd == 1 {
        GeometricDivisionStatus::Unit
    } else if first.sum_gcd < modulus {
        GeometricDivisionStatus::ProperFactor
    } else {
        GeometricDivisionStatus::FullCollision
    };
    let rational_reduction_residue = if first.sum_gcd == 1 {
        let ratio = mul_mod(
            second.sum_residue,
            modular_inverse(first.sum_residue, modulus)?,
            modulus,
        );
        let value = add_mod(
            first_coefficient_residue,
            mul_mod(second_coefficient_residue, ratio, modulus),
            modulus,
        );
        if mul_mod(first.sum_residue, value, modulus) != aggregate_residue {
            return None;
        }
        Some(value)
    } else {
        None
    };
    let public_full_residue = mul_mod(second_coefficient_residue, second_factor % modulus, modulus);
    if first.sum_gcd == modulus
        && (second.sum_residue != second_factor % modulus
            || aggregate_residue != public_full_residue)
    {
        return None;
    }
    let common_stage_gcd = gcd(gcd(first.sum_residue, second.sum_residue), modulus);
    let multiplier_gcd = gcd(second_factor, modulus);
    if multiplier_gcd % common_stage_gcd != 0 {
        return None;
    }

    let common_step = gcd(first_factor - 1, second_factor - 1);
    let common_sum = evaluate_geometric_sum(base, modulus, common_step)?;
    let reduced_base = base % modulus;
    let common_factor_residue = mul_mod(reduced_base, common_sum.sum_residue, modulus);
    let common_factor_gcd = gcd(common_factor_residue, modulus);
    let difference_residue = if second.sum_residue >= first.sum_residue {
        second.sum_residue - first.sum_residue
    } else {
        modulus - (first.sum_residue - second.sum_residue)
    };
    let difference_cofactor_residue = if common_factor_gcd == 1 {
        Some(mul_mod(
            difference_residue,
            modular_inverse(common_factor_residue, modulus)?,
            modulus,
        ))
    } else {
        None
    };

    let formal_at_one = i128::from(first_coefficient)
        .checked_mul(i128::from(first_factor))?
        .checked_add(i128::from(second_coefficient).checked_mul(i128::from(second_factor))?)?;
    let coefficient_sum = i128::from(first_coefficient) + i128::from(second_coefficient);
    let formal_degree = first_factor.checked_mul(second_factor - 1)?;
    let collected_monomial_count = first_factor
        .checked_add(second_factor)?
        .checked_sub(if coefficient_sum == 0 { 2 } else { 1 })?;
    let difference_cofactor_degree = formal_degree.checked_sub(common_step)?.checked_sub(1)?;
    Some(UnequalSignedReductionEvaluation {
        first_factor,
        second_factor,
        first_coefficient,
        second_coefficient,
        first_quotient_residue: first.sum_residue,
        second_quotient_residue: second.sum_residue,
        first_quotient_gcd: first.sum_gcd,
        second_quotient_gcd: second.sum_gcd,
        aggregate_residue,
        aggregate_gcd: gcd(aggregate_residue, modulus),
        first_quotient_status,
        rational_reduction_residue,
        rational_reduction_gcd: rational_reduction_residue.map(|value| gcd(value, modulus)),
        public_full_residue,
        public_full_gcd: gcd(public_full_residue, modulus),
        common_stage_gcd,
        multiplier_gcd,
        has_x_factor: coefficient_sum == 0,
        has_x_minus_one_factor: formal_at_one == 0,
        formal_degree,
        collected_monomial_count,
        common_step,
        difference_residue,
        difference_gcd: gcd(difference_residue, modulus),
        common_factor_residue,
        common_factor_gcd,
        difference_cofactor_residue,
        difference_cofactor_gcd: difference_cofactor_residue.map(|value| gcd(value, modulus)),
        difference_cofactor_degree,
    })
}

/// Evaluate coefficient content, unit-prefix division, and stage-resultant bounds.
pub fn evaluate_rational_residue_audit(
    base: u64,
    modulus: u64,
    first_factor: u64,
    second_factor: u64,
    first_coefficient: i64,
    second_coefficient: i64,
) -> Option<RationalResidueAuditEvaluation> {
    if first_factor < 2
        || second_factor < 2
        || first_factor == second_factor
        || first_coefficient == 0
        || second_coefficient == 0
        || first_coefficient == i64::MIN
        || second_coefficient == i64::MIN
    {
        return None;
    }
    let first = evaluate_geometric_sum(base, modulus, first_factor)?;
    let second = evaluate_geometric_sum(first.power_residue, modulus, second_factor)?;
    let content = gcd(
        first_coefficient.unsigned_abs(),
        second_coefficient.unsigned_abs(),
    );
    let content_i64 = i64::try_from(content).ok()?;
    let primitive_first_coefficient = first_coefficient / content_i64;
    let primitive_second_coefficient = second_coefficient / content_i64;
    let coefficient_residue = |value: i64| i128::from(value).rem_euclid(i128::from(modulus)) as u64;
    let linear_combination = |left: i64, right: i64| {
        add_mod(
            mul_mod(coefficient_residue(left), first.sum_residue, modulus),
            mul_mod(coefficient_residue(right), second.sum_residue, modulus),
            modulus,
        )
    };
    let aggregate_residue = linear_combination(first_coefficient, second_coefficient);
    let primitive_aggregate_residue =
        linear_combination(primitive_first_coefficient, primitive_second_coefficient);
    if aggregate_residue != mul_mod(content % modulus, primitive_aggregate_residue, modulus) {
        return None;
    }
    let status = |value: u64| {
        if value == 1 {
            GeometricDivisionStatus::Unit
        } else if value < modulus {
            GeometricDivisionStatus::ProperFactor
        } else {
            GeometricDivisionStatus::FullCollision
        }
    };
    let content_gcd = gcd(content, modulus);
    let prefix_status = status(first.sum_gcd);
    let (rational_residue, primitive_rational_residue) = if first.sum_gcd == 1 {
        let inverse = modular_inverse(first.sum_residue, modulus)?;
        let ratio = mul_mod(second.sum_residue, inverse, modulus);
        let rational = add_mod(
            coefficient_residue(first_coefficient),
            mul_mod(coefficient_residue(second_coefficient), ratio, modulus),
            modulus,
        );
        let primitive_rational = add_mod(
            coefficient_residue(primitive_first_coefficient),
            mul_mod(
                coefficient_residue(primitive_second_coefficient),
                ratio,
                modulus,
            ),
            modulus,
        );
        if aggregate_residue != mul_mod(first.sum_residue, rational, modulus)
            || primitive_aggregate_residue
                != mul_mod(first.sum_residue, primitive_rational, modulus)
        {
            return None;
        }
        (Some(rational), Some(primitive_rational))
    } else {
        (None, None)
    };
    let first_overlap_gcd = gcd(gcd(first.sum_residue, aggregate_residue), modulus);
    let first_bound_residue = mul_mod(
        second_coefficient.unsigned_abs() % modulus,
        second_factor % modulus,
        modulus,
    );
    let first_public_bound_gcd = gcd(first_bound_residue, modulus);
    let second_overlap_gcd = gcd(gcd(second.sum_residue, aggregate_residue), modulus);
    let second_bound_residue = mul_mod(
        first_coefficient.unsigned_abs() % modulus,
        second_factor % modulus,
        modulus,
    );
    let second_public_bound_gcd = gcd(second_bound_residue, modulus);
    if first_public_bound_gcd % first_overlap_gcd != 0
        || second_public_bound_gcd % second_overlap_gcd != 0
    {
        return None;
    }
    Some(RationalResidueAuditEvaluation {
        first_factor,
        second_factor,
        first_coefficient,
        second_coefficient,
        content,
        primitive_first_coefficient,
        primitive_second_coefficient,
        content_gcd,
        content_status: status(content_gcd),
        first_quotient_residue: first.sum_residue,
        second_quotient_residue: second.sum_residue,
        first_quotient_gcd: first.sum_gcd,
        second_quotient_gcd: second.sum_gcd,
        aggregate_residue,
        aggregate_gcd: gcd(aggregate_residue, modulus),
        primitive_aggregate_residue,
        primitive_aggregate_gcd: gcd(primitive_aggregate_residue, modulus),
        prefix_status,
        rational_residue,
        rational_gcd: rational_residue.map(|value| gcd(value, modulus)),
        primitive_rational_residue,
        primitive_rational_gcd: primitive_rational_residue.map(|value| gcd(value, modulus)),
        first_overlap_gcd,
        first_public_bound_gcd,
        second_overlap_gcd,
        second_public_bound_gcd,
        first_resultant_base: u128::from(second_coefficient.unsigned_abs())
            .checked_mul(u128::from(second_factor))?,
        first_resultant_exponent: first_factor - 1,
        second_resultant_coefficient_base: first_coefficient.unsigned_abs(),
        second_resultant_coefficient_exponent: first_factor.checked_mul(second_factor - 1)?,
        second_resultant_stage_base: second_factor,
        second_resultant_stage_exponent: first_factor - 1,
    })
}

/// Classify when `-S_B(zeta^A)/S_A(zeta)` is rational at primitive order `n`.
pub fn classify_rational_root_orbit(
    first_factor: u64,
    second_factor: u64,
    order: u64,
) -> Option<RationalRootOrbitClassification> {
    if first_factor < 2 || second_factor < 2 || first_factor == second_factor || order < 2 {
        return None;
    }
    let first_zero = first_factor % order == 0;
    let product_mod_order =
        (u128::from(first_factor) * u128::from(second_factor)) % u128::from(order);
    let second_zero = product_mod_order == 0 && !first_zero;
    let outside_stage_zeros = !first_zero && !second_zero;
    let phase_order = u128::from(first_factor) * u128::from(second_factor - 2) + 1;
    let common_step = gcd(first_factor - 1, second_factor - 1);
    let phi4_enabled = first_factor % 4 == 3 && second_factor % 4 == 3;
    let phi6_enabled = first_factor % 6 == 5 && second_factor % 6 == 3;
    let (category, rational_ratio, coefficients) = if !outside_stage_zeros {
        ("stage_zero", None, None)
    } else if (first_factor - 1) % order == 0 && (second_factor - 1) % order == 0 {
        ("common_step", Some(-1), Some((-1, 1)))
    } else if order == 4 && phi4_enabled {
        ("phi4", Some(1), Some((1, 1)))
    } else if order == 6 && phi6_enabled {
        ("phi6", Some(2), Some((2, 1)))
    } else {
        ("irrational", None, None)
    };
    Some(RationalRootOrbitClassification {
        first_factor,
        second_factor,
        order,
        category,
        outside_stage_zeros,
        phase_order,
        phase_divisible: phase_order % u128::from(order) == 0,
        rational_ratio,
        primitive_first_coefficient: coefficients.map(|value| value.0),
        primitive_second_coefficient: coefficients.map(|value| value.1),
        common_step,
        phi4_enabled,
        phi6_enabled,
    })
}

fn geometric_residue(base: u64, modulus: u64, count: u64) -> Option<u64> {
    if count == 0 {
        Some(0)
    } else {
        Some(evaluate_geometric_sum(base, modulus, count)?.sum_residue)
    }
}

fn signed_polynomial_residue(coefficients: &[i64], base: u64, modulus: u64) -> u64 {
    coefficients
        .iter()
        .rev()
        .copied()
        .fold(0, |value, coefficient| {
            let coefficient_residue =
                i128::from(coefficient).rem_euclid(i128::from(modulus)) as u64;
            add_mod(mul_mod(value, base, modulus), coefficient_residue, modulus)
        })
}

fn periodic_residue(pattern: &[i64], length: u64, base: u64, modulus: u64) -> Option<u64> {
    let period = u64::try_from(pattern.len()).ok()?;
    let blocks = length / period;
    let tail = usize::try_from(length % period).ok()?;
    let block = signed_polynomial_residue(pattern, base, modulus);
    let block_sum = geometric_residue(mod_pow(base, period, modulus)?, modulus, blocks)?;
    let tail_value = signed_polynomial_residue(&pattern[..tail], base, modulus);
    Some(add_mod(
        mul_mod(block, block_sum, modulus),
        mul_mod(
            mod_pow(base, blocks.checked_mul(period)?, modulus)?,
            tail_value,
            modulus,
        ),
        modulus,
    ))
}

fn phi6_h_residue(value: u64, modulus: u64) -> Option<u64> {
    Some(add_mod(
        add_mod(
            mod_pow(value, 3, modulus)?,
            mul_mod(2 % modulus, mod_pow(value, 2, modulus)?, modulus),
            modulus,
        ),
        add_mod(mul_mod(2 % modulus, value, modulus), 1 % modulus, modulus),
        modulus,
    ))
}

fn compact_exceptional_cofactor_residue(
    base: u64,
    modulus: u64,
    first_factor: u64,
    second_factor: u64,
    family: &str,
) -> Option<u64> {
    if family == "phi4" {
        let first_blocks = (first_factor - 3) / 4;
        let second_blocks = (second_factor - 3) / 4;
        let first_u = add_mod(
            mul_mod(
                add_mod(1 % modulus, base, modulus),
                geometric_residue(mod_pow(base, 4, modulus)?, modulus, first_blocks)?,
                modulus,
            ),
            mod_pow(base, first_blocks.checked_mul(4)?, modulus)?,
            modulus,
        );
        let nested_base = mod_pow(base, first_factor, modulus)?;
        let nested_u = add_mod(
            mul_mod(
                add_mod(1 % modulus, nested_base, modulus),
                geometric_residue(mod_pow(nested_base, 4, modulus)?, modulus, second_blocks)?,
                modulus,
            ),
            mod_pow(nested_base, second_blocks.checked_mul(4)?, modulus)?,
            modulus,
        );
        let alternating_square =
            (u128::from(modulus) - u128::from(mul_mod(base, base, modulus))) % u128::from(modulus);
        let alternating_square = alternating_square as u64;
        let substituted_factor = geometric_residue(alternating_square, modulus, first_factor)?;
        let first_residual_exponent = first_factor - 2;
        let second_residual_exponent = first_factor.checked_mul(second_factor - 2)?;
        let residual_count = second_residual_exponent.checked_sub(first_residual_exponent)? / 2;
        let residual = mul_mod(
            mod_pow(base, first_residual_exponent, modulus)?,
            geometric_residue(alternating_square, modulus, residual_count)?,
            modulus,
        );
        return Some(add_mod(
            add_mod(
                first_u,
                mul_mod(substituted_factor, nested_u, modulus),
                modulus,
            ),
            residual,
            modulus,
        ));
    }

    let first_blocks = (first_factor - 5) / 6;
    let second_blocks = (second_factor - 3) / 6;
    let first_u = mul_mod(
        phi6_h_residue(base, modulus)?,
        geometric_residue(
            mod_pow(base, 6, modulus)?,
            modulus,
            first_blocks.checked_add(1)?,
        )?,
        modulus,
    );
    let nested_base = mod_pow(base, first_factor, modulus)?;
    let nested_u = add_mod(
        mul_mod(
            phi6_h_residue(nested_base, modulus)?,
            geometric_residue(mod_pow(nested_base, 6, modulus)?, modulus, second_blocks)?,
            modulus,
        ),
        mod_pow(nested_base, second_blocks.checked_mul(6)?, modulus)?,
        modulus,
    );
    let substituted_factor = add_mod(
        periodic_residue(&[1, 1, 0, -1, -1, 0], first_factor, base, modulus)?,
        mul_mod(
            mod_pow(base, first_factor, modulus)?,
            periodic_residue(&[-1, 0, 1, 1, 0, -1], first_factor - 1, base, modulus)?,
            modulus,
        ),
        modulus,
    );
    let fixed_quotient = signed_polynomial_residue(&[-1, -1, 0, 1, 1], base, modulus);
    let residual = mul_mod(
        mul_mod(2 % modulus, mod_pow(base, first_factor, modulus)?, modulus),
        mul_mod(
            fixed_quotient,
            geometric_residue(
                mod_pow(base, 6, modulus)?,
                modulus,
                first_factor.checked_mul(second_blocks)?,
            )?,
            modulus,
        ),
        modulus,
    );
    Some(add_mod(
        add_mod(
            mul_mod(2 % modulus, first_u, modulus),
            mul_mod(substituted_factor, nested_u, modulus),
            modulus,
        ),
        residual,
        modulus,
    ))
}

/// Return exact compact stage and cyclotomic overlap descriptors.
pub fn exceptional_cofactor_overlap(
    first_factor: u64,
    second_factor: u64,
    family: &str,
) -> Option<ExceptionalCofactorOverlap> {
    if first_factor < 2 || second_factor < 2 || first_factor == second_factor {
        return None;
    }
    let product = u128::from(first_factor).checked_mul(u128::from(second_factor))?;
    let cofactor_degree = first_factor
        .checked_mul(second_factor.checked_sub(1)?)?
        .checked_sub(2)?;
    let (
        family,
        order,
        remainder_constant,
        remainder_linear,
        second_stage_power_of_two_exponent,
        stage_overlap_support,
    ) = match family {
        "phi4" if first_factor % 4 == 3 && second_factor % 4 == 3 => {
            let constant_numerator = product
                .checked_add(u128::from(first_factor).checked_mul(2)?)?
                .checked_add(1)?;
            let linear_numerator = product
                .checked_sub(u128::from(first_factor).checked_mul(2)?)?
                .checked_add(1)?;
            (
                "phi4",
                4,
                i128::try_from(constant_numerator / 4).ok()?,
                i128::try_from(linear_numerator / 4).ok()?,
                0,
                "B",
            )
        }
        "phi6" if first_factor % 6 == 5 && second_factor % 6 == 3 => {
            let residual = product
                .checked_sub(u128::from(first_factor).checked_mul(2)?)?
                .checked_add(1)?;
            let linear_numerator = product
                .checked_add(u128::from(first_factor).checked_mul(4)?)?
                .checked_add(4)?;
            (
                "phi6",
                6,
                i128::try_from(residual.checked_mul(2)? / 3)
                    .ok()?
                    .checked_neg()?,
                i128::try_from(linear_numerator / 3).ok()?,
                cofactor_degree,
                "2,B",
            )
        }
        _ => return None,
    };
    let constant_square = remainder_constant.checked_mul(remainder_constant)?;
    let linear_square = remainder_linear.checked_mul(remainder_linear)?;
    let resultant = if family == "phi4" {
        constant_square.checked_add(linear_square)?
    } else {
        constant_square
            .checked_add(remainder_constant.checked_mul(remainder_linear)?)?
            .checked_add(linear_square)?
    };
    Some(ExceptionalCofactorOverlap {
        family,
        order,
        first_factor,
        second_factor,
        cofactor_degree,
        remainder_constant,
        remainder_linear,
        cyclotomic_cofactor_resultant: u128::try_from(resultant).ok()?,
        first_stage_resultant_base: second_factor,
        first_stage_resultant_exponent: first_factor - 1,
        second_stage_power_of_two_exponent,
        second_stage_resultant_base: second_factor,
        second_stage_resultant_exponent: first_factor - 1,
        stage_overlap_support,
    })
}

/// Account for the balanced prime pairs touched by nonzero exact integers.
pub fn length_indexed_support_profile(
    input_length: u32,
    primes: &[u64],
    charged_values: &[i64],
) -> Option<LengthIndexedSupportProfile> {
    if input_length < 4 || primes.len() < 2 {
        return None;
    }
    for (index, prime) in primes.iter().copied().enumerate() {
        if !is_prime(prime) || primes[..index].contains(&prime) {
            return None;
        }
        for second_prime in primes[index + 1..].iter().copied() {
            let product = u128::from(prime).checked_mul(u128::from(second_prime))?;
            let product_bits = u128::BITS - product.leading_zeros();
            if product_bits != input_length {
                return None;
            }
        }
    }
    if charged_values.iter().any(|value| *value == 0) {
        return None;
    }
    let materialized_bit_budget = charged_values.iter().try_fold(0_u64, |total, value| {
        let absolute = value.unsigned_abs();
        let bit_length = u64::from(u64::BITS - absolute.leading_zeros());
        total.checked_add(bit_length)
    })?;
    let hit_primes = primes
        .iter()
        .copied()
        .filter(|prime| {
            charged_values
                .iter()
                .any(|value| value.unsigned_abs() % prime == 0)
        })
        .collect::<Vec<_>>();
    let missed_primes = primes
        .iter()
        .copied()
        .filter(|prime| !hit_primes.contains(prime))
        .collect::<Vec<_>>();
    let population_size = u64::try_from(primes.len()).ok()?;
    let charged_value_count = u64::try_from(charged_values.len()).ok()?;
    let hit_prime_count = u64::try_from(hit_primes.len()).ok()?;
    let missed_count = u64::try_from(missed_primes.len()).ok()?;
    let pair_count = population_size.checked_mul(population_size.checked_sub(1)?)? / 2;
    let forced_miss_pair_count = missed_count.checked_mul(missed_count.saturating_sub(1))? / 2;
    let min_prime_log2_floor = primes
        .iter()
        .map(|prime| u64::BITS - prime.leading_zeros() - 1)
        .min()?;
    if min_prime_log2_floor == 0 {
        return None;
    }
    let support_cap =
        population_size.min(materialized_bit_budget / u64::from(min_prime_log2_floor));
    Some(LengthIndexedSupportProfile {
        input_length,
        population_size,
        min_prime_log2_floor,
        charged_value_count,
        materialized_bit_budget,
        hit_primes,
        missed_primes,
        hit_prime_count,
        forced_miss_pair_count,
        pair_count,
        maximum_coverable_pair_count: pair_count.checked_sub(forced_miss_pair_count)?,
        support_cap,
        necessary_universal_bit_budget: u64::from(min_prime_log2_floor)
            .checked_mul(population_size.checked_sub(1)?)?,
    })
}

/// Test one prime against `A=3, B=2^level+3, g=2` without an exact lift.
pub fn compact_phi4_prime_profile(level: u32, prime: u64) -> Option<CompactPhi4PrimeProfile> {
    if level < 2 || !is_prime(prime) {
        return None;
    }
    let power_of_two = 1_u64.checked_shl(level)?;
    let second_factor = power_of_two.checked_add(3)?;
    let exponent = power_of_two.checked_mul(3)?.checked_add(5)?;
    if prime == 2 {
        return Some(CompactPhi4PrimeProfile {
            level,
            prime,
            second_factor,
            exponent,
            cofactor_residue: 0,
            criterion_residue: 1,
            divides: true,
            rule: "two_adic",
        });
    }
    let cofactor_residue =
        compact_exceptional_cofactor_residue(2, prime, 3, second_factor, "phi4")?;
    let power_residue = mod_pow(2, exponent, prime)?;
    let criterion_residue = ((u128::from(power_residue) + 3) % u128::from(prime)) as u64;
    let (divides, rule) = match prime {
        3 => (false, "three_exception"),
        5 => (level % 4 == 2, "five_quotient"),
        7 => (level % 3 == 2, "seven_quotient"),
        _ => (criterion_residue == 0, "generic_congruence"),
    };
    if divides != (cofactor_residue == 0) {
        return None;
    }
    Some(CompactPhi4PrimeProfile {
        level,
        prime,
        second_factor,
        exponent,
        cofactor_residue,
        criterion_residue,
        divides,
        rule,
    })
}

/// Evaluate the direct-factor, unit-cofactor, and full-collision branches.
pub fn evaluate_exceptional_cyclotomic(
    base: u64,
    modulus: u64,
    first_factor: u64,
    second_factor: u64,
    family: &str,
) -> Option<ExceptionalCyclotomicEvaluation> {
    if modulus < 2 || first_factor < 2 || second_factor < 2 || first_factor == second_factor {
        return None;
    }
    let base = base % modulus;
    if gcd(base, modulus) != 1 {
        return None;
    }
    let (family, order, first_coefficient) = match family {
        "phi4" if first_factor % 4 == 3 && second_factor % 4 == 3 => ("phi4", 4, 1),
        "phi6" if first_factor % 6 == 5 && second_factor % 6 == 3 => ("phi6", 6, 2),
        _ => return None,
    };
    let audit = evaluate_rational_residue_audit(
        base,
        modulus,
        first_factor,
        second_factor,
        first_coefficient,
        1,
    )?;
    let square = u128::from(base) * u128::from(base);
    let cyclotomic_residue = if family == "phi4" {
        ((square + 1) % u128::from(modulus)) as u64
    } else {
        ((square + u128::from(modulus) - u128::from(base) + 1) % u128::from(modulus)) as u64
    };
    let status = |value: u64| {
        if value == 1 {
            GeometricDivisionStatus::Unit
        } else if value < modulus {
            GeometricDivisionStatus::ProperFactor
        } else {
            GeometricDivisionStatus::FullCollision
        }
    };
    let cyclotomic_gcd = gcd(cyclotomic_residue, modulus);
    let cyclotomic_status = status(cyclotomic_gcd);
    let aggregate_status = status(audit.aggregate_gcd);
    let cofactor =
        compact_exceptional_cofactor_residue(base, modulus, first_factor, second_factor, family)?;
    if mul_mod(cyclotomic_residue, cofactor, modulus) != audit.aggregate_residue {
        return None;
    }
    let cofactor_gcd_value = gcd(cofactor, modulus);
    let cofactor_status_value = status(cofactor_gcd_value);
    if cyclotomic_status == GeometricDivisionStatus::Unit
        && cofactor_gcd_value != audit.aggregate_gcd
    {
        return None;
    }
    let (extraction_source, extraction_gcd) =
        if cyclotomic_status == GeometricDivisionStatus::ProperFactor {
            ("cyclotomic", Some(cyclotomic_gcd))
        } else if cofactor_status_value == GeometricDivisionStatus::ProperFactor {
            ("cofactor", Some(cofactor_gcd_value))
        } else if cyclotomic_status == GeometricDivisionStatus::FullCollision {
            if audit.aggregate_gcd != modulus {
                return None;
            }
            ("full_collision", None)
        } else {
            ("none", None)
        };
    let dense_cofactor_degree = first_factor
        .checked_mul(second_factor - 1)?
        .checked_sub(2)?;
    Some(ExceptionalCyclotomicEvaluation {
        base,
        modulus,
        family,
        order,
        first_factor,
        second_factor,
        first_coefficient,
        second_coefficient: 1,
        cyclotomic_residue,
        cyclotomic_gcd,
        cyclotomic_status,
        aggregate_residue: audit.aggregate_residue,
        aggregate_gcd: audit.aggregate_gcd,
        aggregate_status,
        cofactor_residue: Some(cofactor),
        cofactor_gcd: Some(cofactor_gcd_value),
        cofactor_status: Some(cofactor_status_value),
        extraction_source,
        extraction_gcd,
        first_quotient_gcd: audit.first_quotient_gcd,
        second_quotient_gcd: audit.second_quotient_gcd,
        first_public_bound_gcd: audit.first_public_bound_gcd,
        second_public_bound_gcd: audit.second_public_bound_gcd,
        dense_cofactor_degree,
        dense_cofactor_coefficient_count: dense_cofactor_degree.checked_add(1)?,
    })
}

/// Return `ceil(log2(exponent))`, the generic multiplication growth lower bound.
pub fn generic_multiplication_lower_bound(exponent: u64) -> Option<u32> {
    if exponent == 0 {
        return None;
    }
    Some(if exponent == 1 {
        0
    } else {
        u64::BITS - (exponent - 1).leading_zeros()
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn modular_power_handles_wide_products() {
        assert_eq!(mod_pow(u64::MAX - 1, 2, u64::MAX - 58), Some(3249));
    }

    #[test]
    fn perfect_power_uses_maximal_exponent() {
        assert_eq!(perfect_power(64), Some((2, 6)));
        assert_eq!(perfect_power(72), None);
    }

    #[test]
    fn trial_primality_rejects_carmichael_number() {
        assert!(!is_prime(561));
        assert_eq!(trial_division(561), Some(3));
    }

    #[test]
    fn batch_gcd_preserves_per_item_results() {
        assert_eq!(batch_gcd(&[2, 6, 35, 11], 105), Some(vec![1, 3, 35, 1]));
    }

    #[test]
    fn divisor_cover_does_not_imply_profile_separation() {
        assert_eq!(
            analyze_divisor_cover(&[2], &[1, 2]),
            Some(CoverAnalysis {
                divisor_cover: true,
                separates_profile: false,
                distinct_signatures: false,
            })
        );
        assert_eq!(
            analyze_divisor_cover(&[1, 2], &[1, 2]),
            Some(CoverAnalysis {
                divisor_cover: true,
                separates_profile: true,
                distinct_signatures: true,
            })
        );
        assert_eq!(analyze_divisor_cover(&[], &[1, 2]), None);
    }

    #[test]
    fn combined_promise_signature_has_exact_magnitude_barrier() {
        assert_eq!(
            combined_promise_signature(3, &[4, 6]),
            Some(vec![(true, true), (true, false)])
        );
        assert_eq!(
            combined_promise_signature(17, &[4, 6, 12]),
            Some(vec![(false, false); 3])
        );
        assert_eq!(combined_promise_asymmetry(3, 5, &[4, 6]), Some(true));
        assert_eq!(combined_promise_asymmetry(17, 19, &[4, 6, 12]), Some(false));
        assert_eq!(
            combined_promise_hit_count(&[3, 5, 7, 11, 13, 17, 19], &[4, 6]),
            Some(3)
        );
        assert_eq!(combined_promise_signature(9, &[4]), None);
        assert_eq!(combined_promise_asymmetry(3, 3, &[4]), None);
    }

    #[test]
    fn divisor_count_covers_large_value_collision_budget_vectors() {
        assert_eq!(divisor_count(1), Some(1));
        assert_eq!(divisor_count(7), Some(2));
        assert_eq!(divisor_count(840), Some(32));
        assert_eq!(divisor_count(720_720), Some(240));
        assert_eq!(divisor_count(0), None);
    }

    #[test]
    fn multiplication_program_tracks_formal_exponents_and_residues() {
        let steps = [(0, 0), (1, 0), (2, 2), (3, 1)];
        assert_eq!(
            evaluate_multiplication_program(11, 143, &steps),
            Some(StraightLineEvaluation {
                exponents: vec![1, 2, 3, 6, 8],
                residues: vec![11, 121, 44, 77, 22],
            })
        );
        assert_eq!(evaluate_multiplication_program(2, 5, &[(0, 1)]), None);
        assert_eq!(evaluate_multiplication_program(2, 1, &[]), None);
    }

    #[test]
    fn addition_subtraction_program_tracks_signed_exponents_and_units() {
        let steps = [(0, 0, 1), (1, 0, -1), (0, 1, -1), (3, 3, 1), (2, 2, -1)];
        let evaluation = evaluate_addition_subtraction_program(5, 77, &steps)
            .expect("unit-base signed program must evaluate");
        assert_eq!(evaluation.exponents, vec![1, 2, 1, -1, -2, 0]);
        assert_eq!(evaluation.inversion_count, 3);
        assert_eq!(evaluation.residues, vec![5, 25, 5, 31, 37, 1]);
        assert_eq!(evaluate_addition_subtraction_program(7, 77, &[]), None);
        assert_eq!(
            evaluate_addition_subtraction_program(5, 77, &[(0, 0, 0)]),
            None
        );
    }

    #[test]
    fn batch_product_materializes_leaves_and_can_mask_separators() {
        assert_eq!(
            evaluate_batch_product(2, 21, &[2, 3]),
            Some(BatchProductEvaluation {
                exponents: vec![2, 3],
                leaf_residues: vec![3, 7],
                leaf_gcds: vec![3, 7],
                root_residue: 0,
                root_gcd: 21,
                multiplication_count: 1,
            })
        );
        let odd = evaluate_batch_product(2, 35, &[1, 2, 3])
            .expect("canonical unit-base batch must evaluate");
        assert_eq!(odd.multiplication_count, 2);
        assert_eq!(odd.root_residue, 21);
        assert_eq!(evaluate_batch_product(5, 35, &[1]), None);
        assert_eq!(evaluate_batch_product(2, 35, &[2, 2]), None);
    }

    #[test]
    fn product_dag_tracks_multiplicities_without_unfolding() {
        assert_eq!(
            evaluate_product_dag(2, 21, &[2, 3], &[(0, 1)]),
            Some(ProductDagEvaluation {
                exponents: vec![2, 3],
                atom_residues: vec![3, 7],
                atom_gcds: vec![3, 7],
                node_residues: vec![3, 7, 0],
                node_gcds: vec![3, 7, 21],
                multiplicities: vec![vec![1, 0], vec![0, 1], vec![1, 1]],
                occurrence_counts: vec![1, 1, 2],
            })
        );
        let repeated = evaluate_product_dag(4, 9, &[1], &[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)])
            .expect("repeated product DAG must evaluate");
        assert_eq!(repeated.atom_gcds, vec![3]);
        assert_eq!(repeated.node_gcds[1], 9);
        assert_eq!(repeated.multiplicities[5], vec![32]);
        assert_eq!(repeated.occurrence_counts[5], 32);
        assert_eq!(evaluate_product_dag(5, 35, &[1], &[]), None);
        assert_eq!(evaluate_product_dag(2, 35, &[2, 2], &[]), None);
        assert_eq!(evaluate_product_dag(2, 35, &[1], &[(0, 1)]), None);
    }

    #[test]
    fn dyadic_telescope_has_total_division_and_product_paths() {
        let proper = evaluate_dyadic_telescope(4, 15, 1).expect("valid telescope");
        assert_eq!(proper.denominator_gcd, 3);
        assert_eq!(proper.factor_gcds, vec![5]);
        assert_eq!(proper.numerator_gcd, 15);
        assert_eq!(proper.division_status, DyadicDivisionStatus::ProperFactor);
        assert_eq!(proper.division_quotient, None);

        let full = evaluate_dyadic_telescope(1, 6, 3).expect("valid telescope");
        assert_eq!(full.denominator_gcd, 6);
        assert_eq!(full.quotient_gcd, 2);
        assert_eq!(full.division_status, DyadicDivisionStatus::FullCollision);

        let unit = evaluate_dyadic_telescope(2, 35, 3).expect("valid telescope");
        assert_eq!(unit.division_status, DyadicDivisionStatus::Unit);
        assert_eq!(unit.division_quotient, Some(unit.quotient_residue));
        assert_eq!(unit.formal_monomial_count, 8);
        assert_eq!(unit.formal_degree, 7);
    }

    #[test]
    fn arbitrary_geometric_sum_reduces_each_denominator_branch() {
        let unit = evaluate_geometric_sum(2, 15, 2).expect("valid geometric sum");
        assert_eq!(unit.division_status, GeometricDivisionStatus::Unit);
        assert_eq!(unit.division_quotient, Some(unit.sum_residue));
        assert_eq!(unit.sum_gcd, 3);
        assert_eq!(unit.sum_gcd, unit.numerator_gcd);

        let proper = evaluate_geometric_sum(4, 15, 2).expect("valid geometric sum");
        assert_eq!(
            proper.division_status,
            GeometricDivisionStatus::ProperFactor
        );
        assert_eq!(proper.denominator_gcd, 3);
        assert_eq!(proper.sum_gcd, 5);
        assert_eq!(proper.numerator_gcd, 15);

        let full = evaluate_geometric_sum(1, 15, 5).expect("valid geometric sum");
        assert_eq!(full.division_status, GeometricDivisionStatus::FullCollision);
        assert_eq!(full.sum_residue, 5);
        assert_eq!(full.sum_gcd, full.exponent_gcd);

        let repeated = evaluate_geometric_sum(1, 8, 4).expect("valid geometric sum");
        assert_eq!(repeated.sum_gcd, 4);
        assert_eq!(repeated.exponent_gcd, 4);

        let base_case = evaluate_geometric_sum(2, 257, 1).expect("valid geometric sum");
        assert_eq!(base_case.power_residue, 2);
        assert_eq!(base_case.sum_residue, 1);
        assert_eq!(base_case.multiplication_count, 0);
        assert_eq!(base_case.addition_count, 0);
        assert_eq!(evaluate_geometric_sum(5, 15, 3), None);
        assert_eq!(evaluate_geometric_sum(2, 15, 0), None);
    }

    #[test]
    fn nested_quotient_has_total_intermediate_and_composed_paths() {
        let proper = evaluate_nested_quotient(2, 15, 2, 2).expect("valid quotient");
        assert_eq!(proper.intermediate_gcd, 3);
        assert_eq!(proper.quotient_gcd, 5);
        assert_eq!(proper.rational_numerator_gcd, 15);

        let full = evaluate_nested_quotient(2, 15, 4, 5).expect("valid quotient");
        assert_eq!(full.intermediate_gcd, 15);
        assert_eq!(full.inner_power_residue, 1);
        assert_eq!(full.quotient_gcd, full.multiplier_gcd);
    }

    #[test]
    fn iterated_quotient_links_prefixes_and_reduces_every_stage() {
        let value = evaluate_iterated_quotient(2, 15, &[2, 2, 3]).expect("valid iterated quotient");
        assert_eq!(value.prefix_exponents, vec![1, 2, 4, 12]);
        assert_eq!(
            value.final_prefix_residue,
            value.final_quotient_product_residue
        );
        assert_eq!(value.stages[1].intermediate_gcd, 3);
        assert_eq!(value.stages[1].quotient_gcd, 5);
        assert_eq!(value.stages[1].rational_numerator_gcd, 15);

        let full = evaluate_iterated_quotient(2, 15, &[4, 5, 2]).expect("valid full-prefix chain");
        assert_eq!(full.stages[1].intermediate_gcd, 15);
        assert_eq!(full.stages[1].quotient_gcd, full.stages[1].multiplier_gcd);

        assert_eq!(evaluate_iterated_quotient(2, 15, &[]), None);
        assert_eq!(evaluate_iterated_quotient(2, 15, &[2, 0]), None);
        assert_eq!(evaluate_iterated_quotient(5, 15, &[2]), None);
    }

    #[test]
    fn quotient_linear_combination_can_reveal_a_new_proper_factor() {
        let value = evaluate_quotient_linear_combination(2, 9, &[5, 5], &[-1, 1])
            .expect("valid quotient linear combination");
        assert_eq!(value.chain.prefix_exponents, vec![1, 5, 25]);
        assert_eq!(
            value
                .chain
                .stages
                .iter()
                .map(|stage| stage.quotient_residue)
                .collect::<Vec<_>>(),
            vec![4, 7]
        );
        assert_eq!(value.coefficient_residues, vec![8, 1]);
        assert_eq!(value.coefficient_gcds, vec![1, 1]);
        assert_eq!(value.weighted_stage_residues, vec![5, 7]);
        assert_eq!(value.weighted_stage_gcds, vec![1, 1]);
        assert_eq!(value.aggregate_residue, 3);
        assert_eq!(value.aggregate_gcd, 3);
        assert_eq!(
            evaluate_quotient_linear_combination(2, 9, &[5, 5], &[-1]),
            None
        );
    }

    #[test]
    fn symmetric_difference_has_total_endpoint_and_cofactor_paths() {
        let endpoint =
            evaluate_symmetric_quotient_difference(2, 9, 5).expect("valid symmetric difference");
        assert_eq!(endpoint.first_quotient_residue, 4);
        assert_eq!(endpoint.second_quotient_residue, 7);
        assert_eq!(endpoint.difference_gcd, 3);
        assert_eq!(endpoint.endpoint_gcd, 3);
        assert_eq!(
            endpoint.endpoint_status,
            GeometricDivisionStatus::ProperFactor
        );

        let cofactor = evaluate_symmetric_quotient_difference(2, 55, 3)
            .expect("valid cofactor-only difference");
        assert_eq!(cofactor.endpoint_gcd, 1);
        assert_eq!(cofactor.cofactor_residue, 11);
        assert_eq!(cofactor.cofactor_gcd, 11);
        assert_eq!(cofactor.difference_gcd, 11);
        assert_eq!(cofactor.division_cofactor, Some(11));

        assert_eq!(evaluate_symmetric_quotient_difference(2, 9, 1), None);
        assert_eq!(evaluate_symmetric_quotient_difference(3, 9, 5), None);
    }

    #[test]
    fn unequal_signed_reduction_has_total_prefix_and_difference_paths() {
        let cofactor =
            evaluate_unequal_signed_reduction(3, 25, 3, 2, -1, 1).expect("valid unequal reduction");
        assert_eq!(cofactor.first_quotient_residue, 13);
        assert_eq!(cofactor.second_quotient_residue, 3);
        assert_eq!(cofactor.aggregate_gcd, 5);
        assert_eq!(cofactor.rational_reduction_residue, Some(5));
        assert_eq!(cofactor.rational_reduction_gcd, Some(5));
        assert_eq!(cofactor.common_step, 1);
        assert_eq!(cofactor.common_factor_gcd, 1);
        assert_eq!(cofactor.difference_cofactor_gcd, Some(5));

        let common =
            evaluate_unequal_signed_reduction(2, 9, 5, 7, -1, 1).expect("valid common-step path");
        assert_eq!(common.common_step, 2);
        assert_eq!(common.common_factor_gcd, 3);
        assert_eq!(common.difference_gcd, 3);

        let proper = evaluate_unequal_signed_reduction(2, 15, 2, 3, 1, -1)
            .expect("valid proper-prefix path");
        assert_eq!(
            proper.first_quotient_status,
            GeometricDivisionStatus::ProperFactor
        );
        assert_eq!(proper.first_quotient_gcd, 3);

        let full =
            evaluate_unequal_signed_reduction(2, 15, 4, 5, 1, 2).expect("valid full-prefix path");
        assert_eq!(
            full.first_quotient_status,
            GeometricDivisionStatus::FullCollision
        );
        assert_eq!(full.aggregate_gcd, full.public_full_gcd);
        assert_eq!(evaluate_unequal_signed_reduction(2, 9, 3, 3, -1, 1), None);
    }

    #[test]
    fn rational_residue_audit_isolates_content_and_stage_overlap() {
        let phi4 = evaluate_rational_residue_audit(2, 55, 3, 7, 1, 1).expect("valid Phi_4 witness");
        assert_eq!(phi4.first_quotient_gcd, 1);
        assert_eq!(phi4.second_quotient_gcd, 1);
        assert_eq!(phi4.aggregate_gcd, 5);
        assert_eq!(phi4.rational_gcd, Some(5));
        assert_eq!(phi4.first_public_bound_gcd, 1);
        assert_eq!(phi4.second_public_bound_gcd, 1);

        let proper_content =
            evaluate_rational_residue_audit(2, 55, 3, 7, 5, 10).expect("valid proper-content path");
        assert_eq!(proper_content.content_gcd, 5);
        assert_eq!(
            proper_content.content_status,
            GeometricDivisionStatus::ProperFactor
        );
        assert_eq!(proper_content.primitive_aggregate_gcd, 1);

        let full_content =
            evaluate_rational_residue_audit(2, 5, 3, 7, 5, 10).expect("valid full-content path");
        assert_eq!(
            full_content.content_status,
            GeometricDivisionStatus::FullCollision
        );
        assert_eq!(full_content.aggregate_gcd, 5);
    }

    #[test]
    fn rational_root_orbit_has_exactly_three_families() {
        let common = classify_rational_root_orbit(4, 7, 3).expect("valid common-step family");
        assert_eq!(common.category, "common_step");
        assert_eq!(common.rational_ratio, Some(-1));
        assert_eq!(common.primitive_first_coefficient, Some(-1));
        assert_eq!(common.primitive_second_coefficient, Some(1));

        let phi4 = classify_rational_root_orbit(3, 7, 4).expect("valid Phi_4 family");
        assert_eq!(phi4.category, "phi4");
        assert_eq!(phi4.rational_ratio, Some(1));

        let phi6 = classify_rational_root_orbit(5, 3, 6).expect("valid Phi_6 family");
        assert_eq!(phi6.category, "phi6");
        assert_eq!(phi6.rational_ratio, Some(2));

        let obstruction =
            classify_rational_root_orbit(2, 4, 5).expect("valid phase-only obstruction");
        assert!(obstruction.phase_divisible);
        assert_eq!(obstruction.category, "irrational");
        assert_eq!(classify_rational_root_orbit(3, 3, 4), None);
    }

    #[test]
    fn exceptional_cyclotomic_trichotomy_and_residual_witnesses() {
        let direct =
            evaluate_exceptional_cyclotomic(2, 55, 3, 7, "phi4").expect("valid direct witness");
        assert_eq!(
            direct.cyclotomic_status,
            GeometricDivisionStatus::ProperFactor
        );
        assert_eq!(direct.extraction_source, "cyclotomic");
        assert_eq!(direct.extraction_gcd, Some(5));

        let full =
            evaluate_exceptional_cyclotomic(2, 5, 3, 7, "phi4").expect("valid full collision");
        assert_eq!(
            full.cyclotomic_status,
            GeometricDivisionStatus::FullCollision
        );
        assert_eq!(
            full.aggregate_status,
            GeometricDivisionStatus::FullCollision
        );

        for (base, modulus, first_factor, second_factor, family, expected) in [
            (11, 15, 3, 7, "phi4", 5),
            (4, 9, 11, 7, "phi4", 3),
            (8, 35, 5, 3, "phi6", 5),
            (3, 25, 5, 3, "phi6", 5),
        ] {
            let value =
                evaluate_exceptional_cyclotomic(base, modulus, first_factor, second_factor, family)
                    .expect("valid residual witness");
            assert_eq!(value.cyclotomic_status, GeometricDivisionStatus::Unit);
            assert_eq!(value.extraction_source, "cofactor");
            assert_eq!(value.extraction_gcd, Some(expected));
            assert_eq!(value.first_quotient_gcd, 1);
            assert_eq!(value.second_quotient_gcd, 1);
            assert_eq!(value.first_public_bound_gcd, 1);
            assert_eq!(value.second_public_bound_gcd, 1);
        }
        assert_eq!(evaluate_exceptional_cyclotomic(2, 15, 5, 7, "phi4"), None);
    }

    #[test]
    fn exceptional_cofactor_overlap_descriptors_are_exact() {
        let phi4 = exceptional_cofactor_overlap(3, 7, "phi4").expect("valid phi4");
        assert_eq!(phi4.remainder_constant, 7);
        assert_eq!(phi4.remainder_linear, 4);
        assert_eq!(phi4.cyclotomic_cofactor_resultant, 65);
        assert_eq!(phi4.stage_overlap_support, "B");

        let phi6 = exceptional_cofactor_overlap(5, 3, "phi6").expect("valid phi6");
        assert_eq!(phi6.remainder_constant, -4);
        assert_eq!(phi6.remainder_linear, 13);
        assert_eq!(phi6.cyclotomic_cofactor_resultant, 133);
        assert_eq!(phi6.second_stage_power_of_two_exponent, 8);
        assert_eq!(phi6.stage_overlap_support, "2,B");
        assert_eq!(exceptional_cofactor_overlap(5, 7, "phi4"), None);
    }

    #[test]
    fn length_indexed_support_accounting_is_exact() {
        let profile = length_indexed_support_profile(12, &[47, 53, 59, 61], &[47 * 53, -5])
            .expect("valid balanced population");
        assert_eq!(profile.hit_primes, vec![47, 53]);
        assert_eq!(profile.missed_primes, vec![59, 61]);
        assert_eq!(profile.forced_miss_pair_count, 1);
        assert_eq!(profile.pair_count, 6);
        assert_eq!(profile.maximum_coverable_pair_count, 5);
        assert!(profile.hit_prime_count <= profile.support_cap);
        assert_eq!(length_indexed_support_profile(11, &[23, 29], &[23]), None);
        assert_eq!(length_indexed_support_profile(10, &[23, 29], &[0]), None);
    }

    #[test]
    fn compact_phi4_prime_divisibility_rules_are_exact() {
        for (level, prime, expected, rule) in [
            (2, 2, true, "two_adic"),
            (2, 3, false, "three_exception"),
            (2, 5, true, "five_quotient"),
            (3, 5, false, "five_quotient"),
            (2, 7, true, "seven_quotient"),
            (3, 7, false, "seven_quotient"),
            (2, 107, true, "generic_congruence"),
            (4, 11, true, "generic_congruence"),
            (2, 109, false, "generic_congruence"),
        ] {
            let profile = compact_phi4_prime_profile(level, prime).expect("valid prime profile");
            assert_eq!(profile.divides, expected);
            assert_eq!(profile.rule, rule);
            assert_eq!(profile.divides, profile.cofactor_residue == 0);
            if prime > 7 {
                assert_eq!(profile.divides, profile.criterion_residue == 0);
            }
        }
        assert_eq!(compact_phi4_prime_profile(1, 11), None);
        assert_eq!(compact_phi4_prime_profile(2, 9), None);
    }

    #[test]
    fn multiplication_growth_lower_bound_is_exact_on_powers_of_two() {
        assert_eq!(generic_multiplication_lower_bound(1), Some(0));
        assert_eq!(generic_multiplication_lower_bound(3), Some(2));
        assert_eq!(generic_multiplication_lower_bound(1 << 32), Some(32));
        assert_eq!(generic_multiplication_lower_bound(0), None);
    }

    #[test]
    fn invalid_moduli_are_rejected() {
        assert_eq!(mod_pow(2, 10, 0), None);
        assert_eq!(lucas_v(5, 4, 0), None);
        assert_eq!(batch_gcd(&[1], 0), None);
    }

    #[test]
    fn lucas_matrix_matches_recurrence() {
        let parameter = 4_u64;
        let modulus = 667_u64;
        let mut recurrence = vec![2, parameter];
        for index in 2..20 {
            let value =
                (parameter * recurrence[index - 1] + modulus - recurrence[index - 2]) % modulus;
            recurrence.push(value);
        }
        let matrix_values = (0..20)
            .map(|index| lucas_v(index, parameter, modulus).expect("positive modulus"))
            .collect::<Vec<_>>();
        assert_eq!(matrix_values, recurrence);
    }

    #[test]
    fn bounded_rho_has_success_and_failure_vectors() {
        assert_eq!(pollard_rho(8051, 0, 10_000), Some(83));
        assert_eq!(pollard_rho(97, 0, 1_000), None);
        assert_eq!(pollard_rho(8051, 0, 1), None);
    }

    #[test]
    fn stage_one_methods_separate_and_collide_as_expected() {
        assert_eq!(pollard_p_minus_one(10_807, 25, 2), Some(101));
        assert_eq!(pollard_p_minus_one(10_403, 25, 2), None);
        assert_eq!(pollard_p_plus_one(667, 5, 4), Some(29));
        assert_eq!(pollard_p_plus_one(667, 2, 4), None);
    }

    #[test]
    fn separator_candidate_reports_every_branch() {
        assert_eq!(
            evaluate_separator_candidate(15, 3, 1),
            Some(SeparatorOutcome::DirectFactor(3))
        );
        assert_eq!(
            evaluate_separator_candidate(15, 0, 1),
            Some(SeparatorOutcome::InvalidBase)
        );
        assert_eq!(
            evaluate_separator_candidate(15, 2, 1),
            Some(SeparatorOutcome::Miss { residue: 2 })
        );
        assert_eq!(
            evaluate_separator_candidate(15, 2, 2),
            Some(SeparatorOutcome::Factor {
                factor: 3,
                residue: 4
            })
        );
        assert_eq!(
            evaluate_separator_candidate(15, 4, 2),
            Some(SeparatorOutcome::SimultaneousCollision { residue: 1 })
        );
        assert_eq!(evaluate_separator_candidate(1, 2, 1), None);
        assert_eq!(evaluate_separator_candidate(15, 2, 0), None);
    }

    #[test]
    fn lucas_candidate_reports_every_branch() {
        assert_eq!(
            evaluate_lucas_separator_candidate(15, 5, 3),
            Some(LucasSeparatorOutcome::DiscriminantFactor(3))
        );
        assert_eq!(
            evaluate_lucas_separator_candidate(15, 13, 1),
            Some(LucasSeparatorOutcome::DegenerateMiss { residue: 13 })
        );
        assert_eq!(
            evaluate_lucas_separator_candidate(15, 8, 1),
            Some(LucasSeparatorOutcome::DegenerateFactor {
                factor: 3,
                residue: 8,
            })
        );
        assert_eq!(
            evaluate_lucas_separator_candidate(15, 2, 3),
            Some(LucasSeparatorOutcome::DegenerateCollision { residue: 2 })
        );
        assert_eq!(
            evaluate_lucas_separator_candidate(15, 6, 1),
            Some(LucasSeparatorOutcome::Miss { residue: 6 })
        );
        assert_eq!(
            evaluate_lucas_separator_candidate(35, 20, 3),
            Some(LucasSeparatorOutcome::Factor {
                factor: 7,
                residue: 30,
            })
        );
        assert_eq!(
            evaluate_lucas_separator_candidate(6, 3, 12),
            Some(LucasSeparatorOutcome::SimultaneousCollision { residue: 2 })
        );
    }

    #[test]
    fn semismooth_family_has_factor_failure_and_overflow_paths() {
        assert_eq!(semismooth_factor(15, 2, 2, 1), SemismoothOutcome::Factor(3));
        assert_eq!(
            semismooth_factor(21, 2, 3, 1),
            SemismoothOutcome::Unresolved
        );
        assert_eq!(semismooth_factor(21, 3, 3, 1), SemismoothOutcome::Factor(3));
        assert_eq!(
            semismooth_factor(15, 2, 2, 0),
            SemismoothOutcome::InvalidParameters
        );
        assert_eq!(
            semismooth_factor(15, 2, 64, 1),
            SemismoothOutcome::ExponentOverflow
        );
    }

    #[test]
    fn semismooth_success_count_covers_fixed_base_collision() {
        let count = semismooth_successful_residue_count(51, 840).unwrap();
        assert!(12 * count >= 5 * 51);
        assert_eq!(semismooth_successful_residue_count(1, 840), None);
    }

    #[test]
    fn deterministic_modular_power_property() {
        let mut state = 0x004d_4f53_4546_u64;
        for _ in 0..500 {
            state = state
                .wrapping_mul(6_364_136_223_846_793_005)
                .wrapping_add(1);
            let base = state;
            state = state
                .wrapping_mul(6_364_136_223_846_793_005)
                .wrapping_add(1);
            let exponent = state % 64;
            state = state
                .wrapping_mul(6_364_136_223_846_793_005)
                .wrapping_add(1);
            let modulus = state % 10_000 + 1;
            let mut expected = 1 % modulus;
            for _ in 0..exponent {
                expected = ((expected as u128 * base as u128) % modulus as u128) as u64;
            }
            assert_eq!(mod_pow(base, exponent, modulus), Some(expected));
        }
    }

    #[test]
    fn trial_division_matches_exhaustive_small_oracle() {
        for n in 2_u64..5_000 {
            let expected = (2..n).find(|candidate| n % candidate == 0);
            assert_eq!(trial_division(n), expected, "n={n}");
        }
    }
}
