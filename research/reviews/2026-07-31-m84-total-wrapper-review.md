# M84 adversarial total-wrapper review

## Review target and method

The review reconstructed the bounded semantics from:

- `research/proofs/M84-bounded-total-promise-wrappers.md`;
- `python/mosef_reference/promise_wrappers.py`;
- the existing `THM-001` and `THM-002` success lemmas; and
- `tests/test_promise_wrappers.py`.

This is a separate adversarial reconstruction inside the repository, not an
external peer review. The probability arithmetic was checked from the
success complements \(1-5/12=7/12\) and \(1-1/12=11/12\), independently of
the wrapper control flow.

## Threat checklist

| Threat | Adversarial check | Outcome |
|---|---|---|
| `UNRESOLVED` treated as prime or nonmember | Trace every exhausted and child-propagation branch | Rejected; it carries no factors and no membership status |
| Partial factor list exposed as complete | Force the left child to finish before the right child is unresolved | Rejected; child failure discards the accumulated list |
| Invalid factor accepted | Inspect the common recursive split boundary | Rejected; \(1<h<K\) and \(h\mid K\) are asserted before recursion |
| Prime multiplicity lost | Check maximal powers, \(2^e\), \(3^e\), and mixed even inputs | Rejected by exact branch tests |
| Lucas full-discriminant branch skipped | Trace `evaluate_lucas_candidate` under the bounded wrapper | Rejected; the sequence GCD is still evaluated |
| Nonsplit theorem applied to an even node | Trace preprocessing order | Rejected; verified factors \(2\) are removed before Lucas sampling |
| Outside-promise success inferred | Inspect proof, both papers, and result API | Rejected; only totality and no-wrong-factor correctness are unconditional |
| Local tail promoted to a complete tail | Reconstruct recursion count and union bound | Repaired explicitly with the factor \(4m\) and cap at one |
| Independence between recursive nodes assumed | Condition on the complete prior history at every visited node | Rejected; the union bound needs only the conditional local tail |
| Infinite or hidden budget | Inspect the public parameter and cost statement | Rejected; \(s\) is a positive charged iteration count |
| Python oracle advertised as polynomial | Compare module docstring and paper computation model | Rejected; trial division is labeled a small exact reference |
| Sampler or schedule failure hidden | Recheck quantified domain | Repaired; totality assumes valid positive schedules and a total sampler, while invalid API values raise `ValueError` |

## Independent arithmetic reconstruction

For \(s\ge1\), the local failure events satisfy

\[
f_-(s)=(1-5/12)^s=(7/12)^s,\qquad
f_+(s)=(1-1/12)^s=(11/12)^s.
\]

The factor tree has at most \(m\) prime leaves counted with multiplicity,
hence fewer than \(2m\) binary-tree nodes. A maximal-perfect-power base is
not itself a perfect power, so unary power nodes cannot be consecutive and
can be injected into the following binary-tree nodes. The complete wrapper
therefore uses fewer than \(4m\) invocations. For the \(j\)-th possible
randomized node, conditioning on its being reached and on all earlier
outcomes leaves failure probability at most \(f_\pm(s)\). Summing over fewer
than \(4m\) positions gives the two capped bounds in the proof.

No mutual independence between node events was used.

## Review result

PASS for the M84 bounded theorem and executable semantics after making the
global \(4m\) union bound, sampler/schedule domain, and Python performance
limitation explicit.

This review does not recognize either hereditary promise, prove an
outside-promise success rate, or change the OPEN status of general classical
polynomial-time factoring.
