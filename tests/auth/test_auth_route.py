from agrihire import utilities

#Unit test for getting register page
def test_register_page(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b"<title>Register</title>" in response.data
    
    
#Unit test for posting a registration   
def test_register_route(client):
    # Simulate the data when the form is submitted
    form_data = {
        'title': 'Mr',
        'email': 'tester@example.com',
        'firstname': 'John',
        'lastname': 'Doe',
        'phone': '1234567890',
        'password': 'Password1',
        'password_confirm':'Password1',
        'date_of_birth': '1990-01-01',
        'address': '123 Street, City'
    }
    
    #clean up database
    email = 'tester@example.com'
    utilities.delete_user_for_unit_testing(email)
    
    # Send a Post request to the Reggist route
    response = client.post('/register', data=form_data, follow_redirects=True)

    assert response.status_code == 200
    assert b'You have registered successfully!' in response.data
    assert b'Field must be between 2 and 50 characters long.' not in response.data
 
 #Unit test for invaild posting a registration
def test_register_route_invalid(client):
    # Simulate the data when the form is submitted
    form_data = {
        'title': 'Mr',
        'email': 'test@example.com',
        'address': '123 Street, City'
    }
    
    #clean up database
    email = 'test@example.com'
    utilities.delete_user_for_unit_testing(email)
    
    # Send a Post request to the Reggist route
    response = client.post('/register', data=form_data, follow_redirects=True)

    assert response.status_code == 200
    assert b'Input is required!' in response.data
    
#Unit test for posting a login   from flask import current_app
def test_login_route(client):
   
        response = client.post('/login', data={'email': 'coco@gmail.com', 'password': 'Password1'})

        assert response.status_code == 302
        
def test_login_with_nonexistent_email(client):
   
        response = client.post('/login', data={'email': 'coco1@gmail.com', 'password': 'Password1'})

        assert response.status_code == 200
        assert b"There is no registered account with that email" in response.data

def test_login_with_incorrect_password(client):
    # Test login with incorrect password
    response = client.post('/login', data={'email': 'coco@gmail.com', 'password': 'wrong_password'})
    assert response.status_code == 200
    assert b"Incorrect password" in response.data
#Unit test for getting login page    
def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b"<title>Login</title>" in response.data
        