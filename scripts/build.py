"""Build evaluator files only; fail closed on unexpected or identifying content."""
import json,re,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TERMS=[bytes(v) for v in ((99,108,105,112),(99,99,105,112),(100,105,110,111),(112,114,111,118,105,100,101,114),(99,111,115,105,110,101))]

def audit(directory):
    directory=Path(directory).resolve();files=[]
    for path in directory.rglob('*'):
        if path.is_symlink():raise ValueError('Symbolic links are not allowed')
        if not path.is_file():continue
        rel=path.relative_to(directory)
        if str(rel) not in ('index.html','.nojekyll') and not (len(rel.parts)==2 and rel.parts[0]=='images' and path.suffix=='.png'):
            raise ValueError('Unexpected public file: '+str(rel))
        data=path.read_bytes()
        if any(term in data.lower() for term in TERMS) or (path.suffix!='.png' and re.search(rb'[a-zA-Z]:[\\/]',data)):raise ValueError('Forbidden identifying content: '+str(rel))
        if path.suffix=='.png' and not data.startswith(b'\x89PNG\r\n\x1a\n'):raise ValueError('Invalid image')
        files.append(str(rel))
    html=(directory/'index.html').read_text(encoding='utf-8')
    match=re.search(r'window\.VRF_SESSION=(.*?);</script>',html,re.S)
    if not match:raise ValueError('Missing anonymous evaluation session')
    session=json.loads(match.group(1))
    if set(session)!={'schema','session_id','synthetic','rating_scale','tasks'} or session['rating_scale']!={'min':1,'max':5}:raise ValueError('Unexpected session metadata or rating scale')
    expected={'index.html','.nojekyll'}
    for task in session['tasks']:
        if set(task)!={'id','query_image','candidate_image','query_id','candidate_id','group_ids'}:raise ValueError('Unexpected task metadata')
        for field in ('query_image','candidate_image'):
            image=task[field]
            if not re.fullmatch(r'images/[a-f0-9]{64}\.png',image) or not (directory/image).is_file():raise ValueError('Missing or unsafe relative image')
            expected.add(image)
            # Relative assets must remain under a repository Pages subpath.
            from urllib.parse import urljoin
            if not urljoin('https://example.github.io/repository/',image).startswith('https://example.github.io/repository/images/'):
                raise ValueError('Invalid repository base path')
    if {p.replace('\\','/') for p in files}!=expected:raise ValueError('Unreferenced or missing public files')
    return {'public_files':len(files),'images':len(expected)-2,'pairs':len(session['tasks']),'blind_scan':'passed','repository_base_path':'passed'}

def build(root=ROOT):
    root=Path(root).resolve();source=root/'site';target=root/'dist'
    audit(source)
    if target.is_symlink():raise ValueError('Unsafe dist directory')
    target.mkdir(exist_ok=True)
    for path in source.rglob('*'):
        if path.is_file():
            destination=target/path.relative_to(source);destination.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,destination)
    result=audit(target)
    if {str(p.relative_to(source)) for p in source.rglob('*') if p.is_file()}!={str(p.relative_to(target)) for p in target.rglob('*') if p.is_file()}:raise ValueError('Stale dist files')
    return result

if __name__=='__main__':print(json.dumps(build(),sort_keys=True))
