import abc
import logging
import os

from GAP_interfaces import ABCMetaEnhanced

class Module(object):
    __metaclass__ = ABCMetaEnhanced

    def __init__(self, platform, tool_id):

        # Get information from the platform
        self.platform       = platform
        self.config         = self.platform.get_config()
        self.pipeline_data  = self.platform.get_pipeline_data()

        # Global maximum alloted cpu/memory for a given pipeline module
        self.max_nr_cpus    = self.config["platform"]["max_nr_cpus"]
        self.max_mem        = self.config["platform"]["max_mem"]

        # Number of CPUs and amount of memory available on the main server
        self.main_server_nr_cpus    = self.config["platform"]["MS_nr_cpus"]
        self.main_server_mem        = self.config["platform"]["MS_mem"]

        # Number of cpus and amount of memory to be alloted to the module
        self.nr_cpus    = None
        self.mem        = None

        # Paths to working, tmp, and log directories
        self.wrk_dir        = self.config["paths"]["instance_wrk_dir"]
        self.tmp_dir        = self.config["paths"]["instance_tmp_dir"]
        self.bin_dir        = self.config["paths"]["instance_bin_dir"]

        # Dictionary containing key/value pairs of output_file_type => output_file_path (e.g. {"bam":"/home/alex/output.bam"}
        self.output         = None

        # Required tool/resource keys which must be present in config in order to run module
        self.req_tools      = None
        self.req_resources  = None

        # Paths of tools and resources in config
        self.tools          = self.config["paths"]["tools"]
        self.resources      = self.config["paths"]["resources"]

        # Required input/output keys
        self.input_keys             = None
        self.splitted_input_keys    = None
        self.output_keys            = None
        self.splitted_output_keys   = None

        # Name of main module (e.g. FastQC, GATKCatVariants)
        self.main_module_name   = None
        self.tool_id            = tool_id

    def get_output(self):
        return self.output

    def check_requirements(self):

        # Generating the not found lists
        not_found = dict()
        not_found["tools"] = []
        not_found["resources"] = []

        # Identifying if all the required tool keys are found in the config object
        for req_tool_key in self.req_tools:
            if req_tool_key not in self.tools:
                not_found["tools"].append(req_tool_key)

        # Identifying if all the required resource keys are found in the config object
        for req_res_key in self.req_resources:
            if req_res_key not in self.resources:
                not_found["resources"].append(req_res_key)

        return not_found

    def generate_command(self, **kwargs):
        # Base method for generating the command to be run for a module

        # Initialize new dict to hold output files if it doesn't already exist
        self.output = dict()

        # Set and check names of output filepaths
        self.init_output_file_paths(**kwargs)

        # Check to make sure required output files were actually initialized
        self.check_output_files(**kwargs)

        # Get the command to be run
        cmd = self.get_command(**kwargs)

        # Return the final command
        return cmd

    @abc.abstractmethod
    def get_command(self, **kwargs):
        raise NotImplementedError("Class does not have a required \"get_command()\" method!")

    @abc.abstractmethod
    def init_output_file_paths(self, **kwargs):
        raise NotImplementedError("Class does not have a required \"set_output_file_paths()\" method!")

    def check_output_files(self, **kwargs):
        # Check to see that a module's required output files were actually generated in the get_command

        # Boolean to determine whether module is being split or not
        is_split = "split_id" in kwargs

        # Get required output keys based on whether module is split
        required_keys = self.splitted_output_keys if is_split else self.output_keys

        # Check to see that all required keys are in the self.output. Throw error and exit otherwise.
        errors = False
        for required_key in required_keys:
            if required_key not in self.output:
                logging.error("Runtime error: Required output file type '%s' is never generated by module '%s' during runtime." % (required_key, self.__class__.__name__))
                errors = True

        if errors:
            raise NotImplementedError("One or more required output file types are never generated by the get_command function of module: '%s'. Please see the errors above for details."
                                      % self.__class__.__name__)

    def generate_output_file_path(self, output_key, **kwargs):
        # Generate the name of an output file for a module
        # Called inside 'get_command' function of module to get standardized names of output files
        # Automatically adds output key pair to module's dict of output files generated (i.e. self.output)
        # Throws error if generated filename collides with existing input/output filenames

        output_file_path = kwargs.get("output_file_path", None)
        if output_file_path is None:
            # If file_path is not specified in kwargs, automatically generate output filename
            # Otherwise, add the name of the output file specified directly to self.output

            # Get optional arguments
            output_dir          = kwargs.get("output_dir",  self.wrk_dir)
            split_id            = kwargs.get("split_id",    None)
            extension           = kwargs.get("extension",   None)
            prefix              = self.pipeline_data.get_pipeline_name()

            # Optionally get name of split
            split_string = ".split.%s" % (str(split_id)) if split_id is not None else ""

            # Standardize formatting of extensions
            extension = ".%s" % str(extension).lstrip(".")

            # Generate standardized filename
            output_file_name = "%s_%s_%s%s%s" % \
                           (prefix, self.main_module_name, self.tool_id, split_string, extension)

            # Add pathname to filename
            output_file_path = os.path.join(output_dir, output_file_name)

        # Check to make sure output file path doesn't collide with existing filenames in the module
        self.check_for_path_collisions(output_key, output_file_path)

        # Add output file to self.output
        self.output[output_key] = output_file_path

        return output_file_path

    def check_for_path_collisions(self, check_key, check_file, **kwargs):
        # Checks to see if a filename collides with an existing filename either in the current input and output
        for file_type, file_path in self.output.iteritems():
            if file_type != check_key:
                if file_path == check_file:
                    logging.error("Attempted to create two or more output files with the same name in the same module: %s. Please modify names of output files in module '%s'."
                                  % (check_file, self.__class__.__name__))
                    raise IOError("Attempted to create two or more output files with the same name in module '%s'. See above for details!" %
                                  self.__class__.__name__)

    def get_nr_cpus(self):
        return self.nr_cpus

    def get_mem(self):
        return self.mem








