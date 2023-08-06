from akida.core import LayerType, PoolType, NSoC_v1, Padding
import numpy as np


def summary_hardware_incompatibilities(model, hw_version=None):
    """Checks a model compatibility with hardware and prints a summary.

    This method performs parameters value checking for hardware
    compatibility and prints incompatibility messages when needed.

    Args:
        model (:obj:`Model`): the Model to check hardware compatibility
        hw_version (:obj:`HwVersion`, optional): the hardware version to check

    """
    incompatibilities = model_hardware_incompatibilities(model, hw_version)
    if incompatibilities:
        print("Hardware incompatibilities:")
    print("\n".join(incompatibilities))


def model_hardware_incompatibilities(model, hw_version=None):
    """Checks a model compatibility with hardware.

    This method performs parameters value checking for hardware
    compatibility and returns incompatibility messages when needed.

    Args:
        model (:obj:`Model`): the Model to check hardware compatibility
        hw_version (:obj:`HwVersion`, optional): the hardware version to check

    Returns:
        a list of str containing the hardware incompatibilities of the model.
        The list is empty if the model is hardware compatible.

    """
    incompatibilities = []
    for i in range(model.get_layer_count()):
        layer_incompatibility = layer_hardware_incompatibilities(
            model, i, hw_version)
        if layer_incompatibility:
            incompatibilities.append(layer_incompatibility)
    return incompatibilities


def layer_hardware_incompatibilities(model, layer_index, hw_version=None):
    """Checks a layer compatibility with hardware.

    This method performs parameters value checking for hardware
    compatibility and returns incompatibility messages when needed.

    Args:
        model (:obj:`Model`): the Model to check hardware compatibility
        layer_index (int): the layer index.
        hw_version (:obj:`HwVersion`, optional): the hardware version to check

    Returns:
        str: message containing hardware incompatibilities of the layer.
            Empty string if the layer is hardware compatible.

    """

    def full_message(layer_name, msg_list):

        if len(msg_list) > 0:
            return str("Layer " + layer_name + " is not compatible with "
                       "hardware: \n" + "\n".join(msg_list))
        return str()

    layer = model.get_layer(layer_index)
    hw_msg = []
    # inputData layer
    if layer.parameters.layer_type == LayerType.InputData:
        return str()

    if layer.parameters.act_bits not in [1, 2, 4]:
        hw_msg.append("- unsupported act_bits, supported "
                      "values are [1, 2, 4], currently at " +
                      str(layer.parameters.act_bits))

    # fullyConnected layer
    if layer.parameters.layer_type == LayerType.FullyConnected:
        hw_msg += _get_fully_connected_hw_incompatibilities(
            model, layer_index, hw_version)

    # inputConvolutional layer
    if layer.parameters.layer_type == LayerType.InputConvolutional:
        hw_msg += _get_input_conv_hw_incompatibilities(layer, hw_version)

    # convolutional layers
    elif (layer.parameters.layer_type
          in [LayerType.Convolutional, LayerType.SeparableConvolutional]):
        hw_msg += _get_conv_hw_incompatibilities(model, layer_index, hw_version)

    return full_message(layer.name, hw_msg)


def _get_must_be_in_msg(name, param, supported_values):
    """Returns a warning message if the given parameter is not in the
    supported values.

    Args:
        name (str): name of the parameter to display in the message.
        param: parameter to check if valid
        supported_values (list): list of values that param must take.

    Returns:
        list: warning message embedded in a list. Empty if param is valid.
    """
    if param not in supported_values:
        return [f"- {name} must be in {supported_values}, currently at {param}"]
    return []


def _get_must_be_equal_msg(name1, param1, name2, param2):
    """Returns a warning message if the two parameters are not equal.

    Args:
        name1 (str): name of the first parameter to display in the message.
        param1: first parameter to compare with
        name2 (str): name of the second parameter to display in the message.
        param2: second parameter to compare with

    Returns:
        list: warning message embedded in a list. Empty if parameters are equal.
    """
    if param1 != param2:
        return [(f"- {name1} and {name2} must be equal, currently at "
                 f"{param1} and {param2}")]
    return []


