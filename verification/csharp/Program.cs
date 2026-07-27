using System.Numerics;

namespace MosefVerifier;

internal static class Program
{
    private static BigInteger Parse(string[] args, int index, string name)
    {
        if (index >= args.Length || !BigInteger.TryParse(args[index], out BigInteger value))
        {
            throw new ArgumentException($"invalid or missing {name}");
        }
        return value;
    }

    private static BigInteger? TrialFactor(BigInteger n)
    {
        if (n < 2)
        {
            return null;
        }
        if (n % 2 == 0)
        {
            return n == 2 ? null : 2;
        }
        for (BigInteger divisor = 3; divisor <= n / divisor; divisor += 2)
        {
            if (n % divisor == 0)
            {
                return divisor;
            }
        }
        return null;
    }

    private static bool IsPrime(BigInteger n)
    {
        return n >= 2 && TrialFactor(n) is null;
    }

    private static BigInteger Gcd(BigInteger left, BigInteger right)
    {
        return BigInteger.GreatestCommonDivisor(left, right);
    }

    private static string Run(string[] args)
    {
        if (args.Length == 0)
        {
            throw new ArgumentException("missing operation");
        }
        return args[0] switch
        {
            "mod-pow" when args.Length == 4 => RunModPow(args),
            "is-prime" when args.Length == 2 => IsPrime(Parse(args, 1, "n"))
                .ToString()
                .ToLowerInvariant(),
            "trial-factor" when args.Length == 2 => TrialFactor(Parse(args, 1, "n"))
                ?.ToString() ?? "none",
            "batch-gcd" when args.Length == 3 => RunBatchGcd(args),
            "separator" when args.Length == 4 => RunSeparator(args),
            "lucas-separator" when args.Length == 4 => RunLucasSeparator(args),
            "lucas-root-count-direct" when args.Length == 3 =>
                RunLucasRootCountDirect(args),
            "semismooth" when args.Length == 5 => RunSemismooth(args),
            "semismooth-success-count" when args.Length == 3 =>
                RunSemismoothSuccessCount(args),
            "cover-profile" when args.Length == 3 => RunCoverProfile(args),
            "combined-signature" when args.Length == 3 => RunCombinedSignature(args),
            "combined-asymmetry" when args.Length == 4 => RunCombinedAsymmetry(args),
            "combined-hit-count" when args.Length == 3 => RunCombinedHitCount(args),
            "divisor-count" when args.Length == 2 => RunDivisorCount(args),
            "multiplication-program" when args.Length == 4 =>
                RunMultiplicationProgram(args),
            "addition-subtraction-program" when args.Length == 4 =>
                RunAdditionSubtractionProgram(args),
            "batch-product" when args.Length == 4 => RunBatchProduct(args),
            "product-dag" when args.Length == 5 => RunProductDag(args),
            "dyadic-telescope" when args.Length == 4 => RunDyadicTelescope(args),
            "geometric-sum" when args.Length == 4 => RunGeometricSum(args),
            "nested-quotient" when args.Length == 5 => RunNestedQuotient(args),
            "iterated-quotient" when args.Length == 4 => RunIteratedQuotient(args),
            "quotient-linear-combination" when args.Length == 5 =>
                RunQuotientLinearCombination(args),
            "symmetric-quotient-difference" when args.Length == 4 =>
                RunSymmetricQuotientDifference(args),
            "unequal-signed-reduction" when args.Length == 7 =>
                RunUnequalSignedReduction(args),
            "rational-residue-audit" when args.Length == 7 =>
                RunRationalResidueAudit(args),
            "rational-root-orbit" when args.Length == 4 =>
                RunRationalRootOrbit(args),
            "exceptional-cyclotomic" when args.Length == 6 =>
                RunExceptionalCyclotomic(args),
            "exceptional-cofactor-overlap" when args.Length == 4 =>
                RunExceptionalCofactorOverlap(args),
            "multiplication-lower-bound" when args.Length == 2 =>
                RunMultiplicationLowerBound(args),
            _ => throw new ArgumentException("unknown operation or wrong argument count"),
        };
    }

    private static int[] ParsePositiveCsv(string raw, string name)
    {
        if (string.IsNullOrEmpty(raw))
        {
            throw new ArgumentException($"{name} must be nonempty");
        }
        int[] values = raw.Split(',').Select(value => int.Parse(value)).ToArray();
        if (values.Any(value => value <= 0))
        {
            throw new ArgumentException($"{name} values must be positive");
        }
        return values;
    }

    private static BigInteger[] ParseSignedCsv(string raw, string name)
    {
        if (string.IsNullOrEmpty(raw))
        {
            throw new ArgumentException($"{name} must be nonempty");
        }
        return raw.Split(',').Select(value => BigInteger.Parse(value)).ToArray();
    }

    private static string RunCoverProfile(string[] args)
    {
        int[] candidates = ParsePositiveCsv(args[1], "candidates");
        int[] orders = ParsePositiveCsv(args[2], "orders");
        if (orders.Length < 2)
        {
            throw new ArgumentException("orders must contain at least two values");
        }
        int[][] signatures = orders
            .Select(order => candidates
                .Select((candidate, index) => (candidate, index))
                .Where(item => item.candidate % order == 0)
                .Select(item => item.index)
                .ToArray())
            .ToArray();
        bool cover = signatures.All(signature => signature.Length > 0);
        bool separates = candidates.Any(candidate =>
        {
            int hits = orders.Count(order => candidate % order == 0);
            return hits > 0 && hits < orders.Length;
        });
        bool distinct = signatures
            .Select(signature => string.Join(",", signature))
            .Distinct()
            .Count() == signatures.Length;
        return $"cover:{cover.ToString().ToLowerInvariant()}|"
            + $"separates:{separates.ToString().ToLowerInvariant()}|"
            + $"distinct:{distinct.ToString().ToLowerInvariant()}";
    }

    private static (bool Minus, bool Plus)[] CombinedSignature(
        int prime,
        int[] exponents
    )
    {
        if (prime < 3 || prime % 2 == 0 || !IsPrime(prime))
        {
            throw new ArgumentException("prime must be odd prime");
        }
        return exponents
            .Select(exponent => (exponent % (prime - 1) == 0, exponent % (prime + 1) == 0))
            .ToArray();
    }

    private static string RunCombinedSignature(string[] args)
    {
        int prime = ParsePositiveInt(args, 1, "prime");
        int[] exponents = ParsePositiveCsv(args[2], "exponents");
        return string.Join(
            ",",
            CombinedSignature(prime, exponents)
                .Select(bits => $"{(bits.Minus ? 1 : 0)}{(bits.Plus ? 1 : 0)}")
        );
    }

    private static string RunCombinedAsymmetry(string[] args)
    {
        int leftPrime = ParsePositiveInt(args, 1, "left_prime");
        int rightPrime = ParsePositiveInt(args, 2, "right_prime");
        if (leftPrime == rightPrime)
        {
            throw new ArgumentException("primes must be distinct");
        }
        int[] exponents = ParsePositiveCsv(args[3], "exponents");
        bool result = !CombinedSignature(leftPrime, exponents)
            .SequenceEqual(CombinedSignature(rightPrime, exponents));
        return result.ToString().ToLowerInvariant();
    }

    private static string RunCombinedHitCount(string[] args)
    {
        int[] primes = ParsePositiveCsv(args[1], "primes");
        int[] exponents = ParsePositiveCsv(args[2], "exponents");
        int count = primes.Count(prime =>
            CombinedSignature(prime, exponents).Any(bits => bits.Minus || bits.Plus)
        );
        return count.ToString();
    }

    private static string RunDivisorCount(string[] args)
    {
        BigInteger value = Parse(args, 1, "value");
        if (value <= 0)
        {
            throw new ArgumentException("value must be positive");
        }
        BigInteger remaining = value;
        BigInteger divisor = 2;
        BigInteger count = 1;
        while (divisor <= remaining / divisor)
        {
            if (remaining % divisor == 0)
            {
                int exponent = 0;
                while (remaining % divisor == 0)
                {
                    remaining /= divisor;
                    exponent++;
                }
                count *= exponent + 1;
            }
            divisor = divisor == 2 ? 3 : divisor + 2;
        }
        if (remaining > 1)
        {
            count *= 2;
        }
        return count.ToString();
    }

    private static (int Left, int Right)[] ParseSteps(string raw)
    {
        if (string.IsNullOrEmpty(raw))
        {
            throw new ArgumentException("steps must be nonempty");
        }
        return raw.Split(',').Select(step =>
        {
            string[] parents = step.Split(':');
            if (
                parents.Length != 2
                || !int.TryParse(parents[0], out int left)
                || !int.TryParse(parents[1], out int right)
            )
            {
                throw new ArgumentException("each step must have integer left:right form");
            }
            return (left, right);
        }).ToArray();
    }

