from pulsar.apps import rpc

from .link import HttpTaskManager


__all__ = ['TaskQueueRpcMixin']


class TaskQueueRpcMixin(rpc.JSONRPC):
    '''A mixin RPC class for communicating with a task queue.
To use this mixin, you need to have an :ref:`RPC application <apps-rpc>`
and a :ref:`task queue <apps-tasks>` application installed in the arbiter.

It exposes the following functions:

.. method:: job_list([jobnames=None])

    Return the list of jobs registered with task queue with meta information.
    If a list of jobnames is given, it returns only jobs included in the list.
    
    :rtype: A list of dictionaries
    
    
.. method:: run_new_task(jobname, [**kwargs])
    
    Run a new task in the task queue. The task can be of any type
    as long as it is registered in the job registry.

    :parameter jobname: the name of the job to run.
    :parameter kwargs: optional key-valued job parameters.
    :rtype: a dictionary containing information about the request
'''
    
    task_queue_manager = HttpTaskManager('taskqueue')
    
    def rpc_job_list(self, request, jobnames = None):
        '''Dictionary of information about the registered jobs. If
*jobname* is passed, information regrading the specific job will be returned.'''
        return self.task_queue_manager(request,
                                       'job_list',
                                       jobnames = jobnames)
    
    def rpc_next_scheduled_task(self, request, jobname = None):
        '''Return a two elements tuple containing the job name of the next scheduled task
and the time in seconds when the task will run.

:parameter jobname: optional jobname.'''
        return self.task_queue_manager(request,
                                       'next_scheduled',
                                       jobname = jobname)
        
    def rpc_run_new_task(self, request, jobname = None, ack = True, **kwargs):
        '''Run a new task in the task queue. The task can be of any type
as long as it is registered in the job registry.

:parameter jobname: the name of the job to run.
:parameter ack: if ``True`` the request will be send to the caller.
:parameter kwargs: optional task parameters.'''
        req = self.task_queue_manager.maketask(request,jobname,ack)
        return req(**kwargs)
                           
    
        
    