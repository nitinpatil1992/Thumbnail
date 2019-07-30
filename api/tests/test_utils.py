from gazo import utils

class TestUtils:
        
    def test_file_validation_valid_extension_size(self, testapp):
        actual_result_valid_extension = utils.file_validation('png', 100)
        actual_result_invalid_extension = utils.file_validation('jpg', 100)
        actual_result_valid_size = utils.file_validation('png', 100)
        actual_result_invalid_size = utils.file_validation('png', 0)
        assert actual_result_valid_extension == True
        assert actual_result_invalid_extension == False
        assert actual_result_valid_size == True
        assert actual_result_invalid_size == False
