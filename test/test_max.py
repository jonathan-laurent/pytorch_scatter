import pytest
import torch
from torch.autograd import Variable
from torch_scatter import scatter_max_, scatter_max

from .utils import tensor_strs, Tensor


@pytest.mark.parametrize('str', tensor_strs)
def test_scatter_max(str):
    input = [[2, 0, 1, 4, 3], [0, 2, 1, 3, 4]]
    index = [[4, 5, 4, 2, 3], [0, 0, 2, 2, 1]]
    input = Tensor(str, input)
    index = torch.LongTensor(index)
    output = input.new(2, 6).fill_(0)
    expected_output = [[0, 0, 4, 3, 2, 0], [2, 4, 3, 0, 0, 0]]
    expected_arg_output = [[-1, -1, 3, 4, 0, 1], [1, 4, 3, -1, -1, -1]]

    _, arg_output = scatter_max_(output, index, input, dim=1)
    assert output.tolist() == expected_output
    assert arg_output.tolist() == expected_arg_output

    output, arg_output = scatter_max(index, input, dim=1)
    assert output.tolist() == expected_output
    assert arg_output.tolist() == expected_arg_output

    output = Variable(output).fill_(0)
    index = Variable(index)
    input = Variable(input, requires_grad=True)
    scatter_max_(output, index, input, dim=1)

    grad_output = [[10, 20, 30, 40, 50, 60], [15, 25, 35, 45, 55, 65]]
    grad_output = Tensor(str, grad_output)
    expected_grad_input = [[50, 60, 0, 30, 40], [0, 15, 0, 35, 25]]

    output.backward(grad_output)
    assert input.grad.data.tolist() == expected_grad_input


@pytest.mark.parametrize('str', tensor_strs)
def test_scatter_cuda_max(str):
    input = [[2, 0, 1, 4, 3], [0, 2, 1, 3, 4]]
    index = [[4, 5, 4, 2, 3], [0, 0, 2, 2, 1]]
    input = Tensor(str, input)
    index = torch.LongTensor(index)
    output = input.new(2, 6).fill_(0)
    expected_output = [[0, 0, 4, 3, 2, 0], [2, 4, 3, 0, 0, 0]]
    expected_arg_output = [[-1, -1, 3, 4, 0, 1], [1, 4, 3, -1, -1, -1]]

    output, index, input = output.cuda(), index.cuda(), input.cuda()

    _, arg_output = scatter_max_(output, index, input, dim=1)
    print(output)