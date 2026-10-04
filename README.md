# Fanous

A simple microservice to analyze and rename photos.

# Why?
I like to think of myself as an amateur photographer, using both my phone and cameras.
An issue I often face is when I need to find or share a photo I've taken among thousands and thousands, it's difficult to search for it. Despite knowing when it was shot and what it portrays... Most systems name photos with a name like "DSC63180.jpeg" or the like.

Fanous aims to rename photos with more human-centric and searchable names.

# Stack
## Frontend Client
A Laravel Web app, to ingest, process, and output renamed photos.
Responsible for:
- A web interface for the user
- Accepting files
- EXIF and metadata extraction
- Relaying data and images to backend
- Processing output to rename the files using returned outputs from server
- Packaging (zipping) and downloading the files for the user

## Backend Inference Server
Responsible for all the image analysis using Moondream2.
// Dev has yet to start
### Moondream2

# How?


# Gen-AI Disclaimer
I want to be clear about how I utilize generative AI, because the tech's impressive but it's also double-edged...
Since I *actually* enjoy programming, I take steps to ensure understanding and ownership of code I don't write by hand.
**Uses:**
- Use generative AI as a rubber-ducky to bounce ideas back and forth
- Generate boring boilerplate and low-consequence items like Tailwind classes
- Fill in knowledge gaps with new technologies
- Research idiomatic conventions and where I'm lacking
- I never commit a change without parsing line by line and editing where needed
- If I don't understand it, I dont' ship it

# Instructions


# Credits


# Licenses

