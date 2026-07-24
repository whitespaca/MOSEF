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
