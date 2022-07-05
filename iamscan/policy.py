from iamscan.commands import aws_commands
from uuid import uuid4
import os
import re


class Policy:

    def __init__(self):
        self.json = {}
        self.seperate_statements = False
        self.resource = '*'

    def update_policy(self, source_file_path):

        self.file_extension = os.path.splitext(source_file_path)[1]

        self.file_name = os.path.basename(source_file_path)

        self.code = self._read_file(source_file_path)
        
        if self.file_extension == '.js':
            self._parse_js()
        elif self.file_extension == '.py':
            self._parse_py()
        elif self.file_extension == '.sh':
            self._parse_sh() 


    def _read_file(self, path):

        script_file = open(path, 'r')

        code = script_file.readlines()

        script_file.close()

        commentless_code = []
        for line in code:
            if (line.replace(' ', '') + '--')[0] not in ('\n', '#') and (line.replace(' ', '') + '--')[0:2] != '//':
                commentless_code.append(line)
            
        commentless_code = ''.join(commentless_code).replace('\\\n', '').replace('  ','').split('\n')

        code = [line.lstrip() for line in commentless_code]
        
        if self.file_extension == '.js':
            multiline_comment = None
            commentless_code = []
            for line in code:
                if not multiline_comment and line == '/*':
                    multiline_comment = line
                elif multiline_comment and line.split(' ') and len(line.split(' ')[0]) > 1 and line.split(' ')[0][-2:]  == '*/':
                    multiline_comment = None
                elif not multiline_comment:
                    commentless_code.append(line)

        elif self.file_extension == '.py':
            multiline_comment = None
            commentless_code = []
            for line in code:
                if not multiline_comment and line in ('"""', "'''"):
                    multiline_comment = line
                elif multiline_comment == line:
                    multiline_comment = None
                elif not multiline_comment:
                    commentless_code.append(line)

        elif self.file_extension == '.sh':
            commentless_code = code

        return commentless_code


    
    def _append_to_policy(self, actions):

        if self.seperate_statements:

            cleaned_file_name = re.sub(r'\W+', '', self.file_name)

            if cleaned_file_name in [statement.get('Sid') for statement in self.json['Statement'] if statement.get('Sid')]:
                cleaned_file_name += str(uuid4())[-3:]

            self.json['Statement'].append({'Sid': cleaned_file_name, 'Effect': 'Allow', 'Action': sorted(list(set(actions))), 'Resource': self.resource})
        elif not self.json['Statement']:
            self.json['Statement'].append({'Effect': 'Allow', 'Action': sorted(list(set(actions))), 'Resource': self.resource})
        else:
            self.json['Statement'][0]['Action'] = sorted(list(set(self.json['Statement'][0]['Action'] + actions)))



    def _parse_sh(self):
        
            actions = []
            for line in self.code:
                
                line = ' '.join(line.split())
                
                for snippet in line.split('aws '):
                    
                    snippet = snippet.split(' ')
                    
                    if len(snippet) > 1 and aws_commands.get(snippet[0]):
                        
                        client = snippet[0]

                        command = snippet[1]

                        actions = actions + self._create_action(client, command)

            return self._append_to_policy(actions)

        
    def _parse_py(self):

        actions = []
        client_objects = {}
        for line in self.code:
            if 'boto3.client(' in line:

                client = line.split('boto3.client(')[1].split(')')[0].replace("'", '').replace('"', '').split(',')[0].strip()
                
                if aws_commands.get(client):
                
                    if line.split('boto3.client(')[1].split(')')[1] and line.split('boto3.client(')[1].split(')')[1][0] == '.':
                        command = line.split('boto3.client(')[1].split(')')[1][1:].split('(')[0].replace('_', '-')
                        
                        actions = actions + self._create_action(client, command)
                    
                    else:
                        
                        for item in reversed(line.split('boto3.client(')[0] \
                            .replace('=', '').replace(' =', '').replace(' = ', '').replace('= ', '').split(' ')):
                
                            if item:
                                client_objects[item] = client
                                break                       
            else:
                
                for client_object in client_objects.keys():
                    
                    if client_object + '.' in line:

                        client = client_objects[client_object]
                        
                        command = line.split(client_object + '.')[1].split('(')[0].replace('_', '-')

                        actions = actions + self._create_action(client, command)


        return self._append_to_policy(actions)

    

    def _parse_js(self):

        actions = []
        client_objects = {}
        for line in self.code:
            if 'new AWS.' in line:

                client = line.split('new AWS.')[1].split('(')[0].strip()
                
                client_lower = client.lower()
                
                client_hyphens = re.sub(r'(?<!^)(?=[A-Z])', '-', client).lower()
                
                if aws_commands.get(client_lower):
                    client = client_lower
                
                if aws_commands.get(client_hyphens):
                    client = client_hyphens
                
                if aws_commands.get(client):

                    snippet = line.split('new AWS.')[1].split(')')

                    if len(snippet) > 1 and len(snippet[1]) > 0 and snippet[1][0] == '.':
                        command = line.split('new AWS.')[1].split(')')[1][1:].split('(')[0]

                        actions += self._create_action(client, command.lower()) 
                        actions += self._create_action(client, re.sub(r'(?<!^)(?=[A-Z])', '-', command).lower())

                    else:

                        for item in reversed(line.split('new AWS.')[0] \
                            .replace('=', '').replace(' =', '').replace(' = ', '').replace('= ', '').split(' ')):

                            if item:
                                client_objects[item] = client
                                break                       
            else:

                for client_object in client_objects.keys():

                    if client_object + '.' in line:

                        client = client_objects[client_object]

                        command = line.split(client_object + '.')[1].split('(')[0]

                        actions += self._create_action(client, command.lower()) 
                        actions += self._create_action(client, re.sub(r'(?<!^)(?=[A-Z])', '-', command).lower())


        return self._append_to_policy(actions)



    def _create_action(self, client, command):

        actions = []

        special_cases = self._check_special_cases(client, command)

        if special_cases:
            return special_cases
        
        elif aws_commands[client].get(command):
            
            privileges = aws_commands[client][command]
            
            for privilege in privileges:
                
                actions.append(f'{client}:{privilege}')

        return actions



    def _check_special_cases(self, client, command):

        actions = []

        if client == 's3' and aws_commands['s3api'].get(command):

            for privilege in aws_commands['s3api'][command]:
                
                actions.append(f's3api:{privilege}')

        return actions
                            
    