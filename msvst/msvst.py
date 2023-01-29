"""
Python wrapper for MSVST

@author: A.Ruiz
"""
# import logging
from pathlib import Path

from .wrapper import MSVSTWrapper


class MSVST:
    @classmethod
    def _run_process(cls, command, options, input_file, output_file, verbose):
        process = MSVSTWrapper(verbose=verbose)
        process([command] + options + [str(input_file), str(output_file)])

    @staticmethod
    def _set_output_file(input_file):
        return input_file.parent.joinpath(
            f"{input_file.stem}_msvstatrous{input_file.suffix}"
        )


class MSVST2D(MSVST):
    """
    MSVST in 2D
    """

    @classmethod
    def denoise(
        cls, input_file: Path, output_file=None, coupled=False, verbose=False, **kwargs
    ):
        """
        2D MSVST

        Parameters
        ----------
        input_file : Path
            Path for the input fits file.
        output_file : Path, optional
            If None (default), the result is saved in the same path
            as 'input_file', appending the suffix "_msvstatrous" 
            to the file name.
        coupled : bool, optional
            If True, use coupled MSVST, by default False.
        threshold_mode : 0 or 1, optional
            0: p-value threshold (default).
            1: FDR threshold.
        threshold_probability : float, optional
            Two sided Pr or FDR value. 
            If 'threshold_mode' is 0, default 0.000465.
            If 'threshold_mode' is 1, default 0.1.
        border_mode : int, optional
            0: cont.
            1: mirror (default).
            2: period.
            3: zero.
        sigma_level : int or float
            Equivalent Gauss-detection level.
        fdr_indep : bool, optional
            Manual FDR setting. True if FDR coefficients are independent,
            by default False.
        min_scalexy : int, optional
            First detection scale, by default 1.
        max_scalexy : int, optional
            Number of scales for the wavelet transformation, by default 5.
        iteration_mode : 0 or 1, optional
            Iteration modes
            0: Direct iterative mode.
            1: L1-regularized iterative mode (default).
        iterations : int, optional
            Number of iteration. by default 10.
        use_non_default_filter : bool, optional
            If True, use g=Id-h*h as iteration band-pass filter. 
            By default False.
        bias_correction : bool, optional
            If True, correct the VST's bias. By default True.
        positivity_projection : bool, optional
            If True, apply positivity projection. By default True.
        kill_last : bool, optional
            If True, ignore the last approximation band 
            (used with iteration). By default False.
        detpos : bool, optional
            If True, detect only the positive coefficients
            (used with iteration). By default False.
        save_snr_output : bool, optional
            If True, write SNR file for every band in the same 
            path defined by 'output_file'. By default False.
        verbose : bool, optional
            If True, activate verbose mode. By default False.

        Returns
        -------
        Path
            Path where the result is saved.
        """
        if not output_file:
            output_file = cls._set_output_file(input_file)

        command = cls._set_command(coupled)
        options = cls._parse_args(verbose=verbose, **kwargs)

        cls._run_process(command, options, input_file, output_file, verbose)

        return output_file

    @staticmethod
    def _set_command(use_coupled):
        if use_coupled:
            command = "msvst_iwt2d_coupled"
        else:
            command = "msvst_iwt2d"

        return command

    @staticmethod
    def _parse_args(**kwargs):
        args_values = {
            "threshold_probability": ["E", 0.000465],
            "sigma_level": ["s", None],
            "max_scalexy": ["n", 5],
            "min_scalexy": ["F", 1],
            "iteration_mode": ["I", 1],
            "iterations": ["i", 10],
            "border_mode": ["B", 1],
        }
        args_flags = {
            "use_non_default_filter": "T",
            "kill_last": "K",
            "detpos": "p",
            "save_snr_output": "Q",
            "verbose": "v",
        }
        args = []

        fdr_indep = kwargs.pop("fdr_indep", False)
        fdr_setting = 0 if fdr_indep else 1
        args.append(f"-c{fdr_setting}")

        threshold_mode = kwargs.pop("threshold_mode", 0)
        args.append(f"-M{threshold_mode}")

        if threshold_mode == 1:
            args_values["threshold_probability"][1] = 0.1

        for key, [flag, default_value] in args_values.items():
            user_value = kwargs.pop(key, default_value)
            if user_value is not None:
                args.append(f"-{flag}{user_value}")

        for key, flag in args_flags.items():
            user_value = kwargs.pop(key, False)
            if user_value:
                args.append(f"-{flag}")

        correct_vst_bias = kwargs.pop("bias_correction", True)
        if not correct_vst_bias:
            args.append("-b")

        positivity_projection = kwargs.pop("positivity_projection", True)
        if not positivity_projection:
            args.append("-N")

        return args


