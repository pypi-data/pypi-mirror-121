import grpc

from protos import GpuDataManagerStub
from protos.data_provider_pb2 import DataBlobRequest, DataBlob, Status, DataBlobStatus


class DataBlobWrapper:
    def __init__(self, pb):
        self.blob_uuid = pb.blob_uuid
        self.mount_path = pb.mount_path
        self.dataloader_name = pb.dataloader_name


class ReadTaskWrapper:
    def __init__(self, pb):
        self.blob_to_read = DataBlobWrapper(pb.blob_to_read)
        self.offset = pb.offset
        self.count = pb.count


class StopTaskWrapper:
    def __init__(self, pb):
        pass


class StatusWrapper:
    def __init__(self, pb):
        self.success = pb.success
        self.message = pb.message


class StreamingResponseWrapper:
    def __init__(self, pb):
        field = pb.WhichOneof('Event')
        if field == 'read_task':
            self.type = "read_task"
            self.event = ReadTaskWrapper(pb.read_task)
        elif field == 'stop_task':
            self.type = "stop_task"
            self.event = StopTaskWrapper(pb.stop_task)
        elif field == 'status':
            self.type = "status"
            self.event = StatusWrapper(pb.status)
        else:
            assert False


class DataLoaderStateWrapper:
    def __init__(self, pb):
        self.queue_size = pb.queue_size
        self.current_blob_uuid = pb.current_blob_uuid
        self.stopped = pb.stopped


class DataBlobStatusWrapper:
    def __init__(self, pb):
        self.blob_uuid = pb.blob_uuid
        self.status = StatusWrapper(pb.status)


class StreamingRequestWrapper:
    def __init__(self, pb):
        self.worker_id = pb.worker_id
        self.dataloader_name = pb.dataloader_name
        field = pb.WhichOneof('Event')
        if field == 'dataloader_state':
            self.type = "dataloader_state"
            self.event = ReadTaskWrapper(pb.read_task)
        elif field == 'blob_status':
            self.type = "blob_status"
            self.event = StopTaskWrapper(pb.stop_task)
        else:
            assert False


if __name__ == "__main__":
    with grpc.insecure_channel(f'[2a02:6b8:c02:900:0:f816:0:2e]:17001') as channel:
        stub = GpuDataManagerStub(
            channel=channel
        )
        import uuid
        responses = stub.PushData(DataBlobRequest(blob=DataBlob(blob_uuid=str(uuid.uuid4()), mount_path="/debug", dataloader_name="training_generator")))
        print(responses)

    # a = DataBlobStatus(blob_uuid="dcsw", status=Status(success=True, message="awergaewrsgaerg"))
    # b = DataBlobStatusWrapper(a)
    # import pickle
    # print(pickle.dumps(b))
    # print(pickle.dumps(a))




