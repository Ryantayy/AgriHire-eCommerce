#Unit test for getting home page
def test_home(client):
        response = client.get('/home')
        assert response.status_code == 200
        assert b"<title>Homepage - AgriHire</title>" in response.data