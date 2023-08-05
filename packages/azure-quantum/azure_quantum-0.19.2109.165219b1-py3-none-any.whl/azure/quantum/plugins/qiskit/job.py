##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
try:
    from qiskit.providers import JobV1, JobStatus
    from qiskit.result import Result
except ImportError:
    raise ImportError(
        "Missing optional 'qiskit' dependencies. \
To install run: pip install azure-quantum[qiskit]"
    )

from azure.quantum import Job

import logging
logger = logging.getLogger(__name__)

AzureJobStatusMap = {
    "Succeeded": JobStatus.DONE,
    "Waiting": JobStatus.QUEUED,
    "Executing": JobStatus.RUNNING,
    "Failed": JobStatus.ERROR,
    "Cancelled": JobStatus.CANCELLED,
    "Finishing": JobStatus.RUNNING
}

# Constants for output data format:
MICROSOFT_OUTPUT_DATA_FORMAT = "microsoft.quantum-results.v1"
IONQ_OUTPUT_DATA_FORMAT = "ionq.quantum-results.v1"
HONEYWELL_OUTPUT_DATA_FORMAT = "honeywell.quantum-results.v1"

class AzureQuantumJob(JobV1):
    def __init__(
        self,
        backend,
        azure_job=None,
        **kwargs
    ) -> None:
        """
            A Job running on Azure Quantum
        """
        if azure_job is None:
            azure_job = Job.from_input_data(
                workspace=backend.provider().get_workspace(),
                **kwargs
            )

        self._azure_job = azure_job
        self._workspace = backend.provider().get_workspace()

        super().__init__(backend, self._azure_job.id, **kwargs)

    def job_id(self):
        """ This job's id."""
        return self._azure_job.id

    def id(self):
        """ This job's id."""
        return self._azure_job.id

    def refresh(self):
        """ Refreshes the job metadata from the server."""
        return self._azure_job.refresh()

    def submit(self):
        """ Submits the job for execution. """
        self._azure_job.submit()
        return

    def result(self, timeout=None):
        """Return the results of the job."""
        self._azure_job.wait_until_completed(timeout_secs=timeout)

        success = self._azure_job.details.status == "Succeeded"
        results = self._format_results()

        return Result.from_dict(
            {
                "results" : [results],
                "job_id" : self._azure_job.details.id,
                "backend_name" : self._backend.name(),
                "backend_version" : self._backend.version,
                "qobj_id" : self._azure_job.details.name,
                "success" : success,
            }
        )

    def cancel(self):
        """Attempt to cancel the job."""
        self._workspace.cancel_job(self._azure_job)

    def status(self):
        """Return the status of the job, among the values of ``JobStatus``."""
        self._azure_job.refresh()
        return AzureJobStatusMap[self._azure_job.details.status]

    def queue_position(self):
        """Return the position of the job in the queue. Currently not supported."""
        return None

    def _format_results(self):
        """ Populates the results datastructures in a format that is compatible with qiskit libraries. """
        success = self._azure_job.details.status == "Succeeded"
        shots_key = "shots"

        job_result = {
            "data": {},
            "success": success,
            "header": {},
        }

        if success:
            if (self._azure_job.details.output_data_format == MICROSOFT_OUTPUT_DATA_FORMAT):
                job_result["data"] = self._format_microsoft_results()
                job_result["header"] = { "name": self._azure_job.details.name }
                
            elif (self._azure_job.details.output_data_format == IONQ_OUTPUT_DATA_FORMAT):
                job_result["data"] = self._format_ionq_results()
                job_result["header"] = self._azure_job.details.metadata

            elif (self._azure_job.details.output_data_format == HONEYWELL_OUTPUT_DATA_FORMAT):
                job_result["data"] = self._format_honeywell_results()
                job_result["header"] = {"name": self._azure_job.details.name}
                shots_key = "count"

            else:
                job_result["data"] = self._format_unknown_results()
                job_result["header"] = { "name": self._azure_job.details.name }

        shots = self._azure_job.details.input_params[shots_key] if shots_key in self._azure_job.details.input_params else self._backend.options.get(shots_key)
        job_result["shots"] = shots
        return job_result

    def _format_ionq_results(self):
        """ Translate IonQ's histogram data into a format that can be consumed by qiskit libraries. """
        az_result = self._azure_job.get_results()
        shots = int(self._azure_job.details.input_params['shots']) if 'shots' in self._azure_job.details.input_params else self._backend.options.get('shots')
        meas_map = self.metadata["metadata"]["meas_map"]
        num_qubits = self.metadata["metadata"]["num_qubits"]

        if not 'histogram' in az_result:
            raise "Histogram missing from IonQ Job results"

        def _to_bitstring(k):
            # flip bitstring to convert to little Endian
            bitstring = format(int(k), f"0{num_qubits}b")[::-1]
            # flip bitstring to convert back to big Endian
            return "".join([bitstring[n] for n in meas_map])[::-1]

        counts = {}
        histogram = {}
        for key, value in az_result['histogram'].items():
            bitstring = _to_bitstring(key)
            counts[bitstring] = int(shots * value)
            histogram[bitstring] = value

        return {"counts": counts, "probabilities": histogram}

    def _format_microsoft_results(self):
        """ Translate Microsoft's job results histogram into a format that can be consumed by qiskit libraries. """
        az_result = self._azure_job.get_results()
        shots = int(self._azure_job.details.input_params['shots']) if 'shots' in self._azure_job.details.input_params else self._backend.options.get('shots')

        if not 'Histogram' in az_result:
            raise "Histogram missing from Job results"

        histogram = az_result['Histogram']
        counts = {}
        probabilities = {}
        # The Histogram serialization is odd entries are key and even entries values
        # Make sure we have even entries
        if (len(histogram) % 2) == 0:
            items = range(0, len(histogram), 2)
            for i in items:
                key = histogram[i]
                value = histogram[i + 1]
                probabilities[key] = value
                counts[key] = int(shots * value)
        else:
            raise "Invalid number of items in Job results' histogram."

        return {"counts": counts, "probabilities": histogram}
    
    def _format_honeywell_results(self):
        """ Translate IonQ's histogram data into a format that can be consumed by qiskit libraries. """
        az_result = self._azure_job.get_results()
        all_bitstrings = [
            bitstrings for classical_register, bitstrings 
            in az_result.items() if classical_register != "access_token"
        ]
        counts = {}
        combined_bitstrings = ["".join(bitstrings) for bitstrings in zip(*all_bitstrings)]
        shots = len(combined_bitstrings)

        for bitstring in set(combined_bitstrings):
            counts[bitstring] = combined_bitstrings.count(bitstring)

        histogram = {bitstring: count/shots for bitstring, count in counts.items()}

        return {"counts": counts, "probabilities": histogram}

    def _format_unknown_results(self):
        """ This method is called to format Job results data when the job output is in an unknown format."""
        az_result = self._azure_job.get_results()
        return az_result