def _get_must_be_coded_on_msg(name, param_array, bit_number):
    """Returns a warning message if the values of the given array are not in the
    expected bits range.

    Args:
        name (str): name of the parameter to display in the message.
        param_array (:obj:`numpy.ndarray`): a numpy.ndarray to check if valid.
        bit_number (int): bit number in witch the parameter is coded.

    Returns:
        list: warning message embedded in a list. Empty if param is valid.
    """
    limit_low = -2**(bit_number - 1)
    limit_high = 2**(bit_number - 1)
    if not np.logical_and(param_array < limit_high,
                          param_array >= limit_low).all():
        return [
            f"- {name} must be in [{limit_low},{limit_high - 1}], "
            f"currently at {param_array}"
        ]
    return []


def _get_fully_connected_hw_incompatibilities(model, layer_index, hw_version):
    """Checks a FullyConnected layer compatibility with hardware.

    This method performs parameters value checking for hardware
    compatibility and returns incompatibility messages when needed.

    Args:
        model (:obj:`Model`): the Model to check hardware compatibility
        layer_index (int): the layer index.
        hw_version (:obj:`HwVersion`, optional): the hardware version to check

    Returns:
        str: message containing hardware incompatibilities of the layer.
            Empty string if the layer is hardware compatible.
    """

    layer = model.get_layer(layer_index)
    params = layer.parameters
    hw_msg = []

    # Check thresholds
    hw_msg += _get_threshold_incompatibilities(layer, 20)

    hw_msg += _get_must_be_in_msg('weights_bits', params.weights_bits,
                                  [1, 2, 3, 4])
    if layer_index > 0:
        previous_params = model.get_layer(layer_index - 1).parameters
        if "act_bits" in dir(previous_params):
            # Allowed input bitwidth
            allowed_input_bw = [1, 2]
            if hw_version != NSoC_v1:
                allowed_input_bw.append(4)
            input_bw = previous_params.act_bits
            if input_bw not in allowed_input_bw:
                hw_msg.append("- unsupported input dimensions. "
                              "act_bits in previous layer "
                              "must be in " + str(allowed_input_bw) +
                              ", currently at " + str(input_bw))
    if hw_version == NSoC_v1:
        if params.units < 3 and params.activation:
            hw_msg.append("- learn requires at least 3 units, "
                          "currently at " + str(params.units))
    return hw_msg


