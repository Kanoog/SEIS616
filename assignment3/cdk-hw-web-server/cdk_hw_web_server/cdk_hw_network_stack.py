import os.path

#from aws_cdk.aws_s3_assets import Asset as s3Asset

from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam
    # aws_sqs as sqs,
)
from constructs import Construct

class CdkHwNetworkServerStack(Stack):
    
    @property
    def vpc(self):
        return self.cdk_hw_vpc

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        
    
        # creating the VPC with public and private subnet in each of the two AZ
        self.cdk_hw_vpc = ec2.Vpc(self, "cdk_hw_vpc", 
                            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
                            max_azs = 2,
                            subnet_configuration=[{ec2.SubnetConfiguration(name="PublicSubnet01",subnet_type=ec2.SubnetType.PUBLIC)},
                                                {ec2.SubnetConfiguration(name="PrivateSubnet01",subnet_type=ec2.SubnetType.PRIVATE)}]
        )
    
