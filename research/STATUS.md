# Research Status

## M81 outcome

- Date: 2026-07-31.
- Branch: `research/20260731-m81-bitlength-audit`.
- Base: M80 squash merge
  `3bce2703a18156937f9d5acbe1e6d1d80d156ebf`.
- External-review repair: `DEF-001`, `AGENTS.md`, `CODEX.md`, the original
  prompt, affected proofs, and both manuscripts now use the standard binary
  input length
  \[
  \operatorname{bitlength}(N)
  =\lfloor\log_2N\rfloor+1
  =\lceil\log_2(N+1)\rceil .
  \]
- `BAR-064` proves that the former \(\lceil\log_2N\rceil\) quantity is one
  smaller exactly at powers of two and agrees everywhere else. `REF-060`
  records the former all-input identification as refuted.
- Exact impact audit: powers \(2^e\) move to length \(e+1\); odd prime powers
  and residual non-perfect-powers keep their index. Exact perfect-power
  preprocessing preserves the two hereditary promise proofs, while every
  live recursion, sampler, and schedule parameter now names the standard
  length.
- Frozen finite preservation: every balanced selector input is an odd
  semiprime, so its standard and legacy indices agree. EXP-0059 independently
  reconstructed all 26 M50 rows for \(9\le m\le34\), totaling 12,245 primes
  and 11,628,152 distinct pairs; no M31--M46 population, threshold, signature,
  or frozen hash changed.
- EXP-0059 checked all 1,048,576 positive integers through \(2^{20}\), finding
  exactly the 21 powers \(2^0,\ldots,2^{20}\) as discrepancies and 1,048,555
  non-power agreements. Its canonical summary SHA-256 is
  `19435b38800bd75dec6fb628731eaa94a9fc5d0a9898cbf02e0edeec5d4ac709`;
  the schema file SHA-256 is
  `fd3ab80dfca08de5620db8f8d86b60ba2648a626d859579a8e4d5a8404150a46`.
- Validation: full 269-test Python suite (345.528 s), Ruff, strict mypy over
  30 source files, compileall, M0 foundation, bilingual publication
  consistency (268 claims and 58 experiment hashes), EXP-0059 differential,
  Rust formatting/Clippy and 36 tests, and warning-free Release C# build all
  pass. The focused M81 module has 5/5 passing tests, including \(2^{12}\)
  and \(3^8\) recursive perfect-power cases.
- Paper gate: converged XeLaTeX produced 125 English pages and 53 Korean pages
  with no undefined references, citations, overfull boxes, or missing glyphs.
  One pre-existing harmless English underfull paragraph remains. Rendered QA
  covered the English M81 definition/result pages, the full BAR-064 proof, and
  the Korean M81 section. PDF SHA-256 values are
  `71a957c59c98f5135c65b34f54974d6eb49c4d2201cb73a1d6229828b802fadc`
  and
  `dbaada8f8fbb3ed3ad11dea35e3cc0fbc69a70db1935f975319559f372cca070`.
- Scope: M81 corrects exact input-size semantics. It creates no separator,
  recognizes no hereditary promise, proves no UCSS premise, extends no finite
  length range, and does not solve general classical polynomial-time
  factoring.
- Next selected milestone: M82, split the monograph into focused bilingual
  promise-factorization, cyclotomic-extraction, and finite-certificate papers
  while retaining the archival claim map.

### M81 Korean summary

기존 \(m=\lceil\log_2N\rceil\) 표기는 \(N=2^e\)에서 실제 이진
비트길이보다 정확히 1 작았다. M81은 표준 정의
\(m=\lfloor\log_2N\rfloor+1\)로 헌법, 원장, 증명, 영문·국문 논문을
교정했다. 균형 selector 인증 입력은 모두 odd semiprime이므로 이
예외집합에 속하지 않으며, 26개 동결 행과 기존 hash는 유지된다.
이는 정의 결함의 교정이지 새로운 separator나 일반 정수분해 정리가
아니다.

## M80 outcome - research paused

- Date: 2026-07-30.
- Branch: `research/20260730-m60-m80-synthesis`.
- Base: M59 squash merge
  `08fb840d3db052699d274ed58750e0a0cc892e64`.
- M60--M63 close the elementary residue route: exact residue unions,
  endpoint-compatible linear moduli, minimal-divisor antichains, and
  first-period rebucketing do not supply a subleading endpoint bound.
- M64--M65 prove the fixed-channel barrier and preserve polynomially many
  channels as `OPEN-006`.
- M66--M72 define UCSS and prove the complete conditional reduction
  `COND-004`, while explicitly rejecting finite-table uniformity.
- M73--M75 prove `THM-020`: an unconditional polynomial-time algorithm for
  the restricted public-Phi4-separable semiprime class, with branch-total
  evaluation.
- M76--M79 complete the dependency, reproducibility, and adversarial scope
  audits.
- M80 result (`BAR-063`): the original general classical polynomial-time
  factoring goal remains open. The repository contains a restricted
  unconditional theorem, a general conditional theorem, and exact method
  barriers; none is promoted to an unconditional general solution.
- EXP-0058 passes 32 residue profiles, 271 admissible-divisor profiles,
  85,812 exact residue candidates, 10 separator profiles, 94 separated-pair
  checks, 94 proper factors, and 42 row hashes.
- Registered summary SHA-256:
  `98c64e889c9554562f1c934cbbb123fa9e91e8e0fc8a906e4bb7807352670e37`.
- Registered schema SHA-256:
  `fedb065411473ae130f4360b16318df21979d30875675a14c9cf7da4d7f31603`.
- Validation: targeted 22 tests, full 264-test Python suite (336.558 s),
  Ruff, mypy, compileall, M0 foundation, EXP-0058 differential,
  publication consistency (265 claims and 57 experiment hashes), Rust
  formatting/clippy and 36 tests, and Release C# build all pass.
- Paper gate: XeLaTeX produced 125 English pages and 53 Korean pages with
  no undefined references, overfull boxes, or missing glyphs. One harmless
  English underfull paragraph is recorded. SHA-256 values are
  `db3089cbe81a3bc9b2f97e1e4bf54a76b4cedc985ead163b585d5c175fcf010a`
  and
  `da6e1a3c932b84c81fd808020d258a844d9cc9ae8ae778b087b294c466e52e64`;
  rendered QA covered the English two-page synthesis and Korean synthesis
  page.
- Research is paused after M80 by user instruction.

### M80 Korean summary

M60부터 M80까지 residue counting, channel 확장, uniform separator,
conditional reduction, restricted algorithm을 하나의 status-separated
dependency chain으로 완결했다. 일반 정수에 대한 고전적 다항 시간
인수분해 알고리즘은 증명되지 않았다. 대신 public Phi4 signature가
두 인수를 분리하는 제한 class에서는 unconditional algorithm을
증명했고, UCSS existence를 명시적 가정으로 둔 general conditional
theorem을 증명했다. M80 완료에 따라 연구를 일시 중단한다.

## M59 outcome

- Date: 2026-07-30.
- Branch: `research/20260730-m59-half-order-size`.
- Base: M58 squash merge
  `1bb35f42a2ab9d682719dc445dba12823e0e5f1c`.
- Result: `BAR-052` proves that every balanced overlap prime has
  \(p<33^{d_p}\), \(p\equiv1\pmod{2d_p}\),
  \(d_p=\Omega(m)\), and first gap \(q=\Omega(\log m)\).
- Consequence: the size floor removes only an initial logarithmic gap
  range. It does not exclude \(D=\lfloor m/2\rfloor\), so size alone
  cannot delete the largest prefix-LCM term.
- EXP-0057 passes 20 balanced windows, 1,894 prime profiles, 622 eligible
  odd half-orders, 622 strict size and residue checks, and 1,894 hashes.
- Registered summary SHA-256:
  `b3ebb32c0d59bae938475391af569ee9b166972d03cb106c1c6085f6d2dd625e`.
- Registered schema SHA-256:
  `0e40a80364951c2bfda5f4d09769e71d7d6686bb826899f0a7e7e3bf05d60599`.
- Validation: targeted 18-test module, full 260-test Python suite
  (335.312 s), Ruff, mypy, compileall, M0 foundation, EXP-0057
  differential, publication consistency (241 claims and 56 experiment
  hashes), Rust formatting/clippy and 36 tests, and Release C# build pass.
- Paper gate: warning-free XeLaTeX produced 123 English pages and 51 Korean
  pages. SHA-256 values are
  `414f2f982a78bb103865ab738d134a8cb4ad8c869ffa177efdd6cf19f1899f3e`
  and
  `a079f2801a3bcd175d54664d41ea95fa5707db45b851f8120a4c31b58b69d00e`;
  rendered inspection covered both M59 theorem pages.

### M59 Korean summary

M59는 실제 overlap prime의 half-order가 입력 길이에 선형으로
커야 하고, 해당 prime이 \(1\bmod 2d_p\)에 놓여야 함을 증명했다.
그러나 이것이 주는 first-gap 하한은 로그 크기뿐이므로 endpoint
\(q=\lfloor m/2\rfloor\)를 제거하지 못한다. 이는 크기 조건의
방법론적 한계이며 실제 prime occurrence에 대한 부정 명제가 아니다.

## M58 outcome

- Date: 2026-07-30.
- Branch: `research/20260730-m58-overlap-prime-orders`.
- Base: M57 squash merge
  `b155b97b7a00ecc07c0fb45e781fa5ee9df6a812`.
- Research question: which primes can actually divide the overlap integers,
  and does recurrence across gap indices reduce the exact LCM ledger?
- Result: `BAR-051` proves, for every prime \(p>7\),
  \[
  p\mid R_q
  \Longleftrightarrow
  \operatorname{ord}_p(3/32)=2d_p,\quad
  d_p\text{ odd},\quad d_p\mid2^q-1.
  \]
  When nonempty, the full occurrence-level set is exactly the multiples of
  \(a_p=\operatorname{ord}_{d_p}(2)\).
- Consequence: occurrence is periodic, but these repeats are exactly the
  index-divisibility repeats already removed by the prefix LCM. A new
  endpoint improvement would need a restriction on possible first periods
  or half-orders, not another recurrence count.
- EXP-0056 passes 5,129 prime profiles through 50,000, 82,064 direct
  divisibility checks through gap sixteen, 44 finite-window hit primes,
  74 periodic hit positions, and 5,129 sequence hashes.
- Registered canonical summary SHA-256:
  `41eb014eb5071fae4c7a33a98f66e5b7d0529c47cab832dd89fc8b493ed9b485`.
- Registered schema file SHA-256:
  `6ed0636dd95d3ab5a677cedc9859eebcf0148d4628b4ded61a1226f64edca0c8`.
- Validation: the targeted 17-test module, the 259-test Python suite
  (336.822 s), Ruff, mypy, compileall, M0 foundation, EXP-0056 differential,
  publication consistency (237 claims and 55 experiment hashes), Rust
  formatting/clippy and 36 tests, and the Release C# build all pass.
- Paper gate: warning-free XeLaTeX produced 123 English pages and 50 Korean
  pages. The SHA-256 values are
  `f0675cdff39aa73c9f7e1d8510ad616c32c49c1f0bddb94d5fabcab029a2f591`
  and
  `1f8ad27a80ecec37d47dc029266f8cd8994f011a88e314b59b07f5aef97ab3df`,
  respectively; rendered inspection covered the English theorem and
  appendix proof and the Korean theorem page.

### M58 Korean summary

M58은 \(p>7\)이 overlap integer \(R_q\)를 나누는 조건을
\(3/32\bmod p\)의 exact multiplicative order로 완전히 분류했다.
한 prime의 occurrence gap은 임의 집합이 아니라 하나의 first period의
배수 전체이다. 그러나 이 inherited periodicity는 BAR-048의 exact
prefix LCM이 이미 제거한 중복과 같다. 유한 감사의 44/5,129 hit
비율은 asymptotic density로 외삽하지 않는다.

## M57 outcome

- Date: 2026-07-30.
- Branch: `research/20260730-m57-endpoint-zero-slack`.
- Base: M56 squash merge
  `61d42ba1561d719270196c187c7d0a7abef57c6a`.
- Research question: can exact LCM de-duplication and an optimized,
  input-length-dependent overlap threshold produce lower-order slack at the
  uniform \(c=1/2\) endpoint?
- Result: `BAR-050` constructs the endpoint-dense family
  \[
  r_\lambda=2^\lambda-1,\quad
  \Delta_\lambda=2^\lambda-2,\quad
  m_\lambda=\lceil\sqrt{2\lambda\Delta_\lambda}\rceil
  \]
  and proves a threshold-uniform method barrier. For
  \(h\le\lfloor2\Delta/m\rfloor\), the exact LCM charge already consumes the
  conservative population ledger. For larger \(h\), the Hamming capacity is
  \(2^{m/2+\Omega(m\log\lambda/\lambda)}\).
- Consequence: the fixed leading balance
  \(\max\{1/(2x),x/2\}\ge1/2\) has equality only at \(x=1\), and lower-order
  terms on the dense witness do not rescue the BAR-046 certificate.
  `OPEN-005` remains open: certificate failure is not endpoint injectivity.
- EXP-0055 passes 17 scales, 34 endpoint profiles, 17 switch dichotomies,
  47 rational coefficient profiles, and 102 independently reconstructed
  integer hashes.
- Registered canonical summary SHA-256:
  `c5f4a07e514e9307c66b3868a954925bd15ece3b48a2375ed834d8d7db37052f`.
- Registered schema file SHA-256:
  `da399a83a6152ced97e66a1cd747f803b912973f169927f328cf87b7ab22bc1b`.
- Validation: the targeted 16-test module, the 258-test Python suite
  (338.322 s), Ruff, mypy, compileall, M0 foundation, EXP-0055 differential,
  publication consistency (233 claims and 54 experiment hashes), Rust
  formatting/clippy and 36 tests, and the Release C# build all pass.
- Paper gate: warning-free XeLaTeX produced 121 English pages and 49 Korean
  pages. The SHA-256 values are
  `46e818dccf4f7e8942106452365da0a3405c59532264a292fc0cd09cd3d9195d`
  and
  `e5ea73c679e7300d637c2e046f698cbc70e9cdd236af3db0fc08ff606de9e774`,
  respectively; rendered inspection covered the English theorem and
  appendix proof and the Korean theorem page.

### M57 Korean summary

M57은 \(c=1/2\) endpoint를 정확히 포화하는 dense public list family를
구성하고, 모든 threshold \(h\)에서 BAR-046의 exact LCM/Hamming
certificate가 막힘을 증명했다. 작은 \(h\)에서는 \(R_D\)를 포함하는
LCM charge가 population ledger를 이미 소진하고, 큰 \(h\)에서는
low-weight Hamming capacity가 population보다 커진다. 이는 해당
certificate의 zero-slack barrier이지 endpoint signature의 injectivity,
balanced prime occurrence, 또는 일반 정수분해 난이도 정리가 아니다.

## M56 outcome

- Date: 2026-07-30.
- Branch: `research/20260730-m56-dense-full-prefix`.
- Base: M55 squash merge
  `3a9c6f7`.
- Research question: does maximum level packing realize only a sparse subset
  of the BAR-046 gap prefix?
- Result: `BAR-049` proves the exact equality
  \[
  \mathcal G_h(\{s,\ldots,s+\Delta\})
  =\{1,\ldots,\lfloor\Delta/h\rfloor\}.
  \]
  Every gap \(q\) is witnessed by
  \(\{s,s+q,\ldots,s+hq\}\).
- Consequence: realizability filtering deletes no charged gap for the dense
  interval. This does not imply that a balanced prime hits each witness or
  divides each overlap integer.
- EXP-0054 passes 96 constructive profiles, 624 explicit witnesses, 49
  exhaustive profiles, 14,755 subset-GCD enumerations, and 241 sequence
  hashes.
- Registered canonical summary SHA-256:
  `7a15643f88dcb66825845e76b27fdbe174f5f0458c89cdc9a608e15a6abef27a`.
- Registered schema file SHA-256:
  `bc406d68888a9e649d945d9e8d942d48ec30588146b4487067212a5b363c164f`.
- Validation: the targeted 15-test module, the 257-test Python suite
  (347.565 s), Ruff, mypy, compileall, M0 foundation, the 58-check baseline
  differential, EXP-0053 and EXP-0054 differentials, publication consistency
  (229 claims and 53 experiment hashes), Rust formatting/clippy and 36 tests,
  and the Release C# build all pass.
- Paper gate: warning-free XeLaTeX produced 120 English pages and 48 Korean
  pages. The SHA-256 values are
  `c61e590ed9ae3d2e525d3f90ad45b12ddbc052968c7e56225ef58e7b68472f01`
  and
  `219e6a5ecbd38d5c3a4321e6309e2a24b89f7cc40ddf301dec3593b4ee6cdb2a`,
  respectively; rendered inspection covered the English theorem and appendix
  proof and the Korean theorem page.

### M56 Korean summary

M56은 maximum-density interval이 BAR-046에서 charge한 GCD gap prefix
전체를 실제로 실현함을 증명했다. 각
\(q\le\lfloor\Delta/h\rfloor\)에 대해
\(\{s,s+q,\ldots,s+hq\}\)가 interval 안에 있고 offset GCD가 정확히
\(q\)이다. 따라서 dense worst-packed geometry에서는 unrealizable
gap을 제거해도 장부가 전혀 줄지 않는다. 다만 이는 gap의 기하학적
실현일 뿐 balanced prime의 공통 hit나 일반 인수분해 정리가 아니다.

## M55 outcome

- Date: 2026-07-30.
- Branch: `research/20260730-m55-overlap-gcd-lcm`.
- Base: M54 squash merge
  `500ab0b276800d1d035512e7eab2411ee199ecae`.
- Research question: can exact shared-divisor removal make the overlap-prefix
  prime-support ledger asymptotically smaller than its largest term?
- Result: `BAR-048` proves
  \(\gcd(R_a,R_b)=R_{\gcd(a,b)}\) and
  \(R_a\mid R_b\Longleftrightarrow a\mid b\).
- Exact LCM conclusion: for
  \(L_D=\operatorname{lcm}(R_1,\ldots,R_D)\),
  \[
  5(2^D-1)<\log_2L_D
  \le5\cdot2^{D+1}-10-4D.
  \]
  Thus \(\log_2L_D=\Theta(2^D)\); de-duplication changes finite constants
  but not the leading \(D+O(\log m)\) high-weight exponent.
- EXP-0053 passes 144 pair-GCD identities, 144 divisibility equivalences,
  12 prefix LCM profiles, 12 largest-value lower bounds, and 168 exact
  integer-hash checks.
- Registered canonical summary SHA-256:
  `b82926a482dd133d94a3e89f041d23ec225ea2d9d30061d25f6e75c017b01534`.
- Registered schema file SHA-256:
  `d9dd97ea9f29b3b9fb3042992b01a181b39d5c8a8a8ebe7d57d296c3745faeb3`.
- Final gates passed:
  - foundation and bilingual publication checks over 225 claims and 52
    experiment hashes;
  - 256 Python tests in 344.056 seconds, compileall, Ruff, and strict mypy
    over 28 source files;
  - Rust formatting/Clippy and 36 tests, plus a warning-free C# Release build;
  - baseline 58-check, M54, and M55 independent differential checks;
  - warning-free 119-page English and 47-page Korean XeLaTeX builds, with
    visual inspection of the M55 theorem, proof, and Korean section.
- Stable English PDF SHA-256:
  `5438232a464dd9b52b16b52290adccea3a08856be454965e1a9f2d3db0b82c5b`.
- Stable Korean PDF SHA-256:
  `5666ca1ac3dbe1cd404f971cf39870931c2de0331acf0b01ab2955e872ab18b2`.

### M55 Korean summary

M55는 overlap integer \(R_q\) 사이의 shared divisor를 exact GCD와
prefix LCM으로 모두 제거했다. \(\gcd(R_a,R_b)=R_{\gcd(a,b)}\)이고
\(R_a\mid R_b\)는 정확히 \(a\mid b\)와 동치이다. 그러나 exact
union-support ledger \(L_D\)는 마지막 항 \(R_D\)를 포함하므로
\(\log_2L_D=\Theta(2^D)\)가 유지된다. 따라서 shared divisor
deduplication만으로 uniform \(c=1/2\) 끝점의 strict slack을 얻을 수
없다. 이는 balanced prime occurrence에 대한 정리가 아니며 일반
고전적 인수분해는 여전히 열린 문제이다.

## M54 outcome

- Date: 2026-07-30.
- Branch: `research/20260730-m54-realizable-gap-endpoint`.
- Base: M53 squash merge
  `027144c1f47283edf58e5175e1fd90920a45e49f`.
- Research question: can charging only GCD gaps realized by selected
  \((h_m+1)\)-subsets make the BAR-046 maximum gap uniformly smaller?
- Result: `BAR-047` proves
  \(\max\mathcal G_h(T)\le\lfloor\Delta/h\rfloor\) and constructs the
  equality family \(T=\{s,s+q,\ldots,s+hq\}\) for every \(h,q\ge1\).
  Its maximum-density containing interval has \(r=\Delta+1\) and realizes
  the same gap.
- Method conclusion: realizability pruning cannot universally improve the
  leading maximum-gap exponent by a fixed factor or little-o term. This does
  not provide a balanced prime divisor of \(R_q\) or an injective endpoint
  selector.
- EXP-0052 passes 96 extremal equality and dense-interval witnesses, 32 complete ambient
  profiles, 544 subset-GCD enumerations, and 256 sequence-hash checks.
- Registered canonical summary SHA-256:
  `fc09459c7cc6b93a2be7b8255e28fc64f3637e3b9a015ef45757f4b91a7da96c`.
- Registered schema file SHA-256:
  `69c181a7529a6f8a42534146b293add4abe32c3bf845a2da7764d59ad77bcf1c`.
- Final gates passed:
  - foundation and bilingual publication checks over 221 claims and 51
    experiment hashes;
  - 255 Python tests in 344.875 seconds, compileall, Ruff, and strict mypy
    over 28 source files;
  - Rust formatting/Clippy and 36 tests, plus a warning-free C# Release build;
  - baseline 58-check, M53, and M54 independent differential checks;
  - warning-free 119-page English and 47-page Korean XeLaTeX builds, with
    visual inspection of the M54 theorem, proof, and Korean section.
- Stable English PDF SHA-256:
  `27cb85a5d5fcf38c026b1b2df1b87e86dc819eb943e07e0437174aec2c86700c`.
- Stable Korean PDF SHA-256:
  `a6954dc944ee7c6ad082dcfbb072c5dd0b87dde86841150ac105fc87dc20f5e9`.

### M54 Korean summary

M54는 실제 \((h+1)\)-subset이 만드는 GCD gap만 남기면 BAR-046의
최대 gap 상한을 보편적으로 줄일 수 있는지 검사했다. 모든 실현 gap은
\(\lfloor\Delta/h\rfloor\) 이하이지만, 등차수열
\(\{s,s+q,\ldots,s+hq\}\)가 이 상한을 정확히 달성한다. 따라서
realizability만으로 uniform \(c=1/2\) 끝점을 닫을 strict slack은
얻을 수 없다. 이 결과는 geometry ledger의 sharpness일 뿐
\(R_q\)의 balanced prime divisor 존재나 단사 construction을 뜻하지
않는다.

## M53 outcome

- Date: 2026-07-30.
- Branch: `research/20260730-m53-distinct-gap-ledger`.
- Base: M52 squash merge
  `963ccf4fe038d047565a9362200280dd2b10686d`.
- Research question: can repeated \((h_m+1)\)-subset charges be deduplicated
  by their common GCD gap and close the M52 endpoint?
- Candidate result: `BAR-046` charges each possible overlap integer
  \(R_q\), \(1\le q\le\lfloor\Delta_m/h_m\rfloor\), once. The high-weight
  exponent falls from \(x/2+c/x\) to \(c/x\), while the low-weight exponent
  remains \(x/2\).
- Uniform conclusion: every fixed \(0<c<1/2\) is excluded by a rational
  \(2c<x<1\). If \(\ell_m/\log_2m\to a\), the refined range is every fixed
  \(c\) for \(a\le1\), and \(c<a/[4(a-1)]\) for \(1<a\le2\).
- `OPEN-005` preserves the uniform \(c=1/2\) endpoint. The current ledger
  charges gaps that may not be realizable by any selected level subset, so a
  noncertificate is not an injective construction.
- EXP-0051 passes 40 profiles, 40 strict subset reductions, 120
  exact-integer hash checks, 25 finite collision certificates, and 15 finite
  noncertificates.
- Registered canonical summary SHA-256:
  `7b066fc90a8925934886c5e6ee9b819a4dda95bb00c32732430eda3b5d58376b`.
- Registered schema file SHA-256:
  `2828e1c7fcc2deb9e4bc182b5fad74f831626d1728e9376103d56d5e35ce5ac5`.
- Final gates passed:
  - foundation and bilingual publication checks over 217 claims and 50
    experiment hashes;
  - 254 Python tests in 223.114 seconds, compileall, Ruff, and strict mypy over
    28 source files;
  - Rust formatting/Clippy and 36 tests, plus a warning-free C# Release build;
  - the baseline 58-check cross-language differential and the M49, M51, M52,
    and M53 independent checkers, including 120 exact M53 integer-hash checks
    and 40 strict subset-to-gap reductions;
  - warning-free 117-page English and 46-page Korean XeLaTeX builds, with
    visual inspection of the M53 theorem, appendix proof, and Korean theorem
    page.
- Stable English PDF SHA-256:
  `3a58f35b25ca5198a2cb4011058dd7671c838be57a80a231f3d93b006a240e83`.
- Stable Korean PDF SHA-256:
  `62f9bba7d2d1418063cab68ecc400064e3532cd9fbf87bd0f289ea0925c8ca94`.

### M53 Korean summary

M53은 \(h_m+1\)개 subset마다 같은 overlap integer를 반복 charge하지
않고 가능한 GCD gap \(q\le\Delta_m/h_m\)마다 \(R_q\)를 한 번만
charge한다. 그 결과 high-weight 지수는 \((c/x+o(1))m\), low-weight
지수는 \((x/2+o(1))m\)이 된다. 따라서 rational \(2c<x<1\)이 존재하는
모든 fixed \(c<1/2\)에서 exact compact-gap list는 결국 단사일 수
없다. \(c=1/2\) endpoint는 현재 장부에서 strict slack이 없고, 실제
subset이 만들 수 없는 gap도 포함하므로 M54의 열린 문제로 남긴다.

## M52 outcome

- Date: 2026-07-30.
- Branch: `research/20260730-m52-boundary-constants`.
- Base: M51 squash merge
  `66fc37459cb28d491bed6cff4ff341d6362039e7`.
- Research question: which constants at
  \(\Delta_m=\Theta(m^2/\log(r_m+1))\) are excluded by the exact
  higher-overlap ledger?
- Result: `BAR-045` combines distinct-level packing
  \(r_m\le\Delta_m+1\) with the rational order
  \(h_m=\lceil xm/\ell_m\rceil\). The uniform leading exponent
  \(x/2+c/x\) has minimum \(\sqrt{2c}\), proving eventual noninjectivity for
  every fixed \(0<c<1/8\) in the exact family.
- Growth-refined result: if
  \(\ell_m/\log_2m\to a\), every fixed \(c\) is excluded for \(a\le1\), while
  \(c<a/[16(a-1)]\) is excluded for \(1<a\le2\).
- `OPEN-004` preserves \(c=1/8\) and larger constants. The loss of strict
  ledger slack is not an injective construction.
- EXP-0050 passes 20 exact profiles, 60 exact-integer hash checks,
  12 below-endpoint finite collision certificates, eight endpoint-or-above
  noncertificates, and five growth thresholds.
- Registered canonical summary SHA-256:
  `89e5465e4f1bf4d577d77d3c7624682405ecf7b8aa208432916cab2e90a8d3aa`.
- Registered schema file SHA-256:
  `8265f5d4839f892640fe3c3530229bf08d584228850d9c07c35ce9208ac79f52`.
- Final gates passed:
  - foundation, M50 generated-artifact, and bilingual publication checks over
    212 claims and 49 experiment hashes;
  - 253 Python tests in 338.090 seconds, compileall, Ruff, and strict mypy over
    28 source files;
  - Rust formatting/Clippy and 36 tests, plus a warning-free C# Release build;
  - the baseline 58-check cross-language differential and the M49, M51, and
    M52 independent checkers, including 60 exact M52 integer-hash checks;
  - warning-free 114-page English and 45-page Korean XeLaTeX builds, with
    visual inspection of the M52 theorem, appendix proof, and both Korean
    theorem pages.
- Stable English PDF SHA-256:
  `031e95be7d05d7752a8d6b58dfda524d319e81d99a5f12a72d41106bee53d9f8`.
- Stable Korean PDF SHA-256:
  `28a2dbce6b3b59195117671c77f33cc63aac2b60abef7230efa55c1d54b65960`.

### M52 Korean summary

M52는 서로 다른 정수 level을 쓰는 목록이 반드시
\(r_m\le\Delta_m+1\)을 만족한다는 packing 제약을 먼저 비용에 넣는다.
\(\Delta_m\le(c+o(1))m^2/\ell_m\)에서
\(h_m=\lceil xm/\ell_m\rceil\)를 쓰면 exact high-weight 장부의 지수는
\((x/2+c/x+o(1))m\) 이하이고, 최솟값은 \(\sqrt{2c}\)다. 따라서
exact compact-gap family에서 모든 고정 \(c<1/8\)은 결국 단사일 수
없다. \(c=1/8\)은 현재 장부의 한계일 뿐 양성 construction이 아니며
M53의 열린 문제로 유지한다.

