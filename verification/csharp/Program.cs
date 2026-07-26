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
            "semismooth" when args.Length == 5 => RunSemismooth(args),
            "semismooth-success-count" when args.Length == 3 =>
                RunSemismoothSuccessCount(args),
            _ => throw new ArgumentException("unknown operation or wrong argument count"),
        };
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
