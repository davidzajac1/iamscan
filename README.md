# iamscan

![Language](https://img.shields.io/badge/Language-Python-informational?style=flat)
![License](https://img.shields.io/badge/License-MIT-informational?style=flat)
![Version](https://img.shields.io/badge/Version-0.0.1-informational?style=flat)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

iamscan is a command line tool that reads your code and generates an AWS IAM policy with your needed permissions. Keeping track of AWS IAM permissions is annoying and timeconsuming. How often have you seen an update deployed to the cloud followed by `The provided execution role does not have permissions to call CreateSomething on SomeService`? This problem is either solved by manually reading through code or worse by blanketly opening up permissions to speed up the process (`lambda:*`, `s3:*`, etc.). IAM policies should always [grant least privilege](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html#grant-least-privilege) and iamscan can help you accomplish this.



### Installation

iamscan is easiest install via pip for Python versions 3.8+

```bash
$ pip install iamscan
```

### Supported File Types

- Currently iamscan can parse JavaScript Files, Python Files and Shell Scripts, thus the filename extension must be one of .js, .py or .sh
- For JavaScript files iamscan will recongize [AWS SDK for JavaScript v2](https://github.com/awsdocs/aws-javascript-developer-guide-v2/tree/main/doc_source) commands but will not recognize [AWS SDK for JavaScript v3](https://github.com/awsdocs/aws-sdk-for-javascript-v3/tree/main/doc_source) commands
- For Python files iamscan recognizes [`boto3`](https://github.com/boto/boto3) [Low Level Client](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/clients.html) commands but will not recognize [Resource](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/resources.html) based commands
- For Shell Scripts all [`aws-cli`](https://github.com/aws/aws-cli) commands are recognized

### Basic Usage

Call iamscan from the command line and pass in your file or a directory containing multiple files using the `--path` keyword

```bash
$ iamscan --path iamscan -p tests/py/awsec2instances.py
{
  "Version": "2012-10-17",      
  "Statement": [
    {
      "Effect": "Allow",        
      "Action": [
        "ec2:DescribeInstances",
        "ec2:RebootInstances",  
        "ec2:RunInstances",     
        "ec2:StartInstances",
        "ec2:StopInstances",
        "ec2:TerminateInstances"
      ],
      "Resource": "*"
    }
  ]
}
```

Passing in a directory will parse all files in the directory and add their permissions to the policy

```bash
$ iamscan --path iamscan -p tests/py/
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances",
        "ec2:RebootInstances",
        "ec2:RunInstances",
        "ec2:StartInstances",
        "ec2:StopInstances",
        "ec2:TerminateInstances",
        "lambda:CreateFunction",
        "lambda:DeleteFunction",
        "lambda:GetFunctionConfiguration",
        "lambda:UpdateFunctionCode",
        "lambda:UpdateFunctionConfiguration",
        "s3api:CreateBucket",
        "s3api:DeleteBucket",
        "s3api:DeleteObject",
        "s3api:ListBuckets",
        "s3api:ListObjectsV2"
      ],
      "Resource": "*"
    }
  ]
}
```

Use the `--output-format` to change the output to YAML for use with AWS CloudFormation

```bash
$ iamscan --path iamscan -p tests/py/awsec2instances.py --output-format yaml
Statement:
- Effect: Allow
  Action:
  - ec2:DescribeInstances
  - ec2:RebootInstances
  - ec2:RunInstances
  - ec2:StartInstances
  - ec2:StopInstances
  - ec2:TerminateInstances
  Resource: '*'
```

### Command Line Reference

| Command | Description |
| --- | --- |
| -p, --path | The path to a file or directory [REQUIRED] |
| -v, --version | Displays the current version |
| -h, --help | Displays the help message |
| -o, --output-format | The format of the output IAM policy (json \| yaml) defaults to json |
| -i, --id | An Id to add to the IAM policy |
| -r, --resource | One or multiple ARNs to add to the IAM Policy |
| -s, --seperate-statements | Usable when passing a directory as a path, seperates permissions into seperate Statements based on file |


### Contributing

The iamscan repo makes use of a [Makefile](Makefile) with [`pytest`](https://docs.pytest.org/) for local development. First create a virtual environment using the `requirements.txt` file then after any changes are made run `make test` to ensure all the tests pass. If you're change warrants tests add them to the [`test_code.py`](tests/test_code.py) file. After all tests pass please make a Pull Request into the `main` branch

### License

iamscan is released under the MIT License. See the bundled [LICENSE](LICENSE) file for details.

### Credits

- [alfonsof/aws-python-examples](https://github.com/alfonsof/aws-python-examples)
- [swoodford/aws](https://github.com/swoodford/aws)
- [awsdocs/aws-doc-sdk-examples](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/javascript/example_code)