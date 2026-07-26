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
