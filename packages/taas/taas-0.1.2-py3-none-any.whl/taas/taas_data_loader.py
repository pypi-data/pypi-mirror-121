import os
import pickle
import queue
import multiprocessing
import time
import sys
import traceback
import grpc
from typing.io import BinaryIO

from .protos import DataLoaderState, StreamingRequest, ReadTask, DataBlobStatus, Status
from .protos import GpuDataManagerStub
from .config import is_registered, TAAS_ATTR

_taas_dl_class_to_methods = dict()


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
		retries = 0
		while retries < 10:
			try:
				import time
				print("t1 " + str(time.time()) + "\n", flush=True)

				import os
				print(os.environ, flush=True)
				print("\n", flush=True)
				with grpc.insecure_channel(f'{self._gpu_service_host}:{self._gpu_service_port}') as channel:
					stub = GpuDataManagerStub(
						channel=channel
					)
					responses = stub.DataStreaming(
						self.generate_streaming_requests()
					)

					print("t2 " + str(time.time()) + "\n", flush=True)
					print("responses " + str(responses) + "\n", flush=True)
					for response in responses:
						print(response, flush=True)
						field = response.WhichOneof('Event')
						if field == 'read_task' or field == 'stop_task':
							self._request_queue.put(response)
						elif field == 'status':
							if not response.status.success:
								print(response.status.message)
								continue
						else:
							assert False
			except Exception as e:
				print("ERROR:" + str(e) + "\n", flush=True)
				print(f'retries = {retries}', flush=True)
				print(traceback.format_exc())
				print(sys.exc_info()[2])
				retries += 1
				import time
				time.sleep(4)

	def generate_streaming_requests(self) -> StreamingRequest:
		while True:
			if self._response_queue.empty():
				request = StreamingRequest(
					worker_id=self.worker_id,
					dataloader_name=self.dataloader_name,
					dataloader_state=DataLoaderState(
						queue_size=self._request_queue.qsize(),
						current_blob_uuid=self._current_blob_uuid,
						stopped=self._stopped
					)
				)
				print("request " + str(request) + "\n", flush=True)
				time.sleep(5)
				yield request
			while not self._response_queue.empty():
				elem = self._response_queue.get()
				print("request " + str(elem) + "\n", flush=True)
				time.sleep(5)
				yield elem

	def stop(self):
		self._stopped = True


class _TaasDataLoader:

	def __init__(
			self,
			gpu_service_host: str,
			gpu_service_port: int,
			request_queue: queue.Queue,
			response_queue: queue.Queue,
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
		self._batch_queue = queue.Queue(
			maxsize=int(os.environ['QUEUE_MXA_SIZE'])
		)
		self._stop_iteration = False
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
			field = request.WhichOneof('Event')
			if field == 'read_task':
				self._response_queue.put(self.read_task(request.read_task))
			elif field == 'stop_task':
				self._stop_iteration = True
			else:
				assert False

	def read_task(
			self,
			read_task: ReadTask
	) -> StreamingRequest:
		#print("read_task " + "\n", flush=True)
		if read_task.offset != 0:
			raise NotImplementedError
		#print("read_task offset 0 " + "\n", flush=True)
		blob_uuid = read_task.blob_to_read.blob_uuid
		self._proxy._current_blob_uuid = blob_uuid
		n_batches = read_task.count
		i_batches = 0
		success = True
		message = "Read task done!"

		try:
			#print("try open" + "\n", flush=True)
			with open(read_task.blob_to_read.mount_path, mode="rb") as file:
				while i_batches < n_batches:
					batch = read_batch_from_file(
						file=file
					)
					i_batches += 1
					self._batch_queue.put(batch)
		except IOError as e:
			#print(e, flush=True)
			message = e.sterror
			success = False

		return StreamingRequest(
			worker_id=self._proxy.worker_id,
			blob_status=DataBlobStatus(
				blob_uuid=blob_uuid,
				status=Status(
					success=success,
					message=message
				)
			)
		)

	def __iter__(self):
		return self

	def __next__(self):
		#print("__next__", flush=True)
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
		return batch.data()


def read_batch_from_file(file: BinaryIO):
	#print("read_batch_from_file", flush=True)
	int.from_bytes(file.read(4), byteorder='big')
	topic_len = int.from_bytes(file.read(2), byteorder='big')
	file.read(topic_len).decode("utf-8")
	data_len = int.from_bytes(file.read(4), byteorder='big')
	batch = pickle.loads(bytes(list(file.read(data_len))))
	#print("read_batch_from_file batch " + str(batch), flush=True)
	return batch


# TODO pool map

def _create_data_loader(
		gpu_service_host: str,
		gpu_service_port: int,
		dataloader_name: str
) -> _TaasDataLoader:
	request_queue = queue.Queue()
	response_queue = queue.Queue()
	data_loader = _TaasDataLoader(
		gpu_service_host=gpu_service_host,
		gpu_service_port=gpu_service_port,
		request_queue=request_queue,
		response_queue=response_queue,
		dataloader_name=dataloader_name
	)
	return data_loader


def prepare_data_loaders():
	gpu_service_host = os.environ["GPU_SERVICE_HOST"]
	gpu_service_port = int(os.environ["GPU_SERVICE_PORT"])
	for name, dl in vars(sys.modules["__main__"]).items():
		if is_registered(dl):
			taas_dl = _create_data_loader(gpu_service_host, gpu_service_port, name)
			setattr(dl, "_taas_dl_iter", taas_dl)
			setattr(dl, TAAS_ATTR, name)
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
