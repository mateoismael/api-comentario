import boto3
import uuid
import os
import json

# Cliente de S3
s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Parseamos el body (puede llegar como JSON serializado)
    body = event.get('body')
    if isinstance(body, str):
        body = json.loads(body)

    tenant_id = body['tenant_id']
    texto     = body['texto']

    # Leemos el bucket según el stage
    bucket_name = os.environ['BUCKET_NAME']

    # Generamos un UUIDv1 para usar en el nombre del objeto
    uid = str(uuid.uuid1())
    object_key = f"{tenant_id}/{uid}.json"

    comentario = {
        'tenant_id': tenant_id,
        'uuid': uid,
        'detalle': {'texto': texto}
    }

    # Subimos el JSON como objeto a S3
    s3.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=json.dumps(comentario),
        ContentType='application/json'
    )

    # Devolvemos confirmación
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Comentario almacenado en S3',
            'bucket': bucket_name,
            'key': object_key
        })
    }