## M51 outcome

- Date: 2026-07-30.
- Branch: `research/20260730-m51-superlinear-span-cost`.
- Base: M50 squash merge
  `4911cfbf247d09a0b0c2ffab990eda5060ea6cee`.
- Research question: can BAR-043's fixed higher-overlap order be balanced
  against a superlinear public span without hiding subset multiplicity,
  factor access, or superpolynomial evaluation cost?
- Result: `DEF-037` chooses a public-geometry analytical order
  \(h_m\asymp\sqrt{\Delta_m/\log(r_m+1)}\). `BAR-044` proves eventual
  noninjectivity when
  \(\Delta_m\log_2(r_m+1)=o(m^2)\), including every polynomial-size
  \(O(m^{2-\varepsilon})\) span for fixed \(\varepsilon>0\).
- Exact scope retained: one factor-independent
  \(A=3,B_t=2^t+3,g=2\) compact-gap family. The
  \(\Theta(m^2/\log m)\) constant boundary, quadratic and larger spans,
  other compact grammars, adaptive schedules, and general factoring remain
  open.
- EXP-0049 passes 12 superlinear profiles, 62,128 balanced-prime
  signatures, 2,450,864 coordinates, and 12 independent variable-order and
  pair reconstructions. No finite profile is injective or satisfies the
  conservative asymptotic inequality; the proof does not extrapolate those
  observations.
- Registered canonical summary SHA-256:
  `cf4874600194e17b654bd40e29c33b96babff4860758e79c19f7e76981c63fd2`.
- Registered schema file SHA-256:
  `4552818335844443ca9781ab44008a68f18288fdbc557b32c71c4de362cf3003`.
- Final gates passed:
  - foundation, M50 generated-artifact, and bilingual publication checks over
    207 claims and 48 experiment hashes;
  - 251 Python tests in 339.801 seconds, compileall, Ruff, and strict mypy over
    28 source files;
  - Rust formatting/Clippy and 36 tests, plus a warning-free C# Release build;
  - the baseline 58-check cross-language differential and the M46--M49 and
    M51 independent checkers, including 2,450,864 M51 coordinate checks;
  - warning-free 112-page English and 43-page Korean XeLaTeX builds, with
    visual inspection of the M51 theorem, appendix proof, Korean theorem, and
    Korean reproduction/limitations pages.
- Stable English PDF SHA-256:
  `c6bf9c2c7ec173e45bad5485d15ece9571022c6441e5037107f0011a2e3802c9`.
- Stable Korean PDF SHA-256:
  `6c2e465b02f0e151904da516115d86b9c72345cafea3ebf7d2cd5d6602a0be8f`.

### M51 Korean summary

M51은 BAR-043의 고정 overlap 차수 대신 공개 level 목록의 span과 후보 수만
사용하는 \(h_m\asymp\sqrt{\Delta_m/\log(r_m+1)}\)를 택한다. 증가하는
subset 수를 그대로 비용에 포함해도
\(\Delta_m\log_2(r_m+1)=o(m^2)\)이면 고중량 예외 집합과 저중량
signature 공간이 모두 \(2^{o(m)}\)임을 증명한다. 따라서 정확한
compact-gap family에서 모든 polynomial subquadratic span은 결국
단사일 수 없다. 이는 일반 정수분해 lower bound가 아니며
\(\Theta(m^2/\log m)\) 경계와 다른 문법은 여전히 열린 문제다.

## M50 outcome

- Date: 2026-07-30.
- Branch: `research/20260730-m50-publication-feedback`.
- Base: M49 squash merge
  `e286a0042ca2cda57fdc31e143ecc65605ea57fd`.
- Research question: can the current M29--M49 paper and
  computer-assisted finite promise theorem be made externally reviewable
  without changing any mathematical claim status?
- The supplied feedback is treated as a publication-integrity milestone, not
  a request for a new general factoring claim.
- Evidence target:
  - one machine-readable \(m=9..34\) family-relative threshold artifact
    generated from the 16 registered M31--M46 schemas;
  - English and Korean tables generated from the same 26 rows;
  - explicit compact-step versus standard bit-operation accounting;
  - explicit online evaluator versus offline certificate/proof procedure;
  - a minimum checker path and documented language-implementation overlap;
  - removal of unstable numerical claim counts from both titles;
  - structural synthesis of the repeated finite threshold audits while
    preserving detailed evidence.
- Falsification checks:
  - reject any source row whose repair profile is noninjective;
  - reject any mismatch in source file or embedded summary hashes;
  - reject missing or duplicate lengths, wrong local offsets or strict
    endpoints, hand-divergent bilingual rows, or missing scope warnings;
  - do not infer an incremental-repair minimum where the source milestone did
    not separately certify one.
- The initial M50 artifact has schema version `1.0.0`, 26 rows, 16 frozen
  sources, and canonical summary SHA-256
  `1fb6185f73b4bc2243dc2f339c1e823d7c849acd7bf33ef5f288af4baa9d00b3`.
- Final gates passed:
  - foundation and bilingual publication checks over 203 claims and 47
    experiment hashes;
  - the generator check, stdlib-only minimum checker, and seven M50 unit tests;
  - 249 Python tests in 339.450 seconds, compileall, Ruff, and strict mypy over
    28 source files;
  - Rust formatting/Clippy and 36 tests, plus a warning-free C# Release build;
  - the baseline 58-check cross-language differential and the M46--M49
    independent checkers, including 5,440,051 M46 certificate-pair checks,
    1,636,992 M48 coordinates, and 3,645,232 M49 coordinates.
- XeLaTeX produced warning-free 111-page English and 41-page Korean PDFs.
  Rendered title, integrated-table, complexity/trust-boundary, conclusion, and
  reproduction pages have no clipping, overlap, missing glyph, or malformed
  mathematics.
- Stable file SHA-256 values are:
  - M50 JSON:
    `2f9974d45a350f65694bd048bf67dae4b27a90493b07ecd895c251d102aab75b`;
  - English PDF:
    `235bf1a9e073251a132f19b8aab43b775edf7f3c99069357be2a128ad664b3cb`;
  - Korean PDF:
    `ce018b74285714f6e8e2a9eceaf7a8e978ec29662b8db11c508cdd137a59f7cf`.
- Validated environment: Microsoft Windows `10.0.26200` x64,
  PowerShell `5.1.26100.8875`, Python `3.12.8`, Ruff `0.16.0`, mypy
  `2.3.0`, Rust/Cargo `1.84.0`, .NET SDK `8.0.420`, Git
  `2.55.0.windows.1`, Latexmk `4.87`, and XeTeX
  `3.141592653-2.6-0.999997` (MiKTeX 25.4).
- No `research/CLAIMS.md` or `research/PUBLICATION_CLAIMS.md` status or
  statement has changed.
- After M50 delivery and merge, autonomous mathematical research resumes at
  M51. Per the latest user instruction, the bounded milestone loop continues
  through M80 and pauses only after M80 is completed.

### M50 Korean summary

M50은 새로운 정수분해 정리를 주장하지 않고 M29--M49의 유한 증거를 외부
검토 가능한 형태로 재구성했다. M31--M46의 등록 스키마 16개에서
\(m=9,\ldots,34\)의 family-relative threshold 26행을 자동 생성하고,
영문·국문 논문이 동일한 표를 사용하도록 했다. compact-step과 표준
bit-operation, online evaluator와 offline certificate 생성 비용을 분리했으며,
최소 검증기와 certificate 신뢰 경계를 문서화했다. 전체 249개 Python 테스트,
Rust/C# 검증, M46--M49 독립 대조, 무경고 영문 111쪽·국문 41쪽 PDF 빌드와
대표 페이지 시각 검수를 통과했다. 일반 고전적 다항시간 정수분해는 여전히
해결되지 않았고 어떤 claim status도 승격하지 않았다.

## M49 outcome

- Date: 2026-07-29.
- Branch: `research/20260729-m49-wide-span-compact-gaps`.
- Base: M48 squash merge
  `8d13c1544bb87c1d756bd2fde1458aee69af4ddb`.
- `DEF-036` records primes whose compact-gap signatures have weight at least
  \(h+1\), and counts all remaining signatures by the exact Hamming-ball
  capacity \(\sum_{j=0}^{h}\binom{r_m}{j}\).
- If one prime hits levels \(t_0<\cdots<t_h\), `BAR-043` proves that it
  divides
  \[
  R_q=3^{2^q-1}+32^{2^q-1},
  \qquad
  q=\gcd(t_1-t_0,\ldots,t_h-t_0)\le\Delta_m/h.
  \]
  The proof uses the odd quotients
  \((2^{d_i}-1)/(2^q-1)\) to preserve the negative overlap sign under
  Bezout reduction.
- For every fixed linear span \(\Delta_m\le Cm\), choosing a fixed integer
  \(h>2C\) makes the possible high-weight population exponentially smaller
  than the inspected \(\Omega(2^{m/2}/m)\) balanced population. The
  low-weight Hamming-ball capacity is polynomial, so duplicate signatures
  are eventually unavoidable.
- `REF-045` and NR-046 therefore refute every polynomial-size,
  polynomial-cost, linearly wide public level list from this exact
  \(A=3,B_t=2^t+3,g=2\) family.
- EXP-0048 checks 12 span-\(m\) and span-\(2m\) profiles at input lengths
  20, 24, 28, 32, 36, and 40: 62,128 balanced-prime signatures,
  3,645,232 coordinates, three common-support witnesses, and 12 independent
  pair formulas. No profile is injective and no prime reaches the registered
  high-weight threshold. No finite profile satisfies the conservative
  theorem inequality; the asymptotic claim comes only from the proof.
- Registered schema SHA-256:
  `970fb769aa2d307ff691ad19ee1226bae89ad860363fb726348b8d80144239ad`.
  Registered summary SHA-256:
  `958223f09db3abd12b46fcda81cc22a553158c1cc92ef4918ad8f2bc9a3202a9`.
- Final gates passed: foundation and bilingual publication checks
  (203 claims and 47 experiment hashes), 242 Python tests in 375.22 seconds,
  compileall, Ruff, strict mypy over 28 source files, Rust
  formatting/Clippy and 36 tests, and a warning-free C# Release build. The
  independent M49 checker passed all three common-support, 12 profile,
  3,645,232 coordinate, and 12 pair-formula checks.
- XeLaTeX produced warning-free 111-page English and 40-page Korean PDFs.
  Rendered title, M49 result, proof, reproduction, and Korean claim-appendix
  pages have no clipping, overlap, missing glyph, malformed mathematics, or
  unreadable text. Stable artifact SHA-256 values are
  `c9ff791064a5e5e87bb3af689610518d5fb978be474c3130373455c0f04b487f`
  and
  `57dd9428338a54f7dccea04a9e32a10deac88d006c1fdae90c7781256ecc81fb`.
- The result does not cover superlinear level spans, other bases or compact
  grammars, adaptive or input-dependent schedules, arbitrary circuits, or
  general factoring.
- Work pauses after the completed M49 delivery by explicit user instruction;
  no M50 milestone is started.

### M49 Korean summary

M49는 `BAR-042`가 남긴 \(m/2\) 이상의 폭을 고차 공통지지 관계로
처리했다. 하나의 소수가 \(h+1\)개 level을 동시에 hit하면, 첫 level과의
차이들의 최대공약수 \(q\)에 대응하는 단 하나의 overlap 정수
\(R_q=3^{2^q-1}+32^{2^q-1}\)를 나누며 \(q\le\Delta_m/h\)이다. 따라서
어떤 고정 선형 폭 \(\Delta_m\le Cm\)에도 \(h>2C\)를 고정하면 고중량
signature를 가질 수 있는 소수 수는 balanced population보다 지수적으로
작고, 나머지 저중량 signature 공간은 다항식 크기에 불과하다. 이로써
해당 compact-gap family의 모든 다항식 크기·다항식 비용 선형 폭
selector는 점근적으로 injective일 수 없음을 증명했다. 다만 superlinear
폭, 다른 compact grammar, adaptive schedule 및 일반 소인수분해 문제는
여전히 해결되지 않았다. M49 전달 후에는 사용자 지시에 따라 연구를
일시정지한다.

## M48 outcome

- Date: 2026-07-29.
- Branch: `research/20260729-m48-encoded-parameter-escape`.
- Base: M47 squash merge
  `886d572acbe07f707ad4e0dde66592cfc9612b23`.
- Start commit `b9da929664960929f0249acca11cac04e6436296` is pushed. Draft
  PR #59 targets `main`:
  `https://github.com/whitespaca/MOSEF/pull/59`.
- `DEF-035` defines a public increasing list of exact compact \(\Phi_4\)
  candidates \(A=3,B_t=2^t+3,g=2\), with descriptor, modular recurrence,
  GCD, and extraction cost charged. Polynomial branch-total cost requires
  \(\sum_jt_{m,j}=\operatorname{poly}(m)\), not merely a polynomial number
  of descriptors.
- If a prime \(p>7\) hits levels \(t<u\), `BAR-042` proves
  \[
  p\mid R_{u-t}:=
  3^{2^{u-t}-1}+32^{2^{u-t}-1},
  \]
  whose bit length is at most \(5(2^{u-t}-1)+1\). The relation depends only
  on the public gap and is invariant under a common level shift.
- Let \(J_m\) contain balanced primes hitting at least two candidates. Exact
  square-free support charging gives
  \[
  |J_m|\le
  \sum_{i<j}
  \left\lfloor
  \frac{5(2^{t_{m,j}-t_{m,i}}-1)+1}
       {\lfloor(m-1)/2\rfloor}
  \right\rfloor.
  \]
  Outside \(J_m\), only the all-zero and \(r_m\) one-hot signatures occur.
- Combining this bound with `BAR-041`'s inspected
  \(\Omega(2^{m/2}/m)\) balanced-population lower bound proves that every
  polynomial-size list with span
  \(\Delta_m\le(1/2-\varepsilon)m\) is eventually noninjective.
  `REF-044` and NR-045 therefore refute the exact short-span encoded
  compact-gap program.
- The theorem does not cover level spans approaching or exceeding \(m/2\),
  other bases or exceptional families, adaptive or input-dependent
  schedules, other compact grammars, or general factoring.
- ADR-052 keeps descriptor/evaluation cost, exponentially long exact
  cofactors, and analytical overlap support in separate ledgers. It charges
  only the exact pair-overlap consequence and never materializes a cofactor.
- EXP-0047 checks 42 shifted quarter-span profiles, 163,794 balanced-prime
  signatures, 1,636,992 coordinates, 11 exact overlap integers, three
  nontrivial common-support witnesses, and 42 independent pair formulas.
  Forty profiles satisfy the finite theorem inequality; none is injective.
- Registered schema SHA-256:
  `c1a659a6081df2b46f492379b97c9b624f0041772068d19e89337550c19eaa8e`.
  Registered summary SHA-256:
  `48b95a0e1acb799fce06e2aa25492eebc432daef6c6e8c14abd962ef0c7170d2`.
- Final gates passed: foundation and bilingual publication checks
  (199 claims and 46 experiment hashes), 240 Python tests and 249 subtests
  in 261.31 seconds with the cache provider disabled, compileall, Ruff,
  strict mypy over 28 source files, Rust formatting/Clippy and 36 tests, and
  a warning-free C# Release build. The independent M48 checker passed all 11
  overlap, 42 profile, 1,636,992 coordinate, 42 pair-formula, and three
  common-support checks.
- XeLaTeX produced warning-free 108-page English and 39-page Korean PDFs.
  Rendered title, M48 result, proof, reproduction, and claim-appendix pages
  have no clipping, overlap, missing glyph, malformed mathematics, or
  unreadable text. Stable artifact SHA-256 values are
  `42e0c72dc99507c1ebd13cc8d49dc225a45a7bea680a693aff084f52bf504396`
  and
  `036aa00e7fe3c8ee4d76013f3c941f0d0f763f73ba9259f206bd8513c15a374d`.
- Next selected milestone: M49 tests wide-span encoded level lists at and
  beyond the half-length boundary, where the pairwise magnitude bound becomes
  inconclusive and higher-order overlap structure is required.

### M48 Korean summary

M48은 \(B_t=2^t+3\) compact candidate를 polynomial 개 사용하더라도,
public level span이 \((1/2-\varepsilon)m\) 이하이면 충분히 큰 balanced
population을 단사적으로 분리할 수 없음을 증명했다. 두 level을 동시에
hit하는 소수는 level gap만으로 정해지는 exact overlap integer
\(3^{2^d-1}+32^{2^d-1}\)를 나누므로 multi-hit prime 전체를 보수적으로
상계할 수 있다. 나머지 소수에는 all-zero와 one-hot signature만
가능하며, 그 수보다 balanced prime이 지수적으로 많아 duplicate
signature가 생긴다. 이 결과는 exponential exact cofactor를
materialize하지 않으며 shifted window에도 그대로 적용된다. 다만 span이
\(m/2\)에 접근하거나 이를 넘는 wide-span list, 다른 compact family,
adaptive schedule, 일반 정수분해는 열린 범위로 남고 M49에서 다룬다.

## M47 outcome

- Date: 2026-07-29.
- Branch: `research/20260729-m47-polynomial-cap-support`.
- Base: M46 squash merge
  `942302256bbb130df1c9180d3836357009e1a658`.
- Start commit `34f0152fc5e1de875f5f2bc060a5b799a5df3cd0` is pushed. Draft
  PR #58 targets `main`:
  `https://github.com/whitespaca/MOSEF/pull/58`.
- `DEF-034` defines the exact-output bit ledger \(W(m,L)\) over all eight
  positive primitive integers emitted by each exact DEF-032 descriptor. For
  \(b=\operatorname{bitlen}(L)\), every descriptor contributes at most
  \(2L^2b+Lb+9b+5\) bits and there are at most \(2(L-1)^3\) descriptors.
  Hence
  \[
  W(m,L)\le
  2(L-1)^3(2L^2b+Lb+9b+5)=O(L^5\log L).
  \]
- Every balanced support prime \(p\) has
  \(\lfloor(m-1)/2\rfloor\) bits, so charging each nonconstant primitive
  coordinate to an exact nonzero output integer gives
  \(\lfloor(m-1)/2\rfloor h\le W(m,L)\), where \(h\) is the number of
  balanced primes occurring anywhere in the complete selector support.
- The inspected Rosser--Schoenfeld (1962) bounds
  \(x/\log x<\pi(x)\) for \(x\ge17\) and
  \(\pi(x)<1.25506x/\log x\) for \(x>1\), together with the exact check
  \(128\cdot50000^2-81\cdot62753^2=1,026,940,271>0\), imply that the
  complete balanced-prime population has size
  \(\Omega(2^{m/2}/m)\).
- `BAR-041` therefore proves that every factorization-independent DEF-032
  schedule with polynomial numeric cap \(L(m)\) is eventually noninjective:
  at least two balanced primes lie outside all primitive support and receive
  the common all-zero signature. `REF-043` and NR-044 refute the corresponding
  universal injectivity program for this exact grammar.
- The scope is deliberately narrow. The result does not cover polynomial-bit
  encodings of exponentially large numeric parameters, adaptive or
  input-dependent schedules, other compact grammars, arithmetic circuits, or
  general classical factoring algorithms. In particular, the compact gap
  \(B=2^t+3\) from `BAR-022` is outside `BAR-041`.
- ADR-051 adopts exact-output bit charging because it safely handles zeros,
  constants, exact cofactor division, duplicate outputs, and descriptor
  multiplicity without inferring a false lower bound from finite threshold
  data.
- EXP-0046 audits 963 descriptors, 7,704 exact primitive values, 25,346
  branch-support incidences, and 31 independently counted prime populations.
  The cap-profile exact/upper output-bit totals are
  \(3,948/742,400\), \(26,076/3,303,542\),
  \(115,600/18,157,500\), and \(377,063/56,929,700\) for caps
  9, 12, 16, and 20.
- Registered schema SHA-256:
  `a37f9d495de85943a69a6c3fbc122c9f09fbce0f78316c32163c380a782ef525`.
  Registered summary SHA-256:
  `b9c97e8161d3470ad61d20fd9ee8834888e5f0139e1b3fd5b3fbe3b2a6463093`.
- Final gates passed: foundation and bilingual publication checks
  (195 claims and 45 experiment hashes), 235 Python tests and 221 subtests
  in 217.27 seconds with the cache provider disabled, compileall, Ruff,
  strict mypy over 27 source files, Rust formatting/Clippy and 36 tests, and
  a warning-free C# Release build. The independent M47 differential checker
  passed all 963 descriptor, 7,704 exact-value, 25,346 branch-support, and
  31 population checks.
- XeLaTeX produced warning-free 106-page English and 37-page Korean PDFs.
  Rendered title, M47 result, proof, reproduction, and claim-appendix pages
  have no clipping, overlap, missing glyph, malformed mathematics, or
  unreadable text. Stable artifact SHA-256 values are
  `73c05d9940fa8a92d1a63f837383259ab52448e302d3af19241d51231f34cd47`
  and
  `ce5c957371dd40e3c9c54bb69ca8d402a82c6b5890884bc836c472567fc8426a`.
- Next selected milestone: M48 tests whether a polynomial-size public selector
  using polynomial-bit encodings of exponentially large numeric parameters
  can evade `BAR-041` while retaining polynomial branch-total evaluation.

### M47 Korean summary

M47은 정확한 DEF-032 선택자에서 숫자 cap \(L(m)\) 자체가 다항식으로
제한되면, 충분히 큰 모든 입력 길이에서 balanced-prime 모집단을 단사적으로
분리할 수 없음을 증명했다. 핵심은 각 비상수 좌표를 그 좌표를 활성화할 수
있는 소수를 포함한 정확한 공개 정수 출력에 과금하는 것이다. 전체 출력
비트 예산은 \(O(L^5\log L)\)이고 각 balanced prime은
\(\lfloor(m-1)/2\rfloor\)비트를 요구하지만, 전체 balanced-prime 모집단은
Rosser--Schoenfeld의 점검된 소수 계수 경계에 따라
\(\Omega(2^{m/2}/m)\)이다. 따라서 다항식 숫자 cap은 결국 적어도 두 소수를
모든 좌표의 지지집합 밖에 남겨 같은 영벡터 서명을 만든다. 이 장벽은
지수적으로 큰 숫자를 다항식 길이로 부호화하는 매개변수, 적응형 또는
입력 의존형 일정, 다른 압축 문법, 산술 회로, 일반 고전 정수분해
알고리즘에는 적용되지 않는다. 다음 M48은 바로 이 부호화 매개변수의
회피 가능성을 검증한다.

## M46 outcome

- Date: 2026-07-29.
- Branch: `research/20260729-m46-length-34-caps`.
- Base: M45 squash merge
  `0975334e2443adbbc67c62eeaf41f13b2eb3eb65`.
- Start commit `3110dcd557ae5b819af5636a0adb6b05bd7af762` is pushed. Draft
  PR #57 targets `main`:
  `https://github.com/whitespaca/MOSEF/pull/57`.
- The complete \(m=34\) balanced population has 3,299 primes and 5,440,051
  unordered pairs. Both inherited caps fail. Cap 196 leaves
  \(\{97927,99527,127877\}\) and three pairs; cap 200 leaves
  \(\{97927,99527\}\) and one pair.
- Lossless exact partition refinement confines the post-cap-200 transition to
  the last pair. Cap 200 is noninjective and cap 201 is injective, so
  \(L_{34}^{\star}=201\).
- The unique new nonconstant primitive source
  `phi6:149:201:45:cofactor` has pattern \((1,0)\). It appends to 3,297
  predecessor coordinates to give a 3,298-coordinate certificate separating
  all 5,440,051 pairs. The minimum incremental repair size is one; no minimum
  claim is made for the full certificate.
- `THM-019` proves the smallest common finite additive offset through length
  34 is 167, so the repaired public schedule is \(m+167\).
- `BAR-040` proves the exact multiplicative coefficients through length 34
  are \(c>100/17\). The Farey-adjacent witness \(53/9\), larger by
  \(1/153\), gives cap 201.
- `REF-042` and NR-043 record that neither inherited M45 formula survives
  length 34. No recurrence, asymptotic rate, density, recognizer, or general
  factoring conclusion is inferred.
- ADR-050 preserves the exact partition method, registers the two distinct
  public caps, and requires a complete final repair-coordinate census.
- EXP-0045 checks 306,350,153 optimized public local exits, 306,366,391
  optimized cap-201 local exits, 20,278 independent transition exits, 81,112
  repair coordinates, 3,298 construction coordinates, and 5,440,051
  certificate pairs.
- Registered schema SHA-256:
  `34942d674d0451b219bde70fc65909ef3baa6516b08d61df36bf6ea91e8cde61`.
  Registered summary SHA-256:
  `52c7899c6d93a747b52fa531e4261ba842acbceb06ae28f420005f8606c85a11`.
- Independent differential validation passed 16 Rust/C# command
  comparisons, four dense vectors, 1,368,821 public-cap descriptor checks,
  20,278 transition local exits, 81,112 repair-coordinate checks, and
  5,440,051 construction-certificate pairs.
- Final gates passed: foundation and bilingual publication checks
  (191 claims and 44 experiment hashes), 231 Python tests and 206 subtests
  in 316.03 seconds with the cache provider disabled, compileall, Ruff,
  strict mypy over 26 source files, Rust formatting/Clippy and 36 tests, and
  a warning-free C# Release build.
- XeLaTeX produced warning-free 104-page English and 36-page Korean PDFs.
  Rendered title, M46 result, proof, reproduction, and claim-appendix pages
  have no clipping, overlap, missing glyph, malformed mathematics, or
  unreadable text. Stable artifact SHA-256 values are
  `c820e693157a9e70c493f11e965295771315bdab04e73709437314e141e58dfa`
  and
  `b72056d1bbc52bccb8f61a825b1fde5b90e46d083cc812703f1b140c1d827785`.
- Next selected milestone: M47 tests the asymptotic feasibility of every
  polynomially bounded DEF-032 cap by charging the total exact prime-support
  bit budget instead of extrapolating the finite threshold table.

### M46 Korean summary

M46에서는 \(m=34\)의 완전 balanced-prime 모집단 3,299개에 대해 기존
공개 상한 \(m+162=196\)과
\(\lceil147m/25\rceil=200\)을 각각 검사했다. cap 196은
\(\{97927,99527,127877\}\)과 세 충돌 pair를, cap 200은
\(\{97927,99527\}\) 한 pair를 남기므로 두 공식 모두 실패한다.
cap 201에서 추가되는 81,112개 primitive coordinate 중
`phi6:149:201:45:cofactor`만 패턴 \((1,0)\)으로 마지막 pair를
분리한다. 따라서 \(L_{34}^{\star}=201\), 최소 증분 repair 크기는
하나, 유한 envelope는 \(m+167\)과 \(c>100/17\)이다. 이는
\(m>34\), asymptotic cap 성장, 약속 인식, 또는 일반 고전적 다항 시간
정수분해를 증명하지 않는다.

## M45 outcome

- Date: 2026-07-29.
- Branch: `research/20260729-m45-length-33-caps`.
- Base: M44 squash merge
  `0632ce7f42e9cb8b91f3bbda0fc11fb67699574b`.
- PR #56 was independently reviewed, passed every available local and remote
  gate, and was squash-merged as
  `0975334e2443adbbc67c62eeaf41f13b2eb3eb65`.
- The complete \(m=33\) balanced population has 2,410 primes and 2,902,845
  unordered pairs. Both inherited caps fail: cap 168 leaves one 12-prime
  bucket and 66 pairs, while cap 172 leaves one eight-prime bucket and
  28 pairs.
- Lossless exact partition refinement confines all later collisions to the
  cap-172 bucket. The cap-172--195 collision counts are
  \(28,28,28,15,15,10,10,6,6,6,6,6,3,3,3,3,1,1,1,1,1,1,1,0\).
- The sole cap-194 collision is \(\{80309,92671\}\), and cap 195 is
  injective. Therefore \(L_{33}^{\star}=195\).
- The unique new nonconstant primitive source
  `phi4:195:91:20:cofactor` has pattern \((1,0)\). It appends to 2,409
  predecessor coordinates to give a 2,410-coordinate certificate separating
  all 2,902,845 pairs. The minimum incremental repair size is one; no minimum
  claim is made for the full certificate.
- `THM-018` proves the smallest common finite additive offset through length
  33 is 162, so the repaired public schedule is \(m+162\).
- `BAR-039` proves the exact multiplicative coefficients through length 33
  are \(c>194/33\). The Farey-adjacent witness \(147/25\), larger by
  \(1/825\), gives cap 195.
- `REF-041` and NR-042 record that neither inherited M44 formula survives
  length 33. No recurrence, asymptotic rate, density, recognizer, or general
  factoring conclusion is inferred.
- ADR-049 preserves the exact partition method and requires a complete final
  repair-coordinate census rather than treating a first witness as unique.
- EXP-0044 checks 158,193,605 optimized public local exits, 158,945,206
  optimized cap-195 local exits, 1,707,792 independent transition exits,
  224,896 repair coordinates, 2,410 construction coordinates, and 2,902,845
  certificate pairs.
