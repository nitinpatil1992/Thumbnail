class TestImageUpload:

    def test_post_image_valid_file_extension(self, testapp):
        res = testapp.post('/image', upload_files=[('file', 'test.png', b"abcdef")])
        assert res.status_code == 200
    
    def test_post_image_invalid_file_extension(self, testapp):
        res_jpeg = testapp.post('/image', upload_files=[('file', 'test.jpeg', b"abcdef")], expect_errors=True)
        res_gif = testapp.post('/image', upload_files=[('file', 'test.gif', b"abcdef")], expect_errors=True)
        res_bmp = testapp.post('/image', upload_files=[('file', 'test.bmp', b"abcdef")], expect_errors=True)
        res_exif = testapp.post('/image', upload_files=[('file', 'test.exif', b"abcdef")], expect_errors=True)
        assert res_jpeg.status_code == 400 and res_gif.status_code == 400 and res_bmp.status_code == 400 and res_exif.status_code == 400

    def test_post_image_invalid_file_zero_size(self, testapp):
         res = testapp.post('/image', upload_files=[('file', 'test.png', b"")], expect_errors=True)
         assert res.status_code == 400
