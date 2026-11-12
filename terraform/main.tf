resource "null_resource" "dynamodb_table" {
  provisioner "local-exec" {
    command = <<EOT
python3 -c '
import boto3
client = boto3.client("dynamodb", region_name="us-east-1", endpoint_url="http://localhost:4566", aws_access_key_id="test", aws_secret_access_key="test")
existing = client.list_tables()["TableNames"]
if "FinanceTransactions" not in existing:
    client.create_table(
        TableName="FinanceTransactions",
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST"
    )
print("Table ready:", client.list_tables()["TableNames"])
'
EOT
  }
}