- Registered schema SHA-256:
  `a9ba5df141ecefdf9c7a946bd5bf7f17dd44c5748b843385f6e1f0165e311cd2`.
  Registered summary SHA-256:
  `2a3d7c347eeea57c36fd3a585744a30818a5ff0543840607f91514e1786feb23`.
- Independent differential validation passed 16 Rust/C# command
  comparisons, four dense vectors, 866,180 public-cap descriptor checks,
  1,707,792 transition local exits, 224,896 repair-coordinate checks, and
  2,902,845 construction-certificate pairs.
- Final gates passed: foundation and bilingual publication checks
  (187 claims and 43 experiment hashes), 230 Python tests and 206 subtests
  in 295.58 seconds with the cache provider disabled, compileall, Ruff,
  strict mypy over 26 source files, Rust formatting/Clippy and 36 tests, and
  a warning-free C# Release build.
- XeLaTeX produced warning-free 101-page English and 34-page Korean PDFs.
  Rendered title, M45 result, proof, reproduction, and claim-appendix pages
  have no clipping, overlap, missing glyph, malformed mathematics, or
  unreadable text. Stable artifact SHA-256 values are
  `a7133ce0dc09636374e118331b64dfb4f7a828fb9eadd846851e136cc629502e`
  and
  `382af9e3fb1bcceaa4c92cc1497b2361d961b9273a4d74077c1c7eff4c1d5b6d`.
- Next selected milestone: M46 separately tests additive cap 196 and
  multiplicative cap 200 on the complete \(m=34\) population.

### M45 Korean summary

M45에서는 \(m=33\)의 완전 balanced-prime 모집단 2,410개에 대해 기존
공개 상한 \(m+135=168\)과 \(\lceil26m/5\rceil=172\)를 각각 검사했다.
cap 168은 12-prime bucket과 66개 pair를, cap 172는 8-prime bucket과
28개 pair를 남겨 두 공식 모두 실패한다. 정확한 동치분할 전이는
cap 194까지 \(\{80309,92671\}\)을 남기고 cap 195에서 처음 단사가
된다. 유일한 새 좌표 `phi4:195:91:20:cofactor`는 패턴 \((1,0)\)으로
마지막 pair를 분리한다. 따라서 \(L_{33}^{\star}=195\), 최소 증분
repair 크기는 하나, 유한 envelope는 \(m+162\)와 \(c>194/33\)이다.
이는 \(m>33\), asymptotic cap 성장률, 약속 인식, 또는 일반 고전적
다항 시간 정수분해를 증명하지 않는다.

## M44 outcome

- Date: 2026-07-29.
- Branch: `research/20260729-m44-length-32-caps`.
- Base: M43 squash merge
  `ef0750dd74ccfdc60060e690225f8126292ea7f4`.
- Start commit `667f3bc97588b219569926629dc749b5f5738808` is pushed. Draft
  PR #55 targets `main`:
  `https://github.com/whitespaca/MOSEF/pull/55`.
- M44 proof, implementation, registered experiment, and bilingual-paper core
  commit: `ee1f3ab1f6dbd77f2ea45b206a8f4bcbd5a46a6d`.
- The complete \(m=32\) balanced population has 1,750 primes and 1,530,375
  unordered pairs. The inherited public caps both fail: cap 145 leaves one
  14-prime bucket and 91 pairs, while cap 148 leaves one six-prime bucket
  and 15 pairs.
- Exact partition refinement retains precisely the non-singleton
  raw-signature classes. Appending coordinates cannot merge a discarded
  singleton, so the method is lossless and uses no hash or sampling.
- Raw selector inclusion confines every later collision to the cap-148
  bucket. Exact transition profiles at caps 148 through 167 give collision
  counts
  \(15,10,10,10,10,6,6,6,3,3,3,1,1,1,1,1,1,1,1,0\).
- The sole cap-166 collision bucket is \(\{59699,63463\}\), while cap 167
  is injective. Therefore \(L_{32}^{\star}=167\).
- Recording every primitive bit that changes a live class gives 1,748
  cap-166 coordinates that separate all but the last pair. The unique new
  cofactor pattern `phi4:167:119:93:cofactor` \(=(1,0)\) gives a
  1,749-coordinate certificate separating all 1,530,375 pairs.
- The minimum incremental repair size is one: cap 166 proves that zero new
  coordinates cannot suffice, and the displayed coordinate separates the
  final pair. The full 1,749-coordinate certificate is not claimed minimum.
- `THM-017` is `PROVED`: \(L=m+135\) is injective on every complete balanced
  population for \(9\le m\le32\), and 135 is the smallest common integer
  offset because cap 166 fails at length 32.
- `BAR-038` is `PROVED`: the exact multiplicative coefficients through
  length 32 are \(c>83/16\). The endpoint gives failed cap 166, while the
  Farey-adjacent witness \(26/5\), larger by \(1/80\), gives cap 167.
- `REF-040` is `REFUTED`: neither inherited M43 formula survives the new
  complete population. No recurrence or asymptotic rate is inferred.
- ADR-048 replaces retained full raw prefixes with exact equality-partition
  refinement and extracts the binary construction certificate from the same
  splits.
- EXP-0043 checked 82,130,579 optimized public local exits, 82,518,653
  optimized repair-cap local exits, 388,074 optimized and 791,952
  independent transition exits, 165,248 repair-coordinate cases, one
  minimum repair coordinate, 1,749 construction coordinates, and 1,530,375
  certificate pairs.
- Independent validation passed 16 Rust/C# command comparisons, four dense
  vectors, 548,388 public-cap descriptor checks, 791,952 transition
  local-exit checks, 165,248 repair-coordinate checks, and 1,530,375
  construction-certificate pairs.
- Registered schema SHA-256:
  `a05de0bf7941d2c44bf0d5d79488f90f467c33cb5a8ec986ca5de0aa5f39aa21`.
  Registered EXP-0043 summary SHA-256:
  `6d09e1831de30009de0e770dea2d17271e8e00ccff0c09ecd11aba42fdc55b13`.
- Final gates passed: foundation and bilingual publication checks
  (183 claims and 42 experiment hashes), 229 Python tests and 206 subtests
  in 221.28 seconds with the cache provider disabled, compileall, Ruff,
  strict mypy over 26 source files, Rust formatting/Clippy and 36 tests, and
  a warning-free C# Release build.
- XeLaTeX produced final-warning-free 99-page English and 33-page Korean
  PDFs. Rendered bilingual titles, the M44 result and evidence, complete
  proof, reproduction, and claim-appendix pages had no clipping, overlap,
  missing glyph, malformed mathematics, or unreadable text. Stable artifact
  SHA-256 values are
  `68e9a50b2b8494262940f9affe41c0106ff4aa52c9c84672e47b401fb9c31e97`
  and
  `eeb945cd6c90fdb09a9b3dcd884ad2c082f91cff9bae31b75d5383f63de49fd7`.
- Both repaired formulas remain factorization independent and use
  \(O(m^3\log m)\) compact work. Population enumeration, partition
  refinement, certificate extraction, and dense expansion are certificate
  operations. The finite result does not establish a cap growth rate,
  behavior at \(m>32\), promise recognition, or general factoring.
- Next selected milestone: M45 separately tests additive cap 168 and
  multiplicative cap 172 on the complete \(m=33\) population.

### M44 Korean summary

M44에서는 \(m=32\)의 완전한 balanced-prime 모집단 1,750개에 대해 기존
공개 상한 \(m+113=145\)와 \(\lceil60m/13\rceil=148\)을 각각 검사했습니다.
cap 145는 14개 소수의 한 충돌류와 91쌍을, cap 148은 6개 소수의 한
충돌류와 15쌍을 남기므로 두 공식 모두 실패합니다.

정확한 동치분할 정제는 비단일 raw-signature 충돌류만 유지합니다. 새
좌표를 추가해도 이미 다른 prefix는 다시 합쳐질 수 없으므로 이 방법은
손실이 없고 해시나 표본추출을 사용하지 않습니다. cap 148부터 167까지의
충돌쌍 수는
\(15,10,10,10,10,6,6,6,3,3,3,1,1,1,1,1,1,1,1,0\)입니다.
cap 166의 마지막 충돌은 \(\{59699,63463\}\)이고 cap 167은
단사이므로 \(L_{32}^{\star}=167\)입니다.

cap 166까지 기록한 1,748개 원시 좌표는 마지막 한 쌍을 제외한 모든
쌍을 분리합니다. 유일한 새 좌표
`phi4:167:119:93:cofactor`가 패턴 \((1,0)\)으로 그 쌍을 분리하여
1,749-coordinate 인증서를 완성합니다. 따라서 \(9\le m\le32\)의 최소
공통 additive offset은 135이고 정확한 계수 경계는 \(c>83/16\)입니다.
\(26/5\)는 cap 167을 주는 고정 성공 증인입니다. 이 결과는 유한하고
인수분해 의존적인 balanced-semiprime 약속 정리이며 \(m>32\), 점근적
cap 성장률, 약속 인식, 일반 고전 다항시간 정수분해를 증명하지 않습니다.

## M43 outcome

- Date: 2026-07-29.
- Branch: `research/20260729-m43-length-31-caps`.
- Base: M42 squash merge
  `15fb801a35c279e496922b2af8a4ea0d932bb115`.
- Start commit `fa6093971e8037e43b3a2b1beba64dba5e28c0f5` is pushed. Draft
  PR #54 targets `main`:
  `https://github.com/whitespaca/MOSEF/pull/54`.
- M43 proof, implementation, registered experiment, and bilingual-paper core
  commit: `df509f4af028851cefe39447effbd4b1a54cabfb`.
- The complete \(m=31\) balanced population has 1,280 primes and 818,560
  unordered pairs. The inherited public caps both fail: cap 124 leaves one
  18-prime bucket and 153 pairs, while cap 127 leaves one 12-prime bucket
  and 66 pairs.
- Raw selector inclusion confines every later collision to the cap-127
  bucket. Exact transition profiles at caps 127 through 144 give collision
  counts
  \(66,66,66,66,21,21,21,21,10,10,6,6,1,1,1,1,1,0\).
- The sole cap-143 collision bucket is \(\{37483,44963\}\), while cap 144
  is injective. Therefore \(L_{31}^{\star}=144\).
- The complete cap-144 normalization reduces 2,100,384 raw coordinates to
  3,474 nonconstant distinct columns. Selecting 3,361 cap-143 representative
  columns and appending the unique new cofactor pattern
  `phi6:11:105:144:cofactor` \(=(1,0)\) gives a 3,362-coordinate
  certificate separating all 818,560 pairs.
- The minimum incremental repair size is one: cap 143 proves that zero new
  coordinates cannot suffice, and the displayed coordinate separates the
  final pair. The full 3,362-coordinate certificate is not claimed minimum.
- `THM-016` is `PROVED`: \(L=m+113\) is injective on every complete balanced
  population for \(9\le m\le31\), and 113 is the smallest common integer
  offset because cap 143 fails at length 31.
- `BAR-037` is `PROVED`: the exact multiplicative coefficients through
  length 31 are \(c>143/31\). The endpoint gives failed cap 143, while the
  fixed witness \(60/13\), larger by \(1/403\), gives cap 144.
- `REF-039` is `REFUTED`: neither inherited M42 formula survives the new
  complete population. No recurrence or asymptotic rate is inferred.
- ADR-047 combines two lossless public-cap raw profiles with a complete
  12-prime bucket transition and one independent full cap-144 normalized
  profile.
- EXP-0042 checked 231,114,240 raw-prefix local exits, 983,880 transition
  local exits, 336,061,440 repair-profile local exits, 818,560 normalization
  equivalences, 14,688 repair-coordinate cases, one minimum repair
  coordinate, 3,362 construction coordinates, and 818,560 certificate
  pairs.
- Independent validation passed 16 Rust/C# command comparisons, four dense
  vectors, 346,608 public-cap descriptor checks, 983,880 transition
  local-exit checks, 14,688 repair-coordinate checks, and 818,560
  construction-certificate pairs.
- Registered schema SHA-256:
  `d333d0cebe6c79e2c7a02629be8c3c6a2ea84cb651e184a4cd3a08d1bef969db`.
  Registered EXP-0042 summary SHA-256:
  `c15234f614eb9602b6b704700a9660c4a0d486d7e2f965e59af2967eb2cf6888`.
- Final gates passed: foundation and bilingual publication checks
  (179 claims and 41 experiment hashes), 228 Python tests and 206 subtests
  in 177.11 seconds with the cache provider disabled, compileall, Ruff,
  strict mypy over 26 source files, Rust formatting/Clippy and 36 tests, and
  a warning-free C# Release build.
- XeLaTeX produced final-warning-free 97-page English and 31-page Korean
  PDFs. Rendered bilingual titles, the M43 result and evidence, complete
  proof, reproduction, and claim-appendix pages had no clipping, overlap,
  missing glyph, malformed mathematics, or unreadable text. Stable artifact
  SHA-256 values are
  `7ef3b29b83f17c6db1b7b0465ee9efdc36dbbb303a81ced8c6e2290d5b23d77d`
  and
  `68a5b487979f5c7c5d02eb25d9fde761c5a46dbf3714a436b67c6839c762d1ec`.
- Both repaired formulas remain factorization independent and use
  \(O(m^3\log m)\) compact work. Population enumeration, raw-prefix
  comparison, normalization, and dense expansion are certificate operations.
  The finite result does not establish a cap growth rate, behavior at
  \(m>31\), promise recognition, or general factoring.
- Next selected milestone: M44 separately tests additive cap 145 and
  multiplicative cap 148 on the complete \(m=32\) population.

### M43 Korean summary

M43에서는 \(m=31\)의 완전 balanced prime 모집단 1,280개에 대해 기존
공개 상한 \(m+93=124\)와 \(\lceil49m/12\rceil=127\)을 각각 전수
검사했습니다. cap 124는 18개 소수의 153쌍, cap 127은 12개 소수의
66쌍을 남기므로 두 공식 모두 실패합니다.

cap 127 이후의 완전 transition은 충돌 pair 수를
\(66,66,66,66,21,21,21,21,10,10,6,6,1,1,1,1,1,0\)으로
줄입니다. cap 143의 마지막 충돌은 \(\{37483,44963\}\)이고 cap 144는
단사이므로 \(L_{31}^{\star}=144\)입니다. cap 143 대표 좌표
3,361개에 유일한 새 cofactor 좌표 하나를 추가한 3,362-coordinate
certificate가 818,560개 모든 쌍을 분리합니다. cap 143이 실제로
실패하고 이 한 좌표가 충분하므로 새 좌표 한 개가 필요충분합니다.

따라서 \(9\le m\le31\)의 최소 공통 additive offset은 113으로
증가하고, 정확한 곱셈 경계는 \(c>143/31\)가 됩니다.
\(60/13\)은 cap 144를 주는 고정 성공 witness입니다. 이는 유한하고
인수분해 의존적인 balanced-semiprime 약속 정리이며, \(m>31\),
asymptotic cap 성장률, 약속 인식, 일반 고전적 다항 시간 정수분해는
여전히 증명되지 않았습니다.

## M42 outcome

- Date: 2026-07-29.
- Branch: `research/20260729-m42-length-30-caps`.
- Base: M41 squash merge
  `6c8282847aa7667315833581586b5a056e479989`.
- Start commit `2ac95f6db41cb22d2ff7297f94f9d34fcfa3727d` is pushed. Draft
  PR #53 targets `main`:
  `https://github.com/whitespaca/MOSEF/pull/53`.
- M42 proof, implementation, registered experiment, and bilingual-paper core
  commit: `ad565cf3a0d78a3469920d6b958248008ead5181`.
- The complete \(m=30\) balanced population has 927 primes and 429,201
  unordered pairs. The inherited public caps both fail: cap 106 leaves one
  14-prime bucket and 91 pairs, while cap 112 leaves one nine-prime bucket
  and 36 pairs.
- Raw selector inclusion confines every later collision to the cap-112
  bucket. Exact transition profiles at caps 112 through 123 give collision
  counts \(36,36,36,21,21,21,15,10,10,3,3,0\).
- The sole cap-122 collision bucket is
  \(\{28591,29209,29387\}\), while cap 123 is injective. Therefore
  \(L_{30}^{\star}=123\).
- The complete cap-123 normalization reduces 1,317,600 raw coordinates to
  2,503 nonconstant distinct columns. Selecting 2,401 cap-122 representative
  columns and appending the two unique new cofactor patterns
  `phi4:123:59:87:cofactor` \(=(0,0,1)\) and
  `phi4:79:123:54:cofactor` \(=(1,0,0)\) gives a 2,403-coordinate
  certificate separating all 429,201 pairs.
- The minimum incremental repair size is two: one binary coordinate cannot
  separate three primes, and the displayed two coordinates assign distinct
  repair signatures \(2,0,1\).
- `THM-015` is `PROVED`: \(L=m+93\) is injective on every complete balanced
  population for \(9\le m\le30\), and 93 is the smallest common integer
  offset because cap 122 fails at length 30.
- `BAR-036` is `PROVED`: the exact multiplicative coefficients through
  length 30 are \(c>61/15\). The endpoint gives failed cap 122, while the
  fixed witness \(49/12\) gives cap 123.
- `REF-038` is `REFUTED`: neither inherited M41 formula survives the new
  complete population. No recurrence or asymptotic rate is inferred.
- ADR-046 combines two lossless public-cap raw profiles with a complete
  nine-prime bucket transition and one independent full cap-123 normalized
  profile.
- EXP-0041 checked 112,980,906 raw-prefix local exits, 385,398 transition
  local exits, 152,676,900 repair-profile local exits, 429,201 normalization
  equivalences, 88,240 repair-coordinate cases, two minimum repair
  coordinates, 2,403 construction coordinates, and 429,201 certificate
  pairs.
- Independent validation passed 16 Rust/C# command comparisons, four dense
  vectors, 222,258 public-cap descriptor checks, 385,398 transition
  local-exit checks, 88,240 repair-coordinate checks, and 429,201
  construction-certificate pairs.
- Registered schema SHA-256:
  `cd6ca83c68b901a8b9f9572724e33e71d847d0399192691c1868ebdf7982ea9a`.
  Registered EXP-0041 summary SHA-256:
  `37e7339ee919f6497857ac20c45f37c34aa03a2aef6d80bf0779b95db50f2c0d`.
- Final gates passed: foundation and bilingual publication checks
  (175 claims and 40 experiment hashes), 227 Python tests in 170.66 seconds
  with the cache provider disabled, compileall, Ruff, strict mypy over 26
  source files, Rust formatting/Clippy and 36 tests, and a warning-free C#
  Release build.
- XeLaTeX produced final-warning-free 95-page English and 30-page Korean
  PDFs. Rendered bilingual titles, the M42 result and evidence, complete
  proof, reproduction, and claim-appendix pages had no clipping, overlap,
  missing glyph, malformed mathematics, or unreadable text. Stable artifact
  SHA-256 values are
  `cd9942a2445e42de5ce467a495c592c928a2b766a7b2e1fdf83011c2eeec5cbe`
  and
  `78e73a301c63eb86a4e4184050799d8c34ac52abe510cffb64667bef74a19108`.
- Both repaired formulas remain factorization independent and use
  \(O(m^3\log m)\) compact work. Population enumeration, raw-prefix
  comparison, normalization, and dense expansion are certificate operations.
  The finite result does not establish a cap growth rate, behavior at
  \(m>30\), promise recognition, or general factoring.
- Next selected milestone: M43 separately tests additive cap 124 and
  multiplicative cap 127 on the complete \(m=31\) population.

### M42 Korean summary

M42에서는 \(m=30\)의 완전 balanced prime 모집단 927개에 대해 기존
공개 상한 \(m+76=106\)과 \(\lceil26m/7\rceil=112\)을 각각 전수
검사했습니다. cap 106은 14개 소수의 91쌍, cap 112는 9개 소수의
36쌍을 남기므로 두 공식 모두 실패합니다.

cap 112 이후의 완전 transition은 충돌 pair 수를
\(36,36,36,21,21,21,15,10,10,3,3,0\)으로 줄입니다. cap 122의
마지막 충돌은 \(\{28591,29209,29387\}\)이고 cap 123은
단사이므로 \(L_{30}^{\star}=123\)입니다. cap 122 대표 좌표
2,401개에 서로 다른 unit pattern 두 개를 추가한 2,403-coordinate
certificate가 429,201개 모든 쌍을 분리합니다. 세 소수는 한 bit로
분리할 수 없으므로 새 좌표 두 개가 필요충분합니다.

따라서 \(9\le m\le30\)의 최소 공통 additive offset은 93으로
증가하고, 정확한 곱셈 경계는 \(c>61/15\)가 됩니다.
\(49/12\)은 cap 123을 주는 고정 성공 witness입니다. 이는 유한하고
인수분해 의존적인 balanced-semiprime 약속 정리이며, \(m>30\),
asymptotic cap 성장률, 약속 인식, 일반 고전적 다항 시간 정수분해는
여전히 증명되지 않았습니다.

## M41 outcome

- Date: 2026-07-29.
- Branch: `research/20260729-m41-length-29-caps`.
- Base: M40 squash merge
  `0c4895a50749f58ab1c04cef688ebecc1c318db3`.
- Start commit `6a234cf1b8436a1755fcf3ab630ca76a9c694672` is pushed. Draft
  PR #52 targets `main`:
  `https://github.com/whitespaca/MOSEF/pull/52`.
- M41 proof, implementation, registered experiment, and bilingual-paper core
  commit: `a424abb5422c98777580b92f3f9e52da69ec273a`.
- The repaired schedules give distinct caps \(m+76=105\) and
  \(\lceil26m/7\rceil=108\). Complete lossless raw-prefix profiles show that
  both caps are injective on all 685 balanced primes.
- Adjacent exact profiles establish the lower threshold: cap 102 has the sole
  collision \(\{18979,21031\}\), while cap 103 is injective. Therefore
  \(L_{29}^{\star}=103\).
- The complete cap-103 normalization reduces 766,224 raw coordinates to
  1,555 nonconstant distinct columns. Selecting 1,527 representative
  cap-102 columns and appending the unique new pair-distinguishing coordinate
  `phi4:87:95:103:cofactor` gives a 1,528-coordinate certificate separating
  all 234,270 population pairs.
- The minimum incremental repair size is one: the cap-102 collision proves
  that no zero-coordinate repair is possible, and the displayed coordinate
  assigns the final pair the pattern \((0,1)\).
- `THM-014` is `PROVED`: \(L=m+76\) is injective on every complete balanced
  population for \(9\le m\le29\), and 76 remains the smallest common integer
  offset because the controlling row is still \(m=28\).
- `BAR-035` is `PROVED`: the exact multiplicative coefficients through
  length 29 remain \(c>103/28\). The length-29 local endpoint
  \(102/29\) is smaller, and the witness \(26/7\) gives cap 108.
- `REF-037` is `REFUTED`: \(L_{29}^{\star}=103<104=L_{28}^{\star}\), so
  exact thresholds need not be nondecreasing across these different complete
  balanced populations. No decreasing or asymptotic trend is inferred.
- ADR-045 uses one lossless byte per descriptor-prime mask to compare exact
  raw prefixes at caps 102, 103, 105, and 108 without probabilistic hashing,
  followed by an independent full normalized cap-103 profile.
- EXP-0040 checked four raw-prefix profiles, one full normalized profile,
  75,200,670 raw-prefix local exits, 65,607,930 repair-profile local exits,
  234,270 normalization equivalences, 5,989 new repair descriptors, 11,978
  tracked-pair exits, 47,912 new primitive-coordinate checks, one
  distinguishing coordinate, 1,528 construction coordinates, and 234,270
  certificate pairs.
- Independent validation passed 16 Rust/C# command comparisons, four dense
  vectors, 234,270 independent construction pairs, 89,789 predecessor
  descriptor checks, 47,912 repair-coordinate checks, and 191,556 successful
  schedule-inclusion checks.
- Registered schema SHA-256:
  `5be568844cbf1cbf766d32d20d1aee1c6c2708c92ec71db33a5e12e7c6547566`.
  Registered EXP-0040 summary SHA-256:
  `a9d61b984cf77c3c875ddbcdfaa2d6c6d1cd9bd6939d4c35ba4e1433a91d1589`.
- Final gates passed: foundation and bilingual publication checks
  (171 claims and 39 experiment hashes), 226 Python tests and 206 subtests
  in 166.24 seconds with the cache provider disabled, compileall, Ruff,
  strict mypy over 26 source files, Rust formatting/Clippy and 36 tests, and
  a warning-free C# Release build.
- XeLaTeX produced final-warning-free 94-page English and 28-page Korean
  PDFs. Rendered bilingual titles, the M41 result and evidence, complete
  proof, reproduction, and claim-appendix pages had no clipping, overlap,
  missing glyph, malformed mathematics, or unreadable text. Stable artifact
  SHA-256 values are
  `7b5788292139a4252f0300cddecbd714560c787845c09180951bd91ec684a003`
  and
  `10dc9610c376c9550680f2de2d9cc0c4c49b26aefd9b72fadacf1ce9528a8004`.
- Both formulas remain factorization independent and use
  \(O(m^3\log m)\) compact work. Population enumeration, raw-prefix
  comparison, normalization, and dense expansion are certificate operations.
  The finite result does not establish a cap growth rate, behavior at
  \(m>29\), promise recognition, or general factoring.
- Next selected milestone: M42 separately tests additive cap 106 and
  multiplicative cap 112 on the complete \(m=30\) population.

### M41 Korean summary

M41에서는 \(m=29\)의 완전 balanced prime 모집단 685개에 대해 공개
상한 \(m+76=105\)와 \(\lceil26m/7\rceil=108\)을 각각 전수
검사했습니다. 두 상한은 모두 단사입니다. 인접한 정확 계산에서는 cap
102가 \(\{18979,21031\}\) 한 쌍만 충돌시키고 cap 103은 모든 소수를
분리하므로 \(L_{29}^{\star}=103\)입니다.

cap 102의 대표 좌표 1,527개에
`phi4:87:95:103:cofactor` 한 좌표를 추가한 1,528-coordinate
certificate가 234,270개 모든 쌍을 분리합니다. 따라서 새 좌표 한 개가
필요충분합니다. 길이 29의 local offset은 74이지만 길이 28의 offset
76이 더 크므로, \(9\le m\le29\)의 최소 공통 additive offset은
여전히 76이고 곱셈 경계도 \(c>103/28\)로 유지됩니다.

\(L_{29}^{\star}=103<104=L_{28}^{\star}\)이므로 서로 다른 완전
모집단 사이에서 threshold가 반드시 증가한다는 가설은 반박됩니다.
그러나 이 유한 반례는 감소 추세나 asymptotic cap 법칙, promise
인식, 일반 고전적 다항시간 정수분해를 증명하지 않습니다.

## M40 outcome

- Date: 2026-07-29.
- Branch: `research/20260729-m40-length-28-caps`.
- Base: M39 squash merge
  `2dd415534845ce9ef20dc6852cb42d050c7097ca`.
- Start commit `0248758e779d3120b51efe6db0c438ea33782b54` is pushed. Draft
  PR #51 targets `main`:
  `https://github.com/whitespaca/MOSEF/pull/51`.
- M40 proof, implementation, registered experiment, and bilingual-paper core
  commit: `c3a37c7bc7e58adde25d8e845b5b09e22df33dc3`.
- At \(m=28\), the M39 formulas give distinct caps:
  \(m+60=88\) and \(\lceil16m/5\rceil=90\). The complete 507-prime
  population at cap 88 has the sole collision bucket
  \(\{11867,12791,13633,13967,14051,15559\}\), producing 15 failed
  pairs across all 58,464 descriptors.
- All 2,679 descriptors added through cap 90 preserve the same bucket and
  all 15 failed pairs. Raw selector inclusion confines every later collision
  to the original cap-88 bucket.
- Exact incremental transition checks give collision-pair counts
  \(15,15,15,10,6,6,6,3,3,1,1,1,1,1,1,1,0\) at caps 88 through 104.
  The pair \(\{11867,12791\}\) remains equal through all 95,778 cap-103
  descriptors, while cap 104 has no collision.
- The 38,253 descriptors added after cap 88 and through cap 104 induce
  14 nonconstant raw coordinates but exactly five unit patterns on the
  original bucket. Representatives give new signatures
  \(0,16,8,4,2,1\). Appending them to the 908 cap-88 normalized columns
  gives a 913-coordinate certificate separating all 128,271 population
  pairs. All five new patterns are necessary for this incremental repair.
- `THM-013` is `PROVED`: \(L=m+76\) is injective on every complete balanced
  population for \(9\le m\le28\), and 76 is the smallest common integer
  offset on this finite range.
- `BAR-034` is `PROVED`: the exact multiplicative coefficients covering the
  finite thresholds through length 28 are \(c>103/28\). The endpoint gives
  failed cap 103; \(26/7\) is a fixed succeeding witness.
- ADR-044 changes complete-profile evaluation to stream primitive masks
  without retaining one audit object per descriptor-prime pair. Every
  cap-20 selector mask was compared against the original full audit-object
  evaluator on eleven adversarial primes, and all historical M33--M39
  collision regressions remain unchanged.
