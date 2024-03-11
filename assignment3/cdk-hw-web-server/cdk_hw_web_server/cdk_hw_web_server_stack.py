import os.path

from aws_cdk.aws_s3_assets import Asset as S3asset

from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_rds as rds,
    aws_cdk as cdk
    # aws_sqs as sqs,
)

from constructs import Construct

dirname = os.path.dirname(__file__)

class CdkHwWebServerStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, cdk_hw_vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        # Instance Role and SSM Managed Policy
        InstanceRole = iam.Role(self, "InstanceSSM", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))

        InstanceRole.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))
        
        # Create an EC2 instance
        cdk_hw_web_instance1 = ec2.Instance(self, "cdk_hw_web_instance1", vpc=cdk_hw_vpc,
                                            instance_type=ec2.InstanceType("t2.micro"),
                                            machine_image=ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2),
                                            role=InstanceRole)
                                            
        cdk_hw_web_instance2 = ec2.Instance(self, "cdk_hw_web_instance2", vpc=cdk_hw_vpc,
                                            instance_type=ec2.InstanceType("t2.micro"),
                                            machine_image=ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2),
                                            role=InstanceRole)
                                            
        #creating the RDS instance with the MYSQL engine with private subnet group
        my_rds_db = rds.DatabaseInstance(self, "mySQLDB",
                                        engine=rds.DataBaseInstanceEngine.MYSQL,
                                        vpc=cdk_hw_vpc,
                                        vpc_subnets=ec2.SubnetSelection(
                                            subnet_type=ec2.SubnetType.PRIVATE),
                                        port=3306,
                                        removal_policy=cdk.RemovalPolicy.DESTROY
                                        )


        
        # Allow inbound HTTP traffic in security groups for both of the web servers launched on the public subnets
        cdk_hw_web_instance1.connections.allow_from_any_ipv4(ec2.Port.tcp(80))
        cdk_hw_web_instance2.connections.allow_from_any_ipv4(ec2.Port.tcp(80))
        
        # Allow inbound to RDS instance to only web servers' security group
        my_rds_db.connections.allow_from_any_ipv4(ec2.Port.tcp(3306))