class MSVST2D1D(MSVST):
    """
    MSVST in 2D+1D
    """

    @classmethod
    def denoise(cls, input_file: Path, output_file=None, verbose=False, **kwargs):
        """
        2D+1D MSVST denoising algorithm.

        Parameters
        ----------
        input_file : Path
            Path for the input fits file.
        output_file : Path, optional
            If None (default), the result is saved in the same path 
            as 'input_file', appending the suffix "_msvstatrous" 
            to the file name.
        threshold_mode : 0 or 1, optional
            0: p-value threshold (default).
            1: FDR threshold.
        threshold_probability : float, optional
            Two sided Pr or FDR value. 
            If 'threshold_mode' is 0, default 0.000465.
            If 'threshold_mode' is 1, default 0.1.
        border_mode : int, optional
            0: cont.
            1: mirror (default).
            2: period.
            3: zero.
        sigma_level : int or float
            Equivalent Gauss-detection level.
        fdr_indep : bool, optional
            Manual FDR setting. True if FDR coefficients are independent,
            by default False.
        max_scalexy : int, optional
            Number of scales for the 2D wavelet transformation, by default 3.
        min_scalexy : int, optional
            First detection scale in 2D, by default 1.
        max_scalez : int, optional
            Number of scales for the 1D wavelet transformation, by default 5.
        min_scalez : int, optional
            First detection scale in 1D, by default 1.
        iteration_mode : 0 or 1, optional
            Iteration modes
            0: Direct iterative mode.
            1: L1-regularized iterative mode (default).
        iterations : int, optional
            Number of iteration. by default 10.
        use_non_default_filter : bool, optional
            If True, use g=Id-h*h as iteration band-pass filter. 
            By default False.
        kill_last : bool, optional
            If True, ignore the last approximation band 
            (used with iteration). By default False.
        detpos : bool, optional
            If True, detect only the positive coefficients
            (used with iteration). By default False.
        verbose : bool, optional
            If True, activate verbose mode. By default False.

        Returns
        -------
        Path
            Path where the result is saved.
        """
        if not output_file:
            output_file = cls._set_output_file(input_file)

        options = cls._parse_args(verbose=verbose, **kwargs)
        command = "msvst_2d1d"

        cls._run_process(command, options, input_file, output_file, verbose)

        return output_file

    @staticmethod
    def _parse_args(**kwargs):
        args_values = {
            "threshold_probability": ["E", 0.000465],
            "sigma_level": ["s", None],
            "max_scalexy": ["n", 3],
            "max_scalez": ["N", 5],
            "min_scalexy": ["F", 1],
            "min_scalez": ["f", 1],
            "iteration_mode": ["I", 1],
            "iterations": ["i", 10],
            "snr_files_prefix": ["Q", None],
            "border_mode": ["B", 1],
        }
        args_flags = {
            "use_non_default_filter": "T",
            "kill_last": "K",
            "detpos": "p",
            "verbose": "v",
            "varmodcorr": "S",
        }
        args = []

        fdr_indep = kwargs.pop("fdr_indep", False)
        fdr_setting = 0 if fdr_indep else 1
        args.append(f"-c{fdr_setting}")

        threshold_mode = kwargs.pop("threshold_mode", 0)
        args.append(f"-M{threshold_mode}")

        if threshold_mode == 1:
            args_values["threshold_probability"][1] = 0.1

        for key, [flag, default_value] in args_values.items():
            user_value = kwargs.pop(key, default_value)
            if user_value is not None:
                args.append(f"-{flag}{user_value}")

        for key, flag in args_flags.items():
            user_value = kwargs.pop(key, False)
            if user_value:
                args.append(f"-{flag}")

        return args
