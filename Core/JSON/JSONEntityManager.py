import Core.JSON.JsonApplicationLibrary as JsonApplicationLibrary
from Core import Worker
import sys
from PyQt5 import QtCore
from Core.Other import Delegates


class UEntityManager:
    def __init__(self):
        self.workers = []
        self.new_worker_delegate = Delegates.UDelegate()
        self.remove_worker_delegate = Delegates.UDelegate()
        self.SetupUpdateTimer()
        self.UpdateWorkers()

    def SetupUpdateTimer(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.UpdateWorkers)
        timer.setInterval(int(5000))
        timer.start()

    def FindWorkerInWorkersByName(self, worker_name, workers):
        for worker in workers:
            if worker.name == worker_name:
                return worker
        return None

    def FindWorkerInWorkersByID(self, worker_id, workers):
        for worker in workers:
            if worker.id == worker_id:
                return worker
        return None

    def AddWorkerInWorkers(self, worker):
        self.workers.append(worker)
        self.new_worker_delegate.Broadcast(worker)

    def RemoveWorkerFromWorkers(self, worker):
        self.workers.remove(worker)
        self.remove_worker_delegate.Broadcast(worker)

    def UpdateWorkers(self):
        print("Update Complete")
        new_workers = []
        request = JsonApplicationLibrary.GetWorkersRequest()
        if request[0] == 200:
            for json_entity in request[1]['data']:
                worker = Worker.UWorker()
                worker.SerializeJSON(json_entity)
                new_workers.append(worker)
        workers_to_remove = []
        for worker in self.workers:
            if not self.FindWorkerInWorkersByID(worker.id, new_workers):
                workers_to_remove.append(worker)
        for worker in workers_to_remove:
            self.RemoveWorkerFromWorkers(worker)
        workers_to_add = []
        for worker in new_workers:
            if not self.FindWorkerInWorkersByID(worker.id, self.workers):
                workers_to_add.append(worker)
        for worker in workers_to_add:
            self.AddWorkerInWorkers(worker)

    def CreateNewWorker(self):
        pass

    def DeleteWorker(self, worker):
        JsonApplicationLibrary.LoginOnDrupal()
        JsonApplicationLibrary.DeleteWorker(worker)
        self.UpdateWorkers()

    def NewWorker(self, worker):
        JsonApplicationLibrary.LoginOnDrupal()
        JsonApplicationLibrary.PostNewWorker(worker)
        self.UpdateWorkers()

    def PatchWorker(self, worker):
        JsonApplicationLibrary.LoginOnDrupal()
        self.UpdateWorkers()


entity_manager = UEntityManager()