- EXP-0039 checked one full cap profile, seventeen transition profiles, 507
  primes, 58,464 descriptors, 29,641,248 full-profile local exits, 467,712
  raw and 908 normalized coordinates, 128,271 normalization equivalences,
  38,253 new transition descriptors, 229,518 tracked transition exits,
  306,024 raw pattern checks, 255 tracked pair checks, 14 nonconstant raw
  coordinates, five distinct repair patterns, five new repair coordinates,
  and 128,271 construction pairs.
- Independent validation passed 16 Rust/C# command comparisons, four dense
  vectors, 128,271 independent construction pairs, 58,464 additive-cap
  cases, 61,143 multiplicative-cap cases, and 95,778 predecessor cases.
- Registered schema SHA-256:
  `7f45ad32c1abb3d09d0b47c4659b2e3555af7126fa534b786b5a0d0504ed4414`.
  Registered EXP-0039 summary SHA-256:
  `2059fbfc2eff0bfe710427cea5de920362f5dfa6bbf34e3f2143e1513633f0c6`.
- Final gates passed: foundation and bilingual publication checks
  (167 claims and 38 experiment hashes), 225 Python tests in 199.74 seconds
  with the cache provider disabled, compileall, Ruff, strict mypy over 26
  source files, Rust formatting/Clippy and 36 tests, and a warning-free C#
  Release build.
- XeLaTeX produced final-warning-free 92-page English and 27-page Korean
  PDFs. Rendered bilingual titles, M40 result tables, complete proof,
  complexity, reproduction, and claim-appendix pages had no clipping,
  overlap, missing glyph, malformed mathematics, or unreadable text. Stable
  artifact SHA-256 values are
  `f13eaa2b4dbe54b68884b8d8a0186e4d5a301f6396acdccddcbcadefefcde9c1`
  and
  `aa22b243bd5514166094502e58091316708c782162cf8cca4b05eca4b2d990ae`.
- Both formulas remain factorization independent and use
  \(O(m^3\log m)\) compact work. Population enumeration, normalization, and
  dense expansion are certificate operations. The finite result does not
  establish a cap growth rate, behavior at \(m>28\), promise recognition,
  or general factoring.
- Next selected milestone: M41 separately tests additive cap 105 and
  multiplicative cap 108 on the complete \(m=29\) population.

### M40 Korean summary

M40에서는 M39의 두 공개 상한이 \(m=28\)에서 주는 cap 88과 90을
각각 검사했습니다. 두 cap 모두 같은 여섯 소수의 15개 충돌 pair를
남깁니다. selector 포함관계와 새 descriptor의 exact transition으로
이후 충돌을 첫 bucket 안에서 완전 추적했으며, cap 103에서도
\(\{11867,12791\}\)이 충돌하지만 cap 104의 새 coordinate 다섯
개가 원래 bucket을 모두 분리합니다.

따라서 \(9\le m\le28\)에서 \(m+76\)은 작동하며 최소 공통 정수
offset은 76입니다. 곱셈형 경계는 정확히 \(c>103/28\)이고
\(26/7\)은 고정 성공 witness입니다. 이는 유한하고
인수분해 의존적인 balanced-semiprime 약속 정리입니다. \(m>28\),
asymptotic cap 성장률, 약속 인식, 일반 고전적 다항 시간 정수분해는
여전히 증명되지 않았습니다.

## M39 outcome

- Date: 2026-07-29.
- Branch: `research/20260729-m39-length-27-caps`.
- Base: M38 squash merge
  `d87dfe2fecc260d73ae7cc27d54be33c952cb803`.
- Start commit `e4f4ad04842ae0ec5fd41e87ac0ae4c5c18b1c38` is pushed. Draft
  PR #50 targets `main`:
  `https://github.com/whitespaca/MOSEF/pull/50`.
- At \(m=27\), the M38 formulas give distinct caps:
  \(m+45=72\) and \(\lceil27m/10\rceil=73\). The complete 365-prime
  population at cap 72 has the collision bucket
  \(\{9463,9791,10607,10939,11087,11213\}\), producing 15 failed pairs
  across all 31,950 descriptors.
- Cap 73 separates \(9791\), but the remaining five-prime bucket still
  produces ten failed pairs across all 32,400 descriptors. Raw selector
  inclusion confines every later collision to the original cap-72 bucket.
- Exact incremental transition checks reduce the bucket to three primes at
  cap 75 and two primes at cap 81. The pair \(\{10607,10939\}\) remains
  equal through all 52,360 cap-86 descriptors, while cap 87 has no
  collision.
- The descriptors added after cap 72 and through cap 87 induce 235
  nonconstant raw coordinates but exactly five distinct patterns on the
  original bucket. One representative of each pattern gives new signatures
  \(4,1,0,2,8,16\). Appending them to the 625 cap-72 normalized columns
  gives a 630-coordinate certificate separating all 66,430 population
  pairs. All five new patterns are necessary for this incremental repair.
- `THM-012` is `PROVED`: \(L=m+60\) is injective on every complete balanced
  population for \(9\le m\le27\), and 60 is the smallest common integer
  offset on this finite range.
- `BAR-033` is `PROVED`: the exact multiplicative coefficients covering the
  finite thresholds through length 27 are \(c>86/27\). The endpoint gives
  failed cap 86; \(16/5\) is a fixed succeeding witness.
- EXP-0038 checked one full cap profile, sixteen transition profiles, 365
  primes, 31,950 descriptors, 11,661,750 full-profile local exits, 255,600
  raw and 625 normalized coordinates, 66,430 normalization equivalences,
  25,842 new transition descriptors, 155,052 tracked transition exits,
  206,736 raw pattern checks, 240 tracked pair checks, 235 nonconstant raw
  coordinates, five distinct repair patterns, five new repair coordinates,
  and 66,430 construction pairs.
- Independent validation checks 16 Rust/C# command comparisons, 66,430
  dense construction pairs, 31,950 dense additive-cap cases, 32,400 dense
  multiplicative-cap cases, and 52,360 dense predecessor cases.
- Registered schema SHA-256:
  `252126eeb4de40e6c8940d23516419e8f6f4b11dbebe8a84bd8d2cdcf59757cd`.
  Registered EXP-0038 summary SHA-256:
  `4de3a4d7f8474e91ee2e488807149b73e67c1a541018434383db8ede79ce0208`.
- Final gates passed: foundation and bilingual publication checks
  (163 claims and 37 experiment hashes), 223 Python tests in 1,293.06
  seconds with the cache provider disabled, compileall, Ruff, strict mypy
  over 26 source files, Rust formatting/Clippy and 36 tests, and a
  warning-free C# Release build.
- The complete M39 schema generation and independent differential suite
  passed, including 16 Rust/C# command checks, 66,430 dense construction
  pairs, 31,950 additive-cap checks, 32,400 multiplicative-cap checks, and
  52,360 predecessor checks.
- XeLaTeX produced final-warning-free 90-page English and 25-page Korean
  PDFs. Rendered bilingual titles, M39 result, complete proof, complexity,
  and claim-appendix pages had no clipping, overlap, missing glyph,
  malformed mathematics, or unreadable text. Stable artifact SHA-256 values
  are
  `3314a7e7f631a051e96b0c78055d740a7b16947ee442c9c899b9b4f84c4b7c8d`
  and
  `c5f57e98b40ea488d47c8379ecad16672c2950fb1fcf0e51bb80f53f08ff7723`.
- M39 proof, implementation, registered experiment, and bilingual-paper core
  commit:
  `0ca1a3598aafa47b2ee7ed66e56ae3366fbb3510`.
- Both formulas remain factorization independent and use
  \(O(m^3\log m)\) compact work. Population enumeration, normalization, and
  dense expansion are certificate operations. The finite result does not
  establish a cap growth rate, behavior at \(m>27\), promise recognition,
  or general factoring.
- Next selected milestone: M40 separately tests additive cap 88 and
  multiplicative cap 90 on the complete \(m=28\) population.

### M39 Korean summary

M39에서는 M38의 두 공개 상한이 \(m=27\)에서 주는 cap 72와 73을
각각 검사했습니다. cap 72에는 여섯 소수의 15개 충돌 pair가 남고,
cap 73에는 다섯 소수의 열 충돌 pair가 남습니다. selector 포함관계와
새 descriptor의 exact transition으로 이후 충돌을 첫 bucket 안에서
완전 추적했으며, cap 86에서도 \(\{10607,10939\}\)이 충돌하지만
cap 87의 새 coordinate 다섯 개가 원래 bucket을 모두 분리합니다.

따라서 \(9\le m\le27\)에서 \(m+60\)은 작동하며 최소 공통 정수
offset은 60입니다. 곱셈형 상한의 정확한 유한 경계는
\(c>86/27\)입니다. 이 결과는 이후 길이의 asymptotic 성장, promise
인식, 일반 정수분해를 증명하지 않습니다.

## M38 outcome

- Date: 2026-07-28.
- Branch: `research/20260728-m38-length-26-caps`.
- Base: M37 squash merge
  `df3af93a89b764f6be6eec9d55b26b4477749cea`.
- Start commit `95f26a2b2188b44bdcb1452ff79d394027ce6659` is pushed. Draft
  PR #49 targets `main`:
  `https://github.com/whitespaca/MOSEF/pull/49`.
- At \(m=26\), the M37 formulas give distinct caps:
  \(m+40=66\) and \(\lceil257m/100\rceil=67\). The complete 268-prime
  population at cap 66 has the collision bucket
  \(\{6229,6703,6793,6947,7187,7229,7649\}\), producing 21 failed pairs
  across all 23,465 descriptors.
- Cap 67 reduces the complete collision set to
  \(\{7187,7229,7649\}\), which produces three failed pairs across all
  25,938 descriptors. Raw selector inclusion confines every later collision
  to the original cap-66 bucket.
- Exact transition checks preserve the final triple through cap 70 and all
  27,876 descriptors. At cap 71, two new cofactor coordinates have patterns
  \((0,0,1)\) and \((0,1,0)\) on the triple. Appending them to the 561
  cap-67 normalized columns gives a 563-coordinate certificate separating
  all 35,778 population pairs, so 71 is the exact first injective cap.
- `THM-011` is `PROVED`: \(L=m+45\) is injective on every complete balanced
  population for \(9\le m\le26\), and 45 is the smallest common integer
  offset on this finite range.
- `BAR-032` is `PROVED`: the exact multiplicative coefficients covering the
  finite thresholds through length 26 are \(c>35/13\). The endpoint gives
  failed cap 70; \(27/10\) is a fixed succeeding witness.
- EXP-0037 checked two full cap profiles, six transition profiles, 268
  primes, 49,403 descriptor instances, 13,240,004 full-profile local exits,
  395,224 raw and 1,101 normalized coordinates, 35,778 monotonicity checks,
  71,556 normalization equivalences, 113,179 transition descriptor checks,
  792,253 tracked transition exits, two new repair coordinates, and 35,778
  construction pairs.
- Independent validation checks 16 Rust/C# command comparisons, 35,778
  dense construction pairs, 23,465 dense additive-cap cases, 25,938 dense
  multiplicative-cap cases, and 27,876 dense predecessor cases.
- Registered schema SHA-256:
  `68f7e9b710be7960b78c11e4bef06119f00d75a6df2074ed8976f211e6b32a97`.
  Registered EXP-0037 summary SHA-256:
  `c3b758e046f9e6ae722352bd54be62521a32608c43a4fc95237f2e89229a094c`.
- Final gates passed: foundation and bilingual publication checks
  (159 claims and 36 experiment hashes), 222 Python tests in 849.67 seconds
  with the cache provider disabled, compileall, Ruff, strict mypy over 26
  source files, Rust formatting/Clippy and 36 tests, and a warning-free C#
  Release build.
- The complete M38 schema generation and independent differential suite
  passed, including 16 Rust/C# command checks, 35,778 dense construction
  pairs, 23,465 additive-cap checks, 25,938 multiplicative-cap checks, and
  27,876 predecessor checks.
- XeLaTeX produced final-warning-free 88-page English and 24-page Korean
  PDFs. Rendered M38 result, complete proof, complexity, and claim-appendix
  pages had no clipping, overlap, missing glyph, malformed mathematics, or
  unreadable text. Stable artifact SHA-256 values are
  `83ad986bb3462e2787ecf58f342da8a5d743dbb03f85e41fa85af1feb777a4e7`
  and
  `4356b89305ebe521e8c4b371ef6e47983c11b2674624557819f116bc65c841eb`.
- M38 proof, implementation, registered experiment, and bilingual-paper core
  commit:
  `2ea56e314b0675f8639b54072aa3e60406104ce5`.
- Both formulas remain factorization independent and use
  \(O(m^3\log m)\) compact work. The finite result does not establish a cap
  growth rate, behavior at \(m>26\), promise recognition, or general
  factoring.
- Next selected milestone: M39 separately tests additive cap 72 and
  multiplicative cap 73 on the complete \(m=27\) population.

### M38 Korean summary

M38에서는 M37의 두 공개 상한이 \(m=26\)에서 주는 cap 66과 67을
각각 검사했습니다. cap 66에는 일곱 소수의 21개 충돌 pair가 남고,
cap 67에는 세 소수의 세 충돌 pair가 남습니다. selector 포함관계로
이후 충돌을 첫 bucket 안에서 완전 추적했으며, cap 70에서도 triple이
충돌하지만 cap 71의 새 cofactor coordinate 두 개가 이를 분리합니다.

따라서 \(9\le m\le26\)에서 \(m+45\)는 작동하며 최소 공통 정수 offset은
45입니다. 곱셈형 상한의 정확한 유한 경계는 \(c>35/13\)입니다. 이
결과는 이후 길이의 asymptotic 성장, promise 인식, 일반 정수분해를
증명하지 않습니다.

## M37 outcome

- Date: 2026-07-28.
- Branch: `research/20260728-m37-length-25-caps`.
- Base: M36 squash merge
  `2d218cf8a0db630e3d4cb418b16cf9ad05901129`.
- Start commit `750c6e0292a861eee39cd78426c2ca7c80422ca6` is pushed. Draft
  PR #48 targets `main`:
  `https://github.com/whitespaca/MOSEF/pull/48`.
- At \(m=25\), the M36 formulas give distinct caps:
  \(m+27=52\) and \(\lceil209m/100\rceil=53\). The complete 196-prime
  population at cap 52 has the collision bucket
  \(\{4133,4297,4337,4423,4663,5011,5179,5233,5297\}\), producing 36
  failed pairs across all 11,628 descriptors.
- Cap 53 removes \(4133\), but the remaining eight-prime bucket still
  produces 28 failed pairs across all 12,324 descriptors. Raw selector
  inclusion confines all later collisions to the original cap-52 bucket.
- Exact transition checks through cap 64 reduce the collision to
  \(\{5011,5179\}\), which remains equal across all 22,050 descriptors.
  Cap 65 has 23,104 descriptors, 437 normalized columns, and 196 distinct
  signatures. A 169-coordinate certificate separates all
  19,110 population pairs, so 65 is the exact first injective cap.
- `THM-010` is `PROVED`: \(L=m+40\) is injective on every complete balanced
  population for \(9\le m\le25\), and 40 is the smallest common integer
  offset on this finite range.
- `BAR-031` is `PROVED`: the exact multiplicative coefficients covering the
  finite thresholds through length 25 are \(c>64/25\). The endpoint gives
  failed cap 64; \(257/100\) is a fixed succeeding witness.
- EXP-0036 checked three full cap profiles, fourteen transition profiles,
  196 primes, 47,056 descriptor instances, 9,222,976 full-profile local
  exits, 376,448 raw and 1,068 normalized coordinates, 38,220 monotonicity
  checks, 57,330 normalization equivalences, 189,494 transition descriptor
  checks, 1,705,446 tracked transition exits, and 19,110 construction pairs.
- Independent validation checks 16 Rust/C# command comparisons, 19,110
  dense construction pairs, 11,628 dense additive-cap cases, 12,324 dense
  multiplicative-cap cases, and 22,050 dense predecessor cases.
- Registered schema SHA-256:
  `d85d081243f5ae32b38405e35e8921ff3378ccd5bbb19c63eb135b79c4b61524`.
  Registered EXP-0036 summary SHA-256:
  `56e595f3096bebd46184f221d0a81844eeaa8d5b4c46b0f2ccbbecad3be6d5d7`.
- Final gates passed: foundation and bilingual publication checks
  (155 claims and 35 experiment hashes), 221 Python tests with the cache
  provider disabled, compileall, Ruff, strict mypy over 26 source files,
  Rust formatting/Clippy and 36 tests, and a warning-free C# Release build.
- The complete M37 schema generation and independent differential suite
  passed, including 16 cross-language command checks, 19,110 dense
  construction pairs, 11,628 additive-cap checks, 12,324 multiplicative-cap
  checks, and 22,050 predecessor checks.
- XeLaTeX produced final-warning-free 86-page English and 22-page Korean
  PDFs. Rendered title, M37 result, proof, complexity, and claim-appendix
  pages had no clipping, overlap, missing glyph, malformed mathematics, or
  unreadable text. Stable artifact SHA-256 values are
  `40dc1f5091de4d22eae80066f21d622012ed2b7f5fae50014f53bc815a2f5df6`
  and
  `39ae8fc52b219314e9d5d0d0e9ed8923b498309d23f540ada0ac7b19b4e314e9`.
- M37 proof, implementation, registered experiment, and bilingual-paper core
  commit:
  `d23b602122fcf748821d762d80558c20095bf3b7`.
- Both formulas remain factorization independent and use
  \(O(m^3\log m)\) compact work. The finite result does not establish a cap
  growth rate, behavior at \(m>25\), promise recognition, or general
  factoring.
- Next selected milestone: M38 separately tests additive cap 66 and
  multiplicative cap 67 on the complete \(m=26\) population.

### M37 Korean summary

M37에서는 M36의 두 공개 상한이 \(m=25\)에서 주는 cap 52와 53을
각각 검사했습니다. cap 52에는 아홉 소수의 36개 충돌 pair가 남고,
cap 53에는 여덟 소수의 28개 충돌 pair가 남습니다. selector 포함관계로
이후 충돌을 첫 bucket 안에서 완전 추적했으며, cap 64에서도
\(\{5011,5179\}\)이 충돌하지만 cap 65에서는 196-prime population의
signature가 단사가 됩니다.

따라서 \(9\le m\le25\)에서 \(m+40\)은 작동하며 최소 공통 정수 offset은
40입니다. 곱셈형 상한의 정확한 유한 경계는 \(c>64/25\)입니다. 이
결과는 이후 길이의 asymptotic 성장, promise 인식, 일반 정수분해를
증명하지 않습니다.

## M36 outcome

- Date: 2026-07-28.
- Branch: `research/20260728-m36-distinct-caps`.
- Base: M35 squash merge
  `b4d6fba2509a9a0cc334b7dfa195e01c119869a0`.
- Start commit `4159b7fb29aed5c40db388cfeaf66febf9817323` is pushed. Draft
  PR #47 targets `main`:
  `https://github.com/whitespaca/MOSEF/pull/47`.
- At \(m=24\), the M35 formulas give distinct caps:
  \(m+24=48\) and \(\lceil201m/100\rceil=49\). The complete 146-prime
  population at cap 48 has the collision bucket
  \(\{3049,3643,3769,3863,4057\}\), producing ten failed pairs across all
  9,212 descriptors and 73,696 raw coordinates.
- Cap 49 removes \(3769\), but \(\{3049,3643,3863,4057\}\) still produces
  six failed pairs across all 9,408 descriptors. Cap 50 preserves the same
  bucket across all 9,604 descriptors.
- Cap 51 has 11,400 descriptors, 240 normalized columns, and 146 distinct
  signatures. A 130-coordinate certificate separates all 10,585 population
  pairs, so 51 is the exact first injective cap at length 24.
- `THM-009` is `PROVED`: \(L=m+27\) is injective on every complete balanced
  population for \(9\le m\le24\), and 27 is the smallest common integer
  offset on this finite range.
- `BAR-030` is `PROVED`: the exact multiplicative coefficients covering the
  finite thresholds through length 24 are \(c>25/12\). The endpoint gives
  failed cap 50; \(209/100\) is a fixed succeeding witness.
- EXP-0035 checked four cap profiles, 146 primes, 39,624 descriptor
  instances, 5,785,104 local exits, 316,992 raw and 888 normalized
  coordinates, 31,755 monotonicity checks, 42,340 normalization
  equivalences, and 10,585 construction-certificate pairs.
- Independent validation passed 16 Rust/C# command comparisons, 10,585
  dense construction pairs, 9,212 dense additive-cap cases, 9,408 dense
  multiplicative-cap cases, and 9,604 dense predecessor cases.
- Registered schema SHA-256:
  `3709d2e2a35212103ad838f83a25152e996cb33b9b5786d9642935a8d2ccfbcb`.
  Registered EXP-0035 summary SHA-256:
  `7e66da1e71bf93b7c18d614581197c40b42ab9bf1da787dd318f76b77a16bda5`.
- Final gates passed: foundation and bilingual publication checks
  (151 claims and 34 experiment hashes), 220 Python tests with the cache
  provider disabled, compileall, Ruff, strict mypy over 26 source files,
  Rust formatting/Clippy and 36 tests, and a warning-free C# Release build.
- The complete M36 audit and independent differential suite passed, including
  16 cross-language command checks and the dense construction, two failed-cap,
  and predecessor-collision checks reported above.
- XeLaTeX produced final-warning-free 86-page English and 21-page Korean
  PDFs. Rendered title, M36 result, complexity, conclusion, proof,
  reproduction, and claim-appendix pages had no clipping, overlap, missing
  glyph, malformed mathematics, or unreadable text. Stable artifact SHA-256
  values are
  `c87c9130da437b04a05ae5b1d44fab59df72052d30f8fa1121c7a3ed96ad3833`
  and
  `d6f79f58f5e8db537a28ed98a034a02033b72bac2f6629947ce097f8da6f3460`.
- M36 proof, implementation, registered experiment, and bilingual-paper core
  commit:
  `a3bd650251692080b17a6d6c9245af545d344a3b`.
- The formulas remain factorization independent and use
  \(O(m^3\log m)\) compact work. The finite result does not establish a cap
  growth rate, behavior at \(m>24\), promise recognition, or general
  factoring.
- Next selected milestone: M37 separately tests additive cap 52 and
  multiplicative cap 53 on the complete \(m=25\) population.

### M36 Korean summary

M36에서는 M35의 두 공개 선형 상한을 \(m=24\)에서 각각 검사했습니다.
가산 공식의 cap 48에는 다섯 소수의 열 개 충돌 pair가 남고, 곱셈
공식의 cap 49와 그 다음 cap 50에는 네 소수의 여섯 충돌 pair가
남습니다. cap 51에서야 완전한 146-prime population이 단사가 됩니다.

따라서 \(9\le m\le24\)에서는 \(m+27\)이 작동하며 가산 상수 27이
최소입니다. 곱셈형 상한의 정확한 유한 경계는 \(c>25/12\)입니다.
이 결과는 다음 길이나 asymptotic 성장률, promise 인식, 일반
정수분해를 증명하지 않습니다.

## M35 outcome

- Date: 2026-07-28.
- Branch: `research/20260728-m35-next-envelope`.
- Base: M34 squash merge
  `826bc672b0893b2dd1481bfebf4b7f726120fcd4`.
- Start commit `8bbe28ac6d34e0b7423d0be323f0bc9c0a6e7cf5` is pushed. Draft
  PR #46 targets `main`:
  `https://github.com/whitespaca/MOSEF/pull/46`.
- At \(m=23\), both M34 formulas \(m+17\) and
  \(\lceil173m/100\rceil\) give cap 40. The complete 109-prime population has
  the collision bucket \(\{2411,2477,2741,2777,2837\}\), producing ten
  failed pairs across all 5,148 descriptors and 41,184 raw coordinates.
- Caps 41 through 46 remain noninjective. Their collision-pair counts are
  \(10,10,6,3,3,1\); the final cap-46 collision is \(\{2411,2777\}\)
  across all 7,470 descriptors.
- Cap 47 has 9,016 descriptors, 190 normalized columns, and 109 distinct
  signatures. A 94-coordinate certificate separates all 5,886 population
  pairs, so 47 is the exact first injective cap at length 23.
- `THM-008` is `PROVED`: \(L=m+24\) is injective on every complete balanced
  population for \(9\le m\le23\), and 24 is the smallest common integer
  offset on this finite range.
- `BAR-029` is `PROVED`: the exact multiplicative coefficients covering the
  finite thresholds through length 23 are \(c>2\). The endpoint gives failed
  cap 46; \(201/100\) is a fixed succeeding witness.
- EXP-0034 checked eight cap profiles, 109 primes, 53,712 descriptor
  instances, 5,854,608 local exits, 429,696 raw and 1,365 normalized
  coordinates, 41,202 monotonicity checks, 47,088 normalization
  equivalences, and 5,886 construction-certificate pairs.
- Independent validation passed 16 Rust/C# command comparisons, 5,886 dense
  construction pairs, 5,148 dense failed-schedule collision-descriptor cases,
  and 7,470 dense predecessor collision-descriptor cases.
- Registered schema SHA-256:
  `65f97c06c59b60bbf649fdb7146a59c51ab33f7002445344a168be88a3ad459e`.
  Registered EXP-0034 summary SHA-256:
  `e797c329c0935dbed73a810723764755eacc117527394e1d82ab0b792a69d06d`.
- Final gates passed: foundation and bilingual publication checks
  (147 claims and 33 experiment hashes), 219 Python tests plus 206 subtests,
  compileall, Ruff, strict mypy over 26 source files, Rust formatting/Clippy
  and 36 tests, and a warning-free C# Release build.
- The complete M35 audit and independent differential suite passed, including
  16 cross-language command checks and the dense construction, failed-cap,
  and predecessor-collision checks reported above.
- XeLaTeX produced final-warning-free 84-page English and 20-page Korean
  PDFs. Rendered title, M35 result, complexity, proof, reproduction, and
  claim-appendix pages had no clipping, overlap, missing glyph, malformed
  mathematics, or unreadable text. Stable artifact SHA-256 values are
  `c1ae1c7225de909d57f84d5a6dad7d218c1aa92917e3124d84d83c08ef9236cd`
  and
  `84f2c255946c1d020bd703efcff2cd791c4649e8e5bd6ee44dfc7cd7e210937c`.
- M35 proof, implementation, registered experiment, and bilingual-paper core
  commit:
  `1b8357cb898668d55fb200b2e1af4ad0c6d8ba07`.
- The formulas remain factorization independent and use
  \(O(m^3\log m)\) compact work. The finite result does not establish a cap
  growth rate, behavior at \(m>23\), promise recognition, or general
  factoring.
- Next selected milestone: M36 separately tests additive cap 48 and
  multiplicative cap 49 on the complete \(m=24\) population.

### M35 Korean summary

M35에서는 M34의 두 공개 선형 상한을 \(m=23\)에서 반증 검사했습니다.
두 공식은 모두 \(L=40\)이 되고, 다섯 소수의 collision bucket에 열 개
실패 pair가 남습니다. cap 41부터 46까지도 충돌하며, cap 47에서야
완전한 109-prime population이 단사가 됩니다.

따라서 \(9\le m\le23\)에서는 \(m+24\)가 작동하며 가산 상수 24가
최소입니다. 곱셈형 상한의 정확한 유한 경계는 \(c>2\)입니다. 이
결과는 다음 길이나 asymptotic 성장률, promise 인식, 일반 정수분해를
증명하지 않습니다.

## M34 outcome

- Date: 2026-07-28.
- Branch: `research/20260728-m34-next-envelope`.
- Base: M33 squash merge
  `f053a440bbcc9894f357c5d9dad55a2eeab9a1e9`.
- Start commit `b3312dbe39d6d33753bc0ccd160a8af5011c5069` is pushed. Draft
  PR #45 targets `main`:
  `https://github.com/whitespaca/MOSEF/pull/45`.
- At \(m=22\), both M33 formulas \(m+12\) and
  \(\lceil153m/100\rceil\) give cap 34. The complete 80-prime population has
  a nine-prime collision bucket and a two-prime bucket, producing 37 failed
  pairs across all 2,838 descriptors and 22,704 raw coordinates.
- Caps 35 through 38 remain noninjective. Their collision-pair counts are
  \(15,10,6,1\); the final cap-38 collision is \(\{1481,1571\}\) across all
  3,996 descriptors.
- Cap 39 has 5,016 descriptors, 115 normalized columns, and 80 distinct
  signatures. A 73-coordinate certificate separates all 3,160 population
  pairs. The cap-38 collision and raw selector inclusion prove that 39 is the
  exact first injective cap at length 22.
- `THM-007` is `PROVED`: \(L=m+17\) is injective on every complete balanced
  population for \(9\le m\le22\), and 17 is the smallest common integer
  offset on this finite range.
- `BAR-028` is `PROVED`: the exact multiplicative coefficients covering the
  finite thresholds through length 22 are \(c>19/11\). The old
  \(153/100\) witness fails; \(173/100\) is a fixed succeeding witness.
- EXP-0033 checked six cap profiles, 80 primes, 23,190 descriptor instances,
  1,855,200 local exits, 185,520 raw and 578 normalized coordinates, 15,800
  monotonicity checks, 18,960 normalization equivalences, and 3,160
  construction-certificate pairs.
- Independent validation passed 16 Rust/C# command comparisons, 3,160 dense
  construction pairs, 5,676 dense failed-schedule descriptor-bucket cases,
  and 3,996 dense predecessor collision-descriptor cases.
