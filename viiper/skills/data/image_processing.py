"""
Image Processing Skill.

Image manipulation, optimization, and transformation patterns.
"""

from typing import Dict, Any, Optional
from viiper.skills.base import Skill, SkillMetadata, SkillCategory, SkillDifficulty, Dependency, BestPractice, UsageExample, AntiPattern


class ImageProcessingSkill(Skill):
    """
    Image processing and optimization.

    Features:
    - Image resizing
    - Format conversion
    - Compression
    - Watermarking
    - Thumbnail generation
    - EXIF handling
    """

    metadata: SkillMetadata = SkillMetadata(
        name="Image Processing",
        slug="image-processing",
        category=SkillCategory.DATA_PROCESSING,
        difficulty=SkillDifficulty.INTERMEDIATE,
        tags=["image", "processing", "sharp", "pillow", "optimization", "thumbnails"],
        estimated_time_minutes=40,
        description="Image processing for web optimization",
    )

    dependencies: list = [
        Dependency(name="sharp", version="^0.33.2", package_manager="npm", reason="Image processing (Node.js)"),
        Dependency(name="pillow", version="^10.2.0", package_manager="pip", reason="Image processing (Python)"),
        Dependency(name="sharp", version="^0.33.2", package_manager="pip", reason="Image processing (Python)"),
    ]

    best_practices: list = [
        BestPractice(title="Generate Multiple Sizes", description="Create responsive images", code_reference="thumbnail, medium, large", benefit="Faster page loads"),
        BestPractice(title="Use Modern Formats", description="WebP, AVIF for web", code_reference="Convert JPEG to WebP", benefit="50-80% size reduction"),
        BestPractice(title="Strip Metadata", description="Remove EXIF data", code_reference="strip metadata option", benefit="Privacy, smaller files"),
        BestPractice(title="Lazy Loading", description="Defer offscreen images", code_reference="loading='lazy'", benefit="Faster initial load"),
    ]

    usage_examples: list = [
        UsageExample(
            name="Image Processing (Node.js)",
            description="Sharp for image transformations",
            code=r'''import sharp from 'sharp';
import { mkdir } from 'fs/promises';
import { dirname, join, extname, basename } from 'path';

interface ImageOptions {
  widths?: number[];
  quality?: number;
  format?: 'jpeg' | 'png' | 'webp' | 'avif';
  watermark?: { text: string; position: string };
}

export async function processImage(
  inputPath: string,
  outputPath: string,
  options: ImageOptions = {}
): Promise<{ files: string[]; sizes: Record<string, number> }> {
  const {
    widths = [320, 640, 1024, 1920],
    quality = 80,
    format = 'webp',
    watermark,
  } = options;

  await mkdir(dirname(outputPath), { recursive: true });

  const baseName = basename(inputPath, extname(inputPath));
  const files: string[] = [];
  const sizes: Record<string, number> = {};

  for (const width of widths) {
    const fileName = `${baseName}-${width}w.${format}`;
    const filePath = join(dirname(outputPath), fileName);

    let pipeline = sharp(inputPath)
      .resize(width, null, {
        withoutEnlargement: true,
        quality,
      })
      .toFormat(format, { quality });

    // Strip metadata
    pipeline = pipeline.withoutMetadata();

    // Add watermark if specified
    if (watermark) {
      const watermarkBuffer = await createWatermark(watermark.text);
      pipeline = pipeline.composite([{
        input: watermarkBuffer,
        gravity: watermark.position as any,
      }]);
    }

    await pipeline.toFile(filePath);

    const stats = await sharp(filePath).metadata();
    sizes[`${width}w`] = stats.size || 0;
    files.push(fileName);
  }

  return { files, sizes };
}

async function createWatermark(text: string): Promise<Buffer> {
  const svg = `
    <svg width="200" height="50">
      <text x="10" y="35" font-family="Arial" font-size="24" fill="rgba(255,255,255,0.5)">
        ${text}
      </text>
    </svg>
  `;
  return sharp(Buffer.from(svg)).toBuffer();
}

// Generate thumbnail
export async function generateThumbnail(inputPath: string, outputPath: string, size = 200) {
  await sharp(inputPath)
    .resize(size, size, {
      fit: 'cover',
      position: 'center',
    })
    .toFile(outputPath);
}

// Get image dimensions
export async function getImageDimensions(path: string) {
  const metadata = await sharp(path).metadata();
  return { width: metadata.width, height: metadata.height };
}
''',
        ),
        UsageExample(
            name="Image Upload with Processing",
            description="Express route for image uploads",
            code=r'''import express from 'express';
import multer from 'multer';
import { processImage } from '../services/image-processing';
import { s3 } from '../services/s3';

const router = express.Router();
const upload = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: 10 * 1024 * 1024 }, // 10MB
  fileFilter: (req, file, cb) => {
    if (file.mimetype.startsWith('image/')) {
      cb(null, true);
    } else {
      cb(new Error('Only images allowed'));
    }
  },
});

router.post('/upload', upload.single('image'), async (req, res) => {
  try {
    const tempPath = `/tmp/${Date.now()}-${req.file.originalname}`;

    // Save temporarily
    await fs.writeFile(tempPath, req.file.buffer);

    // Process image
    const outputPath = `/tmp/processed-${Date.now()}`;
    const { files, sizes } = await processImage(tempPath, outputPath, {
      widths: [400, 800, 1200],
      format: 'webp',
      quality: 80,
    });

    // Upload to S3
    const urls = await Promise.all(
      files.map(async (file) => {
        const key = `images/${Date.now()}-${file}`;
        await s3.upload({
          Bucket: process.env.S3_BUCKET,
          Key: key,
          Body: fs.createReadStream(join(outputPath, file)),
          ContentType: 'image/webp',
        }).promise();
        return `https://cdn.example.com/${key}`;
      })
    );

    // Cleanup
    await fs.rm(tempPath, { recursive: true });
    await fs.rm(outputPath, { recursive: true });

    res.json({
      success: true,
      urls: {
        thumbnail: urls[0],
        medium: urls[1],
        large: urls[2],
      },
      sizes,
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

export default router;
''',
        ),
        UsageExample(
            name="Image Processing (Python)",
            description="Pillow for image manipulation",
            code=r'''from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

def process_image(
    input_path: str,
    output_dir: str,
    widths: list[int] = None,
    quality: int = 80,
    output_format: str = 'webp',
) -> dict:
    """Process image into multiple sizes"""
    if widths is None:
        widths = [320, 640, 1024, 1920]

    os.makedirs(output_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(input_path))[0]
    result = {'files': [], 'sizes': {}}

    with Image.open(input_path) as img:
        # Convert to RGB if necessary
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')

        for width in widths:
            # Calculate height maintaining aspect ratio
            ratio = width / img.width
            height = int(img.height * ratio)

            # Resize
            resized = img.resize((width, height), Image.Resampling.LANCZOS)

            # Save
            filename = f'{base_name}-{width}w.{output_format}'
            filepath = os.path.join(output_dir, filename)

            resized.save(
                filepath,
                format=output_format.upper(),
                quality=quality,
                optimize=True,
            )

            result['files'].append(filename)
            result['sizes'][f'{width}w'] = os.path.getsize(filepath)

    return result

def generate_thumbnail(input_path: str, output_path: str, size: int = 200):
    """Generate square thumbnail"""
    with Image.open(input_path) as img:
        # Crop to square
        min_dim = min(img.width, img.height)
        left = (img.width - min_dim) // 2
        top = (img.height - min_dim) // 2
        img = img.crop((left, top, left + min_dim, top + min_dim))

        # Resize
        img = img.resize((size, size), Image.Resampling.LANCZOS)
        img.save(output_path, 'WEBP', quality=80)

def add_watermark(image_path: str, text: str, output_path: str):
    """Add text watermark to image"""
    with Image.open(image_path) as img:
        # Create transparent overlay
        txt_layer = Image.new('RGBA', img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt_layer)

        # Add text
        font = ImageFont.truetype('arial.ttf', 36)
        draw.text(
            (img.width - 200, img.height - 50),
            text,
            font=font,
            fill=(255, 255, 255, 128),
        )

        # Composite
        watermarked = Image.alpha_composite(img.convert('RGBA'), txt_layer)
        watermarked.save(output_path, 'PNG')
''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(bad="Original Size Only", why="Serving full-size images", good="Generate multiple sizes"),
        AntiPattern(bad="JPEG for Everything", why="Using wrong format", good="WebP/AVIF for photos, PNG for graphics"),
        AntiPattern(bad="No Compression", why="Unoptimized images", good="Apply quality settings"),
        AntiPattern(bad="EXIF Data Leaked", why="Location data in images", good="Strip metadata"),
    ]

    def generate(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        context = context or {}
        return {
            "files": {
                "services/image-processing.ts": self.usage_examples[0].code,
                "routes/images.ts": self.usage_examples[1].code,
                "services/image_processor.py": self.usage_examples[2].code,
            },
            "metadata": {},
        }
