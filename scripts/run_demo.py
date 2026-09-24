import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from lesson_design_agent.core import lesson_blueprint

plan=lesson_blueprint('Risk analysis','Analyze operational risk',90)
print('Topic:', plan['topic'])
print('Objective:', plan['objective'])
print('Sequence:', plan['sequence'])
print('Accessibility checks:', plan['accessibility_checks'])
