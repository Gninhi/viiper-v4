"""
CSV Processing Skill.

CSV parsing, validation, and transformation patterns.
"""

from typing import Dict, Any, Optional
from viiper.skills.base import Skill, SkillMetadata, SkillCategory, SkillDifficulty, Dependency, BestPractice, UsageExample, AntiPattern


class CSVProcessingSkill(Skill):
    """
    CSV parsing and processing patterns.

    Features:
    - Streaming CSV parsing
    - Validation with schemas
    - Large file handling
    - CSV generation
    - Error handling
    """

    metadata: SkillMetadata = SkillMetadata(
        name="CSV Processing",
        slug="csv-processing",
        category=SkillCategory.DATA_PROCESSING,
        difficulty=SkillDifficulty.INTERMEDIATE,
        tags=["csv", "parsing", "data-processing", "streaming", "validation"],
        estimated_time_minutes=30,
        description="CSV parsing and processing for data import/export",
    )

    dependencies: list = [
        Dependency(name="csv-parse", version="^5.5.2", package_manager="npm", reason="CSV parsing (Node.js)"),
        Dependency(name="csv-stringify", version="^6.4.4", package_manager="npm", reason="CSV generation (Node.js)"),
        Dependency(name="pandas", version="^2.1.0", package_manager="pip", reason="Data processing (Python)"),
        Dependency(name="pydantic", version="^2.5.0", package_manager="pip", reason="Data validation"),
    ]

    best_practices: list = [
        BestPractice(title="Stream Large Files", description="Don't load entire file in memory", code_reference="stream().pipe(parse())", benefit="Handle GB-sized files"),
        BestPractice(title="Validate Rows", description="Schema validation per row", code_reference="Zod/Pydantic validation", benefit="Catch bad data early"),
        BestPractice(title="Error Collection", description="Collect all errors, don't fail fast", code_reference="errors array with line numbers", benefit="Fix all issues at once"),
        BestPractice(title="Progress Tracking", description="Emit progress events", code_reference="on('progress', (p) => ...)", benefit="UX for long operations"),
    ]

    usage_examples: list = [
        UsageExample(
            title="CSV Import (Node.js)",
            description="Stream and validate CSV data",
            code=r'''import { parse } from 'csv-parse';
import { createReadStream } from 'fs';
import { pipeline } from 'stream/promises';
import { z } from 'zod';

const UserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1),
  age: z.string().transform(Number).refine(n => n >= 0),
  role: z.enum(['user', 'admin']).default('user'),
});

type UserInput = z.infer<typeof UserSchema>;

interface ParseResult {
  users: UserInput[];
  errors: { line: number; error: string }[];
}

export async function parseUserCSV(filePath: string): Promise<ParseResult> {
  const results: UserInput[] = [];
  const errors: { line: number; error: string }[] = [];
  let lineCount = 0;

  const parser = parse({
    columns: true,
    skip_empty_lines: true,
    trim: true,
  });

  const stream = createReadStream(filePath);

  for await (const record of stream.pipe(parser)) {
    lineCount++;
    try {
      const user = UserSchema.parse(record);
      results.push(user);
    } catch (error) {
      if (error instanceof z.ZodError) {
        errors.push({
          line: lineCount,
          error: error.errors.map(e => `${e.path.join('.')}: ${e.message}`).join(', '),
        });
      }
    }
  }

  return { users: results, errors };
}

// Usage
const { users, errors } = await parseUserCSV('imports/users.csv');
console.log(`Imported ${users.length} users`);
if (errors.length > 0) {
  console.error(`Found ${errors.length} errors:`, errors);
}
''',
        ),
        UsageExample(
            title="CSV Export (Node.js)",
            description="Generate CSV from data",
            code=r'''import { stringify } from 'csv-stringify/sync';
import { createWriteStream } from 'fs';
import { pipeline } from 'stream/promises';
import { Readable } from 'stream';

interface User {
  id: string;
  email: string;
  name: string;
  createdAt: Date;
}

export async function exportUsersToCSV(users: User[], filePath: string) {
  const records = users.map(user => ({
    id: user.id,
    email: user.email,
    name: user.name,
    created_at: user.createdAt.toISOString(),
  }));

  const output = stringify(records, {
    header: true,
    columns: ['id', 'email', 'name', 'created_at'],
    quoted: true,
  });

  const writeStream = createWriteStream(filePath);
  await pipeline(Readable.from(output), writeStream);
}

// Streaming export for large datasets
export async function streamUsersToCSV(query: any, filePath: string) {
  const writeStream = createWriteStream(filePath);

  // Write header
  writeStream.write('id,email,name,created_at\n');

  const cursor = db.users.findMany(query).cursor();
  let user;
  while ((user = await cursor.next()) !== null) {
    const row = stringify([{
      id: user.id,
      email: user.email,
      name: user.name,
      created_at: user.createdAt.toISOString(),
    }], { quoted: true });
    writeStream.write(row);
  }

  writeStream.end();
}
''',
        ),
        UsageExample(
            title="CSV Processing (Python)",
            description="Pandas for data processing",
            code=r'''import pandas as pd
from pydantic import BaseModel, EmailStr, ValidationError
from typing import List, Tuple

class UserImport(BaseModel):
    email: EmailStr
    name: str
    age: int
    role: str = "user"

def process_user_csv(file_path: str) -> Tuple[List[UserImport], List[dict]]:
    """Process CSV and return valid users and errors"""
    df = pd.read_csv(file_path)

    users = []
    errors = []

    for idx, row in df.iterrows():
        try:
            user = UserImport(
                email=row['email'],
                name=row['name'],
                age=int(row['age']),
                role=row.get('role', 'user'),
            )
            users.append(user)
        except ValidationError as e:
            errors.append({
                'line': idx + 2,  # +2 for header and 0-index
                'error': str(e),
            })

    return users, errors

def export_users_to_csv(users: List[dict], file_path: str):
    """Export users to CSV"""
    df = pd.DataFrame(users)
    df.to_csv(file_path, index=False)

# Usage
users, errors = process_user_csv('imports/users.csv')
print(f"Imported {len(users)} users")
if errors:
    print(f"Found {len(errors)} errors")
''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(title="Loading Entire File", description="Reading large CSVs into memory", solution="Use streaming parser", impact="Memory exhaustion, crashes"),
        AntiPattern(title="No Validation", description="Trusting CSV data", solution="Validate each row with schema", impact="Bad data in database"),
        AntiPattern(title="Silent Failures", description="Skipping invalid rows silently", solution="Collect and report all errors", impact="Data loss, confusion"),
        AntiPattern(title="No Progress Feedback", description="Long operations with no feedback", solution="Emit progress events", impact="Poor UX, users think it's frozen"),
    ]

    def generate(self, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        options = options or {}
        return {
            "files": {
                "services/csv-import.ts": self.usage_examples[0].code,
                "services/csv-export.ts": self.usage_examples[1].code,
                "services/csv_processor.py": self.usage_examples[2].code,
            },
            "metadata": {},
        }
