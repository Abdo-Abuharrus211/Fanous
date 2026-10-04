# To Do:
tasks I need to get to
- [ ] Build endpoints for uploading files from client app - reverse engineer
- [ ] Write the inference via Moondream docs
- [ ] Create driver class for handling state from HTTP request
- [ ] Create class for inference?
- [ ] Write Dockerfile for Compose
- [ ] Test

API contract from Laravel:
```text
API Contract (from frontend code)
POST /caption
  Content-Type: multipart/form-data
  Body: image (file)
  
Response: { "name": "descriptive_name", "description": "full caption" }
```
