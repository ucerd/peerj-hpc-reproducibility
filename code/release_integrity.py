"""Build or verify the exact public release inventory (standard library only)."""
from pathlib import Path
import hashlib
import json
import argparse

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {'MANIFEST.json', 'SHA256SUMS.txt'}


def inventory(root=ROOT):
    files = []
    for p in sorted(root.rglob('*')):
        rel = p.relative_to(root)
        if any(x in {'.git', '__pycache__', '.pytest_cache', '.DS_Store'} for x in rel.parts):
            continue
        if p.is_symlink():
            raise ValueError(f'Symlink not permitted in release: {rel}')
        if not p.is_file() or rel.as_posix() in EXCLUDED or p.suffix in {'.pyc', '.pyo'}:
            continue
        blob = p.read_bytes()
        files.append({'path': rel.as_posix(), 'sha256': hashlib.sha256(blob).hexdigest(), 'bytes': len(blob)})
    return files


def manifest(root=ROOT):
    return {'package': 'PeerJ university HPC design-framework reproducibility',
            'version': (root/'VERSION').read_text().strip(),
            'prepared_date': '2026-11-22',
            'verification_semantics': 'Illustrative calculations and source-table arithmetic; not independent field evaluation or raw benchmark rerun',
            'count_35_sources': 35, 'count_25_requirements': 25,
            'source_specific_cluster_records_conflict': True,
            'files': inventory(root)}


def checksum_text(m):
    return ''.join(f"{f['sha256']}  {f['path']}\n" for f in m['files'])


def verify(root=ROOT):
    actual = manifest(root)
    declared = json.loads((root/'MANIFEST.json').read_text())
    if actual != declared:
        raise ValueError('Manifest mismatch: missing, additional or modified release files')
    if (root/'SHA256SUMS.txt').read_text() != checksum_text(actual):
        raise ValueError('SHA256SUMS.txt differs from manifest')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--write', action='store_true', help='Regenerate integrity metadata after intentional changes')
    args = p.parse_args()
    if args.write:
        m = manifest()
        (ROOT/'MANIFEST.json').write_text(json.dumps(m, indent=2)+'\n')
        (ROOT/'SHA256SUMS.txt').write_text(checksum_text(m))
    verify()
    print('PASS: complete release inventory and SHA-256 digests')


if __name__ == '__main__':
    main()
