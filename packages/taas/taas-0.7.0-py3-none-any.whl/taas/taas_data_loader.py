import os
import pickle
import queue
import multiprocessing
import sys
import grpc
from typing.io import BinaryIO

from .protos import DataLoaderState, StreamingRequest, DataBlobStatus, Status
from .protos import GpuDataManagerStub
from .config import is_registered, TAAS_ATTR

_taas_dl_class_to_methods = dict()


class DataBlobWrapper:
	def __init__(self, pb):
		self.blob_uuid = pb.blob_uuid
		self.mount_path = pb.mount_path
		self.dataloader_name = str(pb.dataloader_name)


class ReadTaskWrapper:
	def __init__(self, pb):
		self.blob_to_read = DataBlobWrapper(pb.blob_to_read)
		self.offset = pb.offset
		self.count = pb.count


class StopTaskWrapper:
	def __init__(self, pb):
		pass


class StatusWrapper:
	def __init__(self, success, message):
		self.success = success
		self.message = message

	@staticmethod
	def from_pb(pb):
		return StatusWrapper(pb.success, pb.message)

	def to_pb(self):
		return Status(success=self.success, message=self.message)


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
			self.event = StatusWrapper.from_pb(pb.status)
		else:
			assert False


class DataLoaderStateWrapper:
	def __init__(self, pb):
		self.queue_size = pb.queue_size
		self.current_blob_uuid = pb.current_blob_uuid
		self.stopped = pb.stopped

	def to_pb(self):
		return DataLoaderState(queue_size=self.queue_size, current_blob_uuid=self.current_blob_uuid, stopped=self.stopped)


class DataBlobStatusWrapper:
	def __init__(self, blob_uuid, status):
		self.blob_uuid = blob_uuid
		self.status = status

	@staticmethod
	def from_pb(pb):
		return DataBlobStatusWrapper(pb.blob_uuid, StatusWrapper.from_pb(pb.status))

	def to_pb(self):
		return DataBlobStatus(blob_uuid=self.blob_uuid, status=self.status.to_pb())


class StreamingRequestWrapper:
	def __init__(self, worker_id, dataloader_name, type_, event):
		self._worker_id = worker_id
		self._dataloader_name = str(dataloader_name)
		self._type = type_
		self._event = event

	@staticmethod
	def from_blob_status(worker_id, dataloader_name, blob_status: DataBlobStatusWrapper):
		return StreamingRequestWrapper(worker_id, dataloader_name, "blob_status", blob_status)

	@staticmethod
	def from_dataloader_state(worker_id, dataloader_name, dataloader_state: DataLoaderStateWrapper):
		return StreamingRequestWrapper(worker_id, dataloader_name, "dataloader_state", dataloader_state)

	@staticmethod
	def from_pb(pb):
		field = pb.WhichOneof('Event')
		if field == 'dataloader_state':
			event = DataLoaderStateWrapper(pb.read_task)
		elif field == 'blob_status':
			event = DataBlobStatusWrapper.from_pb(pb.stop_task)
		else:
			assert False

		return StreamingRequestWrapper(pb.worker_id, pb.dataloader_name, pb.WhichOneof('Event'), event)

	def to_pb(self):
		if self._type == "dataloader_state":
			return StreamingRequest(
				worker_id=self._worker_id,
				dataloader_name=str(self._dataloader_name),
				dataloader_state=self._event.to_pb()
			)
		else:
			return StreamingRequest(
				worker_id=self._worker_id,
				dataloader_name=str(self._dataloader_name),
				blob_status=self._event.to_pb()
			)


class TaasDataLoaderWrapper:

	def __init__(self, taas_dl):
		self._taas_dl_iter = iter(taas_dl)

	def __iter__(self):
		return self._taas_dl_iter


class _DataLoaderProxy:

	def __init__(
			self,
			gpu_service_host: str,
			gpu_service_port: int,
			request_queue: queue.Queue,
			response_queue: queue.Queue,
			dataloader_name: str
	):
		self._gpu_service_host = gpu_service_host
		self._gpu_service_port = gpu_service_port
		self._request_queue = request_queue
		self._response_queue = response_queue
		self._current_blob_uuid = ""
		self.worker_id = int(os.environ["RANK"])
		self._stopped = False
		self.dataloader_name = dataloader_name
		process = multiprocessing.Process(
			target=self.data_loader_streaming
		)
		process.start()

	def data_loader_streaming(self):
		with grpc.insecure_channel(f'{self._gpu_service_host}:{self._gpu_service_port}') as channel:
			stub = GpuDataManagerStub(
				channel=channel
			)
			responses = stub.DataStreaming(
				self.generate_streaming_requests()
			)
			for response in responses:
				field = response.WhichOneof('Event')
				if field == 'read_task' or field == 'stop_task':
					import pickle
					self._request_queue.put(StreamingResponseWrapper(response))
				elif field == 'status':
					if not response.status.success:
						print(response.status.message)
				else:
					assert False

	def generate_streaming_requests(self) -> StreamingRequest:
		import time
		while True:
			if self._response_queue.empty():
				request = StreamingRequest(
					worker_id=self.worker_id,
					dataloader_name=str(self.dataloader_name),
					dataloader_state=DataLoaderState(
						queue_size=self._request_queue.qsize(),
						current_blob_uuid=self._current_blob_uuid,
						stopped=self._stopped
					)
				)
				time.sleep(1)
				yield request
			while not self._response_queue.empty():
				elem = self._response_queue.get().to_pb()
				time.sleep(1)
				yield elem

	def stop(self):
		self._stopped = True