def _get_input_conv_hw_incompatibilities(layer, hw_version):
    """Checks a InputConvolutional layer compatibility with hardware.

    This method performs parameters value checking for hardware
    compatibility and returns incompatibility messages when needed.

    Args:
        layer (:obj:`Layer`): the Layer to check hardware compatibility
        hw_version (:obj:`HwVersion`, optional): the hardware version to check

    Returns:
        str: message containing hardware incompatibilities of the layer.
            Empty string if the layer is hardware compatible.
    """

    hw_msg = []
    p = layer.parameters

    # Define constraints (equality or "is an element of")
    must_be_equal_constraints = [('kernel_width', p.kernel_size[0],
                                  'kernel_height', p.kernel_size[1])]
    must_be_in_constraints = [('kernel_width', p.kernel_size[0], [3, 5, 7]),
                              ('stride_x', p.kernel_stride[0], [1, 2, 3]),
                              ('stride_y', p.kernel_stride[1], [1, 2, 3]),
                              ('padding', p.padding,
                               [Padding.Same, Padding.Valid])]

    pool_must_be_equal_constraints = [('pooling_stride_x', p.pool_stride[0],
                                       'pooling_stride_y', p.pool_stride[1])]
    pool_must_be_in_constraints = [('pooling_width', p.pool_size[0], [1, 2]),
                                   ('pooling_height', p.pool_size[1], [1, 2]),
                                   ('pooling_stride_x', p.pool_stride[0], [2])]

    def get_max_num_filters(kernel_size, rgb):
        if kernel_size not in (3, 5, 7):
            return 0

        if rgb:
            max_num_filters = {3: 192, 5: 64, 7: 32}
            return max_num_filters[kernel_size]

        max_num_filters = {3: 512, 5: 192, 7: 96}
        return max_num_filters[kernel_size]

    # Check thresholds
    hw_msg += _get_threshold_incompatibilities(layer, 24)

    # Check kernel parameters for constraints
    for constraint in must_be_equal_constraints:
        hw_msg += _get_must_be_equal_msg(*constraint)
    for constraint in must_be_in_constraints:
        hw_msg += _get_must_be_in_msg(*constraint)

    # check number of neurons
    rgb = (p.input_shape[2] == 3)
    max_num_filters = get_max_num_filters(p.kernel_size[0], rgb)
    if p.filters < 1 or p.filters > max_num_filters:
        hw_msg.append("- filters should be set between 1 and " +
                      str(max_num_filters))
    # check input width limitations
    max_line_width = 256
    if p.input_shape[0] > max_line_width:
        hw_msg.append("- input width cannot be higher than " +
                      str(max_line_width))
    # NSOC-V1: valid conv with stride != 1 is not supported for now
    if (hw_version == NSoC_v1 and p.padding == Padding.Valid and
        (p.kernel_stride[0] > 1 or p.kernel_stride[1] > 1)):
        hw_msg.append("- Convolution stride must be 1 when having "
                      "padding 'VALID' for NSoC v1")
    # Check pooling parameters
    if p.pool_type == PoolType.Max:
        for constraint in pool_must_be_equal_constraints:
            hw_msg += _get_must_be_equal_msg(*constraint)
        for constraint in pool_must_be_in_constraints:
            hw_msg += _get_must_be_in_msg(*constraint)
    elif p.pool_type == PoolType.Average:
        hw_msg.append("- average pool_type not supported")
    # check if we want to enable wta and if wta is hw compatible
    if p.activation:
        wta = layer.get_variable('wta_groups')
        if not np.array_equal(wta, np.sort(wta)):
            hw_msg.append(" - Only consecutives neurons are allowed "
                          "in the same WTA group.")
    return hw_msg