    private static string RunMultiplicationProgram(string[] args)
    {
        BigInteger value = Parse(args, 1, "base");
        BigInteger modulus = Parse(args, 2, "modulus");
        if (modulus < 2)
        {
            throw new ArgumentException("modulus must be at least two");
        }
        (int Left, int Right)[] steps = ParseSteps(args[3]);
        List<BigInteger> exponents = [BigInteger.One];
        List<BigInteger> residues = [((value % modulus) + modulus) % modulus];
        for (int index = 0; index < steps.Length; index++)
        {
            (int left, int right) = steps[index];
            int available = index + 1;
            if (left < 0 || right < 0 || left >= available || right >= available)
            {
                throw new ArgumentException("parents must be earlier nodes");
            }
            exponents.Add(exponents[left] + exponents[right]);
            residues.Add(residues[left] * residues[right] % modulus);
        }
        return $"exponents:{string.Join(",", exponents)}|"
            + $"residues:{string.Join(",", residues)}";
    }

    private static (int Left, int Right, int Sign)[] ParseSignedSteps(string raw)
    {
        if (string.IsNullOrEmpty(raw))
        {
            throw new ArgumentException("steps must be nonempty");
        }
        return raw.Split(',').Select(step =>
        {
            string[] parts = step.Split(':');
            if (
                parts.Length != 3
                || !int.TryParse(parts[0], out int left)
                || !int.TryParse(parts[1], out int right)
            )
            {
                throw new ArgumentException(
                    "each signed step must have integer left:right:sign form"
                );
            }
            int sign = parts[2] switch
            {
                "+" or "1" => 1,
                "-" or "-1" => -1,
                _ => throw new ArgumentException("signed step sign must be + or -"),
            };
            return (left, right, sign);
        }).ToArray();
    }

    private static BigInteger ModularInverse(BigInteger value, BigInteger modulus)
    {
        BigInteger oldRemainder = value;
        BigInteger remainder = modulus;
        BigInteger oldCoefficient = BigInteger.One;
        BigInteger coefficient = BigInteger.Zero;
        while (remainder != 0)
        {
            BigInteger quotient = oldRemainder / remainder;
            (oldRemainder, remainder) = (
                remainder,
                oldRemainder - quotient * remainder
            );
            (oldCoefficient, coefficient) = (
                coefficient,
                oldCoefficient - quotient * coefficient
            );
        }
        if (oldRemainder != 1)
        {
            throw new ArgumentException("residue is not invertible");
        }
        return ((oldCoefficient % modulus) + modulus) % modulus;
    }

    private static string RunAdditionSubtractionProgram(string[] args)
    {
        BigInteger value = Parse(args, 1, "base");
        BigInteger modulus = Parse(args, 2, "modulus");
        if (modulus < 2)
        {
            throw new ArgumentException("modulus must be at least two");
        }
        BigInteger reducedBase = ((value % modulus) + modulus) % modulus;
        if (Gcd(reducedBase, modulus) != 1)
        {
            throw new ArgumentException("base must be a unit modulo the modulus");
        }
        (int Left, int Right, int Sign)[] steps = ParseSignedSteps(args[3]);
        List<BigInteger> exponents = [BigInteger.One];
        List<BigInteger> residues = [reducedBase];
        int inversionCount = 0;
        for (int index = 0; index < steps.Length; index++)
        {
            (int left, int right, int sign) = steps[index];
            int available = index + 1;
            if (left < 0 || right < 0 || left >= available || right >= available)
            {
                throw new ArgumentException("parents must be earlier nodes");
            }
            exponents.Add(exponents[left] + sign * exponents[right]);
            BigInteger rightResidue = residues[right];
            if (sign == -1)
            {
                rightResidue = ModularInverse(rightResidue, modulus);
                inversionCount++;
            }
            residues.Add(residues[left] * rightResidue % modulus);
        }
        return $"exponents:{string.Join(",", exponents)}|"
            + $"residues:{string.Join(",", residues)}|"
            + $"inversions:{inversionCount}";
    }

    private static string RunBatchProduct(string[] args)
    {
        BigInteger value = Parse(args, 1, "base");
        BigInteger modulus = Parse(args, 2, "modulus");
        if (modulus < 2)
        {
            throw new ArgumentException("modulus must be at least two");
        }
        BigInteger reducedBase = ((value % modulus) + modulus) % modulus;
        if (Gcd(reducedBase, modulus) != 1)
        {
            throw new ArgumentException("base must be a unit modulo the modulus");
        }
        int[] exponents = ParsePositiveCsv(args[3], "exponents");
        if (!exponents.SequenceEqual(exponents.Distinct().Order()))
        {
            throw new ArgumentException("exponents must be strictly increasing");
        }
        List<BigInteger> leaves = exponents
            .Select(exponent =>
                (BigInteger.ModPow(reducedBase, exponent, modulus) - 1 + modulus)
                % modulus
            )
            .ToList();
        BigInteger[] leafGcds = leaves
            .Select(residue => Gcd(residue, modulus))
            .ToArray();
        List<BigInteger> current = [.. leaves];
        int multiplicationCount = 0;
        while (current.Count > 1)
        {
            List<BigInteger> following = [];
            for (int index = 0; index < current.Count; index += 2)
            {
                if (index + 1 == current.Count)
                {
                    following.Add(current[index]);
                }
                else
                {
                    following.Add(current[index] * current[index + 1] % modulus);
                    multiplicationCount++;
                }
            }
            current = following;
        }
        BigInteger root = current[0];
        return $"leaves:{string.Join(",", leaves)}|root:{root}|"
            + $"leaf_gcds:{string.Join(",", leafGcds)}|root_gcd:{Gcd(root, modulus)}|"
            + $"multiplications:{multiplicationCount}";
    }

    private static string RunProductDag(string[] args)
    {
        BigInteger value = Parse(args, 1, "base");
        BigInteger modulus = Parse(args, 2, "modulus");
        if (modulus < 2)
        {
            throw new ArgumentException("modulus must be at least two");
        }
        BigInteger reducedBase = ((value % modulus) + modulus) % modulus;
        if (Gcd(reducedBase, modulus) != 1)
        {
            throw new ArgumentException("base must be a unit modulo the modulus");
        }
        int[] exponents = ParsePositiveCsv(args[3], "exponents");
        if (!exponents.SequenceEqual(exponents.Distinct().Order()))
        {
            throw new ArgumentException("exponents must be strictly increasing");
        }
        (int Left, int Right)[] gates = ParseSteps(args[4]);
        int atomCount = exponents.Length;
        List<BigInteger> nodes = exponents
            .Select(exponent =>
                (BigInteger.ModPow(reducedBase, exponent, modulus) - 1 + modulus)
                % modulus
            )
            .ToList();
        List<BigInteger[]> multiplicities = Enumerable.Range(0, atomCount)
            .Select(index =>
                Enumerable.Range(0, atomCount)
                    .Select(atom => atom == index ? BigInteger.One : BigInteger.Zero)
                    .ToArray()
            )
            .ToList();
        List<BigInteger> occurrences = Enumerable.Repeat(
            BigInteger.One,
            atomCount
        ).ToList();
        for (int index = 0; index < gates.Length; index++)
        {
            (int left, int right) = gates[index];
            int available = atomCount + index;
            if (left < 0 || right < 0 || left >= available || right >= available)
            {
                throw new ArgumentException("gate parents must be earlier nodes");
            }
            nodes.Add(nodes[left] * nodes[right] % modulus);
            multiplicities.Add(
                multiplicities[left]
                    .Zip(multiplicities[right], (leftCount, rightCount) =>
                        leftCount + rightCount
                    )
                    .ToArray()
            );
            occurrences.Add(occurrences[left] + occurrences[right]);
        }
        string profiles = string.Join(
            ";",
            multiplicities.Select(profile => string.Join(",", profile))
        );
        return $"nodes:{string.Join(",", nodes)}|"
            + $"gcds:{string.Join(",", nodes.Select(node => Gcd(node, modulus)))}|"
            + $"multiplicities:{profiles}|occurrences:{string.Join(",", occurrences)}";
    }

