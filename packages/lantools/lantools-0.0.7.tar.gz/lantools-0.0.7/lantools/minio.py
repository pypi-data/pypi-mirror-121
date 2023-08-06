from minio import Minio


class PyMinio:
    def __init__(self, host, port, access_key, secret_key, secure=False):
        self.client = Minio(
            "{}:{}".format(host, port),
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )

    def set_bucket(self, bucket):
        self.bucket = bucket

    def put_file(self, file_path, object_name):
        if self.client.bucket_exists(self.bucket) == False:
            self.client.make_bucket(self.bucket)  # 生成一个bucket，类似文件夹

        return self.client.fput_object(
            bucket_name=self.bucket,
            object_name=object_name,
            file_path=file_path
        )

    def get_object(self, object_name):
        return self.client.get_object(self.bucket, object_name)

    # 删除对象
    def remove_file(self, object_name):
        try:
            self.client.remove_object(self.bucket, object_name)
            print("Sussess")
            return True
        except Exception as err:
            print(err)
            return False