- Registered schema SHA-256:
  `36bd038cd325dc4bb151ffd366b1d47ed670f4ef4b7871343e14624d52fc2968`.
  Registered EXP-0033 summary SHA-256:
  `5f60b3e2d688697ce30a6b40b39d6adbd8fe365cca4dc8e36994090aa2a54b39`.
- Final gates passed: foundation and bilingual publication checks
  (143 claims and 32 experiment hashes), 218 Python tests plus 206 subtests,
  compileall, Ruff, strict mypy over 26 source files, Rust formatting/Clippy
  and 36 tests, and a warning-free C# Release build.
- Regression gates passed: 58 baseline comparisons, the registered M29 audit
  and 34 comparisons, the M30 audit and 34 comparisons, the M31 audit with
  72 command checks, 12 profiles, and 104 dense pairs, the M32 audit with
  64 command checks, 1,930 dense construction pairs, and 5,314 dense
  predecessor checks, and the complete M33 and M34 audits and differential
  checks.
- XeLaTeX produced final-warning-free 83-page English and 19-page Korean
  PDFs. Rendered title, theorem, evidence, proof, reproduction, and claim
  appendix pages had no clipping, overlap, missing glyph, or unreadable text.
  Stable artifact SHA-256 values are
  `0313695ae070ecaea9eb6c5477119d79b76f391b35285b7fbf118a3db49e1059`
  and
  `5929b60506605803380d542baba151fabb545476b7ae5370dbffc7c87ead4b47`.
- M34 proof, implementation, registered experiment, and bilingual-paper core
  commit:
  `f1c0c6b3da647d40c7d476ee05b9afa696805178`.
- The formulas remain factorization independent and use
  \(O(m^3\log m)\) compact work. The finite result does not establish a cap
  growth rate, behavior at \(m>22\), promise recognition, or general
  factoring.
- Next selected milestone: M35 tests \(m+17\) and
  \(\lceil173m/100\rceil\) on the complete \(m=23\) population.

### M34 Korean summary

M34에서는 M33의 두 공개 선형 상한을 \(m=22\)에서 반증 검사했습니다.
두 공식은 모두 \(L=34\)가 되고, 두 collision bucket에 37개 실패 pair가
남습니다. cap 35부터 38까지도 충돌하며, cap 39에서야 완전한 80-prime
population이 단사가 됩니다.

따라서 \(9\le m\le22\)에서는 \(m+17\)이 작동하며 가산 상수 17이
최소입니다. 곱셈형 상한의 정확한 유한 경계는 \(c>19/11\)입니다.
이 결과는 다음 길이나 asymptotic 성장률, promise 인식, 일반 정수분해를
증명하지 않습니다.

## M33 outcome

- Date: 2026-07-28.
- Branch: `research/20260728-m33-linear-cap-recurrence`.
- Base checkpoint: M32 completion PR #43 was squash-merged into `main` as
  `659f820c1511aab6becef1e26d9b4350187786a8`.
- Start commit `fe510a77e6d3656415c2fe98cda3fdce4a274aa5` is pushed. Draft
  PR #44 targets `main`:
  `https://github.com/whitespaca/MOSEF/pull/44`.
- At \(m=21\), both M32 formulas \(m+11\) and
  \(\lceil151m/100\rceil\) give cap 32. The complete 57-prime population has
  a four-prime collision bucket \(\{1031,1231,1319,1433\}\) across all 2,511
  descriptors and 20,088 raw coordinates, producing six failed pairs.
- Cap 33 has 2,752 descriptors, 74 normalized columns, and 57 distinct
  signatures. A 53-coordinate certificate separates all 1,596 population
  pairs. Cap 32's collision and raw selector inclusion prove that 33 is the
  exact first injective cap at length 21.
- `THM-006` is `PROVED`: \(L=m+12\) is injective on every complete balanced
  population for \(9\le m\le21\), and 12 is the smallest common integer
  offset on this finite range.
- `BAR-027` is `PROVED`: the exact multiplicative coefficients covering the
  finite thresholds through length 21 are \(c>32/21\). The old
  \(151/100\) witness fails; \(153/100\) is a fixed succeeding witness.
- EXP-0032 checked two cap profiles, 57 primes, 5,263 descriptor instances,
  299,991 local exits, 42,104 raw and 143 normalized coordinates, 1,596
  monotonicity checks, 3,192 normalization equivalences, and 1,596
  construction-certificate pairs.
- Independent validation passed 28 Rust/C# command comparisons, 1,596 dense
  construction pairs, and all 2,511 dense collision-descriptor cases.
- Registered schema SHA-256:
  `5947cc85d8664fcb1433d7d748a7d7be0be81098c49ddd433cc0645313c77b80`.
  Registered EXP-0032 summary SHA-256:
  `3b6536eaf343951ca0efb50aae08f1b32f36f89e896a9f5a9f2cc6286f1ffa88`.
- Final gates passed: foundation and bilingual publication checks
  (139 claims and 31 experiment hashes), 217 Python tests plus 206 subtests,
  compileall, Ruff, strict mypy over 26 source files, Rust formatting/Clippy
  and 36 tests, and a warning-free C# Release build.
- Regression gates passed: 58 baseline comparisons, the registered M29 audit
  and 34 comparisons, the M30 audit and 34 comparisons, the M31 audit with
  72 command checks, 12 profiles, and 104 dense pairs, the M32 audit with
  64 command checks, 1,930 dense construction pairs, and 5,314 dense
  predecessor checks, and the complete M33 audit and differential check.
- XeLaTeX produced final-warning-free 82-page English and 18-page Korean
  PDFs. Rendered title, theorem, evidence, proof, reproduction, and claim
  appendix pages had no clipping, overlap, missing glyph, or unreadable text.
  Stable artifact SHA-256 values are
  `f875201b611d5521966af680ed7226cab880119748974ca8ca6c874fcdc8a6e6`
  and
  `95393070ca5e979791b62bfdb95db43a039dbb1732c00185cf0a0d144d8ede77`.
- M33 proof, implementation, registered experiment, and bilingual-paper core
  commit:
  `8d604a6f4c3a14b0715de6ac2f7503d2debcff03`.
- The formulas remain factorization independent and use
  \(O(m^3\log m)\) compact work. The finite result does not establish a cap
  growth rate, behavior at \(m>21\), promise recognition, or general
  factoring.
- Next selected milestone: M34 tests \(m+12\) and
  \(\lceil153m/100\rceil\) on the complete \(m=22\) population.

### M33 Korean summary

M33에서는 M32의 두 공개 선형 상한을 바로 다음 길이에서 반증
검사했습니다. \(m=21\)에서 두 공식은 모두 \(L=32\)가 되고,
\(1031,1231,1319,1433\)이 모든 2,511개 descriptor에서 같은
signature를 가져 여섯 소수쌍이 실패합니다.

상한 33에서는 완전한 57-prime population이 단사입니다. 따라서
\(9\le m\le21\)에서는 \(m+12\)가 작동하며 가산 상수 12가 최소입니다.
곱셈형 상한의 정확한 유한 경계는 \(c>32/21\)입니다. 이 결과는 다음
길이나 asymptotic 성장률, promise 인식, 일반 정수분해를 증명하지
않습니다.

## M32 outcome

- Date: 2026-07-28.
- Branch: `research/20260728-m32-widened-selector-cap`.
- Base checkpoint: M31 completion PR #42 was squash-merged into `main` as
  `3e98fe1450f2d3f808f12f8291296ad2bfe01e09`.
- Draft PR #43 targets `main`:
  `https://github.com/whitespaca/MOSEF/pull/43`.
- `DEF-032` separates input length \(m\) from a public cap \(L(m)\ge m\)
  fixed before \(N\). It includes every valid exceptional descriptor through
  \(L\), charges all eight primitive exits and derived outputs, and makes the
  nonunit-base GCD branch total before skipping the unit-only continuation.
- Raw selector inclusion proves monotone pair separation as \(L\) grows.
  Normalized column counts are not assumed monotone; DEF-031's exact
  normalization equivalence transfers the raw relation at each cap.
- The exact minimal caps at \(m=16,17,18,19,20\) are
  \(19,19,27,27,31\). Complete threshold certificates use
  \(10,16,20,26,40\) normalized coordinates, respectively. Each predecessor
  cap has an independently checked collision bucket.
- `THM-005` is `PROVED` on the complete finite balanced-semiprime promise
  \(9\le m\le20\): the public schedule \(L=m+11\) is injective and the
  integer offset 11 is minimal on this range. At \(m=20,L=30\), primes
  \(809,827\) collide, refuting `REF-028`.
- `BAR-026` is `PROVED` for the finite M32 grammar: a multiplicative cap
  \(\lceil cm\rceil\) covers all five new thresholds exactly when \(c>3/2\).
  The infimum is not attained; \(c=3/2\) fails at \(m=20,L=30\), while the
  fixed public witness \(151/100\) works on the registered range.
- The descriptor count is at most \(2(L-1)^3\), so any polynomially bounded
  computable cap has polynomial total construction, compact evaluation, GCD,
  output, and extraction cost. For the two linear schedules the compact work
  is \(O(m^3\log m)\).
- EXP-0031 checked 38 cap profiles, 35,421 descriptor instances, 1,206,359
  local exit profiles, 283,368 raw and 1,289 normalized coordinates, 17,330
  monotonicity pair checks, 3,860 normalization equivalences, and 1,930
  construction-certificate pairs.
- Independent validation passed 64 Rust/C# command comparisons, one explicit
  nonunit-base branch, five threshold profiles, 1,930 dense construction
  pairs, and 5,314 dense predecessor collision-descriptor cases.
- Registered schema SHA-256:
  `24f506ce7cb7ad9b10f8150f064441dbc1450f7402c72a6d228a363834eb9203`.
  Registered EXP-0031 summary SHA-256:
  `5cdc44356ae8ed81d395b033e86403691205c6552bc8da3bf4414b47842463d8`.
- Final gates passed: foundation and bilingual publication checks
  (134 claims and 30 experiment hashes), 216 Python tests plus 206 subtests,
  compileall, Ruff, strict mypy over 26 source files, Rust formatting/Clippy
  and 36 tests, and a warning-free C# Release build.
- Regression gates passed: 58 baseline comparisons, the registered M29 audit
  and 34 comparisons, the registered M30 audit and 34 comparisons, the
  registered M31 audit plus 72 cross-language command checks, 12 profiles,
  and 104 dense pairs, and the complete M32 audit and differential check.
- XeLaTeX produced a final-warning-free 80-page English PDF and 17-page
  Korean PDF. Rendered visual QA of both titles, the M32 table, theorem,
  proof, complexity transition, limits, and claim appendix found no clipping,
  overlap, missing glyph, or unreadable text. Stable artifacts are
  `output/pdf/mosef-paper.pdf` and `output/pdf/mosef-paper-ko.pdf`.
- M32 proof, implementation, registered experiment, and bilingual-paper core
  commit: `c98f0a704bdd4c2f5f5cc5758893e9a35f86c905`. Draft PR #43 will
  be updated with this validated payload before review and merge.
- General classical polynomial-time factoring, an asymptotic injective cap,
  balanced-promise recognition, and every length \(m>20\) remain open.
- Next selected milestone: M33 tests the two fixed public linear caps at
  \(m\ge21\), recording either continued finite injectivity or the first exact
  recurrence collision before widening the threshold again.

### M32 Korean summary

M32에서는 입력 길이 \(m\)과 공개 selector 상한 \(L(m)\)을 분리했습니다.
상한은 입력 \(N\)이나 미지의 소인수를 보기 전에 고정되며, base GCD를
포함한 모든 분기를 비용에 넣었습니다. \(m=16,17,18,19,20\)에서 처음
단사인 정확한 상한은 각각 \(19,19,27,27,31\)입니다.

따라서 \(9\le m\le20\)의 완전한 balanced semiprime 유한 범위에서는
\(L=m+11\)이 모든 서로 다른 소수쌍을 분리하며, 정수 가산 상수 11은
이 범위에서 최소입니다. \(m=20,L=30\)에서는 \(809\)와 \(827\)이
여전히 충돌합니다. 곱셈형 상한 \(\lceil cm\rceil\)은 이 유한 범위를
덮으려면 정확히 \(c>3/2\)여야 하며, \(c=3/2\) 자체는 실패합니다.

이 결과는 명시된 유한 promise에 대한 정리일 뿐입니다. \(m>20\)에서의
단사성, promise 인식, 모든 자연수에 대한 고전적 다항 시간 인수분해는
증명하지 않았고 현재도 열린 문제입니다.

## M31 outcome

- Date: 2026-07-28.
- Branch: `research/20260728-m31-diversified-compact-signatures`.
- M30 completion PR #40 merged into `main` as
  `869a150675dc02b21c3ff12350031c27b51c6ff7`. The earlier stacked M31 start
  PR #41 was merged only into the M30 research branch, so this completion
  branch merged current `origin/main` at `70a8832` before final validation.
- `DEF-031` fixes a factorization-independent selector containing every valid
  exceptional descriptor \((\text{family},A,B,g)\) with
  \(2\le A,B,g\le m\), chosen before \(N\). It charges the base, both stages,
  both public bounds, direct cyclotomic exit, public overlap resultant,
  independent cofactor exit, all GCDs, outputs, and extraction.
- Analytical normalization deletes constant primitive support columns and
  merges duplicates. Aggregate and overlap exits remain charged but are
  Boolean functions of primitive columns, so this normalization preserves
  every pair outcome and does not remove work from the public algorithm.
- `THM-004` is `PROVED`: for every \(9\le m\le15\), the normalized selector
  signature is injective on the complete balanced population
  \(\mathcal P_m\). Complete separating certificates use respectively
  \(1,2,2,3,4,6,10\) coordinates and the independent dense verifier checked
  all 104 promised prime pairs. This is a finite factor-dependent promise
  theorem, not an asymptotic constructor or promise recognizer.
- `BAR-025` is `PROVED`: at \(m=16\), 270 descriptors yield 2,160 raw
  primitive columns. Removing 2,054 constants and merging 96 duplicates
  leaves ten normalized columns, but \(191,227,233\) have identical
  signatures. All three pair products therefore fail every charged exit.
  This is an exact obstruction for the DEF-031 box, not for all polynomial
  selectors.
- `REF-027` is `REFUTED` and NR-028 preserves the boundary: taking both
  exceptional families and every parameter and base through \(m\) is not
  injective at every input length. Wider public ranges, different formulas,
  adaptive schedules, density, recognition, and general factoring remain
  open.
- EXP-0030 exhaustively checked 12 input lengths, 166 balanced primes, 2,816
  descriptors, 63,953 local profiles, 22,528 raw and 152 normalized
  coordinates, 2,034 normalization pair equivalences, 705 marginal cofactor
  separations, and 175 finite collision pairs. The selector was injective for
  \(9\le m\le15\) and noninjective for \(16\le m\le20\).
- Registered schema SHA-256:
  `f27e1681525d9c71f488c07457ed998cd43a8ea85ccac5b6e8e1b1e7227e93d0`.
  Registered EXP-0030 summary SHA-256:
  `423a86409f38a4be1382e611ca94d3e2b08abfe7c1923133ab195db9c3716ae8`.
- Final gates passed: foundation and bilingual publication checks
  (129 claims and 29 experiment hashes), 214 Python tests, compileall, Ruff,
  mypy, Rust formatting/Clippy and 36 tests, warning-free C# Release build,
  58 baseline comparisons, 34 M29 regression comparisons, the registered M30
  audit and 34 M30 comparisons, the registered M31 audit, 72 M31
  cross-language command checks, 12 profile checks, and 104 independent dense
  certificate pair checks.
- XeLaTeX produced a warning-free 78-page English PDF and 15-page Korean PDF.
  Visual QA of the title, M31 theorem and scoped collision, full proofs,
  limitation/next-work sections, reproduction commands, hashes, and Korean
  claim table found no clipping, overlap, missing glyph, or unreadable text.
  Stable artifacts are `output/pdf/mosef-paper.pdf` and
  `output/pdf/mosef-paper-ko.pdf`.
- M31 proof, implementation, experiment, and bilingual-paper commit
  `fa44f445cd8ead4122fe57e790f1ccb51f1206fd` is pushed. Completion Draft
  PR #42 targets `main`:
  `https://github.com/whitespaca/MOSEF/pull/42`.
- Next selected milestone: M32 will parameterize a wider public cap \(L(m)\),
  charge its polynomial degree, and audit the smallest additive and
  multiplicative ranges that repair or preserve the M31 collisions on
  \(16\le m\le20\) without factor-dependent support recognition.

### M31 Korean summary

M31에서는 입력 \(N\)을 받기 전에 두 exceptional family와
\(2\le A,B,g\le m\)의 모든 유효 descriptor를 선택하는 공개 다항
selector를 정의했습니다. 모든 primitive exit를 비용에 포함하고,
상수 support column 제거와 중복 column 병합이 모든 pair outcome을
보존함을 증명했습니다.

\(9\le m\le15\)의 완전한 balanced population에서는 정규화 signature가
단사이며, 104개 소수쌍을 independent dense evaluator로 다시
검사했습니다. 반면 \(m=16\)에서는 \(191,227,233\)이 270개
descriptor의 모든 charged exit에서 같은 signature를 가져 세
semiprime 쌍이 모두 실패합니다. 양성 결과는 인수분해에 의존하는
유한 약속 정리이고, 음성 결과는 정확히 \(2\le A,B,g\le m\)인
selector에만 적용됩니다. 일반 고전적 다항 시간 정수분해 알고리즘,
모든 다항 selector의 하한, asymptotic density 또는 공개 promise
recognizer는 주장하지 않습니다.

## M30 outcome

- Date: 2026-07-28.
- Branch: `research/20260728-m30-compact-support-signatures`.
- The M29 completion PR #38 and M30 start PR #39 were merged before this
  completion cycle. M30 started from checkpoint
  `0b28f17b234dad4091ea72dc04c5844e41a2e942`.
- `DEF-030` fixes the public-before-\(N\) candidate quantifier, analytical
  support signature, compact cost ledger, and factorization-free recognition
  boundary.
- `BAR-024` is `PROVED`: a candidate list separates a square-free pair
  exactly when the two prime signatures differ, so universal pair separation
  is equivalent to injectivity. Signature-bucket sizes \(n_u\) give exactly
  \(\sum_u\binom{n_u}{2}\) failed pairs. Consequently
  \(r\ge\lceil\log_2s\rceil\), or
  \(r\ge\lceil\log_2(s+1)\rceil\) when zero signatures are forbidden. The
  proof also gives the exact balanced-bucket minimum collision count.
- `REF-026` is `REFUTED`: candidates \((15,7)\) cover every prime in
  \(\{3,5,7\}\) and meet the two-candidate nonzero-signature lower bound, but
  signatures \((1,1,2)\) collide on \(3\cdot5\); the two GCDs are 15 and 1.
  NR-027 preserves the scope.
- EXP-0029 exhaustively checked 38,860 signature assignments, 366,284 pairs,
  12 tight minima, 82,019 balanced primes, 2,978,644 canonical-prefix
  coordinates, and 2,034 explicit balanced pairs. The prefix
  \(C_2,\ldots,C_m\) was noninjective at all 32 registered lengths
  \(9\le m\le40\). At \(m=40\), all 22,394 primes had zero signature and all
  250,734,421 pairs collided. This is finite evidence for one polynomial
  compact schedule, not an asymptotic impossibility theorem.
- Python implements arbitrary-width signature and collision accounting. Rust
  independently packs up to 64 coordinates, and C# independently uses
  `BigInteger`; all 34 selected cross-language comparisons passed.
- Registered EXP-0029 summary SHA-256:
  `74db38bf2f8ebeb088b3773fc1d94207cca0c1a73f7efb7a58a82f387dac5212`.
- Final gates passed: foundation and bilingual publication checks
  (124 claims and 28 experiment hashes), 208 Python tests, compileall, Ruff,
  mypy, Rust formatting/Clippy and 36 tests, warning-free C# Release build,
  58 baseline comparisons, 34 M29 regression comparisons, the registered M30
  audit, and 34 M30 comparisons.
- XeLaTeX produced a 75-page English PDF and a 14-page Korean PDF. Visual QA
  of the M30 theorem, full proof, Korean formulas and glyphs, limitations,
  hashes, and page transitions found no clipping, overlap, or unreadable
  text. Stable artifacts are `output/pdf/mosef-paper.pdf` and
  `output/pdf/mosef-paper-ko.pdf`.
- M30 proof/implementation core commit
  `9b9b87092d8ba919fc539a43aeddb18d8269f45f` is pushed to the research
  branch. Draft PR #40 targets `main`:
  `https://github.com/whitespaca/MOSEF/pull/40`.
- Next selected milestone: M31 will define a factorization-independent
  diversified selector over exceptional families, bases, and parameters
  before searching for an injective compact schedule or scoped collision.

### M30 Korean summary

M30에서는 여러 compact cofactor가 만드는 비트열을 각 소수의
signature로 정의했다. 두 소수의 signature가 다를 때에만 어떤 후보의
GCD가 proper factor를 주므로, 모집단의 모든 서로 다른 소수쌍을
분리하는 필요충분조건은 signature 사상의 단사성이다. 후보가 \(r\)개,
소수가 \(s\)개이면 적어도 \(r\ge\lceil\log_2s\rceil\)가 필요하며,
모든 소수가 최소 한 후보에 포함되어야 한다면
\(r\ge\lceil\log_2(s+1)\rceil\)가 필요하다.

단순한 union coverage와 후보 수 하한은 충분하지 않다. 후보
\((15,7)\)은 \(\{3,5,7\}\)의 모든 소수를 덮지만 3과 5의 signature가
같아서 \(N=15\)에서 각각 full collision과 unit만 만든다. 또한
\(C_2,\ldots,C_m\) 접두 일정은 \(9\le m\le40\)의 유한 감사 범위에서
한 번도 단사가 아니었다. 이 결과는 해당 접두 일정의 유한 음성
결과일 뿐이며, 다른 다항식 compact 일정이나 일반 고전적
다항시간 정수분해의 불가능성을 뜻하지 않는다.

## M29 outcome

- Date: 2026-07-28.
- Branch: `research/20260728-m29-compact-cofactor-prime-support`.
- Completed milestone: characterize the prime support of the compact
  length-indexed family \(A=3,B_m=2^m+3,g=2\), including every denominator
  exception, and determine exactly what one resulting cofactor GCD can
  separate on a finite prime population.
- `DEF-029` defines the analytical support. `BAR-023` is `PROVED`: with
  \(E_m=3\cdot2^m+5\),
  \[
  C_m=\frac{16(2^{E_m}+3)}{35},\qquad
  v_2(C_m)=4,\qquad 3\nmid C_m.
  \]
  The quotient-prime rules are
  \(5\mid C_m\Longleftrightarrow m\equiv2\pmod4\) and
  \(7\mid C_m\Longleftrightarrow m\equiv2\pmod3\); for every prime \(p>7\),
  \(p\mid C_m\Longleftrightarrow2^{E_m}\equiv-3\pmod p\).
  Consecutive cofactors satisfy \(\gcd(C_m,C_{m+1})=16\).
- On an \(s\)-prime population with support size \(h\), the single cofactor
  GCD has exactly \(h(s-h)\) proper pair outcomes,
  \(\binom h2\) full collisions, and \(\binom{s-h}{2}\) units. Hence it
  separates at most \(\lfloor s^2/4\rfloor\) pairs and cannot cover all
  pairs when \(s\ge3\). This is a one-candidate signature-cut barrier, not a
  multi-candidate, adaptive-schedule, circuit, or general-factoring lower
  bound.
- `REF-025` is `REFUTED`, and NR-026 preserves the scope boundary:
  exponential exact magnitude and accumulated support across levels do not
  certify universal same-level extraction by one GCD.
- EXP-0028 checked 52,026 prime/level profiles, 51,934 generic
  congruences, 92 quotient-prime cases, 49,742 consecutive-support cases,
  13 exact closed forms and consecutive GCDs, 82,019 balanced primes,
  2,034 explicit pair outcomes, three outcome witnesses, and 34 selected
  Python/Rust/C# comparisons with zero failures. No same-index balanced
  support hit occurred through input length 40; this remains finite empirical
  evidence. Summary SHA-256:
  `8ca6c6310b64e56d37cfbc98caba9deddd02d5c35ea909870341aae8f23efb7a`.
- Full gates pass: foundation and bilingual publication consistency (120
  claims and 27 experiment hashes), 200 Python tests plus 182 subtests,
  bytecode compilation, Ruff 0.16.0, strict mypy 2.3.0 over 24 source files,
  Rust formatting/Clippy/35 tests, C# Release build with zero warnings, the
  58 baseline and 34 M29 cross-language comparisons, and the registered
  EXP-0028 rerun.
- Publication policy is now bilingual. `paper/main.tex` remains the
  authoritative English manuscript, while `paper/main-ko.tex` is a Korean
  companion whose complete 120-claim status inventory is generated from
  `research/PUBLICATION_CLAIMS.md`. The consistency gate rejects missing,
  duplicated, reordered, or status-divergent Korean claim entries.
- XeLaTeX converged to a 73-page English PDF and an 11-page Korean PDF with
  no undefined references, citations, overfull or underfull boxes, package
  warnings, or missing characters. Eleven rendered pages covering both
  titles, M29 statements and proof, experiment/limitations, reproduction
  commands, references, and the Korean claim-table tail passed visual
  inspection. Stable PDFs:
  `output/pdf/mosef-paper.pdf`, SHA-256
  `424d26dbf9624da86240f6fd1c3ec1f3c21b268366f720d4c6aac8d210863c19`;
  `output/pdf/mosef-paper-ko.pdf`, SHA-256
  `967cad591027d0a883d89483a86020ba1d7d721095c56c0a4ca25753fe931356`.
- The validated M29 implementation, proof, experiment, bilingual manuscript,
  and publication-policy changes are commit
  `bb7f3d794d31ab9e1908bd3e672dfa64f8a4e73a`.
- M29 start PR #37 was merged into its M28 base before the validated result
  commits. Completion Draft PR #38 therefore targets `main` and carries the
  complete M29 result:
  `https://github.com/whitespaca/MOSEF/pull/38`.
- Next selected milestone: M30 will determine the exact injectivity criterion
  and minimum candidate count for multi-candidate compact prime signatures
  before proposing any concrete parameter schedule.

### M29 Korean summary

M29에서는 길이별 compact \(\Phi_4\) cofactor의 소수 지지를 직접
분석했습니다. 분모에 포함된 소수 5와 7은 별도의 정확한 합동식으로
처리했고, 그 밖의 소수는 하나의 모듈러 합동식으로 판정할 수 있음을
증명했습니다. 연속한 두 cofactor의 최대공약수는 항상 16입니다.

하나의 cofactor가 유한한 소수 집합을 hit 집합과 miss 집합으로 나누면,
서로 다른 쪽에 놓인 \(h(s-h)\)개의 semiprime 쌍만 proper factor를
만듭니다. 같은 쪽의 두 소수는 각각 full collision 또는 unit 결과를
만들기 때문에, 소수가 세 개 이상이면 한 후보만으로 모든 쌍을
분리할 수 없습니다. 이는 단일 후보에 대한 정확한 장벽이며 여러 후보,
적응형 일정, 일반 산술 회로 또는 일반 정수분해의 하한은 아닙니다.

앞으로는 영문 원고와 함께 한글 동반 원고를 계속 작성합니다. 한글
원고의 전체 claim ID와 상태는 공개 주장 행렬에서 자동 생성하며, 두
원고의 증거 등급이 달라지면 검증 단계가 실패하도록 고정했습니다.
다음 M30은 여러 compact 후보가 만드는 다중 비트 signature가 모든
소수 쌍을 분리하기 위한 정확한 injectivity 조건과 최소 후보 수를
연구합니다.

## M28 outcome

- Date: 2026-07-28.
- Branch: `research/20260728-m28-length-indexed-cofactor-schedule`.
- Completed milestone: formalize schedules selected from the eventual input
  length before the particular \(N\), separate compact modular cost from
  exact-lift materialization, and account for every balanced semiprime pair
  that a materialized support can touch.
- `DEF-028` defines the two cost ledgers. `BAR-022` is `PROVED`: for
  \(\mathcal P_m=\{p\text{ prime}:2^{m-1}\le p^2<2^m\}\),
  \(s_m=|\mathcal P_m|\), \(b_m=\lfloor(m-1)/2\rfloor\), and \(h_m\) hit
  primes, exactly \(\binom{s_m-h_m}{2}\) pairs make every materialized GCD
  one and \(b_mh_m\le W_m\). Universal population coverage therefore needs
  \(h_m\ge s_m-1\) and \(W_m\ge b_m(s_m-1)\).
- `REF-024` is `REFUTED`, and NR-025 preserves the scope boundary. The valid
  family \(A=3,B=2^m+3,g=2\) has \(O(m)\)-bit public parameters and a
  polynomial-time compact modular evaluator, while its exact \(\Phi_4\)
  cofactor has at least \(3\cdot2^m+4\) bits. This proves an exact
  compact/materialized separation, not broad distinct-prime support.
- EXP-0027 checked 91 balanced primes, 623 pair lengths, 2,494 support
  profiles, 751,072 pair/value GCDs, 182,523 forced-unit pairs, 13 exact
  compact-gap cofactors, 52 compact residues, and 24 Python/Rust/C#
  comparisons with zero failures. Summary SHA-256:
  `e0744fdd20d09b103e6e5e237b2e1375290d32d3991951913086965321e29d52`.
