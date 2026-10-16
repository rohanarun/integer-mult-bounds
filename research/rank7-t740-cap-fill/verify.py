#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Registered check: a T740 allocation of PR #2979's unchanged words that attains their fixed-capacity packing cap.

Standard library only (Python 3.10+, assertions enabled); about two to three minutes on one core.
  1. Live input pins: every PR2979 file used has the SHA-256 recorded in SOURCES.json.
  2. Providers: PR2979's two words re-derive the provider registry (per-helper widths, local paid profile, 91 private
     buffers) with PR2979's vendored frame accounting (vendor/preload_move.py frame_report).
  3. Allocation: lift.py rebuilds the T740 ORDER/DISPATCH/FILL from PR2979's literal T74 allocation and
     allocation/RELOCATIONS.json; the canonical payload SHA-256 values equal allocation/EXPECTED.json.
  4. Owners: PR2979's vendored owner engine (PR2839/PR2751 lineage) checks all 2,717,280 roles at T740: helper
     identities, literal source windows, same-call family exclusions, capacities, masks, compact prefixes, the complete
     paid profile (= allocation/PROFILE.json) and the rank-mass identity. Physical stock = live + 408 + 8 + 91 + 2.
  5. Optimal face: PR2979's Fractions-only cap certificate (certificates/RELAX-CAP.json, re-verified with its
     relax_exact.py) gives the cap bracket; exact row multipliers show that [9,9,9]@32, [9,9,9,9,9]@48 and []@48 have
     fixed counts 93/4, 1341/20 and 7619/20 per replica on the optimal face (so an integral optimum needs 20 | T: none at
     T74 or any T < 20, one is possible at T740); the literal idle histogram equals exactly 740 x the optimal basic idle
     profile; every literal bin pattern has identically zero reduced cost; the exact root bracket of the literal profile
     equals the cap bracket.
  6. Moment: PR2917/PR2979's independent dyadic moment auditor with its authenticated baseline re-pinned to PR2979's
     headline (tools/audit_allocation_moment.py): strict gain.
  7. The claim file (CLAIM.json) agrees with all of the above.
