import json
import base64
import datetime
#1. import boto3
import boto3

#2. Create client connection with Bedrock and S3 Services – Link
client_bedrock = boto3.client('bedrock-runtime')
client_s3 = boto3.client('s3')

print(boto3.__version__)

def lambda_handler(event, context):
#3. Store the input data (prompt) in a variable
    input_prompt = event['prompt']
    print(input_prompt)
    
#4. Create a Request Syntax - Details from console and documentation(JSON object) - Link
    response_bedrock = client_bedrock.invoke_model(
        modelId = 'amazon.titan-image-generator-v1',
        contentType = 'application/json',
        accept = 'application/json',
        body = json.dumps ({"taskType": "TEXT_IMAGE", "textToImageParams": {"text": input_prompt } }))
    print(response_bedrock)

#5. 5a. Retrieve from Dictionary, 5b. Convert Streaming Body to Byte using json load 5c. Print
    response_bedrock_byte = json.loads(response_bedrock['body'].read())
    print(response_bedrock_byte)

#6. 6a. Retrieve data with artifact key, 6b. Import Base 64, 6c. Decode from Base64 - Link
    image_data = response_bedrock_byte['images'][0]
    base64_image = image_data.encode('utf-8')
    decoded_image = base64.b64decode(base64_image)
    print(decoded_image)
    print(type(decoded_image))
#7. 7a. Upload the File to S3 using Put Object Method – Link 7b. Import datetime 7c.# Generate the image name to be stored in S3 - Link
    poster_name = 'poster' + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '.png'
    response_s3 = client_s3.put_object(
    Body=decoded_image, 
    Bucket='mvyposterdesign01',
    Key=poster_name
                                    )
    print('File uploaded to S3')

#8. Generate Pre-Signed URL - Link   
    url = client_s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': 'mvyposterdesign01', 'Key': poster_name},
        ExpiresIn=3600
    )
    print(url)
#9. returning the url (get) to api gateway
    return {
        'statusCode': 200,
        'body': url
    }

