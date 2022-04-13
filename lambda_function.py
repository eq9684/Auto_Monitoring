import json
import boto3
#import os
import initialize
import create_alarm

def lambda_handler(event, context):
    event_source = event["source"]
    instance_id = event["detail"]["instance-id"]
    instance_status = event["detail"]["state"]
    cloudwatch = boto3.client("cloudwatch")
    print (event_source + ": " + instance_id + " is " + instance_status)
    result = ""
    
    #初始化，遍历所有EC2 Instance，并创建Alarm
    if (event_source == "aws.ec2.init"):
        initialize.ec2()
    else:
        alarm = boto3.resource("cloudwatch").Alarm("EC2-" + instance_id + "-CPUUtilization")
        #检查EC2 Instance的CloudWatch Alarm是否存在
        try:
            alarm_arn = alarm.alarm_arn
            print ("alarm_arn is " + alarm_arn)
        except Exception as error:
            alarm_arn = None
            #print (error, end=". ")
            print ("alarm_arn is None")
    
        #进行相应的处理操作
        if (instance_status == "running") and (alarm_arn is None):
            print ("Create EC2 Alarm for " + instance_id)
            create_alarm.ec2(instance_id)
            result = "Alarm created"
        elif (instance_status == "terminated") and (alarm_arn is not None):
            print ("Delete EC2 Alarm for " + instance_id)
            cloudwatch.delete_alarms(
                AlarmNames=["EC2-" + instance_id + "-CPUUtilization"],
            )
            result = "Alarm deleted"
        else:
            #print ("No action needed")
            result =  "No action"
    
    
    '''
    #遍历所有RDS Instance
    check_instance.rds()
    '''
        
    return {
        "result": result,
        #"statusCode": json.loads(os.environ["METRICS_LIST"])["metrics"][0]
    }
