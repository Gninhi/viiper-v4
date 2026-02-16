"""Premium File Upload Skill."""

from typing import Dict, Any, Optional
from viiper.skills.base import (
    Skill, SkillMetadata, SkillCategory, SkillDifficulty,
    Dependency, BestPractice, UsageExample, AntiPattern,
)

class FileUploadSkill(Skill):
    """File upload handling with validation and cloud storage."""

    metadata: SkillMetadata = SkillMetadata(
        name="File Upload & Storage",
        slug="file-upload",
        category=SkillCategory.BACKEND_API,
        difficulty=SkillDifficulty.ADVANCED,
        tags=["file-upload", "multer", "s3", "storage", "express", "fastapi"],
        estimated_time_minutes=30,
        description="Secure file uploads with validation, local storage, and S3 integration",
    )

    dependencies: list = [
        Dependency(name="multer", version="^1.4.5-lts.1", package_manager="npm", reason="Multipart file handling (Express)"),
        Dependency(name="@aws-sdk/client-s3", version="^3.470.0", package_manager="npm", reason="AWS S3 client"),
        Dependency(name="python-multipart", version="^0.0.6", package_manager="pip", reason="Multipart support (FastAPI)"),
        Dependency(name="boto3", version="^1.34.0", package_manager="pip", reason="AWS SDK for Python"),
    ]

    best_practices: list = [
        BestPractice(
            title="Validate File Types",
            description="Whitelist allowed MIME types",
            code_reference="Accept only images, PDFs, etc.",
            benefit="Prevent malicious file uploads",
        ),
        BestPractice(
            title="Limit File Size",
            description="Set max file size limits",
            code_reference="Max 10MB per file",
            benefit="Prevent DoS attacks, manage storage",
        ),
        BestPractice(
            title="Sanitize Filenames",
            description="Remove dangerous characters",
            code_reference="Replace spaces, special chars",
            benefit="Prevent path traversal attacks",
        ),
        BestPractice(
            title="Use UUID for Storage",
            description="Don't use original filenames",
            code_reference="Store as {uuid}.{ext}",
            benefit="Avoid collisions, hide original names",
        ),
    ]

    usage_examples: list = [
        UsageExample(
            name="Express File Upload",
            description="Upload single file",
            code='''app.post('/api/upload', upload.single('file'), async (req, res) => {
  const file = req.file
  const url = await uploadToS3(file)
  res.json({ url })
})''',
        ),
        UsageExample(
            name="FastAPI File Upload",
            description="Upload with validation",
            code='''@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    url = await upload_to_s3(file)
    return {"url": url}''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="No file type validation",
            why="Users can upload executables, malware",
            good="Strict MIME type whitelist",
        ),
        AntiPattern(
            bad="Using original filenames",
            why="Path traversal attacks, collisions",
            good="Generate unique filenames (UUID)",
        ),
        AntiPattern(
            bad="No file size limits",
            why="DoS attacks, storage abuse",
            good="Enforce reasonable size limits",
        ),
    ]

    file_structure: dict = {
        "backend/lib/upload.ts": "File upload utilities (Express)",
        "backend/lib/s3.ts": "S3 upload helpers (Node.js)",
        "backend/lib/upload.py": "File upload utilities (FastAPI)",
    }

    express_upload: str = r'''// backend/lib/upload.ts
import multer from 'multer'
import path from 'path'
import crypto from 'crypto'

// Allowed MIME types
const ALLOWED_TYPES = [
  'image/jpeg',
  'image/png',
  'image/gif',
  'image/webp',
  'application/pdf',
  'application/msword',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
]

// Max file size: 10MB
const MAX_FILE_SIZE = 10 * 1024 * 1024

// Storage configuration
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/')
  },
  filename: (req, file, cb) => {
    const uniqueId = crypto.randomUUID()
    const ext = path.extname(file.originalname)
    cb(null, `${uniqueId}${ext}`)
  },
})

// File filter
const fileFilter = (req: any, file: Express.Multer.File, cb: multer.FileFilterCallback) => {
  if (ALLOWED_TYPES.includes(file.mimetype)) {
    cb(null, true)
  } else {
    cb(new Error(`Invalid file type: ${file.mimetype}`))
  }
}

// Multer configuration
export const upload = multer({
  storage,
  fileFilter,
  limits: {
    fileSize: MAX_FILE_SIZE,
  },
})

// Sanitize filename
export function sanitizeFilename(filename: string): string {
  return filename
    .replace(/[^a-zA-Z0-9._-]/g, '_')
    .replace(/\.+/g, '.')
    .replace(/_+/g, '_')
    .toLowerCase()
}