def _get_conv_hw_incompatibilities(model, layer_index, hw_version):
    """Checks a Convolutional or SeparableConvolutional layer compatibility
    with hardware.

    This method performs parameters value checking for hardware
    compatibility and returns incompatibility messages when needed.

    Args:
        model (:obj:`Model`): the Model to check hardware compatibility
        layer_index (int): the layer index.
        hw_version (:obj:`HwVersion`, optional): the hardware version to check

    Returns:
        str: message containing hardware incompatibilities of the layer.
            Empty string if the layer is hardware compatible.
    """

    layer = model.get_layer(layer_index)
    p = layer.parameters
    hw_msg = []

    # Define constraints (equality or "is an element of")
    must_be_equal_constraints = [('kernel_width', p.kernel_size[0],
                                  'kernel_height', p.kernel_size[1])]

    must_be_in_constraints = [('stride_x', p.kernel_stride[0], [1]),
                              ('stride_y', p.kernel_stride[1], [1]),
                              ('padding', p.padding, [Padding.Same])]
    if p.layer_type == LayerType.Convolutional:
        must_be_in_constraints += [('kernel_width', p.kernel_size[0],
                                    [1, 3, 5, 7])]
        bits_list = [1, 2] if hw_version == NSoC_v1 else [1, 2, 4]
        must_be_in_constraints += [('weights_bits', p.weights_bits, bits_list)]
    elif p.layer_type == LayerType.SeparableConvolutional:
        must_be_in_constraints += [('kernel_width', p.kernel_size[0], [3, 5,
                                                                       7]),
                                   ('weights_bits', p.weights_bits, [2, 4])]

    pool_must_be_equal_constraints = [('pooling_width', p.pool_size[0],
                                       'pooling_height', p.pool_size[1]),
                                      ('pooling_stride_x', p.pool_stride[0],
                                       'pooling_stride_y', p.pool_stride[1])]
    pool_must_be_in_constraints = [('pooling_width', p.pool_size[0], [2, 3])]

    # Check kernel parameters for constraints
    for constraint in must_be_equal_constraints:
        hw_msg += _get_must_be_equal_msg(*constraint)
    for constraint in must_be_in_constraints:
        hw_msg += _get_must_be_in_msg(*constraint)

    # Check thresholds
    hw_msg += _get_threshold_incompatibilities(layer, 20)

    if p.pool_type == PoolType.Max:
        # Max pooling forbidden if it is not followed by another NP
        layers_vert_pool = [
            LayerType.Convolutional, LayerType.SeparableConvolutional
        ]
        if hw_version != NSoC_v1:
            layers_vert_pool.append(LayerType.FullyConnected)
        if (layer_index == model.get_layer_count() - 1 or
                model.get_layer(layer_index + 1).parameters.layer_type
                not in layers_vert_pool):
            types = [str(lt).split('.')[-1] for lt in layers_vert_pool]
            types_str = ", ".join(types)
            hw_msg.append("- max pooling on convolutional or separable"
                          " convolutional layer must be followed by"
                          " another layer of one of these types: " + types_str)
        # Check max pooling parameters
        for constraint in pool_must_be_equal_constraints:
            hw_msg += _get_must_be_equal_msg(*constraint)
        for constraint in pool_must_be_in_constraints:
            hw_msg += _get_must_be_in_msg(*constraint)
        if (p.pool_size[0] in [2, 3] and
                p.pool_stride[0] not in range(1, p.pool_size[0] + 1)):
            pw = p.pool_size[0]
            hw_msg.append(
                f"- pool_stride[0] must be in {[*range(1, pw + 1)]} for "
                f"{pw}x{pw} pooling, currently at {p.pool_stride[0]}")
        if p.pool_size[0] > max(layer.input_dims[:2]):
            hw_msg.append(
                "- pooling size must be lower than or equal to input dimensions"
            )
    elif p.pool_type == PoolType.Average:
        hw_msg += _get_avg_pooling_incompatibilities(layer, hw_version)
    return hw_msg


def _get_avg_pooling_incompatibilities(layer, hw_version):
    """Checks global average pooling compatibility with hardware.

    A global average pooling can only be present in a Convolutional or
    SeparableConvolutional layer. This method performs parameters value
    checking for hardware compatibility and returns incompatibility messages
    when needed.

    Args:
        layer (:obj:`Layer`): the Layer to check global average pooling
            hardware compatibility
        hw_version (:obj:`HwVersion`, optional): the hardware version to check

    Returns:
        str: message containing hardware incompatibilities of the layer.
            Empty string if the layer is hardware compatible.
    """
    hw_msg = []

    p = layer.parameters
    if p.pool_size != (-1, -1):
        hw_msg.append("- only global average pooling is supported:"
                      " pool_size parameter must be "
                      "set to (-1, -1) (default)")
    if hw_version == NSoC_v1 and p.filters % 8 != 0:
        hw_msg.append("- with average pooling, number of neurons must"
                      " be a multiple of 8")
    if layer.input_dims[0] > 32:
        hw_msg.append("- with average pooling, the maximum input width"
                      " is 32")
    return hw_msg


def _get_threshold_incompatibilities(layer, bit_number):
    """Checks threshold and act_step compatibility with hardware

    Args:
        layer (:obj:`Layer`): the Layer to check thresholds hardware
            compatibility.
        bit_number (int): bit number in witch the thresholds are coded.

    Returns:
        str: message containing hardware incompatibilities of the layer.
            Empty string if the layer is hardware compatible.
    """
    hw_msg = []
    # Check threshold and act_step parameters
    for param_name in ('threshold', 'act_step'):
        thres = layer.get_variable(param_name)
        hw_msg += _get_must_be_coded_on_msg(param_name, thres, bit_number)
    return hw_msg
