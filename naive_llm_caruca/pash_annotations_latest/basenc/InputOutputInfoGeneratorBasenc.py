from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorBasenc(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["--base64", "--base64url", "--base32", "--base32hex", "--base16", "--base2msbf",
    #                      "--base2lsbf", "--z85", "-d", "-i", "--help", "--version"]
    # list_of_all_options = ["-w"]

    # Which ones do affect input/output?
    # none of them: basenc always reads one stream (FILE, or stdin when no FILE or FILE is "-")
    # and always writes the result to stdout; at most one operand is accepted
    # assumption that version/help not provided

    def generate_info(self) -> None:
        if self.get_operand_list_length() > 1:
            raise Exception('extra operand for basenc, only one FILE is accepted')
        self.if_no_operands_given_stdin_implicitly_used()
        self.all_operands_are_streaming_inputs()
        self.set_implicit_use_of_stdout()
