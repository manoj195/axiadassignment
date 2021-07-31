import boto3

ec2 = boto3.resource('ec2')
vpc = ec2.create_vpc(CidrBlock='172.16.0.0/16')
vpc.create_tags(Tags=[{"Key": "Name", "Value": "axiodvpc"}])

vpc.wait_until_available()
# create an internet gateway and attach it to VPC
internetgateway = ec2.create_internet_gateway()
vpc.attach_internet_gateway(InternetGatewayId=internetgateway.id)
# create a route table and a public route
routetable = vpc.create_route_table()
route = routetable.create_route(DestinationCidrBlock='0.0.0.0/0', GatewayId=internetgateway.id)
pubsubnet = ec2.create_subnet(CidrBlock='172.16.1.0/24', VpcId=vpc.id)
routetable.associate_with_subnet(SubnetId=pubsubnet.id)
privsubnet  = ec2.create_subnet(CidrBlock='172.16.2.0/24', VpcId=vpc.id)
#privroutetable = vpc.create_route_table()

# Create a security group and allow SSH inbound rule through the VPC
securitygroup = ec2.create_security_group(GroupName='axiodsg', Description='only allow SSH traffic', VpcId=vpc.id)
securitygroup.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=22, ToPort=22)
securitygroup.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=80, ToPort=80)
dbsecuritygroup = ec2.create_security_group(GroupName='dbsecuritygroup', Description='DB security group', VpcId=vpc.id)
dbsecuritygroup.authorize_security_group_ingress( 
    GroupName=axiodsg, 
    IpPermissions=[
        {'IpProtocol': 'tcp', 
        'FromPort': 3306, 
        'ToPort': 3306, 
        'UserIdGroupPairs': [{ 'GroupName': dbsecuritygroup }] }
    ],
)

# create a file to store the key locally

outfile = open('ec2-keypair.pem', 'w')

# call the boto ec2 function to create a key pair
key_pair = ec2.create_key_pair(KeyName='ec2-keypair')

# capture the key and store it in a file
KeyPairOut = str(key_pair.key_material)
outfile.write(KeyPairOut)


asgclient = boto3.client('autoscaling')

response = asgclient.create_launch_configuration(
    LaunchConfigurationName='axiodlc',
    ImageId='ami-08bc0dd666f8de033',
    KeyName='ec2-keypair',
    InstanceType='t2.micro',
    InstanceMonitoring={
        'Enabled': True
    }
)