- Full gates pass: foundation and publication consistency (116 claims and 26
  experiment hashes), 194 Python tests plus 172 subtests, bytecode
  compilation, Ruff 0.16.0, strict mypy 2.3.0 over 23 source files, Rust
  formatting/Clippy/34 tests, C# Release build, the 58 baseline and 24 M28
  cross-language comparisons, and the registered EXP-0027 rerun.
- XeLaTeX converged to 71 pages with no undefined references, citations,
  overfull boxes, underfull boxes, or final warnings. Sixteen rendered pages
  covering the title, M28 statements, synthesis table, limitations,
  conclusion, full proof, reproduction commands, and references passed
  visual inspection. Stable PDF: `output/pdf/mosef-paper.pdf`, SHA-256
  `da9349fb7a7e18dc160542acfa85387d47ad5998ab7fd838e0dc9d418a07c7b6`.
- The validated M28 implementation, proof, experiment, manuscript, and
  quality-gate updates are commit
  `285e6a6d767b406c0b8aad86725e20f2b95f77bb`.
- M28 start PR #35 was merged into its stacked M27 base before the result
  commits, and that base was later removed from the remote. Completion Draft
  PR #36 therefore targets `main` and carries the unmerged M27 completion
  together with M28:
  `https://github.com/whitespaca/MOSEF/pull/36`.
- Next selected milestone: M29 will study the distinct balanced-prime support
  of the compact family \(A=3,B=2^m+3,g=2\) directly, without materializing
  the exact cofactor or inferring support from magnitude.

### M28 Korean summary

M28에서는 입력 길이만 보고 정해지는 스케줄의 비용을 두 원장으로
분리했습니다. 정확한 정수 값을 실제로 펼치면 균형 소수 \(h_m\)개를
지원하는 데 최소 \(b_mh_m\)비트가 필요하고, 지원 밖의 두 소수로 만든
세미프라임은 반드시 실패합니다. 그러나 모듈러 계산만 하는 압축
평가기는 지수적으로 긴 정확한 코팩터도 다항 시간에 다룰 수 있으므로,
이 물질화 장벽을 압축 스케줄 전체의 하한으로 확대할 수 없습니다.
M29는 큰 정수의 크기가 아니라 그 정수가 실제로 포함하는 서로 다른
균형 소수의 지지집합을 직접 조사합니다.

## M27 outcome

- Date: 2026-07-28.
- Branch: `research/20260727-m27-exceptional-cofactor-schedule`.
- Completed milestone: classify the exceptional cofactor roots and
  prime-power valuations, isolate every overlap with the two stages and the
  direct cyclotomic factor, and test fixed public cofactor schedules.
- `DEF-027` gives the exact local valuation criterion and the compact
  \(C_4,C_6\) overlap descriptors. Unit-root counts are bounded by
  \(\min(A(B-1)-2,p-1)\), and every proper cofactor GCD remains a total
  factor exit.
- `BAR-021` is `PROVED`. The stage/cofactor resultants are explicit powers
  of \(B\), except for the second-stage/\(C_6\) factor
  \(2^{A(B-1)-2}B^{A-1}\). The direct cyclotomic overlaps reduce to positive
  public integers \(R_4=u_4^2+v_4^2\) and
  \(R_6=u_6^2+u_6v_6+v_6^2\), so all local overlap prechecks are exact.
- `REF-023` is `REFUTED`, and NR-024 preserves the scope barrier. Any fixed
  finite joint schedule charges only finitely many positive integers, hence
  has finite prime support. Choosing two distinct primes outside that support
  gives infinitely many square-free semiprimes on which every charged GCD is
  one. This does not cover input-length-indexed, input-dependent, or adaptive
  schedules.
- Minimized fixed-prefix-16 witnesses are \(2491=47\cdot53\) for the
  \(\Phi_4\) pair \((A,B)=(3,7)\), and \(1537=29\cdot53\) for the
  \(\Phi_6\) pair \((A,B)=(5,3)\).
- EXP-0026 completed 29 exact pair/remainder/resultant checks, 725 root
  enumerations, 30,015 unit-root trials, 60,030 stage implications, 30,015
  cyclotomic implications, 34,104 compact/dense checks, 34,104 valuations,
  27,474 exhaustive semiprime comparisons, and 24 Python/Rust/C# comparisons
  with zero failures. Summary SHA-256:
  `3ef554db904681c3e6764bf3aba3561b1075ee4372735ce06b7f15dcbc39b6f5`.
- Full gates pass: foundation and publication consistency (112 claims and 25
  experiment hashes), 189 Python tests plus 166 subtests, Python bytecode
  compilation, Ruff 0.16.0, strict mypy 2.3.0 over 22 source files, Rust
  formatting/Clippy/33 tests, C# Release build, the 58 baseline and 24 M27
  cross-language comparisons, and the registered EXP-0026 rerun. Ruff,
  mypy, and pytest were installed in isolated `uv tool` environments, and
  BLK-003 is resolved.
- XeLaTeX converged to 68 pages with no undefined references, citations,
  overfull boxes, or final warnings. The title, theorem, proof, reproduction,
  transition, and final pages were rendered and visually inspected. Stable
  PDF: `output/pdf/mosef-paper.pdf`, SHA-256
  `ade1efd06707c71c2fae782754178a22859304a607defbdff95f6039d354a0fd`.
- The validated M27 implementation, proof, experiment, manuscript, and
  quality-gate repair are commit
  `9bc8e6b61458c5ed0cc36a2a3a696439025732b6`.
- M27 start PR #33 is merged. Completion Draft PR #34 stacks the validated
  result on the completed M26 branch:
  `https://github.com/whitespaca/MOSEF/pull/34`.
- Next selected milestone: M28 asks whether an input-length-indexed
  exceptional-cofactor schedule can evade BAR-021 without hidden factor
  access or superpolynomial total cost.

### M27 Korean summary

M27에서는 예외 cofactor의 국소 영점, 소수 거듭제곱 valuation, 두 stage 및
직접 cyclotomic 인자와의 겹침을 정확히 분류했습니다. 고정된 유한 공개
스케줄은 유한한 소수 지지만 충전하므로, 그 지지 밖의 서로 다른 두 소수로
이루어진 무한히 많은 square-free semiprime을 놓칩니다. 이 장벽은
입력 길이에 따라 커지는 스케줄에는 적용되지 않으며, 그 경우가 M28의
다음 연구 대상입니다.

## M26 outcome

- Date: 2026-07-27.
- Branch: `research/20260727-m26-exceptional-cyclotomic`.
- Completed milestone: do the only exceptional rational families,
  \(\Phi_4\) with coefficients \((1,1)\) and \(\Phi_6\) with
  coefficients \((2,1)\), add extraction power beyond direct GCDs with
  their small cyclotomic polynomials?
- `DEF-026` retains both stages, both public overlap bounds, the fixed
  cyclotomic GCD, an independently evaluated compact cofactor, aggregate,
  valuations, extraction, recognition, and charged dense output.
- `BAR-020` is `PROVED`: both exact cofactors have degree
  \(A(B-1)-2\) and constant-size periodic/geometric descriptors evaluable
  without modular division in \(O(\log A+\log B)\) modular operations.
  Capped prime-power valuations add, and proper direct or cofactor GCDs are
  total factor exits.
- `REF-022` is `REFUTED`. Clean square-free residual witnesses are
  \((N,g,A,B)=(15,11,3,7)\) for \(\Phi_4\) and
  \((35,8,5,3)\) for \(\Phi_6\); repeated-prime witnesses are
  \((9,4,11,7)\) and \((25,3,5,3)\). The direct cyclotomic, both stages,
  and both public bounds are units, while the cofactor GCD is proper.
- EXP-0025 completed 29 symbolic divisions, 61,277 compact/dense/product
  checks, 122,583 capped valuation checks, and 20 Python/Rust/C# comparisons
  with zero failures. Summary SHA-256:
  `aa160aff769f98463268f641365c3a7ac498f2c5dc4e70a018f86a4d116bdbbb`.
- Dense output remains charged at \(A(B-1)-1\) coefficients. No public base
  schedule, success density, probability, universal factorization result, or
  broader-circuit theorem is claimed.
- Validation: foundation and publication checks pass with 108 claims and 24
  experiment hashes; 185 Python tests pass; Python compile-all passes; Rust
  formatting, clippy with warnings denied, and all 32 tests pass; C# Release
  build passes; the 58 baseline and 20 M26 cross-language checks pass; the
  registered EXP-0025 rerun has zero failures. Optional Ruff and mypy remain
  unavailable under BLK-003.
- Paper: XeLaTeX converged to 66 pages with no undefined references,
  citations, overfull boxes, or final warnings. The new theorem and appendix
  pages were rendered and visually inspected. Stable PDF:
  `output/pdf/mosef-paper.pdf`, SHA-256
  `848f26b8a8efb79b78851dee5b2bb7cc8612f3170ff6e6df0c06f78672a0d4da`.
- The validated M26 implementation, proof, experiment, and manuscript core
  is commit `cc850a084be6940349c09dc35e0ab73a43f791d6`.
- The earlier M26 start PR #30 was merged. Completion Draft PR #32 stacks
  the two validated M26 commits on the M25 branch and is mergeable:
  `https://github.com/whitespaca/MOSEF/pull/32`.
- Next selected milestone: M27 isolates local cofactor roots and overlaps
  before testing any factorization-independent public schedule.

### M26 Korean summary

M26에서는 \(\Phi_4,\Phi_6\) 예외 계열의 quotient를 전개하지 않고도
주기 계수와 기하급수 합으로 평가하는 정확한 공식을 증명했습니다. 직접
cyclotomic GCD가 1이어도 cofactor가 새 인수를 주는 square-free 및 반복
소수 반례가 모두 존재합니다. 따라서 다음 M27은 이 cofactor의 국소 영점과
stage overlap을 먼저 분류한 뒤 공개 base schedule 가능성을 검토합니다.

## M25 outcome

- Date: 2026-07-27.
- Branch: `research/20260727-m25-rational-root-orbits`.
- Completed milestone: M25, complete Galois-orbit classification of the
  rational root-of-unity ratio outside both stage zero sets.
- `DEF-025` fixes the requested-order orbit model and compact all-order
  descriptor. `THM-003` is `PROVED`: the ratio is rational exactly for
  \[
  n\mid\gcd(A-1,B-1),\quad
  (n,A,B)\equiv(4,3,3)\pmod4,\quad\text{or}\quad
  n=6,\ A\equiv5,\ B\equiv3\pmod6,
  \]
  with respective ratios \(-1,1,2\) and canonical primitive pairs
  \((-1,1),(1,1),(2,1)\).
- Conjugation forces \(n\mid A(B-2)+1\). Normalizing by
  \(A^{-1}\bmod n\) makes \(R+1\) the squared absolute value of a cyclotomic
  integer. Its exact norm leaves only orders four and six beyond the
  common-step family.
- `REF-021` is `REFUTED`, and NR-022 preserves the minimized obstruction:
  \((A,B,n)=(2,4,5)\) satisfies the phase congruence but has irrational
  ratio \((1+\sqrt5)/2\).
- EXP-0024 checked 930 unequal pairs, 237,150 orders, 228,338 exact
  cyclotomic orbit ratios, 2,426 phase candidates, and 81 positive-ratio
  norm identities. It found 513 rational orders in the three proved
  families, 1,913 phase-only irrational orders, zero classification
  failures, and 24 Python/Rust/C# agreements. Canonical summary SHA-256:
  `7e498c64b848973c95501e5e043e2187ab21772c5d7edbbf62f737d36cf9bb13`.
- Square-free \(\Phi_4\), repeated-prime \(\Phi_4\), and square-free
  \(\Phi_6\) modular witnesses give proper GCDs \(5,25,7\) while both
  stages and both public overlap bounds are units.
- Requested-order recognition is polynomial in the binary input lengths.
  Factoring \(\gcd(A-1,B-1)\), listing all its divisors, or expanding
  cyclotomic/numerator polynomials remains charged by actual work and output.
- Full gates passed: foundation and publication consistency (104 claims and
  23 experiment hashes), 180 Python tests and bytecode compilation, Rust
  formatting/Clippy/31 tests, C# Release build with zero warnings or errors,
  58 baseline comparisons, the registered EXP-0024 rerun, and the 24-check
  M25 differential validator. Optional Ruff and mypy remain unavailable
  under BLK-003.
- XeLaTeX converged with no LaTeX warnings, undefined references or
  citations, or overfull/underfull boxes. All 62 pages were rendered and
  visually inspected. Stable PDF: `output/pdf/mosef-paper.pdf`, SHA-256
  `76800e665ea6cf92d9e367bb937974c6c5ecfb4afb73f00d42aeb7194879cbd5`.
- The validated M25 core is commit
  `5cbfb614f886c82e41353f905bd1cb958dd764c5`.
- Draft PR #29 targets `main`:
  `https://github.com/whitespaca/MOSEF/pull/29`. The earlier M25 start PR
  #28 is merged.
- Scope: the theorem classifies one unequal depth-two root-of-unity ratio.
  It proves no schedule, success probability, density, general factoring
  result, or general arithmetic-circuit lower bound.
- Next selected milestone: M26 isolates the direct \(\Phi_4,\Phi_6\) GCDs
  from any residual quotient/cofactor path before proposing schedules.

### M25 Korean summary

M25에서는 예외적인 root-of-unity 비율을 완전히 분류했습니다. 공통차수
계열의 비율은 \(-1\)이고, 그 밖에는 정확히 \(\Phi_4\) 계열의 비율 \(1\)과
\(\Phi_6\) 계열의 비율 \(2\)만 남습니다. 위상 합동만으로는 충분하지
않으며, \((A,B,n)=(2,4,5)\)가 가장 작은 반례입니다. 다음 M26에서는 이
두 고정 cyclotomic 계열이 해당 작은 다항식의 직접 GCD를 넘어서는
잔여 cofactor 추출 경로를 갖는지 조사합니다.

## M24 outcome

- Date: 2026-07-27.
- Branch: `research/20260727-m24-rational-residue`.
- Completed milestone: M24, primitive coefficient-content normalization,
  exact stage resultants, and the exceptional cyclotomic scope.
- `DEF-024` retains the content and first-prefix trichotomies, primitive and
  original aggregates, both aggregate-stage overlap GCDs, compact resultant
  descriptors, extraction, and explicitly bounded exact cyclotomic audits.
- `BAR-019` is `PROVED`. For
  \(F=c_1S_A(X)+c_2S_B(X^A)\),
  \[
  \operatorname{Res}(S_A,F)=(c_2B)^{A-1},\qquad
  \operatorname{Res}(S_B(X^A),F)=c_1^{A(B-1)}B^{A-1}.
  \]
  Aggregate overlap with the first and second stages therefore divides the
  public GCDs \(\gcd(c_2B,N)\) and \(\gcd(c_1B,N)\), respectively.
- At a root of unity away from the stage denominators, the exact condition is
  \[
  c_1(\zeta^A-1)^2+c_2(\zeta-1)(\zeta^{AB}-1)=0.
  \]
  This criterion does not collapse to the M23 boundary factors.
- `REF-020` is `REFUTED`, and NR-021 preserves the obstruction. For
  \((A,B,c_1,c_2)=(3,7,1,1)\), \(\Phi_4\) divides the numerator. At
  \((N,g)=(55,2)\), both stages, coefficient content, and public overlap
  bounds are units, but the aggregate and rational residue have GCD 5.
- EXP-0023 checked 42 unequal pairs, 1,512 coefficient/content/Bezout/root
  cases, 150,528 exact cyclotomic divisions on 1,176 primitive pairs, and
  1,788,696 modular evaluations. It found six exceptional cyclotomic
  factors and 56,586 strict residual proper GCDs, with zero unexplained
  failures and 12 Python/Rust/C# agreements. Canonical summary SHA-256:
  `01953fe34732449aa6a0ec6ba9bc8c0487027a359eb1fc96f9765ce189ec39e8`.
- Resultant descriptors are compact; expanded resultants and polynomial or
  cyclotomic output are charged by their actual bit length or explicit
  search bound.
- Full gates passed: foundation and publication consistency (100 claims and
  22 experiment hashes), 174 Python tests and bytecode compilation, Rust
  formatting/Clippy/30 tests, C# Release build with zero warnings or errors,
  58 baseline comparisons, the registered EXP-0023 rerun, and the 12-check
  M24 differential validator.
- XeLaTeX converged with no LaTeX warnings, undefined references or
  citations, or overfull/underfull boxes. All 59 pages were rendered and
  visually inspected. Stable PDF: `output/pdf/mosef-paper.pdf`, SHA-256
  `0eafe60e8c91ad0e7e3e0775f48017b5dec63cf79a3f54310685db44fc7f3b81`.
- The validated M24 core is commit
  `ca3abb022579e760368810b8956e8a5475620c0b`.
- Draft PR #27 targets `main`:
  `https://github.com/whitespaca/MOSEF/pull/27`. The earlier M24 start PR
  #26 is merged.
- Scope: no uniform exceptional-order classification, recognizer, schedule,
  density, probability, general factoring result, or general-circuit lower
  bound is claimed.
- Next selected milestone: M25 classifies rational values of
  \(-Q_2(\zeta)/Q_1(\zeta)\) through exact Galois-orbit restrictions before
  any schedule-level proposal.

### M24 Korean summary

M24에서는 계수의 공약수를 먼저 분리하고, 두 단계 다항식과 signed
분자의 resultant를 정확히 계산했습니다. 이 결과 단계와의 겹침은
공개된 계수와 \(B\)의 GCD로 완전히 통제됩니다. 그러나
\((A,B,c_1,c_2)=(3,7,1,1)\)에서는 예상 경계 밖의 \(\Phi_4\) 인자가
나타나며, \(N=55,g=2\)에서 모든 단계와 공개 경계가 단위인데도 인수
5가 추출됩니다. 따라서 다음 M25는 이 예외적 root-of-unity 비율이
유리수가 되는 정확한 조건을 조사합니다.

## M23 outcome

- Date: 2026-07-27.
- Branch: `research/20260727-m23-unequal-signed-reduction`.
- Completed milestone: M23, unequal depth-two factors and arbitrary nonzero
  public coefficient pairs.
- `DEF-023` retains both stages, every GCD, the total first-prefix
  unit/proper/full reduction, the normalized difference, its common-step
  factor, residual cofactor, extraction, and requested formal output.
- `BAR-018` is `PROVED`. The stage polynomials are coprime over
  \(\mathbb Q[X]\), their resultant is \(B^{A-1}\), and every integer common
  stage divisor divides \(B\). A unit first prefix reduces the signed form to
  one rational residue, a proper prefix already factors \(N\), and a full
  prefix reduces it to public \(c_2B\).
- For \(h=\gcd(A-1,B-1)\), the normalized difference factors as
  \[
  S_B(X^A)-S_A(X)=XS_h(X)C_{A,B}(X).
  \]
  Its polynomial GCD with either natural endpoint is exactly \(S_h\), and
  prime-power valuations split exactly between the common factor and
  cofactor.
- `REF-019` is `REFUTED`, and NR-020 preserves the residual obstruction.
  At \((N,g,A,B)=(25,3,3,2)\), both stages and the natural common factor are
  units, but the residual cofactor and rational reduction both expose the
  proper factor \(5\). The proper common-factor path is independently
  realized at \((9,2,5,7)\).
- EXP-0022 checked 42 stage coprimality/Bezout identities, 42 common-step
  factorizations, 84 endpoint polynomial GCDs, 672 boundary conditions,
  794,976 signed evaluations, 49,686 normalized differences, and 78,792
  prime-power valuations. All 11,256 proper differences followed a proved
  path, with zero unexplained failures and 12 selected Python/Rust/C#
  agreements. Canonical summary SHA-256:
  `88f103f7a18681abb357cccd4b77f0086f1a7bf165b5e31537c744a2c23d3e04`.
- Full gates passed: foundation and publication consistency (96 claims and 21
  experiment hashes), 167 Python tests and bytecode compilation, Rust
  formatting/Clippy/29 tests, C# Release build with zero warnings or errors,
  58 baseline comparisons, the registered EXP-0022 rerun, and the 12-check
  M23 differential validator. Optional pytest, Ruff, and mypy remain
  unavailable under BLK-003.
- XeLaTeX converged with no warnings, undefined references or citations, or
  overfull/underfull boxes. All 57 pages were rendered and visually
  inspected. Stable PDF: `output/pdf/mosef-paper.pdf`, SHA-256
  `69186d8eddba2c483693f9ec113962ce2b8d8b47215a1ba6044ad96a3c3d22d2`.
- The validated M23 core is commit
  `a2455e805ee3b850f0f7c61d9a521bc90d5773e9`.
- Scope: BAR-018 isolates but does not classify the surviving unit-prefix
  rational residue. It proves no universal schedule, recognizer, density,
  probability, general factoring, or broader-circuit theorem.
- Next action: M24 computes primitive-numerator resultants and cyclotomic
  factors for that rational residue before proposing a theorem.

### M23 Korean summary

M23은 서로 다른 두 기하급수 단계의 일반 signed 결합을 정확히
축약했습니다. 첫 단계가 단위이면 하나의 유리 잔여식만 남고, proper이면
이미 인수를 얻으며, full이면 공개값 \(c_2B\)로 줄어듭니다. 정규화된
차이는 \(XS_{\gcd(A-1,B-1)}\)를 정확히 인수로 가지지만, \(N=25\)
반례는 그 인자가 단위여도 남은 cofactor가 인수 5를 드러낼 수 있음을
보입니다. 따라서 M24는 이 남은 유리 잔여식을 조사합니다.

## M22 outcome

- Date: 2026-07-27.
- Branch: `research/20260727-m22-symmetric-difference`.
- Completed milestone: M22, the symmetric depth-two factor list \((A,A)\)
  with coefficients \((-1,1)\).
- `DEF-022` retains both quotient stages, their difference, endpoint
  \(E_A(g)=g^{A-1}-1\), cofactor
  \(H_A(g)=\sum_{j=1}^{A-1}g^{j-1}S_j(g^{A-1})\), total endpoint semantics,
  every GCD, construction, extraction, and requested formal output.
- `BAR-017` is `PROVED`:
  \[
  S_A(X^A)-S_A(X)=X(X^{A-1}-1)H_A(X).
  \]
  At every \(p^e\mid N\), the capped difference valuation is the capped sum
  of endpoint and cofactor valuations. A unit endpoint preserves the
  cofactor GCD, a proper endpoint already factors \(N\), and a full endpoint
  forces a full difference.
- The M21 witness is an endpoint case:
  \(\gcd(2^4-1,9)=3\). A distinct cofactor case exists at
  \(N=55,g=2,A=3\), where both stages and endpoint are units but
  \(H_3(2)=11\). Thus BAR-017 classifies rather than eliminates signed
  extraction.
- A fixed \(3\times3\) recurrence evaluates the cofactor in \(O(\log A)\)
  modular operations. Its exact sparse output has \(A(A-1)/2\) monomials
  and degree \(A(A-2)\); any requested expansion is charged.
- `REF-018` is `REFUTED`, and NR-019 preserves the failed claim that the
  symmetric mechanism has no compact algebraic classification.
- EXP-0021 checked 23 polynomial identities, 27,209 modular and expanded
  cofactor evaluations, and 43,148 prime-power valuations. All 10,238 proper
  differences followed the endpoint or unit-endpoint cofactor path, with
  zero unexplained failures and 12 selected Python/Rust/C# agreements.
  Canonical summary SHA-256:
  `637cfa34b777126206b269d16c5a3afb027b9d893a2bea00881e85efea8d4fe6`.
- Exact adversarial review passed. No universal schedule, recognition,
  density, probability, or general factoring result is claimed.
- Full gates passed: foundation and publication consistency (92 claims and 20
  experiment hashes), 159 Python tests and bytecode compilation, Rust
  formatting/Clippy/28 tests, C# Release build with zero warnings or errors,
  58 baseline comparisons, the registered EXP-0021 rerun, and the 12-check
  M22 differential validator.
- XeLaTeX converged with no warnings, undefined references or citations, or
  overfull/underfull boxes. All 56 pages were rendered and visually inspected.
  Stable PDF: `output/pdf/mosef-paper.pdf`, SHA-256
  `e7fe6d3d7c82b92a9c9cdbe5291295f9e019b22f63b75cf7bbc092f1a726d7b7`.
- The validated M22 core is commit
  `b0f678f0e576e5fc8be9b14f19f2e297ba5634d7`, pushed to
  `origin/research/20260727-m22-symmetric-difference`. Draft PR #23 targets
  `main`: `https://github.com/whitespaca/MOSEF/pull/23`.
- Next action: M23 computes formal polynomial GCD patterns for unequal
  depth-two factors and general public coefficient pairs.

### M22 Korean summary

M22는 M21의 대칭 차이를 endpoint와 cofactor의 정확한 곱으로
분해했습니다. 기존 \(N=9\) 반례는 endpoint가 이미 인수 3을
드러내지만, \(N=55\)에서는 endpoint가 단위이고 cofactor가 인수
11을 드러냅니다. 따라서 이 메커니즘은 사라지는 것이 아니라 두
경로로 정확히 분류됩니다.

## M21 outcome

- Date: 2026-07-27.
- Branch: `research/20260727-m21-linear-combination`.
- Completed milestone: M21, one charged public signed linear combination of
  explicit DEF-020 quotient stages.
- `DEF-021` charges aligned coefficient encodings and reductions, all retained
  stage exits, scalar multiplications, additions, coefficient, weighted-stage,
  and aggregate GCDs, extraction, and any requested sparse or dense formal
  output.
- `BAR-016` is `PROVED` by exact counterexample. At
  \(N=9,g=2,(A_1,A_2)=(5,5),(c_1,c_2)=(-1,1)\), every charged component has
  GCD one, but the quotient residues \(4,7\) combine to \(3\bmod9\), exposing
  the proper factor \(3\).
- The exact polynomial is
  \[
  S_5(X^5)-S_5(X)
  =-X-X^2-X^3-X^4+X^5+X^{10}+X^{15}+X^{20}.
  \]
  Its eight nonzero monomials are explicitly charged. `REF-017` is
  `REFUTED`, and NR-018 preserves the failed product-to-addition implication.
- EXP-0020 checked 1,100 symbolic descriptors, 177,450 chains, and 1,301,300
  signed combinations. It found 13,800 proper aggregates without a proper
  charged component and 6,262 strict all-unit successes, with zero semantic
  failures and 12 selected Python/Rust/C# agreements. Canonical summary
  SHA-256:
  `34f0f120a1ef3ab08b08fb9c477ea03161f96c8857bcc143e91be51137c85f6f`.
- The exact adversarial audit reconstructed every charged residue, GCD, formal
  coefficient, edge case, and scope boundary. The result is an extraction
  separation, not a universal factoring algorithm or success-rate theorem.
- Full gates passed: foundation and publication consistency (88 claims and 19
  experiment hashes), 153 Python tests and bytecode compilation, Rust
  formatting/Clippy/27 tests, C# Release restore/build with zero warnings or
  errors, 58 baseline comparisons, the registered EXP-0020 rerun, and the
  12-check M21 differential validator.
- XeLaTeX converged with no warnings, undefined references or citations, or
  overfull/underfull boxes. All 52 pages were rendered and visually inspected.
  Stable PDF: `output/pdf/mosef-paper.pdf`, SHA-256
  `e934547a6b3d7eaabb5b7648a3feb77b4688e689c694eba36ceba8f222e2bde5`.
- The validated M21 milestone commit is
  `4128a320726c022d892aaf4ffb17349d322ccb2b`. It is an ancestor of
  `origin/main`; PR #21 merged it at
  `e2e5bea5f01424a605ddd2ff4e7824410b760b6d`.

### M21 Korean summary

M21은 곱셈 전용 결과가 부호 있는 덧셈으로 확장되지 않음을 정확한
반례로 확인했습니다. \(N=9\)에서 모든 단계 값은 단위이지만 두 몫의
차는 3이 되어 인수 3을 드러냅니다. 이 결과는 새로운 추출 경로의
존재를 보인 것이며, 일반 정수 인수분해 알고리즘을 증명한 것은
아닙니다. M22는 이 상쇄가 성공하는 소수 거듭제곱 조건부터
특성화합니다.

## M20 outcome

- Date: 2026-07-27.
- Branch: `research/20260727-m20-iterated-quotient`.
- Completed milestone: M20, the public iterated geometric-quotient chain with
  \(M_0=1\), \(M_i=\prod_{j\le i}A_j\), and exact certificates
  \[
  S_{M_i}(X)=S_{M_{i-1}}(X)S_{A_i}(X^{M_{i-1}}).
  \]
- `DEF-020` charges every public factor and prefix, three binary evaluators
  per stage, both total denominator paths, all retained outputs and GCDs, the
  product aggregate, extraction, and requested dense, sparse, or expanded
  prefix output.
- `BAR-015` is `PROVED`: every stage follows BAR-014; a unit prefix preserves
  the quotient/numerator GCD, a proper prefix already factors \(N\), and a
  full prefix reduces the quotient GCD to public \(\gcd(A_i,N)\). Every
  composed denominator independently follows BAR-013. A proper final-product
  GCD implies a proper explicit stage-quotient GCD by a zero-safe unit/full
  dichotomy.
