# EC2 Image Builder send approval notifications before sharing AMIs

## Introduction

In some situations, you may be required to manually validate the [Amazon Machine Image (AMI)](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html) built from an [Amazon Elastic Compute Cloud (Amazon EC2)](https://aws.amazon.com/ec2/) Image Builder pipeline before sharing this AMI to other AWS accounts or to an AWS Organization. Currently, Image Builder provides an end-to-end pipeline that automatically shares AMIs after they’ve been built.

In this post, we will walk through the steps to enable approval notifications before AMIs are shared with other AWS accounts. Having a manual approval step could be useful if you would like to verify the AMI configurations before it is shared to other AWS accounts or an AWS Organization. This reduces the possibility of incorrectly configured AMIs being shared to other teams which in turn could lead to downstream issues if applications are installed using this AMI. This solution uses serverless resources to send an email with a link that automatically shares the AMI with the specified AWS accounts. Users select this link after they’ve verified that the AMI is built according to specifications.

![Architecture](./images/figure1-architecture-diagram.png)

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

