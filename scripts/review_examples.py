"""Reproduce the labeled worked example; this is not an empirical study."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from lesson_design_agent import core
outputs={'total minutes: 5+10+10+5': sum([5,10,10,5]), 'share of two 10-minute phases': 20/30}
result={'kind':'illustrative_calculation','note':'Illustrative time-budget arithmetic; not a scored lesson.','outputs':outputs}
(ROOT/'results/review_examples.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