    private static string RunDyadicTelescope(string[] args)
    {
        BigInteger value = Parse(args, 1, "base");
        BigInteger modulus = Parse(args, 2, "modulus");
        BigInteger levelValue = Parse(args, 3, "levels");
        if (modulus < 2 || levelValue < 0 || levelValue > 63)
        {
            throw new ArgumentException(
                "modulus must be at least two and levels must lie in [0, 63]"
            );
        }
        int levels = (int)levelValue;
        BigInteger reducedBase = ((value % modulus) + modulus) % modulus;
        if (Gcd(reducedBase, modulus) != 1)
        {
            throw new ArgumentException("base must be a unit modulo the modulus");
        }

        List<BigInteger> powers = [reducedBase];
        for (int index = 0; index < levels; index++)
        {
            powers.Add(powers[^1] * powers[^1] % modulus);
        }
        List<BigInteger> factors = powers
            .Take(levels)
            .Select(power => (power + 1) % modulus)
            .ToList();
        List<BigInteger> factorGcds = factors
            .Select(factor => Gcd(factor, modulus))
            .ToList();
        BigInteger quotient = factors.Count == 0
            ? BigInteger.One % modulus
            : factors[0];
        foreach (BigInteger factor in factors.Skip(1))
        {
            quotient = quotient * factor % modulus;
        }

        BigInteger denominator = (reducedBase - 1 + modulus) % modulus;
        BigInteger denominatorGcd = Gcd(denominator, modulus);
        BigInteger numerator = (powers[^1] - 1 + modulus) % modulus;
        string divisionStatus;
        string divisionQuotient;
        if (denominatorGcd == 1)
        {
            divisionStatus = "unit";
            divisionQuotient = (
                numerator * ModularInverse(denominator, modulus) % modulus
            ).ToString();
        }
        else if (denominatorGcd < modulus)
        {
            divisionStatus = "proper_factor";
            divisionQuotient = "none";
        }
        else
        {
            divisionStatus = "full_collision";
            divisionQuotient = "none";
        }
        BigInteger monomials = BigInteger.One << levels;
        return $"powers:{string.Join(",", powers)}|"
            + $"factors:{string.Join(",", factors)}|"
            + $"factor_gcds:{string.Join(",", factorGcds)}|"
            + $"denominator:{denominator}|denominator_gcd:{denominatorGcd}|"
            + $"numerator:{numerator}|numerator_gcd:{Gcd(numerator, modulus)}|"
            + $"quotient:{quotient}|quotient_gcd:{Gcd(quotient, modulus)}|"
            + $"division_status:{divisionStatus}|division_quotient:{divisionQuotient}|"
            + $"degree:{monomials - 1}|monomials:{monomials}|squarings:{levels}|"
            + $"products:{Math.Max(0, levels - 1)}";
    }

    private static string RunGeometricSum(string[] args)
    {
        BigInteger value = Parse(args, 1, "base");
        BigInteger modulus = Parse(args, 2, "modulus");
        BigInteger exponent = Parse(args, 3, "exponent");
        if (modulus < 2 || exponent < 1)
        {
            throw new ArgumentException(
                "modulus must be at least two and exponent must be positive"
            );
        }
        BigInteger reducedBase = ((value % modulus) + modulus) % modulus;
        if (Gcd(reducedBase, modulus) != 1)
        {
            throw new ArgumentException("base must be a unit modulo the modulus");
        }

        List<int> bits = [];
        for (BigInteger remaining = exponent; remaining > 0; remaining >>= 1)
        {
            bits.Add((int)(remaining & BigInteger.One));
        }
        BigInteger power = reducedBase;
        BigInteger geometricSum = BigInteger.One % modulus;
        int multiplicationCount = 0;
        int additionCount = 0;
        for (int bitIndex = bits.Count - 2; bitIndex >= 0; bitIndex--)
        {
            geometricSum = geometricSum * ((BigInteger.One + power) % modulus) % modulus;
            power = power * power % modulus;
            multiplicationCount += 2;
            additionCount++;
            if (bits[bitIndex] == 1)
            {
                geometricSum = (geometricSum + power) % modulus;
                power = power * reducedBase % modulus;
                multiplicationCount++;
                additionCount++;
            }
        }

        BigInteger denominator = (reducedBase - 1 + modulus) % modulus;
        BigInteger denominatorGcd = Gcd(denominator, modulus);
        BigInteger numerator = (power - 1 + modulus) % modulus;
        string divisionStatus;
        string divisionQuotient;
        if (denominatorGcd == 1)
        {
            divisionStatus = "unit";
            divisionQuotient = (
                numerator * ModularInverse(denominator, modulus) % modulus
            ).ToString();
        }
        else if (denominatorGcd < modulus)
        {
            divisionStatus = "proper_factor";
            divisionQuotient = "none";
        }
        else
        {
            divisionStatus = "full_collision";
            divisionQuotient = "none";
        }

        return $"power:{power}|sum:{geometricSum}|"
            + $"denominator:{denominator}|denominator_gcd:{denominatorGcd}|"
            + $"numerator:{numerator}|numerator_gcd:{Gcd(numerator, modulus)}|"
            + $"sum_gcd:{Gcd(geometricSum, modulus)}|"
            + $"exponent_gcd:{Gcd(exponent, modulus)}|"
            + $"division_status:{divisionStatus}|division_quotient:{divisionQuotient}|"
            + $"bit_length:{bits.Count}|degree:{exponent - 1}|monomials:{exponent}|"
            + $"multiplications:{multiplicationCount}|additions:{additionCount}";
    }

    private static (BigInteger Power, BigInteger Sum) GeometricPair(
        BigInteger value,
        BigInteger modulus,
        BigInteger exponent
    )
    {
        if (modulus < 2 || exponent < 1)
        {
            throw new ArgumentException("invalid geometric-pair domain");
        }
        BigInteger reducedBase = ((value % modulus) + modulus) % modulus;
        if (Gcd(reducedBase, modulus) != 1)
        {
            throw new ArgumentException("base must be a unit modulo the modulus");
        }
        List<int> bits = [];
        for (BigInteger remaining = exponent; remaining > 0; remaining >>= 1)
        {
            bits.Add((int)(remaining & BigInteger.One));
        }
        BigInteger power = reducedBase;
        BigInteger sum = BigInteger.One % modulus;
        for (int bitIndex = bits.Count - 2; bitIndex >= 0; bitIndex--)
        {
            sum = sum * ((BigInteger.One + power) % modulus) % modulus;
            power = power * power % modulus;
            if (bits[bitIndex] == 1)
            {
                sum = (sum + power) % modulus;
                power = power * reducedBase % modulus;
            }
        }
        return (power, sum);
    }

    private static string RunNestedQuotient(string[] args)
    {
        BigInteger value = Parse(args, 1, "base");
        BigInteger modulus = Parse(args, 2, "modulus");
        BigInteger innerExponent = Parse(args, 3, "inner_exponent");
        BigInteger multiplier = Parse(args, 4, "multiplier");
        (BigInteger innerPower, BigInteger intermediate) = GeometricPair(
            value, modulus, innerExponent
        );
        (BigInteger outerPower, BigInteger quotient) = GeometricPair(
            innerPower, modulus, multiplier
        );
        (_, BigInteger rationalNumerator) = GeometricPair(
            value, modulus, innerExponent * multiplier
        );
        if (
            rationalNumerator != intermediate * quotient % modulus
            || outerPower != BigInteger.ModPow(
                ((value % modulus) + modulus) % modulus,
                innerExponent * multiplier,
                modulus
            )
        )
        {
            throw new ArgumentException("nested quotient identity failed");
        }
        BigInteger composedDenominator = (innerPower - 1 + modulus) % modulus;
        BigInteger endpoint = (outerPower - 1 + modulus) % modulus;
        BigInteger intermediateGcd = Gcd(intermediate, modulus);
        BigInteger composedGcd = Gcd(composedDenominator, modulus);
        string rationalStatus = intermediateGcd == 1
            ? "unit"
            : intermediateGcd < modulus ? "proper_factor" : "full_collision";
        string composedStatus = composedGcd == 1
            ? "unit"
            : composedGcd < modulus ? "proper_factor" : "full_collision";
        string rationalQuotient = intermediateGcd == 1
            ? (rationalNumerator * ModularInverse(intermediate, modulus) % modulus).ToString()
            : "none";
        string composedQuotient = composedGcd == 1
            ? (endpoint * ModularInverse(composedDenominator, modulus) % modulus).ToString()
            : "none";
        return $"inner_power:{innerPower}|intermediate:{intermediate}|"
            + $"intermediate_gcd:{intermediateGcd}|quotient:{quotient}|"
            + $"quotient_gcd:{Gcd(quotient, modulus)}|"
            + $"rational_numerator:{rationalNumerator}|"
            + $"rational_numerator_gcd:{Gcd(rationalNumerator, modulus)}|"
            + $"composed_denominator:{composedDenominator}|"
            + $"composed_denominator_gcd:{composedGcd}|endpoint:{endpoint}|"
            + $"endpoint_gcd:{Gcd(endpoint, modulus)}|"
            + $"multiplier_gcd:{Gcd(multiplier, modulus)}|"
            + $"rational_status:{rationalStatus}|rational_quotient:{rationalQuotient}|"
            + $"composed_status:{composedStatus}|composed_quotient:{composedQuotient}";
    }

