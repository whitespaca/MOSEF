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
