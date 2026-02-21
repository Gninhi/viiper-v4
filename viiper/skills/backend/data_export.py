"""Premium Data Export Patterns Skill."""

from typing import Dict, Any, Optional
from viiper.skills.base import (
    Skill, SkillMetadata, SkillCategory, SkillDifficulty,
    Dependency, BestPractice, UsageExample, AntiPattern,
)

class DataExportSkill(Skill):
    """Patterns for exporting data to CSV, Excel, and PDF formats."""

    metadata: SkillMetadata = SkillMetadata(
        name="Data Export Library",
        slug="data-export",
        category=SkillCategory.BACKEND_API,
        difficulty=SkillDifficulty.INTERMEDIATE,
        tags=["export", "csv", "excel", "pdf", "pandas", "exceljs"],
        estimated_time_minutes=40,
        description="Professional file export patterns for multi-format data extraction including CSV, Excel, and PDF.",
    )

    dependencies: list = [
        Dependency(name="exceljs", version="^4.4.0", package_manager="npm", reason="Advanced Excel generation"),
        Dependency(name="jspdf", version="^2.5.1", package_manager="npm", reason="PDF generation"),
        Dependency(name="pandas", version="^2.1.0", package_manager="pip", reason="Data manipulation and CSV/Excel export"),
        Dependency(name="openpyxl", version="^3.1.2", package_manager="pip", reason="Excel support for pandas"),
        Dependency(name="fpdf2", version="^2.7.4", package_manager="pip", reason="PDF generation in Python"),
    ]

    best_practices: list = [
        BestPractice(
            title="Stream Large Exports",
            description="Use streaming responses for large CSV exports to avoid memory exhaustion.",
            code_reference="res.setHeader('Content-Type', 'text/csv'); stream.pipe(res);",
            benefit="Handles 1M+ rows without crashing the server.",
        ),
        BestPractice(
            title="Consistent Date Formatting",
            description="Always format dates in a standard ISO string or localized format before export.",
            code_reference="date.toISOString()",
            benefit="Prevents corrupted spreadsheets due to regional date differences.",
        ),
        BestPractice(
            title="Background Processing",
            description="Offload heavy PDF or large Excel generation to background jobs (BullMQ/Celery).",
            code_reference="exportTask.add({ userId, format: 'pdf' });",
            benefit="Prevents API timeouts on heavy exports.",
        ),
    ]

    usage_examples: list = [
        UsageExample(
            name="Node.js Excel Export",
            description="Generating a multi-sheet Excel file.",
            code='''const workbook = new ExcelJS.Workbook();
const sheet = workbook.addWorksheet('Users');
sheet.columns = [{ header: 'ID', key: 'id' }, { header: 'Name', key: 'name' }];
sheet.addRows(userData);
await workbook.xlsx.writeFile('export.xlsx');''',
        ),
        UsageExample(
            name="Python Pandas CSV Export",
            description="Quick CSV export from a list of dicts.",
            code='''df = pd.DataFrame(data)
csv_buffer = StringIO()
df.to_csv(csv_buffer, index=False)
return csv_buffer.getvalue()''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(
            bad="Generating large files in memory",
            why="Will crash the process if multiple users request large exports simultaneously.",
            good="Use streams or temporary files on disk.",
        ),
        AntiPattern(
            bad="Including sensitive data in exports",
            why="Risk of leaking user passwords or private tokens in CSV downloads.",
            good="Explicitly select visible columns (schema projection).",
        ),
    ]

    file_structure: dict = {
        "backend/lib/export_service.ts": "Multi-format export service (Node.js)",
        "backend/lib/export_service.py": "Multi-format export service (Python)",
    }

    export_ts: str = r'''// backend/lib/export_service.ts
import ExcelJS from 'exceljs'
import { jsPDF } from 'jspdf'
import 'jspdf-autotable'

export class ExportService {
  /**
   * Export to Excel
   */
  async toExcel(data: any[], fileName: str) {
    const workbook = new ExcelJS.Workbook()
    const worksheet = workbook.addWorksheet('Data')
    
    // Auto-generate columns from first object
    if (data.length > 0) {
      worksheet.columns = Object.keys(data[0]).map(key => ({
        header: key.charAt(0).toUpperCase() + key.slice(1),
        key: key,
        width: 20
      }))
    }
    
    worksheet.addRows(data)
    
    // Style header
    worksheet.getRow(1).font = { bold: true }
    
    return workbook.xlsx.writeBuffer()
  }

  /**
   * Export to PDF
   */
  async toPDF(data: any[], title: str) {
    const doc = new jsPDF()
    doc.text(title, 14, 15)
    
    const headers = Object.keys(data[0] || {})
    const rows = data.map(item => Object.values(item))
    
    ;(doc as any).autoTable({
      head: [headers],
      body: rows,
      startY: 20,
    })
    
    return doc.output('arraybuffer')
  }
}
'''

    export_py: str = r'''# backend/lib/export_service.py
import pandas as pd
from fpdf import FPDF
from io import BytesIO

class ExportService:
    @staticmethod
    def to_csv(data: list) -> str:
        df = pd.DataFrame(data)
        return df.to_csv(index=False)

    @staticmethod
    def to_excel(data: list) -> bytes:
        df = pd.DataFrame(data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        return output.getvalue()

    @staticmethod
    def to_pdf(data: list, title: str) -> bytes:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=title, ln=True, align='C')
        
        if not data:
            return pdf.output(dest='S')
            
        # Basic table rendering
        headers = list(data[0].keys())
        col_width = 190 / len(headers)
        
        # Headers
        pdf.set_font("Arial", 'B', size=10)
        for header in headers:
            pdf.cell(col_width, 10, header, border=1)
        pdf.ln()
        
        # Rows
        pdf.set_font("Arial", size=9)
        for row in data:
            for header in headers:
                pdf.cell(col_width, 10, str(row.get(header, "")), border=1)
            pdf.ln()
            
        return pdf.output(dest='S')
'''

    def generate(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        return {
            "backend/lib/export_service.ts": self.export_ts,
            "backend/lib/export_service.py": self.export_py,
        }