    private static string RunIteratedQuotient(string[] args)
    {
        BigInteger value = Parse(args, 1, "base");
        BigInteger modulus = Parse(args, 2, "modulus");
        int[] factors = ParsePositiveCsv(args[3], "factors");
        BigInteger prefix = BigInteger.One;
        List<BigInteger> prefixes = [prefix];
        List<string> stages = [];
        BigInteger quotientProduct = BigInteger.One % modulus;
        BigInteger? previousNumerator = null;
        BigInteger finalNumerator = BigInteger.One % modulus;
        foreach (int factorValue in factors)
        {
            BigInteger factor = factorValue;
            (BigInteger innerPower, BigInteger intermediate) = GeometricPair(
                value, modulus, prefix
            );
            (BigInteger outerPower, BigInteger quotient) = GeometricPair(
                innerPower, modulus, factor
            );
            (_, BigInteger rationalNumerator) = GeometricPair(
                value, modulus, prefix * factor
            );
            if (
                rationalNumerator != intermediate * quotient % modulus
                || previousNumerator is not null
                    && intermediate != previousNumerator.Value
            )
            {
                throw new ArgumentException("iterated quotient identity failed");
            }
            quotientProduct = quotientProduct * quotient % modulus;
            if (quotientProduct != rationalNumerator)
            {
                throw new ArgumentException("iterated product identity failed");
            }
            BigInteger composedDenominator = (innerPower - 1 + modulus) % modulus;
            BigInteger endpoint = (outerPower - 1 + modulus) % modulus;
            BigInteger intermediateGcd = Gcd(intermediate, modulus);
            BigInteger composedGcd = Gcd(composedDenominator, modulus);
            string rationalStatus = intermediateGcd == 1
                ? "unit"
                : intermediateGcd < modulus ? "proper_factor" : "full_collision";
            string composedStatus = composedGcd == 1
                ? "unit"
                : composedGcd < modulus ? "proper_factor" : "full_collision";
            stages.Add(
                $"{innerPower},{intermediate},{intermediateGcd},"
                + $"{quotient},{Gcd(quotient, modulus)},"
                + $"{rationalNumerator},{Gcd(rationalNumerator, modulus)},"
                + $"{composedGcd},{Gcd(endpoint, modulus)},"
                + $"{Gcd(factor, modulus)},{rationalStatus},{composedStatus}"
            );
            previousNumerator = rationalNumerator;
            finalNumerator = rationalNumerator;
            prefix *= factor;
            prefixes.Add(prefix);
        }
        return $"prefixes:{string.Join(",", prefixes)}|"
            + $"final_product:{quotientProduct}|final_prefix:{finalNumerator}|"
            + $"final_gcd:{Gcd(finalNumerator, modulus)}|"
            + $"stages:{string.Join(";", stages)}";
    }

    private static string RunQuotientLinearCombination(string[] args)
    {
        BigInteger value = Parse(args, 1, "base");
        BigInteger modulus = Parse(args, 2, "modulus");
        int[] factors = ParsePositiveCsv(args[3], "factors");
        BigInteger[] coefficients = ParseSignedCsv(args[4], "coefficients");
        if (factors.Length != coefficients.Length)
        {
            throw new ArgumentException("factors and coefficients must have equal length");
        }
        if (modulus < 2)
        {
            throw new ArgumentException("modulus must be at least two");
        }

        BigInteger prefix = BigInteger.One;
        List<BigInteger> quotients = [];
        foreach (int factorValue in factors)
        {
            BigInteger factor = factorValue;
            (BigInteger innerPower, _) = GeometricPair(value, modulus, prefix);
            (_, BigInteger quotient) = GeometricPair(innerPower, modulus, factor);
            quotients.Add(quotient);
            prefix *= factor;
        }

        BigInteger[] coefficientResidues = coefficients
            .Select(coefficient => ((coefficient % modulus) + modulus) % modulus)
            .ToArray();
        BigInteger[] coefficientGcds = coefficients
            .Select(coefficient => Gcd(coefficient, modulus))
            .ToArray();
        BigInteger[] weighted = coefficientResidues
            .Zip(quotients, (coefficient, quotient) => coefficient * quotient % modulus)
            .ToArray();
        BigInteger[] quotientGcds = quotients.Select(item => Gcd(item, modulus)).ToArray();
        BigInteger[] weightedGcds = weighted.Select(item => Gcd(item, modulus)).ToArray();
        BigInteger aggregate = weighted.Aggregate(
            BigInteger.Zero,
            (current, item) => (current + item) % modulus
        );

        return $"factors:{string.Join(",", factors)}|"
            + $"coefficients:{string.Join(",", coefficients)}|"
            + $"coefficient_residues:{string.Join(",", coefficientResidues)}|"
            + $"coefficient_gcds:{string.Join(",", coefficientGcds)}|"
            + $"quotients:{string.Join(",", quotients)}|"
            + $"quotient_gcds:{string.Join(",", quotientGcds)}|"
            + $"weighted:{string.Join(",", weighted)}|"
            + $"weighted_gcds:{string.Join(",", weightedGcds)}|"
            + $"aggregate:{aggregate}|aggregate_gcd:{Gcd(aggregate, modulus)}";
    }

    private static BigInteger[,] MultiplyMatrix3(
        BigInteger[,] left,
        BigInteger[,] right,
        BigInteger modulus
    )
    {
        BigInteger[,] result = new BigInteger[3, 3];
        for (int row = 0; row < 3; row++)
        {
            for (int column = 0; column < 3; column++)
            {
                for (int inner = 0; inner < 3; inner++)
                {
                    result[row, column] = (
                        result[row, column] + left[row, inner] * right[inner, column]
                    ) % modulus;
                }
            }
        }
        return result;
    }

    private static (BigInteger[,] Matrix, int Count) PowerMatrix3(
        BigInteger[,] matrix,
        BigInteger exponent,
        BigInteger modulus
    )
    {
        BigInteger[,] result =
        {
            { BigInteger.One, BigInteger.Zero, BigInteger.Zero },
            { BigInteger.Zero, BigInteger.One, BigInteger.Zero },
            { BigInteger.Zero, BigInteger.Zero, BigInteger.One },
        };
        BigInteger[,] power = matrix;
        BigInteger remaining = exponent;
        int count = 0;
        while (remaining != 0)
        {
            if (!remaining.IsEven)
            {
                result = MultiplyMatrix3(result, power, modulus);
                count++;
            }
            remaining >>= 1;
            if (remaining != 0)
            {
                power = MultiplyMatrix3(power, power, modulus);
                count++;
            }
        }
        return (result, count);
    }

    private static (BigInteger Cofactor, int MatrixCount) CompactSymmetricCofactor(
        BigInteger value,
        BigInteger modulus,
        BigInteger exponent
    )
    {
        BigInteger n = exponent - 1;
        BigInteger y = BigInteger.ModPow(value, n, modulus);
        BigInteger xy = value * y % modulus;
        BigInteger[,] transition =
        {
            { value, BigInteger.One, BigInteger.Zero },
            { BigInteger.Zero, xy, BigInteger.Zero },
            { value, BigInteger.One, BigInteger.One },
        };
        (BigInteger[,] powered, int count) = PowerMatrix3(
            transition,
            n - 1,
            modulus
        );
        BigInteger[] initial = [BigInteger.One % modulus, xy, BigInteger.One % modulus];
        BigInteger[] state = new BigInteger[3];
        for (int row = 0; row < 3; row++)
        {
            for (int column = 0; column < 3; column++)
            {
                state[row] = (
                    state[row] + powered[row, column] * initial[column]
                ) % modulus;
            }
        }
        return (state[2], count);
    }

    private static string RunSymmetricQuotientDifference(string[] args)
    {
        BigInteger value = Parse(args, 1, "base");
        BigInteger modulus = Parse(args, 2, "modulus");
        BigInteger exponent = Parse(args, 3, "exponent");
        if (modulus < 2 || exponent < 2)
        {
            throw new ArgumentException(
                "modulus must be at least two and exponent at least two"
            );
        }
        BigInteger reducedBase = ((value % modulus) + modulus) % modulus;
        (BigInteger firstPower, BigInteger firstQuotient) = GeometricPair(
            reducedBase,
            modulus,
            exponent
        );
        (_, BigInteger secondQuotient) = GeometricPair(
            firstPower,
            modulus,
            exponent
        );
        BigInteger difference = (
            (secondQuotient - firstQuotient) % modulus + modulus
        ) % modulus;
        BigInteger endpoint = (
            BigInteger.ModPow(reducedBase, exponent - 1, modulus)
            - 1
            + modulus
        ) % modulus;
        BigInteger endpointGcd = Gcd(endpoint, modulus);
        string endpointStatus = endpointGcd == 1
            ? "unit"
            : endpointGcd < modulus ? "proper_factor" : "full_collision";
        (BigInteger cofactor, int matrixCount) = CompactSymmetricCofactor(
            reducedBase,
            modulus,
            exponent
        );
        if (difference != reducedBase * endpoint % modulus * cofactor % modulus)
        {
            throw new ArgumentException("symmetric quotient-difference identity failed");
        }
        string divisionCofactor = endpointGcd == 1
            ? (
                difference
                * ModularInverse(reducedBase * endpoint % modulus, modulus)
                % modulus
            ).ToString()
            : "none";
        return $"exponent:{exponent}|first_quotient:{firstQuotient}|"
            + $"second_quotient:{secondQuotient}|difference:{difference}|"
            + $"difference_gcd:{Gcd(difference, modulus)}|endpoint:{endpoint}|"
            + $"endpoint_gcd:{endpointGcd}|endpoint_status:{endpointStatus}|"
            + $"cofactor:{cofactor}|cofactor_gcd:{Gcd(cofactor, modulus)}|"
            + $"division_cofactor:{divisionCofactor}|"
            + $"cofactor_monomials:{exponent * (exponent - 1) / 2}|"
            + $"cofactor_degree:{exponent * (exponent - 2)}|"
            + $"matrix_multiplications:{matrixCount}";
    }

