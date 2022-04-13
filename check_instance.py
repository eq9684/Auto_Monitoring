import json
import boto3

#遍历所有EC2 Instance，返回instance_id
def ec2():
    ec2instance = boto3.resource('ec2').instances.all()
    ec2_list = []
    for i in ec2instance:
        ec2_list.append(i.instance_id)
    print ("There are " + str(len(ec2_list)) + " EC2 instances")
    return ec2_list
    
#遍历所有RDS Instance，返回DBInstanceIdentifier
def rds():
    rdsinstance = boto3.client("rds").describe_db_instances()
    print ("There are " + str(len(list(rdsinstance))-1) + " databases")
    for i in range (0, len(list(rdsinstance))):
        print ("DB instance " + str(i) , end=" ")
        if (list(rdsinstance)[i] == "DBInstances"):
            print ("is " + rdsinstance["DBInstances"][i]["Engine"] + ", " + rdsinstance["DBInstances"][i]["DBInstanceIdentifier"] + ", " + rdsinstance["DBInstances"][i]["DBInstanceArn"])
    return True