// Get file extension
export function getFileExtension(filename: string): string {
  return path.extname(filename).toLowerCase()
}

// Validate file size
export function isFileSizeValid(size: number): boolean {
  return size <= MAX_FILE_SIZE && size > 0
}
'''

    s3_upload: str = '''// backend/lib/s3.ts
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3'
import { randomUUID } from 'crypto'
import path from 'path'
import fs from 'fs'

const s3Client = new S3Client({
  region: process.env.AWS_REGION || 'us-east-1',
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID!,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY!,
  },
})

const BUCKET_NAME = process.env.S3_BUCKET_NAME!

interface UploadResult {
  url: string
  key: string
  bucket: string
}

export async function uploadToS3(
  file: Express.Multer.File
): Promise<UploadResult> {
  const fileBuffer = fs.readFileSync(file.path)
  const ext = path.extname(file.originalname)
  const key = `uploads/${randomUUID()}${ext}`

  const command = new PutObjectCommand({
    Bucket: BUCKET_NAME,
    Key: key,
    Body: fileBuffer,
    ContentType: file.mimetype,
    ACL: 'public-read',
  })

  await s3Client.send(command)

  // Clean up local file
  fs.unlinkSync(file.path)

  const url = `https://${BUCKET_NAME}.s3.amazonaws.com/${key}`

  return { url, key, bucket: BUCKET_NAME }
}

export async function uploadBufferToS3(
  buffer: Buffer,
  filename: string,
  contentType: string
): Promise<UploadResult> {
  const ext = path.extname(filename)
  const key = `uploads/${randomUUID()}${ext}`

  const command = new PutObjectCommand({
    Bucket: BUCKET_NAME,
    Key: key,
    Body: buffer,
    ContentType: contentType,
    ACL: 'public-read',
  })

  await s3Client.send(command)

  const url = `https://${BUCKET_NAME}.s3.amazonaws.com/${key}`

  return { url, key, bucket: BUCKET_NAME }
}
'''

    fastapi_upload: str = '''# backend/lib/upload.py
from fastapi import UploadFile, HTTPException, status
import os
import uuid
import boto3
from botocore.exceptions import ClientError
from pathlib import Path
import mimetypes

# Allowed MIME types
ALLOWED_TYPES = {
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}

# Max file size: 10MB
MAX_FILE_SIZE = 10 * 1024 * 1024

def validate_file_type(file: UploadFile) -> None:
    """Validate file MIME type."""
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type: {file.content_type}. Allowed: {', '.join(ALLOWED_TYPES)}"
        )

async def validate_file_size(file: UploadFile) -> None:
    """Validate file size."""
    # Read file to check size
    content = await file.read()
    size = len(content)

    if size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Max size: {MAX_FILE_SIZE / (1024 * 1024)}MB"
        )

    if size == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty file"
        )

    # Reset file pointer
    await file.seek(0)

def sanitize_filename(filename: str) -> str:
    """Sanitize filename."""
    filename = filename.lower()
    filename = "".join(c if c.isalnum() or c in "._-" else "_" for c in filename)
    return filename

async def save_upload_file(file: UploadFile, destination: str) -> str:
    """Save uploaded file to local storage."""
    # Generate unique filename
    ext = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(destination, unique_filename)

    # Ensure directory exists
    os.makedirs(destination, exist_ok=True)

    # Save file
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    return file_path

class S3Uploader:
    """S3 file upload handler."""

    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            region_name=os.getenv("AWS_REGION", "us-east-1"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )
        self.bucket_name = os.getenv("S3_BUCKET_NAME")

    async def upload_file(self, file: UploadFile) -> dict:
        """Upload file to S3."""
        try:
            # Validate
            validate_file_type(file)
            await validate_file_size(file)

            # Generate unique key
            ext = Path(file.filename).suffix
            key = f"uploads/{uuid.uuid4()}{ext}"

            # Upload to S3
            content = await file.read()
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=content,
                ContentType=file.content_type,
                ACL="public-read",
            )

            url = f"https://{self.bucket_name}.s3.amazonaws.com/{key}"

            return {
                "url": url,
                "key": key,
                "bucket": self.bucket_name,
                "size": len(content),
                "content_type": file.content_type,
            }

        except ClientError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to upload file: {str(e)}"
            )
'''

    def generate(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        return {
            "backend/lib/upload.ts": self.express_upload,
            "backend/lib/s3.ts": self.s3_upload,
            "backend/lib/upload.py": self.fastapi_upload,
        }
