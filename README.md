This project provides a simple API for uploading and processing CSV files.

## Steps to Run the Project

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Shanidh/csv_uplaod_gi.git
   ```

2. **Set Up the Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   ```

3. **Install the Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Run the Server:**
   ```bash
   python manage.py runserver
   ```

   The project should now be running on `http://127.0.0.1:8000/`.


## Testing the API

- **Endpoint:** `/upload-csv/`
- **Method:** POST
- **Body:** Use `multipart/form-data` to upload a CSV file.

### Sample CSV File
```csv
name,email,age
John Doe,johndoe@example.com,25
Invalid Email,invalid_email,30
Empty Name,,35
Old User,olduser@example.com,130
```

### Example Using Curl
```bash
curl -X POST http://127.0.0.1:8000/upload-csv/ \
  -F "file=@test.csv"
```


### Response Example
```json
{
  "total_saved": 1,
  "total_rejected": 3,
  "validation_errors": [
    {
      "row": {
        "name": "Invalid Email",
        "email": "invalid_email",
        "age": "30"
      },
      "errors": {
        "email": ["Enter a valid email address."]
      }
    },
    {
      "row": {
        "name": "Empty Name",
        "email": "",
        "age": "35"
      },
      "errors": {
        "name": ["This field may not be blank."],
        "email": ["This field may not be blank."]
      }
    },
    {
      "email": "olduser@example.com",
      "error": "Duplicate email."
    }
  ]
}
```
