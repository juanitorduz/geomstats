"""Unit tests for vectorization functions."""

import tests.helper as helper

import geomstats.backend as gs
import geomstats.tests
import geomstats.vectorization


class TestVectorizationMethods(geomstats.tests.TestCase):
    def setUp(self):
        @geomstats.vectorization.decorator(['vector', 'vector'])
        def foo(tangent_vec_a, tangent_vec_b):
            result = gs.einsum(
                'ni,ni->ni', tangent_vec_a, tangent_vec_b)
            result = helper.to_vector(result)
            return result

        @geomstats.vectorization.decorator(['vector', 'vector'])
        def foo_scalar_output(tangent_vec_a, tangent_vec_b):
            result = gs.einsum(
                'ni,ni->n', tangent_vec_a, tangent_vec_b)
            result = helper.to_scalar(result)
            return result

        @geomstats.vectorization.decorator(['vector', 'vector', 'scalar'])
        def foo_scalar_input_output(tangent_vec_a, tangent_vec_b, in_scalar):
            aux = gs.einsum(
                'ni,ni->n', tangent_vec_a, tangent_vec_b)
            result = gs.einsum('n,nk->n', aux, in_scalar)
            result = helper.to_scalar(result)
            return result

        @geomstats.vectorization.decorator(['vector', 'vector', 'scalar'])
        def foo_optional_input(tangent_vec_a, tangent_vec_b, in_scalar=None):
            if in_scalar is None:
                in_scalar = gs.array([[1]])
            aux = gs.einsum(
                'ni,ni->n', tangent_vec_a, tangent_vec_b)
            result = gs.einsum('n,nk->n', aux, in_scalar)
            result = helper.to_scalar(result)
            return result

        @geomstats.vectorization.decorator(
            ['else', 'vector', 'else', 'vector', 'scalar'])
        def foo_else(else_a, tangent_vec_a, else_b, tangent_vec_b):
            result = (else_a + else_b) * gs.einsum(
                'ni,ni->n', tangent_vec_a, tangent_vec_b)
            result = helper.to_scalar(result)
            return result

        @geomstats.vectorization.decorator(['scalar'])
        def is_scalar_vectorized(scalar):
            is_scalar_vec = gs.ndim(scalar) == 2
            has_dim_1 = gs.shape(scalar)[-1] == 1
            result = is_scalar_vec and has_dim_1
            result = helper.to_scalar(result)
            return result

        @geomstats.vectorization.decorator(['vector'])
        def is_vector_vectorized(vector):
            is_vector_vec = gs.ndim(vector) == 2
            is_vector_vec = helper.to_scalar(is_vector_vec)
            return is_vector_vec

        @geomstats.vectorization.decorator(['matrix'])
        def is_matrix_vectorized(matrix):
            is_matrix_vec = gs.ndim(matrix) == 3
            is_matrix_vec = helper.to_scalar(is_matrix_vec)
            return is_matrix_vec

        self.foo = foo
        self.foo_scalar_output = foo_scalar_output
        self.foo_scalar_input_output = foo_scalar_input_output
        self.foo_optional_input = foo_optional_input
        self.foo_else = foo_else
        self.is_scalar_vectorized = is_scalar_vectorized
        self.is_vector_vectorized = is_vector_vectorized
        self.is_matrix_vectorized = is_matrix_vectorized

    @geomstats.tests.np_and_tf_only
    def test_decorator_with_squeeze_dim0(self):
        vec_a = gs.array([1, 2, 3])
        vec_b = gs.array([0, 1, 0])
        result = self.foo(vec_a, vec_b)
        expected = gs.array([0, 2, 0])

        self.assertAllClose(result.shape, expected.shape)
        self.assertAllClose(result, expected)

    @geomstats.tests.np_and_tf_only
    def test_decorator_without_squeeze_dim0(self):
        vec_a = gs.array([[1, 2, 3]])
        vec_b = gs.array([0, 1, 0])
        result = self.foo(vec_a, vec_b)
        expected = gs.array([[0, 2, 0]])

        self.assertAllClose(result.shape, expected.shape)
        self.assertAllClose(result, expected)

    @geomstats.tests.np_and_tf_only
    def test_decorator_vectorization(self):
        vec_a = gs.array([[1, 2, 3], [1, 2, 3]])
        vec_b = gs.array([0, 1, 0])
        result = self.foo(vec_a, vec_b)
        expected = gs.array([[0, 2, 0], [0, 2, 0]])

        self.assertAllClose(result.shape, expected.shape)
        self.assertAllClose(result, expected)

    @geomstats.tests.np_and_tf_only
    def test_decorator_scalar_with_squeeze_dim1(self):
        vec_a = gs.array([1, 2, 3])
        vec_b = gs.array([0, 1, 0])
        result = self.foo_scalar_output(vec_a, vec_b)
        expected = 2

        self.assertAllClose(result, expected)

    @geomstats.tests.np_and_tf_only
    def test_decorator_scalar_without_squeeze_dim1(self):
        vec_a = gs.array([1, 2, 3])
        vec_b = gs.array([0, 1, 0])
        scalar = 4
        result = self.foo_scalar_input_output(vec_a, vec_b, scalar)
        expected = 8

        self.assertAllClose(result, expected)

    @geomstats.tests.np_and_tf_only
    def test_decorator_scalar_output_vectorization(self):
        vec_a = gs.array([[1, 2, 3], [1, 2, 3]])
        vec_b = gs.array([0, 1, 0])
        result = self.foo_scalar_output(vec_a, vec_b)
        expected = gs.array([2, 2])

        self.assertAllClose(result.shape, expected.shape)
        self.assertAllClose(result, expected)

    def test_decorator_optional_input(self):
        vec_a = gs.array([1, 2, 3])
        vec_b = gs.array([0, 1, 0])
        result = self.foo_optional_input(vec_a, vec_b)
        expected = 2

        self.assertAllClose(result, expected)

    def test_decorator_else(self):
        vec_a = gs.array([1, 2, 3])
        vec_b = gs.array([0, 1, 0])
        else_a = 1
        else_b = 1
        result = self.foo_else(else_a, vec_a, else_b, vec_b)
        expected = 4

        self.assertAllClose(result, expected)

    def test_is_scalar_vectorized(self):
        scalar = 1.3
        result = self.is_scalar_vectorized(scalar)
        expected = True
        self.assertAllClose(result, expected)

    def test_is_scalar_vectorized_with_kwargs(self):
        scalar = 1.3
        result = self.is_scalar_vectorized(scalar=scalar)
        expected = True
        self.assertAllClose(result, expected)

    def test_is_vector_vectorized(self):
        vector = gs.array([1.3, 3.3])
        result = self.is_vector_vectorized(vector)
        expected = True
        self.assertAllClose(result, expected)

    def test_is_vector_vectorizedi_with_kwargs(self):
        vector = gs.array([1.3, 3.3])
        result = self.is_vector_vectorized(vector=vector)
        expected = True
        self.assertAllClose(result, expected)

    def test_is_matrix_vectorized(self):
        matrix = gs.array([[1.3, 3.3], [1.2, 3.1]])
        result = self.is_matrix_vectorized(matrix)
        expected = True
        self.assertAllClose(result, expected)

    def test_is_matrix_vectorized_with_kwargs(self):
        matrix = gs.array([[1.3, 3.3], [1.2, 3.1]])
        result = self.is_matrix_vectorized(matrix=matrix)
        expected = True
        self.assertAllClose(result, expected)

    def test_vectorize_args(self):
        point_types = ['scalar']
        args = (1.3,)
        result = geomstats.vectorization.vectorize_args(point_types, args)
        expected = (gs.array([[1.3]]),)
        self.assertAllClose(result, expected)

    def test_vectorize_kwargs(self):
        point_types = ['scalar']
        kwargs = {'scalar_name': 1.3}
        result_dict = geomstats.vectorization.vectorize_kwargs(
            point_types, kwargs)
        expected_dict = {'scalar_name': gs.array([[1.3]])}

        keys = expected_dict.keys()
        result = gs.array([result_dict[key] for key in keys])
        expected = gs.array([expected_dict[key] for key in keys])

        self.assertAllClose(result, expected)
