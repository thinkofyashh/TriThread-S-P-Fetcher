import yaml 
import threading 
from queue import Queue
import json
from workers.WebWorker import WebWorker
from workers.postgresWorker import PostgresWorkerSchedular
from workers.YahooFinanceWorker import YahooFinanceWorkerScheduler

WORKER_REGISTRY={
    "WebWorker":WebWorker,
    "YahooFinanceWorkerScheduler":YahooFinanceWorkerScheduler,
    "PostgresWorkerSchedular":PostgresWorkerSchedular
}

class PipelineThread(threading.Thread):
    def __init__(self,yaml_path):
        super().__init__()
        self.yaml_path=yaml_path


    def run(self):
        runner=YamlPipelineReader(self.yaml_path)    
        runner.run()


class YamlPipelineReader():
    def __init__(self,yaml_path):
        self.path=yaml_path
        self.config={}
        self.queue={}
        self.worker={}
        self.thread_count=0


    def _load_pipeline(self):
        with open(self.path,"r") as ff:
            data=yaml.safe_load(ff)
            self.config=data
            


    def _createqueue(self):
        for step in self.config['data_flow']:
            for key,value in step.items():
                value=step[key]
                if isinstance(value,str) and value.endswith("_queue"):
                    queue_name=value
                    if queue_name not in self.queue:
                        self.queue[queue_name]=Queue()
                    


    def _initialize_worker(self,step):
        worker_name=step.get("worker")

        if not worker_name:
            return None
        
        worker_class=WORKER_REGISTRY[worker_name]
        
        if 'input_queue' in step and 'output_queue' in step :
            return worker_class(self.queue[step['input_queue']],self.queue[step['output_queue']])
        
        if 'input_queue' in step :
            return worker_class(self.queue[step['input_queue']])
        
        return worker_class()
    
    def _load_symbols(self,step):


        data=""
        with open(step["input"],"r") as f:
            data=json.load(f)

        output_queue=self.queue[step['output']]

        for item in data:
            self.queue[step['output']].put(item['symbol'])


    def _start_worker(self,step_name):
        worker_list=self.worker[step_name]

        for worker in worker_list:
            if worker:
                worker.start()
                
    def _load_threadCount(self):
        thread_count=self.config['settings']["thread_count"]
        self.thread_count=thread_count     

    def _shutdown(self):
        for i in range(self.thread_count):
            self.queue['symbol_queue'].put("DONE")

        self.queue['symbol_queue'].join()

        for worker in self.worker['fetch_price']:
            worker.join()

        for i in range(self.thread_count):
            self.queue['postgres_queue'].put("DONE")

        self.queue['postgres_queue'].join()

        for worker in self.worker['store_price']:
            worker.join()    

    def run(self):
        self._load_pipeline()
        self._load_threadCount()
        self._createqueue()
        

        for step in self.config['data_flow']:
                
                if "worker" not in step:
                    continue

                step_name=step["step"]
                self.worker[step_name]=[]

                count=self.thread_count if 'input_queue' in step else 1

                for i in range(count):
                    worker=self._initialize_worker(step)
                    self.worker[step_name].append(worker)

                
        self._start_worker("scrape_companies_data")

        for worker in self.worker["scrape_companies_data"]:
            worker.join()

        self._start_worker("store_price")
        self._start_worker("fetch_price")

        for step in self.config['data_flow']:
            if step['step']== "load_symbols":
                self._load_symbols(step)

        self._shutdown()        








    

