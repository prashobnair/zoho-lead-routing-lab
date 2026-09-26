import argparse
import json
from pathlib import Path
from routing import route_leads

def main():
    parser = argparse.ArgumentParser(description='Simulate fictional lead routing offline')
    parser.add_argument('fixture')
    args = parser.parse_args()
    try:
        data = json.loads(Path(args.fixture).read_text(encoding='utf-8'))
        print(json.dumps(route_leads(data['leads']), indent=2, sort_keys=True))
    except (KeyError, ValueError, OSError) as exc:
        parser.exit(1, f'Input error: {exc}\n')

if __name__ == '__main__':
    main()
