import json
import boto3

def ec2(instance_id):
    cloudwatch = boto3.client("cloudwatch")
    configureDB = boto3.client("dynamodb")
    
    '''
    #判断dynamoDB是否存在 (待加入：如果不存在则创建dynamoDB并写入Alarm参数定义)
    try: 
        Table =configureDB.describe_table(TableName="Automonitor_configuration")
        print (Table["Table"]["TableArn"])
    except Exception as error:
       print ("table not exist")
    
   #从dynamodb检索所有EC2 Alarm参数定义
    alarm_parameter_list=configureDB.query(
        TableName="Automonitor_configuration", 
        KeyConditionExpression='eventsource = :eventsource',
        ExpressionAttributeValues={
            ':eventsource': {'S': 'aws.ec2'}
        }
    )
    print (alarm_parameter_list["Items"])
    print ("Get "+ str(len(alarm_parameter_list["Items"])) + " results in configureDB")

    for i in (0, (len(alarm_parameter_list["Items"])-1)):
        print (alarm_parameter_list["Items"][i]["MetricName"])
    '''
    
    #Alarm参数定义（先用LIST定义，以后从dynamodb获取）
    alarm_parameter_CPU=["GreaterThanThreshold", 2, 2, "CPUUtilization","AWS/EC2", 60, "Average", 70, "Alarm when server CPU exceeds 70%", "Percent"]
    alarm_parameter_Memory=["GreaterThanThreshold", 2, 2, "mem_used_percent","CWAgent", 60, "Average", 70, "Alarm when server Memory used exceeds 70%", "Percent"]
    alarm_parameter_Disk=["GreaterThanThreshold", 2, 2, "disk_used_percent","CWAgent", 60, "Average", 10, "Alarm when server Disk used exceeds 70%", "Percent"]
    
    cloudwatch.put_metric_alarm(
            AlarmName="EC2-" + instance_id + "-" + alarm_parameter_CPU[3],
            #ComparisonOperator=json.loads(alarm_parameter_list)["Item"][0]["ComparisonOperator"],
            ComparisonOperator=alarm_parameter_CPU[0],
            EvaluationPeriods=alarm_parameter_CPU[1],
            DatapointsToAlarm=alarm_parameter_CPU[2],
            MetricName=alarm_parameter_CPU[3],
            Namespace=alarm_parameter_CPU[4],
            Period=alarm_parameter_CPU[5],
            Statistic=alarm_parameter_CPU[6],
            Threshold=alarm_parameter_CPU[7],
            ActionsEnabled=True,
            AlarmActions=[
                "arn:aws:sns:us-west-2:096454897560:Automonitor_raw_message"
            ],
            AlarmDescription=alarm_parameter_CPU[8],
            Dimensions=[
            {
                "Name": "InstanceId",
                "Value": instance_id
            },
            ],
            Unit=alarm_parameter_CPU[9]
        )
        
    cloudwatch.put_metric_alarm(
        AlarmName="EC2-" + instance_id + "-" + alarm_parameter_Memory[3],
        #ComparisonOperator=json.loads(alarm_parameter_list)["Item"][0]["ComparisonOperator"],
        ComparisonOperator=alarm_parameter_Memory[0],
        EvaluationPeriods=alarm_parameter_Memory[1],
        DatapointsToAlarm=alarm_parameter_Memory[2],
        MetricName=alarm_parameter_Memory[3],
        Namespace=alarm_parameter_Memory[4],
        Period=alarm_parameter_Memory[5],
        Statistic=alarm_parameter_Memory[6],
        Threshold=alarm_parameter_Memory[7],
        ActionsEnabled=True,
        AlarmActions=[
            "arn:aws:sns:us-west-2:096454897560:Automonitor_raw_message"
        ],
        AlarmDescription=alarm_parameter_Memory[8],
        Dimensions=[
        {
            "Name": "InstanceId",
            "Value": instance_id
        },
        ],
        Unit=alarm_parameter_Memory[9]
    )
        
    cloudwatch.put_metric_alarm(
        AlarmName="EC2-" + instance_id + "-" + alarm_parameter_Disk[3] + "-root",
        #ComparisonOperator=json.loads(alarm_parameter_list)["Item"][0]["ComparisonOperator"],
        ComparisonOperator=alarm_parameter_Disk[0],
        EvaluationPeriods=alarm_parameter_Disk[1],
        DatapointsToAlarm=alarm_parameter_Disk[2],
        MetricName=alarm_parameter_Disk[3],
        Namespace=alarm_parameter_Disk[4],
        Period=alarm_parameter_Disk[5],
        Statistic=alarm_parameter_Disk[6],
        Threshold=alarm_parameter_Disk[7],
        ActionsEnabled=True,
        AlarmActions=[
            "arn:aws:sns:us-west-2:096454897560:Automonitor_raw_message"
        ],
        AlarmDescription=alarm_parameter_Disk[8],
        Dimensions=[
        {
            "Name": "InstanceId",
            "Value": instance_id
        },
        {
            "Name": "path",
            "Value": "/"
        }
        ],
        Unit=alarm_parameter_Disk[9]
    )
    
    cloudwatch.put_metric_alarm(
        AlarmName="EC2-" + instance_id + "-" + alarm_parameter_Disk[3] + "-app",
        #ComparisonOperator=json.loads(alarm_parameter_list)["Item"][0]["ComparisonOperator"],
        ComparisonOperator=alarm_parameter_Disk[0],
        EvaluationPeriods=alarm_parameter_Disk[1],
        DatapointsToAlarm=alarm_parameter_Disk[2],
        MetricName=alarm_parameter_Disk[3],
        Namespace=alarm_parameter_Disk[4],
        Period=alarm_parameter_Disk[5],
        Statistic=alarm_parameter_Disk[6],
        Threshold=alarm_parameter_Disk[7],
        ActionsEnabled=True,
        AlarmActions=[
            "arn:aws:sns:us-west-2:096454897560:Automonitor_raw_message"
        ],
        AlarmDescription=alarm_parameter_Disk[8],
        Dimensions=[
        {
            "Name": "InstanceId",
            "Value": instance_id
        },
        {
            "Name": "path",
            "Value": "/app"
        }
        ],
        Unit=alarm_parameter_Disk[9]
    )
        
    return True