    private static string RunUnequalSignedReduction(string[] args)
    {
        BigInteger value = Parse(args, 1, "base");
        BigInteger modulus = Parse(args, 2, "modulus");
        BigInteger firstFactor = Parse(args, 3, "first_factor");
        BigInteger secondFactor = Parse(args, 4, "second_factor");
        BigInteger firstCoefficient = Parse(args, 5, "first_coefficient");
        BigInteger secondCoefficient = Parse(args, 6, "second_coefficient");
        if (
            modulus < 2
            || firstFactor < 2
            || secondFactor < 2
            || firstFactor == secondFactor
            || firstCoefficient == 0
            || secondCoefficient == 0
        )
        {
            throw new ArgumentException("invalid unequal signed-reduction domain");
        }
        BigInteger reducedBase = ((value % modulus) + modulus) % modulus;
        (BigInteger firstPower, BigInteger firstQuotient) = GeometricPair(
            reducedBase,
            modulus,
            firstFactor
        );
        (_, BigInteger secondQuotient) = GeometricPair(
            firstPower,
            modulus,
            secondFactor
        );
        BigInteger firstCoefficientResidue = (
            (firstCoefficient % modulus) + modulus
        ) % modulus;
        BigInteger secondCoefficientResidue = (
            (secondCoefficient % modulus) + modulus
        ) % modulus;
        BigInteger aggregate = (
            firstCoefficientResidue * firstQuotient
            + secondCoefficientResidue * secondQuotient
        ) % modulus;
        BigInteger firstGcd = Gcd(firstQuotient, modulus);
        string prefixStatus = firstGcd == 1
            ? "unit"
            : firstGcd < modulus ? "proper_factor" : "full_collision";
        string rational = "none";
        string rationalGcd = "none";
        if (firstGcd == 1)
        {
            BigInteger rationalResidue = (
                firstCoefficientResidue
                + secondCoefficientResidue
                    * secondQuotient
                    * ModularInverse(firstQuotient, modulus)
            ) % modulus;
            if (aggregate != firstQuotient * rationalResidue % modulus)
            {
                throw new ArgumentException("unit-prefix rational reduction failed");
            }
            rational = rationalResidue.ToString();
            rationalGcd = Gcd(rationalResidue, modulus).ToString();
        }
        BigInteger publicFull = (
            secondCoefficientResidue * (secondFactor % modulus)
        ) % modulus;
        if (
            firstGcd == modulus
            && (
                secondQuotient != secondFactor % modulus
                || aggregate != publicFull
            )
        )
        {
            throw new ArgumentException("full-prefix public reduction failed");
        }

        BigInteger commonStageGcd = Gcd(
            Gcd(firstQuotient, secondQuotient),
            modulus
        );
        BigInteger multiplierGcd = Gcd(secondFactor, modulus);
        if (multiplierGcd % commonStageGcd != 0)
        {
            throw new ArgumentException("common stage divisor did not divide multiplier");
        }

        BigInteger commonStep = Gcd(firstFactor - 1, secondFactor - 1);
        (_, BigInteger commonSum) = GeometricPair(
            reducedBase,
            modulus,
            commonStep
        );
        BigInteger commonFactor = reducedBase * commonSum % modulus;
        BigInteger commonFactorGcd = Gcd(commonFactor, modulus);
        BigInteger difference = (
            secondQuotient - firstQuotient + modulus
        ) % modulus;
        string cofactor = "none";
        string cofactorGcd = "none";
        if (commonFactorGcd == 1)
        {
            BigInteger cofactorResidue = (
                difference * ModularInverse(commonFactor, modulus)
            ) % modulus;
            cofactor = cofactorResidue.ToString();
            cofactorGcd = Gcd(cofactorResidue, modulus).ToString();
        }

        bool hasXFactor = firstCoefficient + secondCoefficient == 0;
        bool hasXMinusOneFactor = (
            firstCoefficient * firstFactor
            + secondCoefficient * secondFactor
            == 0
        );
        BigInteger formalDegree = firstFactor * (secondFactor - 1);
        BigInteger collectedMonomials = firstFactor + secondFactor
            - (hasXFactor ? 2 : 1);
        BigInteger cofactorDegree = formalDegree - commonStep - 1;
        return $"first_factor:{firstFactor}|second_factor:{secondFactor}|"
            + $"first_coefficient:{firstCoefficient}|second_coefficient:{secondCoefficient}|"
            + $"first_quotient:{firstQuotient}|second_quotient:{secondQuotient}|"
            + $"first_quotient_gcd:{firstGcd}|"
            + $"second_quotient_gcd:{Gcd(secondQuotient, modulus)}|"
            + $"aggregate:{aggregate}|aggregate_gcd:{Gcd(aggregate, modulus)}|"
            + $"prefix_status:{prefixStatus}|rational:{rational}|"
            + $"rational_gcd:{rationalGcd}|public_full:{publicFull}|"
            + $"public_full_gcd:{Gcd(publicFull, modulus)}|"
            + $"common_stage_gcd:{commonStageGcd}|multiplier_gcd:{multiplierGcd}|"
            + $"x_factor:{hasXFactor.ToString().ToLowerInvariant()}|"
            + $"x_minus_one_factor:{hasXMinusOneFactor.ToString().ToLowerInvariant()}|"
            + $"formal_degree:{formalDegree}|collected_monomials:{collectedMonomials}|"
            + $"common_step:{commonStep}|difference:{difference}|"
            + $"difference_gcd:{Gcd(difference, modulus)}|"
            + $"common_factor:{commonFactor}|common_factor_gcd:{commonFactorGcd}|"
            + $"cofactor:{cofactor}|cofactor_gcd:{cofactorGcd}|"
            + $"cofactor_degree:{cofactorDegree}";
    }

