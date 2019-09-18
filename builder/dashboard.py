import sys

class Dashboard:
    task = ""
    task_progress = ""
    step = ""
    status = ""
    log_trace = ""
    status_progress = ""

    last_status = ""

    def update(self):
        status = "[{task_progress}]({task})[{step}][{status_progress}%]({status}) {trace}\r".format(
            task_progress = self.task_progress,
            task = self.task,
            step = self.step,
            status = self.status,
            status_progress = self.status_progress,
            trace = self.log_trace,
        )
        self.tail(status)

    def tail(self, status):
        if len(self.last_status) > len(status):
            sys.stdout.write(" " * len(self.last_status) + "\r")
            sys.stdout.flush()

        self.last_status = status
        sys.stdout.write(status)
        sys.stdout.flush()


    def set_task(self, task, index, length):
        self.step = ""
        self.status = ""
        self.status_progress = ""
        self.log_trace = ""

        self.task = task
        self.task_progress = "{i}/{o}".format(i=index, o=length)
        self.update()

    def set_status(self, status):
        self.status = status
        self.log_trace = ""
        self.update()

    def set_step(self, step):
        self.step = step

    def set_progress(self, progress):
        self.status_progress = progress
        self.update()

    def trace(self,trace):
        self.log_trace = trace
        self.update()

    def log(self, text):
        copy = self.last_status
        self.tail("")
        print(text) # and moves up
        self.tail(copy)