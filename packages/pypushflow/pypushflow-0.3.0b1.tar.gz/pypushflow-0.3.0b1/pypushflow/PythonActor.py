#
# Copyright (c) European Synchrotron Radiation Facility (ESRF)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

__authors__ = ["O. Svensson"]
__license__ = "MIT"
__date__ = "28/05/2019"

import os
import time
import pprint
import logging
import datetime
import traceback
import importlib
import multiprocessing
import multiprocessing.pool

from pypushflow.AbstractActor import AbstractActor


logger = logging.getLogger("pypushflow")


#############################################################################
# Create no daemon processes
# See : https://stackoverflow.com/a/53180921
#


class NoDaemonProcess(multiprocessing.Process):
    @property
    def daemon(self):
        return False

    @daemon.setter
    def daemon(self, value):
        pass


class NoDaemonContext(type(multiprocessing.get_context())):
    Process = NoDaemonProcess


# We sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
# because the latter is only a wrapper function, not a proper class.
class Edna2Pool(multiprocessing.pool.Pool):
    def __init__(self, *args, **kwargs):
        kwargs["context"] = NoDaemonContext()
        super().__init__(*args, **kwargs)


#
#
#############################################################################


class AsyncFactory:
    def __init__(self, func, callback=None, errorCallback=None):
        self.func = func
        self.callback = callback
        self.errorCallback = errorCallback
        self.pool = Edna2Pool(1)

    def call(self, *args, **kwargs):
        logger.debug(
            "Before apply_async, func=%s, callback=%s, errorCallback=%s",
            self.func,
            self.callback,
            self.errorCallback,
        )
        logger.debug("args=%s, kwargs=%s", args, kwargs)
        self.pool.apply_async(
            self.func,
            args=args,
            kwds=kwargs,
            callback=self.callback,
            error_callback=self.errorCallback,
        )
        self.pool.close()
        logger.debug(
            "After apply_async, func=%s, callback=%s, errorCallback=%s",
            self.func,
            self.callback,
            self.errorCallback,
        )


class PythonActor(AbstractActor):
    def __init__(
        self, parent=None, name="Python Actor", errorHandler=None, script=None, **kw
    ):
        super().__init__(parent=parent, name=name, **kw)
        self.parentErrorHandler = errorHandler
        self.listErrorHandler = []
        self.script = script
        self.inData = None
        self.af = None

    def connectOnError(self, errorHandler):
        self.listErrorHandler.append(errorHandler)

    def trigger(self, inData: dict):
        logger.info("In trigger %s, inData = %s", self.name, pprint.pformat(inData))
        self.setStarted()
        self.inData = dict(inData)
        self.uploadInDataToMongo(actorData={"inData": inData}, script=self.script)

        try:
            module = importlib.import_module(os.path.splitext(self.script)[0])
        except Exception as e:
            logger.error("Error when trying to import script '%s'", self.script)
            time.sleep(1)
            self.errorHandler(e)
            return

        with self._postpone_end_thread(self.resultHandler, self.errorHandler) as (
            resultHandler,
            errorHandler,
        ):
            self.af = AsyncFactory(
                module.run, callback=resultHandler, errorCallback=errorHandler
            )
            self.af.call(**self.inData)

    def resultHandler(self, result: dict):
        # Handle the result
        logger.debug("In resultHandler for '%s'", self.name)
        self._finishedSuccess(result)

        # Trigger actors
        downstreamData = dict(self.inData)
        downstreamData.update(result)
        self._triggerDownStreamActors(downstreamData)

    def errorHandler(self, exception: Exception):
        # Handle the result
        logger.error(
            "Error in python actor '%s'! Not running down stream actors %s",
            self.name,
            [actor.name for actor in self.listDownStreamActor],
        )
        result = self._parseException(exception)
        self._finishedFailure(result)

        # Trigger actors
        downstreamData = dict(self.inData)
        downstreamData["WorkflowException"] = result
        self._triggerErrorHandlers(downstreamData)

    def _parseException(self, exception: Exception) -> dict:
        errorMessage = str(exception)
        if isinstance(exception.__cause__, multiprocessing.pool.RemoteTraceback):
            exception = exception.__cause__
            logger.error(exception)
        elif isinstance(exception, multiprocessing.pool.MaybeEncodingError):
            # This exception has no traceback
            logger.error(exception)
        else:
            logger.exception(exception)
        traceBack = traceback.format_exception(
            type(exception), exception, exception.__traceback__
        )
        return {
            "errorMessage": errorMessage,
            "traceBack": traceBack,
        }

    def _triggerDownStreamActors(self, downstreamData: dict):
        for downStreamActor in self.listDownStreamActor:
            logger.debug(
                "In trigger %s, triggering actor %s, inData=%s",
                self.name,
                downStreamActor.name,
                downstreamData,
            )
            downStreamActor.trigger(downstreamData)

    def _triggerErrorHandlers(self, downstreamData: dict):
        for errorHandler in self.listErrorHandler:
            errorHandler.trigger(downstreamData)
        if self.parentErrorHandler is not None:
            logger.error(
                "Trigger on error on errorHandler '%s'", self.parentErrorHandler.name
            )
            self.parentErrorHandler.triggerOnError(inData=downstreamData)

    def _finishedSuccess(self, result: dict):
        self.setFinished()
        self.uploadOutDataToMongo(
            actorData={
                "stopTime": datetime.datetime.now(),
                "status": "finished",
                "outData": result,
            }
        )
        if "workflowLogFile" in result:
            self.setMongoAttribute("logFile", result["workflowLogFile"])
        if "workflowDebugLogFile" in result:
            self.setMongoAttribute("debugLogFile", result["workflowDebugLogFile"])

    def _finishedFailure(self, result: dict):
        self.setFinished()
        self.uploadOutDataToMongo(
            actorData={
                "stopTime": datetime.datetime.now(),
                "status": "error",
                "outData": result,
            }
        )
