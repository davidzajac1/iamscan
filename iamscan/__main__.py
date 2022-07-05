import os
import sys
import yaml
import json
import argparse
from iamscan.policy import Policy
from iamscan import __version__

def main(args=None):

    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action='version', version=f'iamscan {__version__}')
    parser.add_argument('-p', '--path', type=str, required=True)
    parser.add_argument('-o', '--output-format', choices=['json', 'yaml'], type=str, required=False, default='json')
    parser.add_argument('-i', '--id', type=str, required=False)
    parser.add_argument('-r', '--resource', nargs='+', type=str, required=False, default='*')
    parser.add_argument('-s', '--seperate-statements', required=False, action='store_true', default=False)
    args = parser.parse_args()


    if os.path.isfile(args.path):

        file_extension = os.path.splitext(args.path)[1]

        if file_extension not in ('.js', '.py', '.sh'):
            raise TypeError(f'File extension {file_extension} is not supported. Only .js, .py and .sh are supported.')

        if args.seperate_statements:
            raise AttributeError('--seperate-statements flag only available when multple files are passed in path.')

        files = [args.path]

    elif os.path.isdir(args.path):

        files = []
        num_files = 0
        for r, d, f in os.walk(args.path):
            for file in f:
                if os.path.splitext(file)[1] in ('.js', '.py', '.sh'):
                    files.append(os.path.join(r, file))

                num_files += 1
                if num_files > 10000:
                    raise OverflowError('No more than 10,000 files allowed in path.')

    else:
        raise TypeError('--path must be valid system path to a file or directory.')


    policy = Policy()

    if args.id:
        policy.json['Id'] = args.id

    policy.json['Version'] =  '2012-10-17'

    policy.json['Statement'] = []

    if args.seperate_statements:
        policy.seperate_statements = True

    policy.resource = args.resource

    for file in files:

        policy.update_policy(file)

    if args.output_format == 'json':
        print(json.dumps(policy.json, indent=2))
    elif args.output_format == 'yaml':
        policy.yaml = yaml.dump(policy.json, sort_keys=False)
        print(policy.yaml)



if __name__ == "__main__":
    sys.exit(main())