    private static string RunRationalResidueAudit(string[] args)
    {
        BigInteger value = Parse(args, 1, "base");
        BigInteger modulus = Parse(args, 2, "modulus");
        BigInteger firstFactor = Parse(args, 3, "first_factor");
        BigInteger secondFactor = Parse(args, 4, "second_factor");
        BigInteger firstCoefficient = Parse(args, 5, "first_coefficient");
        BigInteger secondCoefficient = Parse(args, 6, "second_coefficient");
        if (
            modulus < 2
            || firstFactor < 2
            || secondFactor < 2
            || firstFactor == secondFactor
            || firstCoefficient == 0
            || secondCoefficient == 0
        )
        {
            throw new ArgumentException("invalid rational-residue audit domain");
        }
        BigInteger reducedBase = ((value % modulus) + modulus) % modulus;
        (BigInteger firstPower, BigInteger firstQuotient) = GeometricPair(
            reducedBase,
            modulus,
            firstFactor
        );
        (_, BigInteger secondQuotient) = GeometricPair(
            firstPower,
            modulus,
            secondFactor
        );
        BigInteger content = Gcd(
            BigInteger.Abs(firstCoefficient),
            BigInteger.Abs(secondCoefficient)
        );
        BigInteger primitiveFirst = firstCoefficient / content;
        BigInteger primitiveSecond = secondCoefficient / content;
        BigInteger Normalize(BigInteger coefficient) =>
            ((coefficient % modulus) + modulus) % modulus;
        BigInteger LinearCombination(BigInteger left, BigInteger right) =>
            (
                Normalize(left) * firstQuotient
                + Normalize(right) * secondQuotient
            ) % modulus;
        string Status(BigInteger divisor) => divisor == 1
            ? "unit"
            : divisor < modulus ? "proper_factor" : "full_collision";
        BigInteger aggregate = LinearCombination(
            firstCoefficient,
            secondCoefficient
        );
        BigInteger primitiveAggregate = LinearCombination(
            primitiveFirst,
            primitiveSecond
        );
        if (aggregate != content % modulus * primitiveAggregate % modulus)
        {
            throw new ArgumentException("coefficient-content normalization failed");
        }
        BigInteger contentGcd = Gcd(content, modulus);
        BigInteger firstGcd = Gcd(firstQuotient, modulus);
        string rational = "none";
        string rationalGcd = "none";
        string primitiveRational = "none";
        string primitiveRationalGcd = "none";
        if (firstGcd == 1)
        {
            BigInteger ratio = (
                secondQuotient * ModularInverse(firstQuotient, modulus)
            ) % modulus;
            BigInteger rationalResidue = (
                Normalize(firstCoefficient)
                + Normalize(secondCoefficient) * ratio
            ) % modulus;
            BigInteger primitiveRationalResidue = (
                Normalize(primitiveFirst)
                + Normalize(primitiveSecond) * ratio
            ) % modulus;
            if (
                aggregate != firstQuotient * rationalResidue % modulus
                || primitiveAggregate
                    != firstQuotient * primitiveRationalResidue % modulus
            )
            {
                throw new ArgumentException("unit-prefix rational reduction failed");
            }
            rational = rationalResidue.ToString();
            rationalGcd = Gcd(rationalResidue, modulus).ToString();
            primitiveRational = primitiveRationalResidue.ToString();
            primitiveRationalGcd = Gcd(
                primitiveRationalResidue,
                modulus
            ).ToString();
        }
        BigInteger firstOverlapGcd = Gcd(
            Gcd(firstQuotient, aggregate),
            modulus
        );
        BigInteger firstPublicBoundGcd = Gcd(
            BigInteger.Abs(secondCoefficient) * secondFactor,
            modulus
        );
        BigInteger secondOverlapGcd = Gcd(
            Gcd(secondQuotient, aggregate),
            modulus
        );
        BigInteger secondPublicBoundGcd = Gcd(
            BigInteger.Abs(firstCoefficient) * secondFactor,
            modulus
        );
        if (
            firstPublicBoundGcd % firstOverlapGcd != 0
            || secondPublicBoundGcd % secondOverlapGcd != 0
        )
        {
            throw new ArgumentException("stage overlap escaped public bound");
        }
        return $"first_factor:{firstFactor}|second_factor:{secondFactor}|"
            + $"first_coefficient:{firstCoefficient}|second_coefficient:{secondCoefficient}|"
            + $"content:{content}|primitive_first_coefficient:{primitiveFirst}|"
            + $"primitive_second_coefficient:{primitiveSecond}|content_gcd:{contentGcd}|"
            + $"content_status:{Status(contentGcd)}|first_quotient:{firstQuotient}|"
            + $"second_quotient:{secondQuotient}|first_quotient_gcd:{firstGcd}|"
            + $"second_quotient_gcd:{Gcd(secondQuotient, modulus)}|"
            + $"aggregate:{aggregate}|aggregate_gcd:{Gcd(aggregate, modulus)}|"
            + $"primitive_aggregate:{primitiveAggregate}|"
            + $"primitive_aggregate_gcd:{Gcd(primitiveAggregate, modulus)}|"
            + $"prefix_status:{Status(firstGcd)}|rational:{rational}|"
            + $"rational_gcd:{rationalGcd}|primitive_rational:{primitiveRational}|"
            + $"primitive_rational_gcd:{primitiveRationalGcd}|"
            + $"first_overlap_gcd:{firstOverlapGcd}|"
            + $"first_public_bound_gcd:{firstPublicBoundGcd}|"
            + $"second_overlap_gcd:{secondOverlapGcd}|"
            + $"second_public_bound_gcd:{secondPublicBoundGcd}|"
            + $"first_resultant_base:{BigInteger.Abs(secondCoefficient) * secondFactor}|"
            + $"first_resultant_exponent:{firstFactor - 1}|"
            + $"second_resultant_coefficient_base:{BigInteger.Abs(firstCoefficient)}|"
            + $"second_resultant_coefficient_exponent:{firstFactor * (secondFactor - 1)}|"
            + $"second_resultant_stage_base:{secondFactor}|"
            + $"second_resultant_stage_exponent:{firstFactor - 1}";
    }

    private static string RunRationalRootOrbit(string[] args)
    {
        BigInteger firstFactor = Parse(args, 1, "first_factor");
        BigInteger secondFactor = Parse(args, 2, "second_factor");
        BigInteger order = Parse(args, 3, "order");
        if (
            firstFactor < 2
            || secondFactor < 2
            || firstFactor == secondFactor
            || order < 2
        )
        {
            throw new ArgumentException("invalid rational-root orbit domain");
        }
        bool firstZero = firstFactor % order == 0;
        bool secondZero = firstFactor * secondFactor % order == 0 && !firstZero;
        bool outsideStageZeros = !firstZero && !secondZero;
        BigInteger phaseOrder = firstFactor * (secondFactor - 2) + 1;
        BigInteger commonStep = Gcd(firstFactor - 1, secondFactor - 1);
        bool phi4Enabled = firstFactor % 4 == 3 && secondFactor % 4 == 3;
        bool phi6Enabled = firstFactor % 6 == 5 && secondFactor % 6 == 3;
        string category = "irrational";
        string ratio = "none";
        string firstCoefficient = "none";
        string secondCoefficient = "none";
        if (!outsideStageZeros)
        {
            category = "stage_zero";
        }
        else if (
            (firstFactor - 1) % order == 0
            && (secondFactor - 1) % order == 0
        )
        {
            category = "common_step";
            ratio = "-1";
            firstCoefficient = "-1";
            secondCoefficient = "1";
        }
        else if (order == 4 && phi4Enabled)
        {
            category = "phi4";
            ratio = "1";
            firstCoefficient = "1";
            secondCoefficient = "1";
        }
        else if (order == 6 && phi6Enabled)
        {
            category = "phi6";
            ratio = "2";
            firstCoefficient = "2";
            secondCoefficient = "1";
        }
        string Boolean(bool value) => value.ToString().ToLowerInvariant();
        return $"first_factor:{firstFactor}|second_factor:{secondFactor}|"
            + $"order:{order}|category:{category}|"
            + $"outside_stage_zeros:{Boolean(outsideStageZeros)}|"
            + $"phase_order:{phaseOrder}|"
            + $"phase_divisible:{Boolean(phaseOrder % order == 0)}|"
            + $"rational_ratio:{ratio}|"
            + $"primitive_first_coefficient:{firstCoefficient}|"
            + $"primitive_second_coefficient:{secondCoefficient}|"
            + $"common_step:{commonStep}|phi4_enabled:{Boolean(phi4Enabled)}|"
            + $"phi6_enabled:{Boolean(phi6Enabled)}";
    }

    private static string RunExceptionalCyclotomic(string[] args)
    {
        BigInteger value = Parse(args, 1, "base");
        BigInteger modulus = Parse(args, 2, "modulus");
        BigInteger firstFactor = Parse(args, 3, "first_factor");
        BigInteger secondFactor = Parse(args, 4, "second_factor");
        string family = args[5];
        if (
            modulus < 2
            || firstFactor < 2
            || secondFactor < 2
            || firstFactor == secondFactor
        )
        {
            throw new ArgumentException("invalid exceptional-cyclotomic domain");
        }
        BigInteger reducedBase = ((value % modulus) + modulus) % modulus;
        if (Gcd(reducedBase, modulus) != 1)
        {
            throw new ArgumentException("base must be a unit");
        }
        BigInteger order;
        BigInteger firstCoefficient;
        if (
            family == "phi4"
            && firstFactor % 4 == 3
            && secondFactor % 4 == 3
        )
        {
            order = 4;
            firstCoefficient = 1;
        }
        else if (
            family == "phi6"
            && firstFactor % 6 == 5
            && secondFactor % 6 == 3
        )
        {
            order = 6;
            firstCoefficient = 2;
        }
        else
        {
            throw new ArgumentException("family congruences do not hold");
        }
        (BigInteger firstPower, BigInteger firstQuotient) = GeometricPair(
            reducedBase,
            modulus,
            firstFactor
        );
        (_, BigInteger secondQuotient) = GeometricPair(
            firstPower,
            modulus,
            secondFactor
        );
        BigInteger aggregate = (
            firstCoefficient * firstQuotient + secondQuotient
        ) % modulus;
        BigInteger aggregateGcd = Gcd(aggregate, modulus);
        BigInteger cyclotomic = family == "phi4"
            ? (reducedBase * reducedBase + 1) % modulus
            : (
                reducedBase * reducedBase - reducedBase + 1
            ) % modulus;
        cyclotomic = (cyclotomic + modulus) % modulus;
        BigInteger cyclotomicGcd = Gcd(cyclotomic, modulus);
        string Status(BigInteger divisor) => divisor == 1
            ? "unit"
            : divisor < modulus ? "proper_factor" : "full_collision";
        string cofactor = "none";
        string cofactorGcd = "none";
        string cofactorStatus = "none";
        string extractionSource = "none";
        string extractionGcd = "none";
        BigInteger quotient = CompactExceptionalCofactor(
            reducedBase,
            modulus,
            firstFactor,
            secondFactor,
            family
        );
        BigInteger quotientGcd = Gcd(quotient, modulus);
        if (cyclotomic * quotient % modulus != aggregate)
        {
            throw new ArgumentException("compact cofactor identity failed");
        }
        cofactor = quotient.ToString();
        cofactorGcd = quotientGcd.ToString();
        cofactorStatus = Status(quotientGcd);
        if (cyclotomicGcd == 1 && quotientGcd != aggregateGcd)
        {
            throw new ArgumentException("unit cancellation changed GCD");
        }
        if (cyclotomicGcd > 1 && cyclotomicGcd < modulus)
        {
            extractionSource = "cyclotomic";
            extractionGcd = cyclotomicGcd.ToString();
        }
        else if (quotientGcd > 1 && quotientGcd < modulus)
        {
            extractionSource = "cofactor";
            extractionGcd = quotientGcd.ToString();
        }
        else if (cyclotomicGcd == modulus)
        {
            if (aggregateGcd != modulus)
            {
                throw new ArgumentException("full Phi collision did not force F=0");
            }
            extractionSource = "full_collision";
        }
        BigInteger firstGcd = Gcd(firstQuotient, modulus);
        BigInteger secondGcd = Gcd(secondQuotient, modulus);
        BigInteger firstPublicBoundGcd = Gcd(secondFactor, modulus);
        BigInteger secondPublicBoundGcd = Gcd(
            firstCoefficient * secondFactor,
            modulus
        );
        BigInteger denseDegree = firstFactor * (secondFactor - 1) - 2;
        return $"base:{reducedBase}|modulus:{modulus}|family:{family}|"
            + $"order:{order}|first_factor:{firstFactor}|second_factor:{secondFactor}|"
            + $"first_coefficient:{firstCoefficient}|second_coefficient:1|"
            + $"cyclotomic_residue:{cyclotomic}|cyclotomic_gcd:{cyclotomicGcd}|"
            + $"cyclotomic_status:{Status(cyclotomicGcd)}|"
            + $"aggregate_residue:{aggregate}|aggregate_gcd:{aggregateGcd}|"
            + $"aggregate_status:{Status(aggregateGcd)}|"
            + $"cofactor_residue:{cofactor}|cofactor_gcd:{cofactorGcd}|"
            + $"cofactor_status:{cofactorStatus}|extraction_source:{extractionSource}|"
            + $"extraction_gcd:{extractionGcd}|first_quotient_gcd:{firstGcd}|"
            + $"second_quotient_gcd:{secondGcd}|"
            + $"first_public_bound_gcd:{firstPublicBoundGcd}|"
            + $"second_public_bound_gcd:{secondPublicBoundGcd}|"
            + $"dense_cofactor_degree:{denseDegree}|"
            + $"dense_cofactor_coefficient_count:{denseDegree + 1}";
    }

