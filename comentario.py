import boto3
import uuid
import os
import json

def lambda_handler(event, context):
    # 1) Parseo de la entrada
    body = event.get('body', {})
    tenant_id = body['tenant_id']
    texto     = body['texto']

    # 2) Construcción del objeto comentario
    uuidv1 = str(uuid.uuid1())
    comentario = {
        'tenant_id': tenant_id,
        'uuid': uuidv1,
        'detalle': {'texto': texto}
    }

    # 3) Inserción en DynamoDB
    nombre_tabla = os.environ["TABLE_NAME"]
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(nombre_tabla)
    table.put_item(Item=comentario)

    # 4) Push al bucket S3 correspondiente al stage
    s3 = boto3.client('s3')
    bucket = os.environ['BUCKET_NAME']
    # Organizo por tenant y uso el mismo UUID
    key = f"{tenant_id}/{uuidv1}.json"
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=json.dumps(comentario)
    )

    # 5) Retorno
    return {
        'statusCode': 200,
        'body': json.dumps({
            'mensaje': 'Comentario registrado y almacenado en S3',
            'comentario': comentario
        })
    }
