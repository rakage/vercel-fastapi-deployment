from time import time
from fastapi import FastAPI, __version__
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, HTTPException
from google.cloud import firestore
import os

app = FastAPI()
encoded_credentials = os.getenv("FIRESTORE_CREDENTIALS")
if not encoded_credentials:
    raise ValueError("FIRESTORE_CREDENTIALS environment variable is not set")
# Initialize Firestore client
db = firestore.Client()


app.mount("/static", StaticFiles(directory="static"), name="static")

html = f"""
<!DOCTYPE html>
<html>
    <head>
        <title>FastAPI on Vercel</title>
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon" />
    </head>
    <body>
        <div class="bg-gray-200 p-4 rounded-lg shadow-lg">
            <h1>Hello from FastAPI@{__version__}</h1>
            <ul>
                <li><a href="/docs">/docs</a></li>
                <li><a href="/redoc">/redoc</a></li>
            </ul>
            <p>Powered by <a href="https://vercel.com" target="_blank">Vercel</a></p>
        </div>
    </body>
</html>
"""

@app.get("/")
async def root():
    return HTMLResponse(html)

@app.get("/qna/{category}/{sub_category}")
async def read_item(category: str, sub_category: str):
    try:
        # Get document from Firestore
        doc_ref = db.collection(category).document(sub_category)
        print(doc_ref)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/ping')
async def hello():
    return {'res': 'pong', 'version': __version__, "time": time()}