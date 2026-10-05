# To Do:
tasks I need to get to
- [X] Build endpoints for uploading files from client app - reverse engineer
- [X] Write the inference via Moondream docs
- [X] Create driver class for handling state from HTTP request
- [X] Create class for inference?
- [X] Write Dockerfile for Compose
- [ ] Test
- [ ] Refactor model modules and Driver class to be more modular and use models types

API contract from Laravel:
```text
API Contract (from frontend code)
POST /caption
  Content-Type: multipart/form-data
  Body: image (file)
  
Response: { "name": "descriptive_name", "description": "full caption" }
```