    private static string RunExceptionalCofactorOverlap(string[] args)
    {
        BigInteger firstFactor = Parse(args, 1, "first_factor");
        BigInteger secondFactor = Parse(args, 2, "second_factor");
        string family = args[3];
        if (
            firstFactor < 2
            || secondFactor < 2
            || firstFactor == secondFactor
        )
        {
            throw new ArgumentException("invalid exceptional-cofactor domain");
        }
        BigInteger order;
        BigInteger remainderConstant;
        BigInteger remainderLinear;
        BigInteger secondPowerOfTwoExponent;
        string overlapSupport;
        BigInteger cofactorDegree = firstFactor * (secondFactor - 1) - 2;
        if (
            family == "phi4"
            && firstFactor % 4 == 3
            && secondFactor % 4 == 3
        )
        {
            order = 4;
            remainderConstant = (
                firstFactor * (secondFactor + 2) + 1
            ) / 4;
            remainderLinear = (
                firstFactor * (secondFactor - 2) + 1
            ) / 4;
            secondPowerOfTwoExponent = 0;
            overlapSupport = secondFactor.ToString();
        }
        else if (
            family == "phi6"
            && firstFactor % 6 == 5
            && secondFactor % 6 == 3
        )
        {
            order = 6;
            remainderConstant = -2 * (
                firstFactor * (secondFactor - 2) + 1
            ) / 3;
            remainderLinear = (
                firstFactor * (secondFactor + 4) + 4
            ) / 3;
            secondPowerOfTwoExponent = cofactorDegree;
            overlapSupport = $"2,{secondFactor}";
        }
        else
        {
            throw new ArgumentException("family congruences do not hold");
        }
        BigInteger resultant = family == "phi4"
            ? remainderConstant * remainderConstant
                + remainderLinear * remainderLinear
            : remainderConstant * remainderConstant
                + remainderConstant * remainderLinear
                + remainderLinear * remainderLinear;
        return $"family:{family}|order:{order}|first_factor:{firstFactor}|"
            + $"second_factor:{secondFactor}|cofactor_degree:{cofactorDegree}|"
            + $"remainder_constant:{remainderConstant}|"
            + $"remainder_linear:{remainderLinear}|"
            + $"cyclotomic_cofactor_resultant:{resultant}|"
            + $"first_stage_resultant_base:{secondFactor}|"
            + $"first_stage_resultant_exponent:{firstFactor - 1}|"
            + $"second_stage_power_of_two_exponent:{secondPowerOfTwoExponent}|"
            + $"second_stage_resultant_base:{secondFactor}|"
            + $"second_stage_resultant_exponent:{firstFactor - 1}|"
            + $"stage_overlap_support:{overlapSupport}";
    }

    private static BigInteger GeometricResidue(
        BigInteger value,
        BigInteger modulus,
        BigInteger count
    ) => count == 0
        ? BigInteger.Zero
        : GeometricPair(value, modulus, count).Sum;

    private static BigInteger PolynomialResidue(
        BigInteger[] coefficients,
        BigInteger value,
        BigInteger modulus
    )
    {
        BigInteger result = BigInteger.Zero;
        for (int index = coefficients.Length - 1; index >= 0; index--)
        {
            result = (
                result * value + coefficients[index]
            ) % modulus;
        }
        return (result + modulus) % modulus;
    }

    private static BigInteger PeriodicResidue(
        BigInteger[] pattern,
        BigInteger length,
        BigInteger value,
        BigInteger modulus
    )
    {
        BigInteger period = pattern.Length;
        BigInteger blocks = length / period;
        int tail = (int)(length % period);
        BigInteger block = PolynomialResidue(pattern, value, modulus);
        BigInteger blockSum = GeometricResidue(
            BigInteger.ModPow(value, period, modulus),
            modulus,
            blocks
        );
        BigInteger tailValue = PolynomialResidue(
            pattern.Take(tail).ToArray(),
            value,
            modulus
        );
        return (
            block * blockSum
            + BigInteger.ModPow(value, blocks * period, modulus) * tailValue
        ) % modulus;
    }

    private static BigInteger CompactExceptionalCofactor(
        BigInteger value,
        BigInteger modulus,
        BigInteger firstFactor,
        BigInteger secondFactor,
        string family
    )
    {
        if (family == "phi4")
        {
            BigInteger firstBlocks = (firstFactor - 3) / 4;
            BigInteger secondBlocks = (secondFactor - 3) / 4;
            BigInteger firstU = (
                (1 + value)
                    * GeometricResidue(
                        BigInteger.ModPow(value, 4, modulus),
                        modulus,
                        firstBlocks
                    )
                + BigInteger.ModPow(value, 4 * firstBlocks, modulus)
            ) % modulus;
            BigInteger nestedBase = BigInteger.ModPow(
                value,
                firstFactor,
                modulus
            );
            BigInteger nestedU = (
                (1 + nestedBase)
                    * GeometricResidue(
                        BigInteger.ModPow(nestedBase, 4, modulus),
                        modulus,
                        secondBlocks
                    )
                + BigInteger.ModPow(nestedBase, 4 * secondBlocks, modulus)
            ) % modulus;
            BigInteger alternatingSquare = (
                -value * value % modulus + modulus
            ) % modulus;
            BigInteger substitutedFactor = GeometricResidue(
                alternatingSquare,
                modulus,
                firstFactor
            );
            BigInteger firstResidualExponent = firstFactor - 2;
            BigInteger secondResidualExponent = firstFactor
                * (secondFactor - 2);
            BigInteger residualCount = (
                secondResidualExponent - firstResidualExponent
            ) / 2;
            BigInteger residual = BigInteger.ModPow(
                value,
                firstResidualExponent,
                modulus
            ) * GeometricResidue(
                alternatingSquare,
                modulus,
                residualCount
            ) % modulus;
            return (
                firstU + substitutedFactor * nestedU + residual
            ) % modulus;
        }

        BigInteger phi6FirstBlocks = (firstFactor - 5) / 6;
        BigInteger phi6SecondBlocks = (secondFactor - 3) / 6;
        BigInteger H(BigInteger item) => (
            BigInteger.ModPow(item, 3, modulus)
            + 2 * BigInteger.ModPow(item, 2, modulus)
            + 2 * item
            + 1
        ) % modulus;
        BigInteger phi6FirstU = H(value) * GeometricResidue(
            BigInteger.ModPow(value, 6, modulus),
            modulus,
            phi6FirstBlocks + 1
        ) % modulus;
        BigInteger nested = BigInteger.ModPow(
            value,
            firstFactor,
            modulus
        );
        BigInteger phi6NestedU = (
            H(nested)
                * GeometricResidue(
                    BigInteger.ModPow(nested, 6, modulus),
                    modulus,
                    phi6SecondBlocks
                )
            + BigInteger.ModPow(nested, 6 * phi6SecondBlocks, modulus)
        ) % modulus;
        BigInteger substituted = (
            PeriodicResidue(
                [1, 1, 0, -1, -1, 0],
                firstFactor,
                value,
                modulus
            )
            + BigInteger.ModPow(value, firstFactor, modulus)
                * PeriodicResidue(
                    [-1, 0, 1, 1, 0, -1],
                    firstFactor - 1,
                    value,
                    modulus
                )
        ) % modulus;
        BigInteger fixedQuotient = PolynomialResidue(
            [-1, -1, 0, 1, 1],
            value,
            modulus
        );
        BigInteger phi6Residual = (
            2
            * BigInteger.ModPow(value, firstFactor, modulus)
            * fixedQuotient
            * GeometricResidue(
                BigInteger.ModPow(value, 6, modulus),
                modulus,
                firstFactor * phi6SecondBlocks
            )
        ) % modulus;
        return (
            2 * phi6FirstU
            + substituted * phi6NestedU
            + phi6Residual
        ) % modulus;
    }