class _TaasDataLoader:
	def __init__(
			self,
			gpu_service_host: str,
			gpu_service_port: int,
			request_queue: multiprocessing.Queue,
			response_queue: multiprocessing.Queue,
			dataloader_name: str
	):
		"""
		Parameters
		--------
		request_queue : очередь из прокси в лоадер
		response_queue : очередь из лоадера в прокси
		"""
		self._request_queue = request_queue
		self._response_queue = response_queue
		self._batch_queue = multiprocessing.Queue(
			maxsize=int(os.environ['QUEUE_MAX_SIZE'])
		)
		self._stop_iteration = False
		self._dataloader_name = dataloader_name
		self._proxy = _DataLoaderProxy(
			gpu_service_host=gpu_service_host,
			gpu_service_port=gpu_service_port,
			request_queue=request_queue,
			response_queue=response_queue,
			dataloader_name=dataloader_name
		)
		process = multiprocessing.Process(
			target=self.update_batches
		)
		process.start()

	def update_batches(self):
		while True:
			request = self._request_queue.get()
			field = request.type
			if field == 'read_task':
				self._response_queue.put(self.read_task(request.event))
			elif field == 'stop_task':
				self._stop_iteration = True
			else:
				assert False

	def read_task(
			self,
			read_task: ReadTaskWrapper
	) -> StreamingRequestWrapper:
		if read_task.offset != 0:
			raise NotImplementedError
		blob_uuid = read_task.blob_to_read.blob_uuid
		self._proxy._current_blob_uuid = blob_uuid
		n_batches = read_task.count
		i_batches = 0
		success = True
		message = "Read task done!"

		try:
			with open(read_task.blob_to_read.mount_path, mode="rb") as file:
				while i_batches < n_batches:
					batch = read_batch_from_file(
						file=file
					)
					i_batches += 1
					self._batch_queue.put(batch)
		except IOError as e:
			message = e.sterror
			success = True
		except EOFError:
			message = "EOF"
			success = True

		return StreamingRequestWrapper.from_blob_status(self._proxy.worker_id, self._dataloader_name, DataBlobStatusWrapper(blob_uuid, StatusWrapper(success, message)))

	def __iter__(self):
		return self

	def __next__(self):
		batch = None
		while batch is None:
			if self._stop_iteration:
				self._proxy.stop()
				raise StopIteration
			try:
				batch = self._batch_queue.get(
					timeout=int(os.environ['BATCH_QUEUE_TIMEOUT'])
				)
			except queue.Empty:
				pass
		return batch


def read_batch_from_file(file: BinaryIO):
	int.from_bytes(file.read(4), byteorder='big')
	topic_len = int.from_bytes(file.read(2), byteorder='big')
	file.read(topic_len).decode("utf-8")
	data_len = int.from_bytes(file.read(4), byteorder='big')
	batch = pickle.loads(bytes(list(file.read(data_len))))
	return batch


# TODO pool map

def _create_data_loader(
		gpu_service_host: str,
		gpu_service_port: int,
		dataloader_name: str
) -> _TaasDataLoader:
	request_queue = multiprocessing.Queue()
	response_queue = multiprocessing.Queue()
	data_loader = _TaasDataLoader(
		gpu_service_host=gpu_service_host,
		gpu_service_port=gpu_service_port,
		request_queue=request_queue,
		response_queue=response_queue,
		dataloader_name=str(dataloader_name)
	)
	return data_loader


def prepare_data_loaders():
	gpu_service_host = os.environ["GPU_SERVICE_HOST"]
	gpu_service_port = int(os.environ["GPU_SERVICE_PORT"])
	for name, dl in vars(sys.modules["__main__"]).items():
		if is_registered(dl):
			taas_dl = _create_data_loader(gpu_service_host, gpu_service_port, str(name))
			setattr(dl, "_taas_dl_iter", taas_dl)
			setattr(dl, TAAS_ATTR, str(name))
			_taas_dl_class_to_methods[dl.__class__] = dl.__class__.__iter__
			dl.__class__.__iter__ = TaasDataLoaderWrapper.__iter__


def restore_data_loaders():
	for cls, it in _taas_dl_class_to_methods.items():
		cls.__iter__ = it
	for _, dl in vars(sys.modules["__main__"]).items():
		if is_registered(dl):
			setattr(dl, TAAS_ATTR, True)
			delattr(dl, "_taas_dl_iter")
	_taas_dl_class_to_methods.clear()

# GPU code
# import taas
# taas.prepare_data_loaders()
# try:
#   USER_CODE
# finally:
#       taas.restore_data_loaders()