Failure controls are in controls.py (separately registered).
Rohan Arun, with substantial AI assistance (Anthropic Claude). Apache-2.0.
"""
import argparse
import collections
import hashlib
import json
import shutil
import sys
import tempfile
import time
import types
from fractions import Fraction as Q
from pathlib import Path

PKG = Path(__file__).resolve().parent
SRC = PKG.parent / 'rank7-joint-endframes'
ROOT = PKG.parent.parent
sys.path.insert(0, str(PKG))
import lift as L  # noqa: E402

T, BUFFERS, HELPERS, CENTRES, GUARDS = 740, 91, 408, 8, 2


def need(condition, message):
    if not condition:
        raise AssertionError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(name, path):
    module = types.ModuleType(name)
    module.__file__ = str(path)
    sys.modules[name] = module
    exec(compile(Path(path).read_bytes(), str(path), 'exec'), module.__dict__)
    return module


def check_pins():
    sources = L.read(PKG / 'SOURCES.json')
    inputs = [f for f in sources['files'] if f['usage'] == 'input']
    need(len(inputs) >= 17, 'pinned PR2979 inputs')
    for f in inputs:
        need(sha(ROOT / f['path']) == f['sha256'], 'live input pin ' + f['path'])
    return {f['path']: f['sha256'] for f in inputs}


def derive_providers():
    frames = load('rank7_frames_t740', SRC / 'vendor/preload_move.py')
    derived = {}
    for tag, pid in (('base', 'gauge44'), ('extra', 'extra')):
        word = L.read(SRC / f'data/WORD-{tag}.json.gz')
        profile, inventory = frames.frame_report(word)
        need(profile == word['report']['local_profile'] and inventory == word['report']['width_inventory'], 'frame report ' + tag)
        helpers = sorted(set(range(224, 704)) - set(word['removed']))
        widths = [len(word['helper_final'].get(str(h), [0] * 9)) - len(word['start_extra'].get(str(h), [])) for h in helpers]
        need(len(helpers) == HELPERS and len(word['centers']) == CENTRES and sorted(set(widths)) == [4, 5, 6, 7, 8, 9], 'helpers ' + tag)
        buffers = {r for gate in word['cleanup'] for r in (gate[1:3] if gate[0] == 'add' else gate[1:2]) if r >= 704}
        need(buffers == {704 + int(h) for h in word['helper_final']} and len(buffers) == BUFFERS, 'private buffers ' + tag)
        derived[pid] = {'widths': widths, 'actual_paid_profile': {int(k): v for k, v in profile.items()}}
    registry = L.read(SRC / 'allocation/PROVIDERS.json')
    need({k: {'widths': v['widths'], 'actual_paid_profile': {int(r): n for r, n in v['actual_paid_profile'].items()}}
          for k, v in registry.items()} == derived, 'PR2979 provider registry = its actual words')
    return derived


def optimal_face(providers):
    """Re-verify PR2979's cap certificate and return (cap_lo, cap_hi, idle_per_replica, tight(cap, counts) predicate)."""
    sys.path.insert(0, str(SRC / 'tools'))
    import relax as X
    import relax_exact as RE
    cert = L.read(SRC / 'certificates/RELAX-CAP.json')
    loc = {int(k): v for k, v in cert['local_per_call'].items()}
    inv = {int(k): v for k, v in cert['inventory_per_call'].items()}
    for pv in providers.values():
        need(pv['actual_paid_profile'] == loc and dict(collections.Counter(pv['widths'])) == inv, 'certificate = actual words')
    r = RE.verify_basis(cert['local_per_call'], cert['inventory_per_call'], cert['basis_patterns'])
    need(r['status'] == 'PASS_EXACT_RELAXATION_CAP' and r['patterns'] == 2551 and r['tight_patterns'] == 12, 'cap certificate')
    need((Q(r['cap_lower']), Q(r['cap_upper'])) == (Q(cert['cap_lower']), Q(cert['cap_upper'])), 'cap bracket')
    # exact reduced-cost rows (same algebra as relax_exact.verify_basis): tight <=> identically zero
    widths, caps = sorted(inv), sorted(X.BINS)
    basis = [RE.pattern_of(e, widths, X.BINS) for e in cert['basis_patterns']]
    cols = [X.column(p, caps, widths) for p in basis]
    Binv = X.rat_inverse([[cols[k][i] for k in range(len(basis))] for i in range(len(cols[0]))])
    Y = []
    for j in range(len(cols[0])):
        row = collections.Counter()
        for k, p in enumerate(basis):
            if p[2] and Binv[k][j]:
                row[p[2]] += Binv[k][j]
        Y.append(row)

    def tight(cap, ws):
        counts = tuple(list(ws).count(w) for w in widths)
        idle = cap - sum(ws)
        a = X.column((cap, counts, idle), caps, widths)
        coeff = collections.Counter({idle: Q(1)} if idle else {})
        for j, aj in enumerate(a):
            for k, v in Y[j].items():
                coeff[k] -= aj * v
        return not any(v != 0 for v in coeff.values())
    # Why T740: on the optimal face some pattern counts are fixed. Find row multipliers lam with lam . A = unit vector on the
    # tight columns (exact Gaussian elimination); then that count equals lam . rhs per replica for every optimal solution.
    tight_list = [(cap, counts) for cap, counts, idle in X.patterns(X.BINS, widths)
                  if tight(cap, [w for w, k in zip(widths, counts) for _ in range(k)])]
    need(len(tight_list) == 12, 'twelve tight patterns')
    rhs = [Q(X.BINS[c]) for c in caps] + [9 * Q(inv[w]) for w in widths]
    cols = [X.column((cap, counts, cap - sum(w * k for w, k in zip(widths, counts))), caps, widths) for cap, counts in tight_list]

    def fixed_count(index):
        # solve sum_i lam_i * cols[j][i] = [j == index] for all tight j (overdetermined; must be consistent)
        n = len(rhs)
        rows = [[Q(cols[j][i]) for i in range(n)] + [Q(int(j == index))] for j in range(len(cols))]
        piv, r = [], 0
        for col in range(n):
            k = next((k for k in range(r, len(rows)) if rows[k][col] != 0), None)
            if k is None:
                continue
            rows[r], rows[k] = rows[k], rows[r]
            rows[r] = [v / rows[r][col] for v in rows[r]]
            for k2 in range(len(rows)):
                if k2 != r and rows[k2][col] != 0:
                    rows[k2] = [a - rows[k2][col] * b for a, b in zip(rows[k2], rows[r])]
            piv.append(col)
            r += 1
        if any(all(v == 0 for v in row[:n]) and row[n] != 0 for row in rows):
            return None
        lam = [Q(0)] * n
        for k, col in enumerate(piv):
            lam[col] = rows[k][n]
        return sum(l * b for l, b in zip(lam, rhs))
    name = lambda cap, counts: '%d:%s' % (cap, '+'.join(str(w) for w, k in zip(widths, counts) for _ in range(k)) or 'empty')
    fixed = {name(*tight_list[j]): fixed_count(j) for j in range(len(tight_list))}
    fixed = {k: v for k, v in fixed.items() if v is not None}
    need(fixed.get('32:9+9+9') == Q(93, 4) and fixed.get('48:9+9+9+9+9') == Q(1341, 20) and fixed.get('48:empty') == Q(7619, 20), 'counts fixed on the optimal face')
    need(all((T * v).denominator == 1 for v in fixed.values()) and any((74 * v).denominator != 1 for v in fixed.values()), 'integral at T740, not at T74')
    need(all(any((t * v).denominator != 1 for v in fixed.values()) for t in range(1, 20)), 'no integral optimum for T < 20')
    optimal_face.fixed = {k: str(v) for k, v in sorted(fixed.items())}
    return Q(r['cap_lower']), Q(r['cap_upper']), {int(k): Q(v) for k, v in r['idle_per_replica'].items()}, tight


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', type=Path, help='optional fresh directory: writes the T740 allocation and RESULT.json')
    args = ap.parse_args()
    if not __debug__:
        raise SystemExit('refusing python -O: this checker relies on assertions')
    start = time.monotonic()
    pins = check_pins()
    providers = derive_providers()
    engine = load('owners2979_t740', SRC / 'allocation/vendor/independent_owners.py')
    plan, template = L.read(SRC / 'allocation/vendor/PLAN.json.gz'), L.read(SRC / 'allocation/vendor/TEMPLATE.json.gz')
    relocations = L.read(PKG / 'allocation/RELOCATIONS.json')
    expected = L.read(PKG / 'allocation/EXPECTED.json')
    claimed = {int(k): v for k, v in L.read(PKG / 'allocation/PROFILE.json').items()}
    need(len(relocations) == expected['relocations'] == 332, 'relocation count')
    Tn, order, dispatch, fill, touched = L.build(SRC / 'allocation', relocations, providers)
    need(Tn == T and len(touched) == expected['touched_bins'], 'T740 and touched bins')
    payload = {'ORDER.json': L.digest(order), 'DISPATCH.json': L.digest(dispatch), 'FILL.json.gz': L.digest(fill),
               'PROFILE.json': L.digest({str(r): n for r, n in sorted(claimed.items())})}
    need(payload == expected['payload_sha256'], 'canonical T740 payloads')
    d = {(s, r): p for s, r, p in dispatch}
    need(len(d) == len(dispatch) == 9 * T, 'unique literal dispatch')
    t0 = time.monotonic()
    result, win, _ = engine.check(T, order, fill, d, claimed, plan, template, providers)
    engine_seconds = time.monotonic() - t0
    need(result['roles'] == 9 * T * HELPERS == 2717280 and result['rank_mass'] == 65088 * T, 'complete roles and mass')
    physical = result['live'] + HELPERS + CENTRES + BUFFERS + GUARDS
    need(physical == expected['physical'] == 663549, 'physical stock')
    # optimal face
    cap_lo, cap_hi, idle_rep, tight = optimal_face(providers)
    idle = {int(k): v for k, v in result['idle'].items()}
    need(idle == {r: T * n for r, n in idle_rep.items()}, 'literal idle histogram = 740 x optimal basic idle profile')
    width = {pid: pv['widths'] for pid, pv in providers.items()}
    contents = collections.defaultdict(list)
    for t, h, o, c, p, z in fill['rows']:
        contents[o, c, p].append(width[d[tuple(order[t])]][h])
    census = collections.Counter()
    for (o, c), (cap, lo, hi) in win.items():
        for p in range(112):
            census[cap, tuple(sorted(contents.get((o, c, p), [])))] += 1
    need(all(tight(cap, ws) for cap, ws in census), 'every literal bin pattern is on the optimal face')
    sys.path.insert(0, str(SRC / 'tools'))
    import root as R
    lo, hi = R.kappa_from_profile(claimed, T)
    need((lo, hi) == (cap_lo, cap_hi), 'exact root bracket of the literal profile = fixed-capacity cap bracket')
    # baseline: PR2979's literal T74 profile and claim
    claim2979 = L.read(SRC / 'CLAIM.json')
    base_profile = {int(k): v for k, v in L.read(SRC / 'allocation/PROFILE.json').items()}
    b_lo, b_hi = R.kappa_from_profile(base_profile, 74)
    need(Q(claim2979['kappa']) < b_lo < b_hi < cap_lo, 'PR2979 literal root below the cap')
    # independent dyadic moment auditor, baseline re-pinned to PR2979's headline
    moment = load('moment_t740', PKG / 'tools/audit_allocation_moment.py')
    with tempfile.TemporaryDirectory() as tmp:
        cand, base = Path(tmp) / 'candidate', Path(tmp) / 'baseline'
        cand.mkdir()
        base.mkdir()
        (cand / 'ORDER.json').write_bytes(L.canonical(order))
        (cand / 'PROFILE.json').write_bytes(L.canonical({str(r): n for r, n in sorted(claimed.items())}))
        for name, src in (('CLAIM.json', SRC / 'CLAIM.json'), ('ORDER.json', SRC / 'allocation/ORDER.json'), ('PROFILE.json', SRC / 'allocation/PROFILE.json')):
            shutil.copyfile(src, base / name)
        audit = moment.run(cand, base)
    need(audit['status'] == 'PASS_SEPARATE_EXACT_RATIONAL_FRONTIER_MOMENT', 'moment auditor')
    target = Q(audit['target'])
    need(Q(audit['previous']) == Q(claim2979['kappa']) < target < lo, 'strict gain over the PR2979 headline')
    claim = L.read(PKG / 'CLAIM.json')
    need(Q(claim['kappa']) == target and Q(claim['complex_lower']) == Q(audit['outer_endpoint']), 'claimed headline')
    need(Q(claim['gain_over_pr2979']) == target - Q(claim2979['kappa']), 'claimed gain')
    need((Q(claim['root_lower']), Q(claim['root_upper'])) == (lo, hi) == (Q(claim['fixed_inventory_cap']['cap_lower']), Q(claim['fixed_inventory_cap']['cap_upper'])), 'claimed root = cap')
    need({int(k): v for k, v in claim['profile'].items()} == claimed and claim['replicas'] == T and claim['physical_families'] == physical, 'claimed profile/T/physical')
    out = dict(status='PASS_RANK7_T740_CAP_FILL', T=T, calls=9 * T, roles=result['roles'], relocations=len(relocations),
               touched_bins=len(touched), physical=physical, idle=result['idle'], profile=result['profile'],
               pattern_census={'%d:%s' % (cap, '+'.join(map(str, ws)) or 'empty'): n for (cap, ws), n in sorted(census.items())},
               root_lower=str(lo), root_upper=str(hi), cap_lower=str(cap_lo), cap_upper=str(cap_hi), fixed_on_optimal_face_per_replica=optimal_face.fixed,
               pr2979_literal_root=[str(b_lo), str(b_hi)], target=audit['target'], target_decimal=audit['target_decimal'],
               gain_over_pr2979=audit['gain'], gain_decimal=audit['gain_decimal'], payload_sha256=payload, input_sha256=pins,
               engine_seconds=round(engine_seconds, 1), seconds=round(time.monotonic() - start, 1),
               scope='Finite literal T740 owner geometry, paid profile and exact moment for PR2979\'s unchanged words; '
                     'PR2979\'s word/native checks are inherited unchanged; complete admission/outer release at T740 is separate.')
    if args.work:
        work = args.work.resolve()
        need(not work.exists() and not work.is_relative_to(PKG), 'fresh work directory outside the package')
        L.write(work / 'allocation', T, order, dispatch, fill, claimed)
        (work / 'RESULT.json').write_text(json.dumps(out, sort_keys=True, indent=1) + '\n')
    print(json.dumps({k: out[k] for k in ('status', 'T', 'roles', 'relocations', 'physical', 'idle', 'target_decimal', 'gain_decimal', 'seconds')}))
    print('PASS_RANK7_T740_CAP_FILL', audit['target_decimal'])


if __name__ == '__main__':
    main()