- For \(L=\sum_i\operatorname{bitlength}(A_i)\), every prefix has at most
  \(L\) bits, so compact evaluation uses \(O(rL)\) modular operations and
  \(r\le L\). Stage \(i\) has \(A_i\) sparse monomials,
  \(M_i-M_{i-1}+1\) dense positions, and a requested expanded prefix has
  \(M_i\) entries.
- Two independent reviews passed after repairs to a residue-level congruence,
  the zero-safe aggregate argument, expanded-prefix charging, and literal
  multiplication accounting. The adversarial review additionally passed
  58,680 small chains and a 256-bit prefix stress case.
- `REF-016` is `REFUTED`; NR-017 records that product-only iteration creates
  no success outside the charged stage and prefix exits. It may mask an
  earlier proper stage as a later full aggregate collision. This is not a
  lower bound for cross-stage addition, general rational programs, or
  arithmetic circuits.
- EXP-0019 checked 155 symbolic chains, 430 exact stage identities, 5,190
  coefficients, 190,805 modular chains, 529,330 stages, 338,525 prefix
  linkages, and 1,249,465 residue identities. All 68,260 proper final
  products had a proper stage quotient; there were zero unexplained cases and
  all 12 selected Python/Rust/C# comparisons agreed. Canonical summary
  SHA-256:
  `06cbbb13eca00655d33da9858117de6920d1e63f6bbfe95794ec18642000f9da`.
- Full gates passed: foundation and publication consistency (84 claims and 18
  experiment hashes), 147 Python tests and bytecode compilation, Rust
  formatting/Clippy/26 tests, C# Release restore/build with zero warnings or
  errors, 58 baseline comparisons, EXP-0019, and the 12-check M20
  differential validator.
- XeLaTeX converged with no warnings, undefined references or citations, or
  overfull/underfull boxes. All 50 pages were rendered and visually
  inspected. Stable PDF: `output/pdf/mosef-paper.pdf`, SHA-256
  `6cd6eaef92fda55c6eec886c65340a5a9150d4b3c09add6d281ef60cbb37fbe7`.
- The validated M20 milestone commit is
  `11255cca8a3186249f19d8f018270b575b05cc92`. Publication is blocked by
  BLK-022: the remote branch remains at `2978f613255e7ef22cc051f485900c5a4fefd4eb`,
  GitHub CLI is unauthenticated, and no M20 pull request was created or
  verified.
- Next action: M21 should define the smallest factorization-independent
  signed linear-combination grammar over explicit certified quotient stages
  and test whether cross-stage cancellation invalidates component-to-
  aggregate GCD implications.

## Korean summary

M20을 완료했습니다. 공개 인수 사슬의 각 기하급수 몫 단계를
unit/proper/full로 분기하면 새 인수 추출 경로가 생기지 않으며, 최종
곱의 GCD가 proper이면 명시된 단계 몫 중 하나도 proper임을
증명했습니다. 결정적 탐색, Python/Rust/C# 교차 검증, 독립 검토 두 건,
전체 출판 검사, 50쪽 PDF 시각 검증이 모두 통과했습니다. 다음 M21은
단계 값 사이의 덧셈과 뺄셈이 이 결론을 벗어나는지 조사합니다.

## M19 outcome

- Date: 2026-07-27.
- Branch: `research/20260727-m19-nested-quotient`.
- Completed milestone: M19, the cancellation-obscured two-stage identity
  \[
  S_{AB}(X)/S_A(X)=S_B(X^A).
  \]
- `DEF-019` and `BAR-014` distinguish the rational denominator \(S_A(g)\)
  from the composed denominator \(g^A-1\), give both paths total
  unit/proper/full semantics, and charge construction, residue, GCD,
  certificate, and expanded-output costs.
- `BAR-014` is `PROVED`: a unit intermediate denominator makes rational
  numerator and quotient GCDs identical; a proper denominator is already a
  factor; and a full denominator forces \(g^A\equiv1\pmod N\), so the
  quotient GCD is the public \(\gcd(B,N)\). The composed denominator
  independently follows BAR-013.
- Two independent adversarial reviews passed after repairing the
  residue-versus-GCD wording and the sparse/dense formal-output accounting.
  The quotient has degree \(A(B-1)\), \(B\) nonzero monomials, and
  \(A(B-1)+1\) dense coefficient positions.
- `REF-015` is `REFUTED`; NR-016 records that cancellation in this exact
  two-stage identity does not create a proper quotient success outside the
  rational numerator, proper intermediate denominator, public multiplier,
  and composed-denominator paths. This is not a general rational-circuit
  lower bound.
- EXP-0018 checked 144 symbolic identities, 6,084 coefficients, 177,264
  modular circuits, and 354,528 residue identities. The rational-denominator
  split was 120,444 unit, 46,932 proper, and 9,888 full cases; the composed
  split was 74,028 unit, 66,936 proper, and 36,300 full cases. There were zero
  unexplained reductions and all 12 selected Python/Rust/C# comparisons
  agreed. Canonical summary SHA-256:
  `a6d1bd1344b439901f3d40b9dc226fbcedcaba6886d07363461b0814db6aa2aa`.
- Full gates passed: foundation and publication consistency (80 claims and 17
  experiment hashes), 141 Python tests and bytecode compilation, Rust
  formatting/Clippy/25 tests, C# Release restore/build with zero warnings or
  errors, 58 baseline comparisons, EXP-0018, and the 12-check M19
  differential validator. Optional third-party pytest, Ruff, and mypy remain
  unavailable under BLK-003.
- XeLaTeX converged with no warnings, undefined references or citations, or
  overfull/underfull boxes. All 47 pages, including the revised title and
  abstract, Section 20, results table, limitations, conclusion, complete
  proof, and reproduction appendix, were rendered and visually inspected.
  Stable PDF: `output/pdf/mosef-paper.pdf`, SHA-256
  `783ccf5f60de1cad688c638f4ef59a3f69f5dfffcd3a596ace4637ac8867db8f`.
- The implementation/proof checkpoint is
  `557731c0feefe1c58b65ab24c6b7b6552cd392bc`; the validated completion
  commit is `5d15540d372642dd4ca61f5ecf324026dbd55adf`.
- The completion push was rejected before execution under BLK-021 because
  publishing this specific repository payload was not explicitly authorized.
  The remote branch remains at the checkpoint commit, GitHub CLI is
  unauthenticated, and no pull request was created or verified.
- Next action: M20 should formalize an iterated public factor chain
  \(M=\prod_i A_i\), give every prefix denominator a total branch, and test
  whether induction reduces every quotient success to a charged prefix exit
  or public multiplier.

## Korean summary

M19를 완료했습니다. 두 단계 기하급수 몫의 중간 분모와 합성 분모를
각각 unit/proper/full로 분기하면, 상쇄가 새로운 숨은 인수 추출 경로를
만들지 않음을 증명했습니다. 두 독립 검토와 세 언어 구현, 결정적
탐색, 전체 출판 검사, 47쪽 PDF 시각 검증이 통과했습니다. 다음 M20은
이 구조를 공개 인수 사슬의 여러 단계로 확장할 수 있는지 조사합니다.

## M18 outcome

- Date: 2026-07-27.
- Branch: `research/20260727-m18-geometric-sum`.
- Completed milestone: M18, the charged left-to-right binary circuit for
  \[
  S_M(X)=\sum_{i=0}^{M-1}X^i=\frac{X^M-1}{X-1}
  \]
  at an arbitrary public positive exponent \(M\).
- `DEF-018` gives the exact even/odd pair grammar for
  \((P_M,S_M)=(X^M,\sum_{i<M}X^i)\), total unit, proper-factor, or
  full-collision denominator semantics, and explicit charges for the encoded
  base and exponent, preprocessing, construction, operations, outputs, GCDs,
  extraction, and any expanded coefficient output.
- `BAR-013` is `PROVED`: a unit denominator makes quotient and endpoint GCDs
  identical; a proper denominator is already a factor; and a full denominator
  gives \(S_M(g)\equiv M\pmod N\), so the quotient GCD is the public
  \(\gcd(M,N)\). The proper branch preserves success existence, not divisor
  value: \(N=15,g=4,M=2\) gives denominator GCD \(3\), quotient GCD \(5\),
  and a full endpoint collision.
- For \(\ell=\operatorname{bitlength}(M)\), the exact composition counts are
  \(2(\ell-1)+\operatorname{popcount}(M)-1\) multiplications and
  \((\ell-1)+\operatorname{popcount}(M)-1\) additions. The post-reduction
  residue circuit is \(O(\ell\operatorname{poly}(k))\), while total work is
  polynomial in the charged base, modulus, and exponent lengths. Compact
  formal metadata uses \(O(\ell)\) bits; expanded output has \(M\) entries.
- `REF-014` is `REFUTED`; NR-015 records that compact arbitrary-exponent
  evaluation still produces one quotient value, not a new extraction path
  beyond endpoint, denominator, and public-exponent GCDs.
- EXP-0017 checked 64 symbolic identities, 2,080 coefficients, 320,896
  modular circuits, 1,323,696 binary-prefix steps, and 320,896 residue
  identities. All 166,784 unit, 134,272 proper, and 19,840 full denominator
  reductions held with zero unexplained reductions. All 12 selected
  Python/Rust/C# comparisons agreed. Canonical summary SHA-256:
  `0f182c819374451a3fd8d9ddb7ffc75580ac363186e19bd804eb28fe1371d2bd`.
- Independent source/scope review required explicit accounting for the
  encoded base length and reduction; the repaired review passed. Independent
  adversarial review passed the proof, \(M=1\), even and repeated-prime
  moduli, exact counters, \(M=2^{64}-1\), a 129-bit exponent in the
  arbitrary-precision implementations, and the registered three-language
  checks.
- Full gates passed: foundation and publication consistency (76 claims and
  16 experiment hashes), 135 Python tests and bytecode compilation, Rust
  format/Clippy/24 tests, C# Release restore/build with zero warnings or
  errors, 58 baseline comparisons, EXP-0017, and the 12-check M18
  differential validator. Optional third-party pytest, Ruff, and mypy remain
  unavailable under BLK-003.
- XeLaTeX converged with no warnings, undefined references or citations, or
  overfull/underfull boxes. All 45 pages, including the revised title and
  abstract, Section 19, results table, limitations, conclusion, complete
  proof, and reproduction appendix, were rendered and visually inspected.
  Stable PDF: `output/pdf/mosef-paper.pdf`, SHA-256
  `85eb9b46fad3ebd5b336be49d56bdcadcc750d0c203bc58e1889a08ac858c31e`.
- Core implementation/proof/paper commit:
  `9f36ee9c75d8f13d2883301da63404747e358bcc`.
- The core commit is synchronized to
  `origin/research/20260727-m18-geometric-sum`. No pull request was created
  or verified because GitHub CLI remains unauthenticated. The local
  status/cleanup follow-up is commit `c6f4dc3`; its push is blocked under
  BLK-020 because this specific external payload was not explicitly
  authorized.
- Next action: M19 should formalize the cancellation-obscured two-stage
  identity \(S_{AB}(X)/S_A(X)=S_B(X^A)\), including total intermediate
  denominator semantics and a division-free composed path.

## Korean summary

M18은 임의의 공개 지수 \(M\)에 대한 geometric sum을 이진 합성으로
\(O(\log M)\) 단계에 계산하지만, 새로운 인수분해 경로를 만들지는
못함을 증명했습니다. 분모가 unit이면 endpoint GCD와 같고, proper이면
분모 자체가 이미 인수이며, full collision이면 결과가 공개된
\(\gcd(M,N)\)로 환원됩니다. 이는 일반 rational circuit 하한이 아니며,
다음 단계는 중간 분모가 nonunit일 수 있는 두 단계 quotient입니다.

## M17 outcome

- Date: 2026-07-27.
- Branch: `research/20260727-m17-rational-circuit`.
- Completed milestone: M17, the charged dyadic exact-division and repeated
  composition circuit
  \[
  (X^{2^t}-1)/(X-1)=\sum_{i<2^t}X^i
  =\prod_{j<t}(X^{2^j}+1).
  \]
- `DEF-017` gives every denominator a total unit, proper-factor, or
  full-collision branch and retains the division-free product in every case.
  It charges the public factorization-free constructor, \(t\) squarings,
  \(t\) explicit dyadic factors, \(\max(0,t-1)\) product multiplications,
  extended-GCD division attempt, requested outputs, GCDs, and extraction.
- `BAR-012` is `PROVED`: valid division equals the factor product; every
  proper quotient GCD implies a proper dyadic-factor GCD; and every proper
  numerator GCD implies a proper denominator or dyadic-factor GCD. The
  proper factor value need not be identical: \(N=8,g=1,t=2\) has component
  GCDs \(2,2\) but quotient GCD \(4\).
- The compact circuit uses \(O(t+1)\) modular operations and
  \(O((t+1)\operatorname{poly}(k))\) bit operations. Degree and monomial
  metadata use \(O(t+1)\) bits, but an expanded formal coefficient output
  has \(2^t\) entries. Those monomials are terms of one quotient value, not
  separately extracted exponent tests.
- `REF-013` is `REFUTED`; NR-014 records that dyadic geometric compression
  cannot create an exponential test family or a proper success when every
  explicit component GCD is trivial or full. At \(N=15,g=4,t=1\),
  denominator/factor GCDs \(3,5\) aggregate to full numerator GCD \(15\).
  At \(N=6,g=1,t=3\), division has a full denominator collision while the
  division-free quotient GCD is \(2\).
- EXP-0016 checked 11 symbolic identities, 2,047 coefficients, 55,154
  modular circuits, 275,770 repeated-squaring recurrences, 55,154 product
  identities, 22,757 proper quotient implications, and 25,430 proper
  numerator implications with zero unexplained proper successes. All 12
  selected Python/Rust/C# comparisons agreed. Canonical summary SHA-256:
  `1db5968e635901bc00eda0fdaa211aefe16af630741459eb9eb7f51ab50fc219`.
- Independent source/scope review required exact unreduced lifts and weakened
  exact factor-value wording. Independent adversarial review additionally
  required \(t=0\) cost repair and exact implementation of the reported
  product multiplication count. Both repaired re-reviews passed.
- Full gates passed: foundation and publication consistency (72 claims and
  15 experiment hashes), 127 Python tests and bytecode compilation, Rust
  format/Clippy/23 tests, C# Release restore/build with zero warnings or
  errors, EXP-0016, and the 12-check differential validator. Optional
  third-party pytest, Ruff, and mypy remain unavailable under BLK-003.
- XeLaTeX converged with no warnings, undefined references or citations, or
  overfull/underfull boxes. All 43 pages, including the revised title and
  abstract, theorem, results, limitations, full proof, and reproduction
  appendix, were rendered and visually inspected. Stable PDF:
  `output/pdf/mosef-paper.pdf`, SHA-256
  `48e9b77dbe4973bc9e9e8b9a66b2efb61d7d5f7ff45224f1b1530f031e35abc9`.
- Local milestone implementation/proof/paper commit:
  `8a09b70497451a23711d853f94af0eb8b9fbeea4`.
- Remote publication is blocked under BLK-019: the safety reviewer rejected
  the M17 branch push because this specific external payload has not been
  explicitly authorized. GitHub CLI is also unauthenticated, so no pull
  request was created.
- Next action: M18 should formalize the arbitrary-exponent binary geometric
  sum \(S_M(X)\), including its odd/even composition recurrences and the
  full-denominator reduction \(S_M(1)\equiv M\pmod N\).

## Korean summary

M17은 \(2^t\)개 단항식을 가진 dyadic geometric quotient를 압축 계산해도
그것이 \(2^t\)개의 독립 GCD 검사가 되지는 않음을 보였습니다. 분모가
비가역인 경우도 proper factor, full collision, unit으로 모두 분기하며,
어떤 proper quotient 또는 numerator 성공도 분모나 \(t\)개 dyadic factor
중 하나의 proper 성공을 동반합니다. 일반 rational/compositional circuit에
대한 하한은 아니며, 다음 단계는 임의 지수 \(M\)의 binary geometric sum
회로입니다.

## M16 outcome

- Date: 2026-07-27.
- Branch: `research/20260727-m16-product-dag`.
- Completed milestone: M16, the explicit-atom product-only DAG whose shared
  subproducts are evaluated once while formal leaf occurrences remain
  non-materialized.
- `DEF-016` charges the public-input, factorization-free constructor, explicit
  exponent atoms, product gates, requested residue or formal outputs, GCDs,
  and extraction. `BAR-011` is `PROVED`: every node has an exact
  nonnegative atom-multiplicity product and positive-multiplicity
  prime-power valuation formula; every proper node GCD implies a proper used
  atom GCD; and gate \(s\) has at most \(2^s\) unfolded occurrences, tightly.
- Sharing therefore permits exponential repeated formal occurrences but does
  not synthesize exponentially many distinct exponent tests or a proper
  success absent from the explicit atom table. A complete optional formal
  table has \(O(a(a+t)(t+1))\) bits for \(a\) atoms and \(t\) gates.
  `REF-012` is `REFUTED`, and NR-013 records the scoped negative result.
- Aggregation can worsen extraction. The single atom at
  \(N=9,g=4,d=1\) has proper GCD \(3\), but its first self-product has full
  GCD \(9\). The complementary \(N=21,g=2,\Delta=(2,3)\) union collision
  also persists.
- The BAR-008 transfer remains separate: at each input length the explicit
  atom list must be common and factorization-independent, and its exponents
  must have \(O(k\log k)\) bits. Addition, subtraction, division,
  composition, closed-form atom synthesis, modulus-specific identities,
  adaptive factor dependence, other groups, and general arithmetic circuits
  remain outside BAR-011.
- EXP-0015 checked 611,572 exact product-DAG syntaxes, 3,033,586 gate
  occurrences, 517,020 residue circuits, 2,282,274 node semantics, and
  3,581,928 valuation components. All 856,512 proper-node implications held,
  84,013 product nodes masked a used atom success as a full collision, the
  exact occurrence maxima were \(2,4,8,16,32\), and the 10 selected
  Python/Rust/C# comparisons agreed. Canonical summary SHA-256:
  `431faf3c71fc0f13c3152bffd06faa5e7eb96382164e40611979c8573e41a12d`.
- Independent source-scope review required positive-multiplicity valuation
  sums to avoid \(0\cdot(+\infty)\) and removed unsupported minimality
  wording. Independent adversarial review required the \(t=0\) formal-table
  repair, a used-atom rather than global-atom audit predicate, the corrected
  84,013 reachable-mask count, and accurate all-moduli box wording. Both
  re-reviews passed.
- Full gates passed: foundation and publication consistency (68 claims and
  14 experiment hashes), 118 Python tests and bytecode compilation, Rust
  format/Clippy/22 tests, C# Release build with zero warnings or errors,
  EXP-0015, and the 10-check differential validator. Optional third-party
  pytest, Ruff, and mypy remain unavailable under BLK-003.
- XeLaTeX converged with no warnings, undefined references or citations, or
  overfull/underfull boxes. All 41 pages, including the revised abstract,
  theorem, results, limitations, full proof, and reproduction appendix, were
  rendered and visually inspected. Stable PDF:
  `output/pdf/mosef-paper.pdf`, SHA-256
  `6880cfc1740496123ea8aa9f8d8ad029de8adbfad4f29996b4750e9960989023`.
- Local milestone implementation/proof/paper commit:
  `0728628b5ffe5387b926080de8674f22d1c8dadf`.
- Remote publication is blocked under BLK-018: the safety reviewer rejected
  the M16 branch push because this specific external payload has not been
  explicitly authorized. GitHub CLI is also unauthenticated, so no pull
  request was created.
- Next action: M17 should formalize a richer rational or compositional
  circuit, beginning with the dyadic telescoping identity, and charge failed
  division, formal output, residue evaluation, and factor extraction.

## 한국어 요약

M16에서는 명시적으로 계산한 \(g^{d_i}-1\) 원자들을 곱셈 DAG에서
재사용하는 비물질화 모델을 검증했습니다. 공유를 통해 형식적 반복
횟수는 \(2^t\)까지 늘릴 수 있지만, 새로운 서로 다른 지수 검사를
만들거나 사용된 원자에 없던 인수를 얻을 수는 없습니다. 이 결과는
일반 산술 회로 하한이 아니며, 덧셈ㆍ나눗셈ㆍ합성ㆍ폐쇄형 원자 생성은
다음 연구 범위로 남습니다.

## M15 outcome

- Date: 2026-07-27.
- Branch: `research/20260727-m15-implicit-batch`.
- Completed milestone: M15, the selector-described standard product tree
  whose every selected residue leaf is enumerated, evaluated, stored, and
  charged.
- `DEF-015` fixes the leaf-materialized semantics. `BAR-010` is `PROVED`:
  the root GCD has the exact sum-of-prime-power-valuations formula, every
  proper root GCD implies a proper individual leaf GCD, aggregation may mask
  individual separators as a full collision, and an \(n\)-leaf binary tree
  has exactly \(n-1\) internal multiplications in addition to its \(n\)
  charged leaf evaluations and materializations.
- Polynomial charged work therefore permits only polynomially many
  materialized leaves. The BAR-008 transfer is separate: for each input
  length the complete leaf list must also be common and
  factorization-independent, and its ordinary exponent lengths must be
  \(O(k\log k)\). No result is claimed for specialized circuits without leaf
  materialization.
- `REF-011` is `REFUTED`; NR-012 records that compact selector syntax does
  not compress a standard materialized batch. The explicit witness
  \(N=21,g=2,\Delta=\{2,3\}\) has proper leaf GCDs \(3,7\) but root GCD
  \(21\).
- EXP-0014 checked 3,821,928 nonempty batches, 6,488,889 valuation
  components, 1,333,349 proper-root implications, and 4,096 exact tree
  counts. It recorded 850,538 masked separator batches. Its canonical summary
  SHA-256 is
  `c4c3f20cc193dc90728d19fa5809d794d9ee07474fe093f12439cf3d16508529`;
  the selected Python/Rust/C# differential validator passed 10 checks.
- Independent adversarial review initially rejected equality wording for a
  population upper bound and the missing common factorization-independent
  transfer hypothesis. Both were repaired, and re-review passed. Independent
  source-scope review found no external citation requirement and confirmed
  the non-general-circuit boundary.
- Full gates passed: foundation and publication consistency (64 claims and
  13 experiment hashes), 111 Python tests and bytecode compilation, Rust
  format/Clippy/21 tests, C# Release build with zero warnings or errors,
  EXP-0014, and the 10-check differential validator. XeLaTeX converged
  without final warnings to a 38-page PDF; all pages and the new theorem,
  proof, results, limitations, and reproduction pages were rendered and
  visually inspected. The stable PDF SHA-256 is
  `9ae325caaf98428d15443638e90063e4896b9fa191cb60c9d5b6145084280ca6`.
- Local milestone implementation/proof/paper commit:
  `21b6673898d672659412c0cb4300f6ed6c00a5f6`.
- The push was rejected before execution because this specific M15 payload
  lacks explicit authorization for external GitHub publication. BLK-017
  records the local-only branch, and no M15 pull request was created.
- Optional third-party Python `pytest`, Ruff, and mypy gates remain
  unavailable under BLK-003.
- Next selected milestone: M16, define the smallest uniform
  non-materializing product circuit and determine whether its formal output
  or proper-factor extraction can avoid DEF-015's leaf cost without assuming
  a general arithmetic-circuit lower bound.

## M14 outcome

- Date: 2026-07-27.
- Branch: `research/20260727-m14-addition-subtraction`.
- Completed milestone: M14, the explicitly charged same-base
  addition-subtraction representation beyond multiplication-only DEF-010.
- `DEF-014` charges every product, extended-GCD inversion, parent/sign/output
  table entry, and retained output after a base GCD precheck. `BAR-009` is
  `PROVED`: \(x_i=g^{z_i}\) and \(|z_i|\le2^i\); negative exponents give
  exactly the same raw GCD and capped valuations as their positive absolute
  values, while zero gives only the full collision. A common fixed-base
  schedule with \(T(k)=O(k\log k)\) therefore transfers to BAR-008 and has a
  \(2^{o(k)}\) factor-scale combined hit set and stipulated-population
  fraction \(2^{-\alpha k+o(k)}\).
- `REF-010` is `REFUTED`; NR-011 records that charged same-base ratios and
  inversions alone do not restore a nonvanishing exponent-mediated
  \(p-1/p+1\) promise fraction. Proper factors returned by the initial base
  GCD remain separate algorithmic exits.
- EXP-0013 completed 2,403,786 node-growth checks, 190,344 direct residue
  checks, 646,400 sign-symmetry checks, 10,100 unit prechecks, 6,127 proper
  nonunit prechecks, and 570 full-nonunit prechecks. It observed 734,190
  negative and 251,685 zero outputs and exact maxima
  \(1,2,4,8,16,32,64\). Its canonical summary SHA-256 is
  `7203d3fc6ee67d5af3984c2b5c1eefb1640275dccdecaf979fed645d2d0fbb7d`;
  the selected Python/Rust/C# differential validator passed 24 checks.
- Independent adversarial review reproduced the focused tests, registered
  experiment, and differential validator, then separately enumerated
  self-ratios and checked prime powers and 20,000 lower-bound boundary cases
  without finding a defect. Independent source-scope review found no new
  citation requirement and confirmed the theorem's charged, factor-oblivious,
  same-base, unit-branch scope.
- Full gates passed: foundation and publication consistency (60 claims and
  12 experiment hashes), 106 Python tests and bytecode compilation, Rust
  format/Clippy/20 tests, C# Release build with zero warnings or errors,
  EXP-0013, and the 24-check differential validator. XeLaTeX converged
  without final warnings to a 36-page PDF; all pages and the new theorem,
  proof, results, and reproduction pages were rendered and visually
  inspected. The stable PDF SHA-256 is
  `6ccdff994d04783b3a05170c28a1b6ccab9f1dca8c46dd8bbb64498655479f28`.
- Local milestone implementation/proof/paper commit:
  `e80115bd27200c0ec0f37a388cd4e9a4bbac9769`.
- Follow-up status commit: `4f92cbe`. The push failed because Windows Git
  had no credentials (`SEC_E_NO_CREDENTIALS`); BLK-016 records the
  unpublished branch, and no M14 pull request was created.
- The result excludes implicit exponential batches, fixed-modulus
  equal-residue shortcuts, factor-dependent adaptation, special
  endomorphisms, unrelated multi-base expressions, other groups/channels,
  population existence or natural density, and general factoring.
- Optional third-party Python `pytest`, Ruff, and mypy gates remain
  unavailable under BLK-003.
- Next selected milestone: M15, formalize the smallest explicitly charged
  implicit product/remainder-tree or arithmetic-circuit batch and determine
  whether it can test exponentially many factor-scale exponents without
  paying for output extraction.

## M13 outcome

- Date: 2026-07-27.
- Branch: `research/20260727-m13-general-factor-scale`.
- Completed milestone: M13, the general explicit factor-scale divisor
  question at the exact \(O(k\log k)\) exponent-length boundary.
- `DEF-013` gives the exact small/large-prime split budget. `BAR-008` is
  `PROVED`: every common polynomial-size explicit schedule whose exponents
  have bit length \(O(k\log k)\) hits only
  \(2^{O(k\log\log k/\log k)}=2^{o(k)}\) primes at any fixed
  \(O(k)\)-bit factor scale. BAR-003 therefore gives promised-pair fraction
  \(2^{-\alpha k+o(k)}\) on every stipulated common-input-length population
  of size at least \(2^{\alpha k}\), and BAR-005 transfers the conclusion to
  fixed-base DEF-010 schedules with \(O(k\log k)\) charged nodes.
- `REF-009` is `REFUTED`; NR-010 records that squareful multiplicities,
  prime powers, mixed exponents, and noninitial prime supports do not evade
  the boundary. The result excludes longer exponents, exponentially many
  explicit exponents, adaptive factor-dependent schedules, richer compressed
  representations, other group channels, population existence or natural
  density, and general factoring.
- EXP-0012 completed 1,572,816 split-bound checks, 4,421,736 exact
  divisor-membership checks, and 5,344,372 prime-candidate checks. Its
  canonical summary SHA-256 is
  `a564c00c8eaafad6f5be31d8705147578e6c86d9e6f42c6a9bacf3b0d93591d3`.
  The focused Python/Rust/C# validator passed 36 checks.
- Independent adversarial review reproduced the focused tests, registered
  experiment, differential validator, and publication gate, then added
  209,958 exact divisor-bound cases and 467,958 canonical
  labeled-occurrence mappings. It explicitly exercised 53,454 \(A=0\),
  37,864 \(J=0,A>0\), 97,702 \(A<2J\), and 20,938
  \(A\ge2J,J>0\) cases without finding a defect.
- Independent source review found no imported theorem or new citation
  requirement: BAR-008 is elementary and depends only on proved internal
  BAR-003 and BAR-005. The manuscript avoids novelty claims.
- Full gates passed: foundation and publication consistency (56 claims and
  11 experiment hashes), 99 Python tests and bytecode compilation, Rust
  format/Clippy/19 tests, C# Release build with zero warnings or errors, the
  registered experiment and focused differential validator, and a clean
  converged 33-page XeLaTeX build. All pages and the new theorem/proof pages
  were rendered and visually inspected. The stable PDF SHA-256 is
  `7d821784f7aabc1b8791101189ce7844a157f5299f6fa60d9b35b747316cec4d`.
