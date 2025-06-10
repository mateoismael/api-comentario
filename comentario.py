import boto3
import uuid
import os
import json

# Cliente de S3
s3 = boto3.client('s3')

def lambda_handler(event, context):
    # 1) Parsear body (puede llegar como string JSON)
    body = event.get('body', {})
    if isinstance(body, str):
        body = json.loads(body)

    tenant_id = body['tenant_id']
    texto     = body['texto']

    # 2) Nombre del bucket según el stage (viene de serverless.yml)
    bucket_name = os.environ['BUCKET_NAME']

    # 3) Generar UUIDv1 para el nombre del objeto
    uuid1 = str(uuid.uuid1())
    object_key = f"{tenant_id}/{uuid1}.json"

    # 4) Contenido a subir
    comentario = {
        'tenant_id': tenant_id,
        'uuid': uuid1,
        'detalle': {'texto': texto}
    }

    # 5) Push a S3
    s3.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=json.dumps(comentario),
        ContentType='application/json'
    )

    # 6) Responder con confirmación
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Comentario almacenado en S3',
            'bucket': bucket_name,
            'key': object_key
        })
    }
