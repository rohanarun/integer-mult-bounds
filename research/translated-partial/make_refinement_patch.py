#!/usr/bin/env python3
"""Reproduce the parameter-only source patch against pinned PR21, not upstream.

Rohan Arun, with OpenAI Codex assistance; inherited attribution is retained.
"""
from difflib import unified_diff
from hashlib import sha256
from pathlib import Path
import json
import subprocess

ROOT=Path(__file__).resolve().parents[2]
BASE='5ba6cf0bfb68f2be8d15610e7972207c50254d6a'
FILES=['README.md','NOTICE','Makefile','docs/research/current-status.md',
       'research/translated-partial/README.md','research/translated-partial/verify.py',
       'research/translated-partial/make_refinement_patch.py',
       'research/translated-partial/refinement-source.json',
       'notes/translated-partial-note.tex','notes/translated-partial-assembly.tex',
       'tests/test_translated_partial.py']


def main():
    manifest=json.loads((ROOT/'research/translated-partial/refinement-source.json').read_text())
    assert manifest['base_commit']==BASE
    for path,digest in manifest['baseline_source_sha256'].items():
        original=subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
        assert sha256(original).hexdigest()==digest,path
    check=ROOT/'build/translated-refinement/pinned-patch-check'
    check.mkdir(parents=True,exist_ok=True)
    pieces=[]
    for path in FILES:
        result=subprocess.run(['git','show',BASE+':'+path],cwd=ROOT,capture_output=True)
        original=result.stdout.decode() if result.returncode==0 else ''
        current=(ROOT/path).read_text()
        dest=check/path
        dest.parent.mkdir(parents=True,exist_ok=True)
        if result.returncode==0:
            dest.write_text(original)
        elif dest.exists():
            dest.unlink()
        pieces.extend(unified_diff(original.splitlines(keepends=True),current.splitlines(keepends=True),
                                   fromfile='a/'+path if original else '/dev/null',tofile='b/'+path))
    patch=ROOT/'patches/translated-parameter-refinement.patch'
    patch.write_text(''.join(pieces))
    args=['git','apply','--directory='+str(check.relative_to(ROOT))]
    subprocess.run(args+['--check',str(patch)],cwd=ROOT,check=True)
    subprocess.run(args+[str(patch)],cwd=ROOT,check=True)
    assert all((check/p).read_bytes()==(ROOT/p).read_bytes() for p in FILES)
    print('PASS focused parameter patch against pinned PR21 '+BASE+'; '+str(len(FILES))+' source files')


if __name__=='__main__':main()
