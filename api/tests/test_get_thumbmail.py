import pytest, uuid, os, json

class TestGetThumb:
    _request_id = None
    _non_request_id = 'test_thumbnail'
        
    def test_get_valid_thumb(self, testapp):
        res = testapp.post('/image', upload_files=[('file', 'test.png', b"abcdef")])
        json_data = json.loads(res.body)
        self._request_id = json_data["request_id"]
        res = testapp.get('/image/'+ self._request_id + '/thumbnail')
        assert res.status_code == 200
    
    def test_get_invalid_thumb(self, testapp):
        res = testapp.get('/image/'+ self._non_request_id + '/thumbnail', expect_errors=True)
        assert res.status_code == 404
