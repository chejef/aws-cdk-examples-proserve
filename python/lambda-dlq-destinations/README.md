# Welcome to your CDK Python project!


The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project. The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory. To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth 
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

# Create and destroy commands for design pattern 1

$ cdk deploy SQSDLQStock

$ cdk destroy SQSDLQStock

# Create and destroy commands for design pattern 2

$ cdk deploy LambdaDlqStack

$ cdk destroy LambdaDlqStack

# Create and destroy commands for design pattern 3

$ cdk deploy LambdaDestinationDlqStack

$ cdk destroy LambdaDestinationDlqStack


Enjoy!
