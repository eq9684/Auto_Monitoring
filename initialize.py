import json
import boto3
import create_alarm

def ec2():
    #初始化创建所有EC2实例的Alarm
    print ("execute initialize.ec2()")
    ec2instance = boto3.resource('ec2').instances.all()
    for i in ec2instance:
        print (i.instance_id)
        alarm = boto3.resource("cloudwatch").Alarm("EC2-" + i.instance_id + "-CPUUtilization")
        
        #检查EC2 Instance的CloudWatch Alarm是否存在
        try:
            alarm_arn = alarm.alarm_arn
            print ("alarm_arn is " + alarm_arn)
        except Exception as error:
            alarm_arn = None
            #print (error, end=". ")
            print ("alarm_arn is None, Create EC2 Alarm for " + i.instance_id)
            create_alarm.ec2(i.instance_id)

    return True