    private static string RunMultiplicationLowerBound(string[] args)
    {
        BigInteger exponent = Parse(args, 1, "exponent");
        if (exponent < 1)
        {
            throw new ArgumentException("exponent must be positive");
        }
        int result = 0;
        BigInteger capacity = BigInteger.One;
        while (capacity < exponent)
        {
            capacity <<= 1;
            result++;
        }
        return result.ToString();
    }

    private static string RunModPow(string[] args)
    {
        BigInteger modulus = Parse(args, 3, "modulus");
        if (modulus <= 0)
        {
            throw new ArgumentException("modulus must be positive");
        }
        BigInteger exponent = Parse(args, 2, "exponent");
        if (exponent < 0 || exponent > int.MaxValue)
        {
            throw new ArgumentException("exponent must fit a nonnegative Int32");
        }
        return BigInteger.ModPow(Parse(args, 1, "base"), (int)exponent, modulus).ToString();
    }

    private static string RunBatchGcd(string[] args)
    {
        BigInteger modulus = Parse(args, 1, "modulus");
        if (modulus <= 0)
        {
            throw new ArgumentException("modulus must be positive");
        }
        return string.Join(
            ",",
            args[2].Split(',').Select(value => Gcd(BigInteger.Parse(value), modulus))
        );
    }

    private static string RunSeparator(string[] args)
    {
        BigInteger n = Parse(args, 1, "n");
        BigInteger g = Parse(args, 2, "base");
        BigInteger exponent = Parse(args, 3, "exponent");
        if (n < 2 || exponent <= 0 || exponent > int.MaxValue)
        {
            throw new ArgumentException(
                "n must be at least 2 and exponent must fit a positive Int32"
            );
        }

        BigInteger reducedBase = ((g % n) + n) % n;
        BigInteger baseGcd = Gcd(reducedBase, n);
        if (baseGcd > 1 && baseGcd < n)
        {
            return $"direct_factor|{baseGcd}|none";
        }
        if (baseGcd == n)
        {
            return "invalid_base|none|none";
        }

        BigInteger residue = BigInteger.ModPow(reducedBase, (int)exponent, n);
        BigInteger factor = Gcd(residue - 1, n);
        if (factor == 1)
        {
            return $"miss|none|{residue}";
        }
        if (factor == n)
        {
            return $"simultaneous_collision|none|{residue}";
        }
        return $"factor|{factor}|{residue}";
    }

    private static string RunLucasSeparator(string[] args)
    {
        BigInteger n = Parse(args, 1, "n");
        BigInteger parameter = Parse(args, 2, "parameter");
        BigInteger exponent = Parse(args, 3, "exponent");
        if (n < 2 || exponent <= 0 || exponent > int.MaxValue)
        {
            throw new ArgumentException(
                "n must be at least 2 and exponent must fit a positive Int32"
            );
        }

        parameter = ((parameter % n) + n) % n;
        BigInteger discriminantGcd = Gcd(parameter * parameter - 4, n);
        if (discriminantGcd > 1 && discriminantGcd < n)
        {
            return $"discriminant_factor|{discriminantGcd}|none";
        }
        BigInteger residue = LucasV((int)exponent, parameter, n);
        BigInteger factor = Gcd(residue - 2, n);
        if (discriminantGcd == n && factor == 1)
        {
            return $"degenerate_miss|none|{residue}";
        }
        if (discriminantGcd == n && factor == n)
        {
            return $"degenerate_collision|none|{residue}";
        }
        if (discriminantGcd == n)
        {
            return $"degenerate_factor|{factor}|{residue}";
        }
        if (factor == 1)
        {
            return $"miss|none|{residue}";
        }
        if (factor == n)
        {
            return $"simultaneous_collision|none|{residue}";
        }
        return $"factor|{factor}|{residue}";
    }

    private static string RunLucasRootCountDirect(string[] args)
    {
        int prime = ParsePositiveInt(args, 1, "prime");
        int exponent = ParsePositiveInt(args, 2, "exponent");
        if (prime < 3 || prime % 2 == 0)
        {
            throw new ArgumentException("prime must be odd");
        }
        int count = 0;
        for (int parameter = 0; parameter < prime; parameter++)
        {
            if (LucasV(exponent, parameter, prime) == 2 % prime)
            {
                count++;
            }
        }
        return count.ToString();
    }

    private static BigInteger LucasV(int index, BigInteger parameter, BigInteger modulus)
    {
        BigInteger previous = 2 % modulus;
        if (index == 0)
        {
            return previous;
        }
        BigInteger current = parameter % modulus;
        for (int value = 1; value < index; value++)
        {
            BigInteger next = (parameter * current - previous) % modulus;
            previous = current;
            current = next < 0 ? next + modulus : next;
        }
        return current;
    }

    private static int ParsePositiveInt(string[] args, int index, string name)
    {
        BigInteger value = Parse(args, index, name);
        if (value < 1 || value > int.MaxValue)
        {
            throw new ArgumentException($"{name} must fit a positive Int32");
        }
        return (int)value;
    }

    private static BigInteger StageOneExponent(int bound)
    {
        BigInteger exponent = 1;
        for (int value = 2; value <= bound; value++)
        {
            exponent = exponent / Gcd(exponent, value) * value;
        }
        return exponent;
    }

    private static string RunSemismooth(string[] args)
    {
        BigInteger n = Parse(args, 1, "n");
        int baseBound = ParsePositiveInt(args, 2, "base_bound");
        int smoothBound = ParsePositiveInt(args, 3, "smooth_bound");
        int cofactorBound = ParsePositiveInt(args, 4, "cofactor_bound");
        if (n < 2 || baseBound < 2)
        {
            throw new ArgumentException("n must be at least 2 and base_bound at least 2");
        }

        BigInteger stageExponent = StageOneExponent(smoothBound);
        BigInteger lastBase = BigInteger.Min(baseBound, n - 1);
        for (BigInteger currentBase = 2; currentBase <= lastBase; currentBase++)
        {
            BigInteger baseGcd = Gcd(currentBase, n);
            if (baseGcd > 1 && baseGcd < n)
            {
                return $"factor:{baseGcd}";
            }
            if (baseGcd == n)
            {
                continue;
            }
            for (int multiplier = 1; multiplier <= cofactorBound; multiplier++)
            {
                BigInteger exponent = multiplier * stageExponent;
                BigInteger residue = BigInteger.ModPow(currentBase, exponent, n);
                BigInteger factor = Gcd(residue - 1, n);
                if (factor > 1 && factor < n)
                {
                    return $"factor:{factor}";
                }
            }
        }
        return "unresolved";
    }

    private static string RunSemismoothSuccessCount(string[] args)
    {
        BigInteger n = Parse(args, 1, "n");
        BigInteger exponent = Parse(args, 2, "exponent");
        if (n < 2 || exponent < 1)
        {
            throw new ArgumentException("n must be at least 2 and exponent positive");
        }

        BigInteger count = 0;
        for (BigInteger currentBase = 0; currentBase < n; currentBase++)
        {
            BigInteger baseGcd = Gcd(currentBase, n);
            bool success;
            if (baseGcd > 1 && baseGcd < n)
            {
                success = true;
            }
            else if (baseGcd == n)
            {
                success = false;
            }
            else
            {
                BigInteger residue = BigInteger.ModPow(currentBase, exponent, n);
                BigInteger factor = Gcd(residue - 1, n);
                success = factor > 1 && factor < n;
            }
            if (success)
            {
                count++;
            }
        }
        return count.ToString();
    }

    public static int Main(string[] args)
    {
        try
        {
            Console.WriteLine(Run(args));
            return 0;
        }
        catch (Exception error) when (error is ArgumentException or FormatException)
        {
            Console.Error.WriteLine($"ERROR: {error.Message}");
            return 2;
        }
    }
}
