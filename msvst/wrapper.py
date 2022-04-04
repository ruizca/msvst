import os
import subprocess
import pkg_resources
from pathlib import Path


class MSVSTWrapper(object):
    """ 
    Parent class for the wrapping of MSVST commands.
    """
    _bin_path = Path(pkg_resources.resource_filename("msvst", "bin"))
    
    def __init__(self, env=None, verbose=False):
        """ 
        Initialize the MSVSTWrapper class by setting properly the
        environment.
        
        Parameters
        ----------
        env : dict, optional
            the current environment in which the MSVST command will be
            executed. Default None, the current environment.
        verbose : bool, optional
            control the verbosity level. By default is False.
        """
        self.environment = env
        self.verbose = verbose
        if env is None:
            self.environment = os.environ

    def __call__(self, cmd):
        """ 
        Run the Sparse2d command.
        
        Parameters
        ----------
        cmd : list of str
            The command to execute.
        """
        _cmd = self._parse_cmd(cmd)
        process = self._run_cmd(_cmd)

        self.stdout, self.stderr, self.exitcode = self._parse_output(process)
        self._check_run(_cmd)

    def _run_cmd(self, cmd):
        if self.verbose:
            print(f"[info] Executing MSVST command: {' '.join(cmd)}...")

        command = str(self._bin_path.joinpath(cmd[0]))
        options = cmd[1:]
        _cmd = [command] + options
        
        # Execute the command
        process = subprocess.Popen(
            _cmd, env=self.environment, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        if self.verbose:
            self._stream_output(process)

        return process

    def _check_run(self, cmd):
        if self.exitcode != 0 or self.stderr or "Error" in self.stdout:
            raise RuntimeError(
                cmd[0], " ".join(cmd[1:]), self.stderr + self.stdout
            )

    @staticmethod
    def _parse_output(process):
        stdout, stderr = process.communicate()
        exitcode = process.returncode

        return stdout.decode("utf-8"), stderr.decode("utf-8"), exitcode

    @staticmethod
    def _parse_cmd(cmd):
        # Command must contain only strings
        return [str(elem) for elem in cmd]

    @staticmethod
    def _stream_output(process):
        while _stream_process(process):
            pass


def _stream_process(process):
    go = process.poll() is None

    for line in process.stdout:
        # logging.info(line.decode("utf8"))
        if b"Error" in line:
            print(line.decode("utf8"), end="")
        else:
            print(f"[info] {line.decode('utf8')}", end="")

    for line in process.stderr:
        # logging.info(line.decode("utf8"))
        print(f"Error: {line.decode('utf8')}", end="")

    return go