- Local milestone commit:
  `6628ea8158458ba2b3c660ee9d70fc651fa0bbfa`. The sandboxed push lacked
  Windows credentials, and external publication was not authorized; BLK-015
  records the unpublished branch. GitHub CLI is unauthenticated, so no M13
  pull request was created.
- Optional third-party Python `pytest`, Ruff, and mypy gates remain
  unavailable under BLK-003.
- Next selected milestone: M14, formalize a minimal explicitly costed
  representation outside DEF-010 and test whether it can expose
  factor-scale divisor families beyond BAR-008 without hidden exponential
  expansion.

## M12 outcome

- Date: 2026-07-27.
- Branch: `research/20260726-m12-prime-yield`.
- Completed milestone: M12, the critical/supercritical first-primes
  primorial prime-yield question at target-factor scale.
- `DEF-012` defines the exact factorial support threshold and binomial
  divisor-candidate bound. `BAR-007` is `PROVED`: for \(r(k)=O(k)\), only
  \(2^{O(k\log\log k/\log k)}=2^{o(k)}\) divisors of \(P_{r(k)}\) are small
  enough to equal \(q\pm1\) for \(q\le2^{\beta k}\). Hence the promised-pair
  fraction is at most \(2^{-\alpha k+o(k)}\) on every stipulated
  \(2^{\alpha k}\)-size common-input-length population.
- `REF-008` is `REFUTED`; NR-009 records the scale mismatch between
  \(2^{\Theta(k)}\) total primorial divisors and the subexponential
  factor-scale subset. The result uses no prime-distribution hypothesis and
  does not extend to arbitrary boundary exponent families.
- EXP-0011 completed 9,961,434 divisor checks, 145,413 support checks,
  290,826 prime-candidate checks, 16 balanced-population formula checks, 32
  cross-language comparisons, and four Python-only scale-bound records. Its
  canonical summary SHA-256 is
  `bad46ee8f6638d98d19bc4479da998ea55af4d1617fef10cfc2c3ea973f39751`.
- Independent adversarial review found and then verified the repair of the
  omitted \(T\le r<2T\) binomial case. Its extra audit checked 139,986 exact
  thresholds/formulas, 20,010 divisor supports, 153,456 channel-disjointness
  cases, 9,352 nested-hit containments, and 500 factorial/node transfers.
- Independent source review confirmed Lichtman's exact power-scale
  shifted-prime theorem and that it supplies no polylogarithmic,
  square-free, primorial-supported, or simultaneous-channel yield statement.
- Full gates passed: foundation and publication consistency (52 claims and
  ten experiment hashes), 93 Python tests and bytecode compilation, Rust
  format/Clippy/19 tests, C# Release build with zero warnings or errors, the
  registered M12 experiment and 36-count focused validator, and a clean
  converged 30-page XeLaTeX build. The updated sections and full proof were
  rendered and visually inspected. The stable PDF SHA-256 is
  `8fbc253727c4f42bd1e1248f09ca9a67431692ea4faea189a3f0fce11bcf8ee5`.
- Local milestone commit:
  `53915509bc257f343f61a814b1ec90bcd0ed8aeb`. The sandboxed push lacked
  Windows credentials, and the external push was not authorized; BLK-014
  records that the local branch is ahead of its existing remote ref. No M12
  pull request exists.
- Optional third-party Python `pytest`, Ruff, and mypy gates remain
  unavailable under BLK-003.
- Next selected milestone: M13, classify non-primorial squareful and
  noninitial-support exact-boundary families by factor-scale divisor yield
  per charged construction node.

## M11 outcome

- Date: 2026-07-26.
- Branch: `research/20260726-m11-boundary-constant`.
- Completed milestone: M11, the exact \(\Theta(k\log k)\) multiplication
  straight-line boundary.
- `DEF-011` gives an exact integer divisor budget whose monotone envelope
  satisfies
  \(\log_2 R(L)\le(1+o(1))L/\log_2L\).
- `BAR-006` is `PROVED`: a polynomial-size common schedule with
  \(L(k)\le(c+o(1))k\log_2k\) hits at most \(2^{ck+o(k)}\) odd primes.
  On a supplied common-input-length population of size at least
  \(2^{\alpha k}\), its promised-pair fraction therefore vanishes when
  \(c<\alpha\). The \(c=0\) endpoint and the fixed-base DEF-010 transfer are
  included explicitly.
- The first-primes primorial \(P_r\) supplies an explicit boundary-capacity
  family: \(\ell(P_r)=\Theta(r\log r)\), \(\tau(P_r)=2^r\), and ordinary
  binary evaluation uses at most \(2\ell(P_r)-2\) multiplication nodes.
  This does not supply an asymptotic prime-yield lower bound.
- `REF-007` is `REFUTED`; NR-008 records that repeated squaring reaches the
  boundary while its exposed exponent divisors remain only powers of two.
- EXP-0010 checked all 262,143 positive exponents below \(2^{18}\), enumerated
  all divisors and \(d\pm1\) candidates for the first 12 primorials, and
  executed 1,777,936 exact trial divisions. At \(r=12\), the 43-bit exponent
  had 4,096 divisors, 67 binary nodes, and 897 disjoint-channel prime hits
  split 449/448. The canonical summary SHA-256 is
  `22699f23a1421805cb472ddca1723e8d580d601cd25ca72b8b2cd134743e4f83`.
- Independent adversarial review reproduced the seven focused tests,
  registered experiment, 32 differential comparisons, and publication gate,
  then added 10,000 exact-budget cases, 200,000 divisor-count cases,
  primorial accounting through \(r=50\), and 131,054 channel checks through
  \(r=16\). No mathematical defect was found, including in the \(c=0\)
  transfer or stipulated-population scope.
- Independent source review checked the official Rosser--Schoenfeld scan at
  printed page 69 and confirmed equation (3.13), its strict inequality,
  natural-log convention, and \(r\ge6\) hypothesis. The imported result is
  used only for the primorial construction range; no prime-yield or novelty
  statement is attributed to it.
- Full validation passed: foundation and publication consistency (47 claims
  and nine experiment hashes), 86 Python tests and bytecode compilation, Rust
  format/Clippy/19 tests, C# Release build with zero warnings or errors, all
  registered M1--M11 searches and differential suites, and a clean converged
  28-page XeLaTeX build. Every page was rendered and visually inspected; the
  stable PDF SHA-256 is
  `bfd6a0f165c20dd5db0f7822d6b9decd253a96da26d295a157f799b6cdeba812`.
- Optional third-party Python `pytest`, Ruff, and mypy gates remain unavailable
  under BLK-003; dependency-free unit tests and compilation are the validated
  Python substitutes in this environment.
- Scope: BAR-006 is a hit-set upper bound for common
  factorization-independent schedules on a supplied finite population. It
  constructs no exponentially large common-input-length population, proves no
  natural-density or prime-yield theorem, recognizes no promise class, and is
  not a general algebraic or factoring lower bound.
- Next selected milestone: M12, isolate whether an explicit critical or
  supercritical boundary family admits a rigorously supported uniform
  \(d\pm1\) prime-yield statement after population normalization.

## M11 execution snapshot

- Date: 2026-07-26.
- Branch: `research/20260726-m11-boundary-constant`.
- Core implementation/proof commit:
  `cd391e5cf64207ea7dc2f6e4dd55cf469af45424`.
- Registered experiment commit:
  `de290aea906d0a868fafa958c789227e94904d37`.
- Reviewed manuscript and milestone completion commit:
  `a681071f73a22f02e0007923fa03d9e1c4b30d98`.
- Remote delivery: blocked by BLK-013. The policy-reviewed push attempt was
  rejected because the user has not explicitly authorized external GitHub
  egress for the new M11 payload; the local GitHub CLI is also unauthenticated.
- Next selected milestone: M12, an explicit critical/supercritical
  boundary-family prime-yield theorem or obstruction.

## M10 outcome

- Date: 2026-07-26.
- Branch: `research/20260726-m10-straight-line-compression`.
- Completed milestone: M10, a restricted multiplication straight-line
  compression barrier.
- `DEF-010` defines a factor-oblivious multiplication-only DAG with explicit
  parent/output indices, exact formal exponents, charged construction, and
  charged node-by-node modular evaluation.
- `BAR-005` is `PROVED`: node \(i\) represents \(g^{e_i}\) with
  \(e_i\le2^i\). Exact formal realization of \(g^d\) therefore needs at least
  \(\lceil\log_2d\rceil\) multiplication nodes, tight for powers of two by
  repeated squaring.
- A common schedule with fixed initial-base count and total charged nodes
  \(T(k)=o(k\log k)\) has \(E(k)\le T(k)+O(1)\) and
  \(L(k)\le T(k)+1\), so BAR-004 still applies. Polynomial \(T(k)\) cannot
  hide a superpolynomial-bit formal exponent in this model.
- `REF-006` is `REFUTED`; NR-007 records that the compact descriptor
  \(2^{2^s}\) requires exactly \(2^s\) charged multiplications inside
  DEF-010.
- EXP-0009 enumerated all 1,587,600 commutative seven-node programs and
  checked 1,647,202 constructed nodes for exponent growth and direct residue
  agreement. Seventeen tower levels and 24 Python/Rust/C# comparisons passed.
  Its canonical summary SHA-256 is
  `67508cf957fa356350a707a58f1079aebcea4f02481ff826cd5ed09727d210fa`.
- Independent adversarial review reproduced the registered search, 5/5
  focused unit tests, and 24/24 differential checks, then added 645,350 node
  checks across 20,000 deterministic random programs, 200,000 arbitrary-\(d\)
  lower-bound edge checks, and tower levels 0--20. Independent source-scope
  review confirmed that the proof is elementary and needs no new citation.
- Full validation passed: foundation and publication consistency (42 claims,
  eight experiment hashes), 79 Python tests and bytecode compilation, Rust
  format/Clippy/19 tests, C# Release restore/build with zero warnings or
  errors, all registered M1--M10 searches and differential suites, and a clean
  converged 25-page XeLaTeX build. Every page was rendered and visually
  inspected; the stable PDF SHA-256 is
  `5b64504d4bf18f2646defdcd512f4e2bd96c6b34cca5a03d7f874050a8acd0e0`.
- Scope: BAR-005 concerns exact formal exponents in a factor-oblivious
  multiplication-only same-base DAG. It is not a fixed-modulus residue,
  generic-group, richer-algebraic, natural-density, recognizer, factoring, or
  general lower-bound result, and it leaves
  \(T(k)\not=o(k\log k)\) open.
- 한국어 요약: 짧은 지수 표기만으로 계산 비용을 숨길 수는 없다. 이
  곱셈 전용 모델에서는 곱셈 한 번마다 형식적 지수 길이가 최대 한
  비트만 증가하며, 정확한 \(k\log k\) 경계는 다음 과제로 남는다.
- Next selected milestone: M11, specify and test one divisor-rich
  \(\Theta(k\log k)\)-node schedule family.

## M10 execution snapshot

- Date: 2026-07-26.
- Branch: `research/20260726-m10-straight-line-compression`.
- Completed milestone: M10.
- Core implementation/proof commit:
  `5501d2d1d2a6a5c584fdc03f905e9a36a6054733`.
- Registered experiment commit:
  `18f104fdb69b8fd96f5776796047487ef211f03a`.
- Validated milestone completion commit:
  `bd822de928ff14fd6ee0e270d50862591ee36918`.
- Remote delivery: blocked by `BLK-012`; the policy-reviewed push attempt was
  rejected because the user has not explicitly authorized external GitHub
  egress for this new M10 payload.
- Next selected milestone: M11, the exact
  \(\Theta(k\log k)\) straight-line schedule boundary.

## M9 outcome

- Branch: `research/20260726-m9-divisor-rich-schedules`.
- Completed milestone: M9, an explicit-list exponent-encoding divisor barrier
  for the combined local \(p-1/p+1\) promises.
- `DEF-009` defines the exact integer one-length budget
  \[
  B(\ell)=(\ell+1)^{\lfloor\sqrt\ell\rfloor}2^{A_\ell}
  \]
  and its monotone envelope \(Q\), where \(A_\ell\) is the largest integer
  satisfying
  \((\lfloor\sqrt\ell\rfloor+1)^{A_\ell}<2^\ell\).
- `BAR-004` is `PROVED`: every exponent satisfies
  \(\tau(d)\le B(\ell(d))\), with
  \(\log_2Q(L)=O(L/\log L)\). A factorization-independent explicit schedule
  with polynomial list size and \(L(k)=o(k\log k)\) therefore hits at most
  \(2^{o(k)}\) odd primes.
- On every stipulated finite odd-prime population of size at least
  \(2^{\alpha k}\), whose distinct products all have common input length
  \(k\), the uniform combined-promised pair fraction is at most
  \(2^{-\alpha k+o(k)}\) and tends to zero. This is not a prime-distribution
  existence claim or a natural-density theorem.
- `REF-005` is `REFUTED`; NR-006 records the minimal bounded value-only
  counterexample \((d,p,q,N)=(7,3,5,15)\).
- EXP-0008 checked 262,143 exact divisor budgets and single-exponent hit
  bounds, 2,306,048 direct prime-oracle comparisons, 987 record-family bounds,
  and 46 selected Python/Rust/C# comparisons. Its canonical summary SHA-256
  is
  `b8357f9436ef4d31d072f62dab4f3c8dedad41d6f1787803bf5df2f485ca53ed`.
- Independent adversarial review reproduced the registered search and added
  200,000 divisor-budget checks, 128 small-length boundaries, 24 density caps,
  and 57 \(O(k)\)-bit large-value cases. It identified and verified repairs
  for upper-bound notation and oscillatory \(L(k)\). Independent source-scope
  review confirmed that the proof is elementary and requires no new citation,
  while prohibiting novelty, prime-distribution, recognizer, or general
  lower-bound framing.
- Full validation passed: foundation and publication consistency (38 claims,
  seven experiment hashes), 74 Python tests and bytecode compilation, Rust
  format/Clippy/17 tests, C# Release restore/build with zero warnings or
  errors, all registered M1--M9 searches and differential suites, and a clean
  converged 22-page XeLaTeX build. Every page was rendered and visually
  inspected; the stable PDF SHA-256 is
  `7bc17c4a48a02052b6bedc241cb9c81016542d701c920b652b383103276305fd`.
- Scope: the result does not cover compressed or batched implicit families,
  adaptive factor-dependent schedules, exponentially many explicit
  exponents, \(L(k)\not=o(k\log k)\), or other algebraic mechanisms. It is not
  a recognizer, natural-density theorem, factoring lower bound, or general
  classical factoring result.
- 한국어 요약: 명시적으로 나열하고 개별 평가하는 다항 개수의 지수는 각
  지수 길이가 \(o(k\log k)\)이면 전체 \(p\pm1\) 적중 소수 집합이
  준지수적 크기에 머문다. 지숫값이 인수보다 크다는 사실만으로는 약속
  포함을 보장하지 않는다.
- Next selected milestone: M10, specify one evaluable compressed or
  \(L(k)\not=o(k\log k)\) representation model before searching for an escape
  theorem or a stronger obstruction.

## M9 execution snapshot

- Date: 2026-07-26.
- Branch: `research/20260726-m9-divisor-rich-schedules`.
- Completed milestone: M9.
- Core implementation/proof commit:
  `1416d70a6bc39a4c7491e9ec86e4e67f96293962`.
- Registered experiment commit:
  `fcdb3eb76c942b6c8019ef3002b138385a7ec5b9`.
- Validated milestone completion commit:
  `12f2172aaaca8016baccca109d28e0e7cbb8db98`.
- Remote delivery: blocked by `BLK-011`; the policy-reviewed push attempt was
  rejected because the user has not explicitly authorized external GitHub
  egress for this new M9 payload.
- Next selected milestone: M10, a rigorously specified compressed or
  \(L(k)\not=o(k\log k)\) exponent representation with exact construction and
  evaluation accounting.

## M8 outcome

- Branch: `research/20260726-m8-promise-recognition`.
- Completed milestone: M8, a self-contained common-schedule
  finite-distribution and magnitude barrier for the union of the local
  \(p-1\) and \(p+1\) semiprime promises.
- `DEF-008` defines the combined prime signature
  \[
  \sigma_\Delta(p)=
  ((\mathbf1_{p-1\mid d},\mathbf1_{p+1\mid d}))_{d\in\Delta}.
  \]
  It is evaluated at an unknown factor for analysis and is not an
  \(N\)-only recognizer.
- `BAR-003` is `PROVED`: a distinct-prime semiprime is in the local, hence
  hereditary, promise union exactly when its two signatures differ. For a
  finite \(s\)-prime set with \(h\) nonzero signatures, the promised fraction
  is at most \(h(2s-h-1)/(s(s-1))\), with
  \(h\le2\sum_{d\in\Delta}\tau(d)\le4|\Delta|\sqrt{\max\Delta}\).
- Every prime above \(\max\Delta+1\) has zero signature. Thus the explicitly
  defined balanced-semiprime distribution has exact zero density under the
  stated strict magnitude hypothesis and an asymptotically vanishing upper
  bound under the stated sparsity hypothesis.
- `REF-004` is `REFUTED`; NR-005 records the smallest unrestricted witness
  \((\Delta,N)=(\{1\},15)\). This witness is not labeled as a member of the
  balanced interval.
- EXP-0007 checked 987 exponent families, 296,100 direct/signature pairs,
  184,994 magnitude-zero pairs, 2,443 balanced zero-density cases, and 28
  cross-language comparisons. Its summary SHA-256 is
  `fb2f861f1670c3e4f68a0e8b461f430e7e10eeb966d9f5bec48886c810dd6cd3`.
- Independent adversarial review reconstructed the proof and additionally
  checked 1,920,600 pairs, 1,940 finite bounds, 20,000 divisor bounds, and
  27,284 balanced bit-length pairs. Independent source-scope review found no
  external citation dependency and approved the no-novelty framing.
- Full validation passed: foundation and publication consistency (34 claims,
  six experiment hashes), 66 Python tests, Python bytecode compilation, Rust
  format/Clippy/16 tests, C# Release restore/build with zero warnings or
  errors, all registered M1--M8 searches and differential suites, and a clean
  converged 19-page XeLaTeX build. Every PDF page was rendered and visually
  inspected; the stable PDF SHA-256 is
  `70c926a864636f11206936ba13887f5847f5742f93a3f9e54d4ba4a1174e57a9`.
- General classical factoring remains open. M8 proves no recognizer, natural
  density theorem, universal schedule barrier, or general lower bound.

## M7 outcome

- Branch: `research/20260726-m7-nonsplit-lucas`.
- Completed milestone: M7, a factorization-independent random-parameter
  theorem on a hereditary nonsplit Lucas-asymmetry promise class.
- `LEM-003` is `PROVED`:
  \[
  \#\{P\bmod q:V_d(P,1)=2\}
  =\frac{\gcd(d,q-1)+\gcd(d,q+1)}2.
  \]
  Its proof also counts degenerate roots and the \((q-1)/2\) nonsplit
  parameters without importing an uninspected finite-field lemma.
- `DEF-007` records the hereditary factor-dependent promise
  \(p+1\mid d,\ q+1\nmid d\). It is nonempty but is not recognized by the
  algorithm.
- `THM-002` is `PROVED`: fresh exact uniform \(P\bmod K\), with every
  discriminant and sequence branch retained, gives a correct almost-sure
  complete factorer with expected polynomial bit complexity on DEF-007 and
  at least \(1/12\) success probability at each witness trial.
- EXP-0006 checked 1,040 root formulas, 714 ordered witnesses, and 75,934
  proved-event splits. The minimum proved-event probability was \(8/51\);
  the summary SHA-256 is
  `23ed0067d2ccb642c3676ff4ea3f5c34e1e622f6372626aa84377eac74b7d905`.
- Independent adversarial review checked 2,481,900 additional root parameters
  and 1,080 repeated-factor/multiprime event splits. Independent source review
  approved the Williams/Lehmer boundary after repairs; neither the root count
  nor THM-002 is attributed to Williams or claimed as a novelty result.
- General classical polynomial-time factoring remains open. THM-002 supplies
  no membership recognizer, density theorem, statistical independence claim,
  or outside-promise termination guarantee.

## M6 outcome

- Branch: `research/20260726-m6-publishable-manuscript`.
- Completed milestone: M6, the first claim-complete publishable manuscript.
- Manuscript core commit:
  `9aac77921421fd69a4ab83e879cf50084f3024f3`.
- Validated milestone completion commit:
  `72f969df01555730cf2a27e96530444fdfa39b81`.
- The paper centers one restricted positive result (`THM-001`) and two
  structural barriers (`BAR-001`, `BAR-002`) without enlarging any hypothesis;
  `OPEN-002` and `OPEN-003` remain explicit.
- `research/PUBLICATION_CLAIMS.md` maps all 26 ledger claims into the paper.
  `scripts/check_publication.py` enforces unique claim IDs and matching
  statuses, all five full proofs, four registered experiment hashes, required
  sections, overclaim exclusions, and a real 40-hex M6 core commit.
- The reproduction appendix records exact PowerShell commands, workspace-local
  .NET state, experiment core commits, hashes, and the stable PDF path.
- Independent adversarial review reconstructed LEM-001, LEM-002, THM-001,
  BAR-001, and BAR-002; reproduced all experiment hashes and differential
  suites; and found no remaining theorem, source, hash, complexity, command, or
  publication-checker blocker after repairs.
- General classical polynomial-time integer factoring remains open. M6 is a
  restricted theorem plus two scoped barriers, not a universal algorithm or a
  general lower bound.

## M8 execution snapshot

- Date: 2026-07-26.
- Branch: `research/20260726-m8-promise-recognition`.
- Completed milestone: M8.
- Core implementation/proof commit:
  `bc8b25222823e06830530eac3962271c6d14a7ca`.
- Registered experiment commit:
  `a4895df3c0cf4de54b59932acf9f2e4ecbef2463`.
- Validated milestone completion commit:
  `3e2018616e6ac63e8f8632e42f65d34c22c00f90`.
- Remote delivery: blocked by `BLK-010`; the policy-reviewed push attempt was
  rejected because this new M8 payload lacks explicit authorization for
  external GitHub egress.
- Next selected milestone: M9, explicit divisor-rich schedules with
  polynomial-bit-length exponent values outside BAR-003's magnitude regime.

## M5 outcome

- `DEF-006` defines
  \(G_M(N,a,d)=\gcd(a^d-1,N)\),
  \(G_\Delta(N,P)=\gcd(P^2-4,N)\), and
  \(G_L(N,P,d)=\gcd(V_d(P,1)-2,N)\), including every miss, factor,
  collision, and full-discriminant sequence branch.
- `BAR-002` is `PROVED`: for the conjugate map
  \(P=a+a^{-1}\),
  \[
  V_d(P,1)-2=a^{-d}(a^d-1)^2,\qquad
  P^2-4=a^{-2}(a^2-1)^2.
  \]
  The residues have identical prime support, and their raw GCDs agree for
  square-free \(N\).
- If the exponent family contains \(2\), any proper derived Lucas or
  discriminant GCD implies a proper multiplicative-family GCD. Adding the
  conjugate Lucas family therefore cannot enlarge the multiplicative success
  domain.
- The map can degrade repeated-prime valuations:
  \((N,a,P,d)=(25,2,15,4)\) gives discriminant GCD \(1\),
  multiplicative GCD \(5\), and Lucas GCD \(25\).
- A full discriminant GCD is not a complete sequence outcome:
  \((N,P,d)=(15,8,1)\) has discriminant GCD \(15\) but sequence GCD \(3\).
- Arbitrary \(P\) remains outside the barrier. The exact witness
  \((N,a,P,d)=(15,2,9,3)\) has multiplicative GCD \(1\), discriminant
  GCD \(1\), and Lucas GCD \(5\).
- The Williams source audit confirms that the conjugate discriminant is a
  square and forces the split \(p-1\) branch, not the nonsplit \(p+1\)
  branch. Williams does not claim independence for this pairing.
- Independent literature and proof audits approved the algebra, exact failure
  semantics, source boundary, and map-specific theorem scope.

## Reproducible evidence

- Proof:
  `research/proofs/BAR-002-conjugate-channel-correlation.md`.
- Source audit:
  `research/literature/SRC-005-williams-p-plus-one.md`.
- Experiment:
  `research/experiments/EXP-0005-m5-multigroup-correlation.md`.
- Negative result: `research/NEGATIVE_RESULTS.md` NR-004.
- Python semantics: `python/mosef_reference/multigroup.py`.
- Independent selected verifiers: Rust `u64` and C# `BigInteger`.
- Registered bounds: composite moduli through 700, unit bases through 32,
  Lucas parameters through 32, and exponents through 12; deterministic
  exhaustive enumeration with no seed.
- Result: 9,773 conjugate families, 117,276 identities, 36,048 pointwise
  success implications, 69,192 square-free GCD equalities, and zero
  derived-Lucas-only family successes.
- Multiplicative and combined success counts were both 9,037. Independently
  parameterized same-exponent complements were counted separately and not
  interpreted probabilistically.
- Canonical summary SHA-256:
  `98f2be052a315231292c73319fa98066cf4d8fc4cd66740f207b2d99c7f616f5`.

## Validation

- `python scripts/validate_foundation.py`: PASS.
- `python -m unittest discover -s tests -v`: PASS (58 tests).
- `python -m compileall -q python scripts tests`: PASS.
- `python -m pytest`, Ruff, and mypy: unavailable under BLK-003; no dependency
  was added merely to hide the environment limitation.
- `cargo fmt --all --check`: PASS.
- `cargo clippy --workspace --all-targets --all-features -- -D warnings`:
  PASS.
- `cargo test --workspace --all-features`: PASS (15 Rust tests).
- Workspace-scoped `dotnet restore` and `dotnet build`: PASS with zero
  warnings and errors.
- Baseline differential validation: PASS (58 checks).
- M2 search and differential validation: PASS (78,860 candidates and 24
  cross-language checks).
- M3 search and differential validation: PASS (557 witnesses and 22
  cross-language checks).
- M4 search and differential validation: PASS (4,095 families, 114,660
  pair-profile checks, and 12 cross-language checks).
- M5 registered search: PASS (9,773 families and 117,276 identity checks).
- M5 Python/Rust/C# differential validation: PASS (18 checks).
- M7 registered search: PASS (1,040 root formulas, 714 witnesses, and 75,934
  proved-event split checks).
- M7 Python/Rust/C# differential validation: PASS (26 checks).
- `python scripts/check_publication.py`: PASS (30 claims and 5 registered
  experiment hashes).
- Independent M7 proof and source-scope review: PASS after repairing the
  \(p=3\) non-strict inequality, Legendre notation, finite-field cyclicity
  proof, and Williams/Lehmer attribution.
- `latexmk -xelatex -outdir=tmp/pdfs -interaction=nonstopmode -halt-on-error
  paper/main.tex`: PASS; the clean converged log has no warnings, undefined
  references or citations, and no overfull or underfull boxes.
- Poppler render and page-by-page visual inspection: PASS (17 pages; no
  clipping, overlap, malformed mathematics, or broken claim labels).
- Final PDF: `output/pdf/mosef-paper.pdf`, SHA-256
  `c2d9f499fb1540468d54c192491e395ec710a65a1d59c6d36ba5b217c3b1b5a2`.

## Remote state, blockers, and next action

- M2 pull request `https://github.com/whitespaca/MOSEF/pull/2` is merged into
  `main`.
- M3 and M4 remote delivery remain blocked by explicit content-egress
  authorization requirements under BLK-005 and BLK-006.
- Optional pytest/Ruff/mypy tools remain unavailable under BLK-003.
- The M5 remote branch is now visible at
  `origin/research/20260726-m5-multigroup-correlation`; `gh` is not
  authenticated, so no M5 pull request was verified or created.
- M6 local delivery is complete. Its branch is now visible at
  `origin/research/20260726-m6-publishable-manuscript`; no M6 pull request was
  verified or created.
- M7 local research and publication validation are complete. The
  policy-required push attempt was rejected because this exact new branch
  payload lacks explicit authorization for external content egress; see
  BLK-009. No M7 pull request exists.
- Next action: M8 should define factorization-independent observables before
  proposing a recognizer or input-density claim for the combined \(p-1\) and
  \(p+1\) hereditary classes.

## 한국어 요약

M5에서는 곱셈 채널 \(a^d-1\)과 Lucas 채널 \(V_d(P,1)-2\)를 정확히
비교했습니다. 자연스러운 결합 \(P=a+a^{-1}\)을 사용하면 Lucas 잔여식은
곱셈 잔여식의 제곱에 단위원을 곱한 형태가 되므로 새로운 소인수 지지집합을
만들지 못합니다. 지수 집합에 2가 포함되면 두 채널을 합쳐도 곱셈 채널보다
성공 범위가 넓어지지 않으며, \(N=25\)에서는 오히려 유용한 GCD 5가 전체
충돌 25로 악화됩니다. 다만 독립적으로 선택한 Lucas 매개변수는 이 장벽의
대상이 아니며, 작은 범위에서는 곱셈 실패를 보완하는 정확한 예도
확인했습니다. 이 결과는 일반 정수분해 알고리즘이나 모든 다중 그룹
구성에 대한 하한을 뜻하지 않습니다.
