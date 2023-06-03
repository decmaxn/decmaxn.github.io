# Homebrew Tap


## Homebrew Tap
Currently I have only 3 taps
```bash
 % brew tap
homebrew/cask
homebrew/cask-versions
homebrew/core
```
When searching, the results are from those 3 taps. 
```bash
 % brew search aws-sam-cli
==> Formulae
aws-sam-cli                                                                             aws-sso-cli

==> Casks
aws-vpn-client
```
Let's add another Tap, it's from AWS.
```bash
% brew tap aws/tap
Running `brew update --auto-update`...
% brew tap
aws/tap
homebrew/cask
homebrew/cask-versions
homebrew/core
```
When you search again, now it shows more results from the new tap, they have aws/tap as prefix.
```bash
% brew search aws-sam-cli
==> Formulae
aws-sam-cli                                               aws/tap/aws-sam-cli-beta-cdk                              aws/tap/aws-sam-cli-rc
aws/tap/aws-sam-cli                                       aws/tap/aws-sam-cli-nightly                               aws-sso-cli

==> Casks
aws-vpn-client
```
Find all packages included in a particular tap
```bash
 % brew search --formula aws/tap
==> Formulae
aws/tap/aws-ddbsh                  aws/tap/aws-simple-ec2-cli         aws/tap/ec2-instance-selector      aws/tap/eksdemo                    aws/tap/smithy-cli
aws/tap/aws-sam-cli                aws/tap/cbmc-starter-kit           aws/tap/ec2-metadata-mock          aws/tap/emr-on-eks-custom-image    aws/tap/xray-daemon
aws/tap/aws-sam-cli-beta-cdk       aws/tap/cbmc-viewer                aws/tap/ec2-spot-interrupter       aws/tap/k8s-tools                  aws-okta
aws/tap/aws-sam-cli-nightly        aws/tap/container-tools            aws/tap/eks-anywhere               aws/tap/lightsailctl
aws/tap/aws-sam-cli-rc             aws/tap/copilot-cli                aws/tap/eks-node-viewer            aws/tap/qldbshell
```
